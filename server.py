from __future__ import annotations

import argparse
import cgi
import json
import threading
import time
import uuid
from dataclasses import dataclass, field
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from campaign_app.models import CampaignResult
from campaign_app.pipeline import run_campaign_pipeline
from campaign_app.validation import validate_inputs
from campaign_app.web_support import (
    InMemoryUpload,
    build_campaign_inputs_from_api_payload,
    build_result_manifest,
    estimate_job_progress,
)


ROOT_DIR = Path(__file__).resolve().parent
JOB_TTL_SECONDS = 60 * 60
JOBS: dict[str, "CampaignJob"] = {}
JOBS_LOCK = threading.Lock()


@dataclass
class CampaignJob:
    job_id: str
    render_mode: str
    status: str = "queued"
    progress: int = 0
    logs: list[str] = field(default_factory=list)
    error: str = ""
    result: CampaignResult | None = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def append_log(self, message: str) -> None:
        with self.lock:
            self.logs.append(message)
            self.progress = estimate_job_progress(len(self.logs), self.render_mode)
            self.updated_at = time.time()

    def mark_running(self) -> None:
        with self.lock:
            self.status = "running"
            self.progress = max(self.progress, 4)
            self.updated_at = time.time()

    def mark_complete(self, result: CampaignResult) -> None:
        with self.lock:
            self.result = result
            self.status = "complete"
            self.progress = 100
            self.updated_at = time.time()

    def mark_error(self, error_message: str) -> None:
        with self.lock:
            self.error = error_message
            self.status = "error"
            self.progress = 100
            self.updated_at = time.time()

    def snapshot(self) -> dict:
        with self.lock:
            return {
                "jobId": self.job_id,
                "state": self.status,
                "progress": self.progress,
                "logs": list(self.logs),
                "error": self.error,
            }


def prune_expired_jobs() -> None:
    cutoff = time.time() - JOB_TTL_SECONDS
    with JOBS_LOCK:
        expired_ids = [job_id for job_id, job in JOBS.items() if job.updated_at < cutoff]
        for job_id in expired_ids:
            JOBS.pop(job_id, None)


def create_job(render_mode: str) -> CampaignJob:
    prune_expired_jobs()
    job = CampaignJob(job_id=uuid.uuid4().hex, render_mode=render_mode)
    with JOBS_LOCK:
        JOBS[job.job_id] = job
    return job


def get_job(job_id: str) -> CampaignJob | None:
    with JOBS_LOCK:
        return JOBS.get(job_id)


def run_job(job: CampaignJob, inputs) -> None:
    job.mark_running()
    try:
        result = run_campaign_pipeline(inputs, logger=job.append_log)
    except Exception as exc:
        job.mark_error(str(exc))
        return
    job.mark_complete(result)


class FashionCampaignHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)

        if parsed.path == "/":
            self.path = "/index.html"
            return super().do_GET()

        if parsed.path == "/api/health":
            return self.send_json(HTTPStatus.OK, {"status": "ok"})

        if parsed.path.startswith("/api/campaigns/"):
            return self.handle_campaign_get(parsed)

        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/campaigns":
            return self.handle_campaign_create()
        self.send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})

    def handle_campaign_create(self) -> None:
        try:
            fields, files = self.parse_multipart_form()
        except ValueError as exc:
            return self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        garment_upload = build_upload(files.get("garmentFile"))
        model_upload = build_upload(files.get("modelFile"))
        inputs = build_campaign_inputs_from_api_payload(fields, garment_upload, model_upload)
        missing_fields = validate_inputs(inputs)

        if missing_fields:
            return self.send_json(
                HTTPStatus.BAD_REQUEST,
                {
                    "error": "ValidationError",
                    "missingFields": missing_fields,
                },
            )

        job = create_job(inputs.render_mode)
        job.append_log("Solicitud recibida. Preparando pipeline...")
        worker = threading.Thread(target=run_job, args=(job, inputs), daemon=True)
        worker.start()

        return self.send_json(HTTPStatus.ACCEPTED, {"jobId": job.job_id})

    def handle_campaign_get(self, parsed) -> None:
        path_parts = [part for part in parsed.path.split("/") if part]
        if len(path_parts) < 4:
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})

        job_id = path_parts[2]
        action = path_parts[3]
        job = get_job(job_id)
        if not job:
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "Job no encontrado."})

        if action == "status":
            return self.send_json(HTTPStatus.OK, job.snapshot())

        if action == "result":
            if job.status != "complete" or job.result is None:
                return self.send_json(
                    HTTPStatus.CONFLICT,
                    {"error": "El resultado aun no esta disponible."},
                )
            return self.send_json(HTTPStatus.OK, build_result_manifest(job_id, job.result))

        if action == "model-reference":
            return self.serve_model_reference(job)

        if action == "download.zip":
            return self.serve_zip(job)

        if action == "images" and len(path_parts) == 5:
            try:
                image_index = int(path_parts[4])
            except ValueError:
                return self.send_json(HTTPStatus.BAD_REQUEST, {"error": "Indice de imagen invalido."})
            query = parse_qs(parsed.query)
            return self.serve_image(job, image_index=image_index, download_requested="download" in query)

        return self.send_json(HTTPStatus.NOT_FOUND, {"error": "Ruta no encontrada."})

    def serve_model_reference(self, job: CampaignJob) -> None:
        if job.status != "complete" or job.result is None:
            return self.send_json(
                HTTPStatus.CONFLICT,
                {"error": "La referencia del modelo aun no esta disponible."},
            )

        extension = mime_to_extension(job.result.model_ref_mime)
        filename = f"model_reference{extension}"
        return self.send_binary(
            HTTPStatus.OK,
            job.result.model_ref_bytes,
            content_type=job.result.model_ref_mime,
            filename=filename,
            as_attachment=False,
        )

    def serve_image(self, job: CampaignJob, image_index: int, download_requested: bool) -> None:
        if job.status != "complete" or job.result is None:
            return self.send_json(
                HTTPStatus.CONFLICT,
                {"error": "Las imagenes aun no estan disponibles."},
            )

        if image_index < 1 or image_index > len(job.result.result_images):
            return self.send_json(HTTPStatus.NOT_FOUND, {"error": "Imagen no encontrada."})

        image_bytes = job.result.result_images[image_index - 1]
        filename = f"shooting_result_{image_index}.png"
        return self.send_binary(
            HTTPStatus.OK,
            image_bytes,
            content_type="image/png",
            filename=filename,
            as_attachment=download_requested,
        )

    def serve_zip(self, job: CampaignJob) -> None:
        if job.status != "complete" or job.result is None:
            return self.send_json(
                HTTPStatus.CONFLICT,
                {"error": "El ZIP aun no esta disponible."},
            )

        return self.send_binary(
            HTTPStatus.OK,
            job.result.zip_bytes,
            content_type="application/zip",
            filename="fashion_campaign_complete.zip",
            as_attachment=True,
        )

    def parse_multipart_form(self) -> tuple[dict[str, str], dict[str, dict]]:
        content_type = self.headers.get("Content-Type", "")
        if not content_type.startswith("multipart/form-data"):
            raise ValueError("Content-Type invalido. Se esperaba multipart/form-data.")

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": content_type,
                "CONTENT_LENGTH": self.headers.get("Content-Length", "0"),
            },
            keep_blank_values=True,
        )

        fields: dict[str, str] = {}
        files: dict[str, dict] = {}
        for key in form.keys():
            item = form[key]
            if isinstance(item, list):
                item = item[0]

            if item.filename:
                files[key] = {
                    "filename": Path(item.filename).name,
                    "content": item.file.read(),
                }
                continue

            fields[key] = item.value

        return fields, files

    def send_json(self, status_code: int, payload: dict) -> None:
        response = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(response)

    def send_binary(
        self,
        status_code: int,
        payload: bytes,
        content_type: str,
        filename: str,
        as_attachment: bool,
    ) -> None:
        disposition = "attachment" if as_attachment else "inline"
        self.send_response(status_code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Content-Disposition", f'{disposition}; filename="{filename}"')
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)


def build_upload(file_payload: dict | None) -> InMemoryUpload | None:
    if not file_payload:
        return None
    return InMemoryUpload(
        name=file_payload["filename"],
        content=file_payload["content"],
    )


def mime_to_extension(mime_type: str) -> str:
    if mime_type == "image/png":
        return ".png"
    if mime_type == "image/webp":
        return ".webp"
    if mime_type == "image/jpeg":
        return ".jpg"
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description="Fashion Campaign frontend + Python backend server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), FashionCampaignHandler)
    print(f"Serving on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
