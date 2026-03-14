from __future__ import annotations

import os
from dataclasses import dataclass

from campaign_app.models import CampaignInputs, CampaignResult
from campaign_core.constants import DEFAULT_RENDER_MODE, RENDER_MODE_CONFIG


STYLE_MODE_LABELS = {
    "preset": "Preset optimizado",
    "custom": "Prompt personalizado",
}

LOCATION_MODE_LABELS = {
    "preset": "Preset optimizado",
    "custom": "Prompt personalizado",
}

MODEL_MODE_LABELS = {
    "preset": "Preset de descripcion",
    "custom": "Descripcion personalizada",
    "upload": "Subir imagen del modelo",
}

LOOK_SUBTITLES = [
    "Full body / walking pose",
    "Medium shot / seated pose",
    "Low angle / static pose",
    "Detail shot / in motion",
]


@dataclass
class InMemoryUpload:
    name: str
    content: bytes

    def getbuffer(self):
        return memoryview(self.content)


def guess_mime_type(filename: str, default: str = "application/octet-stream") -> str:
    lower_name = filename.lower()
    if lower_name.endswith(".png"):
        return "image/png"
    if lower_name.endswith(".webp"):
        return "image/webp"
    if lower_name.endswith(".jpg") or lower_name.endswith(".jpeg"):
        return "image/jpeg"
    if lower_name.endswith(".zip"):
        return "application/zip"
    return default


def build_campaign_inputs_from_api_payload(
    payload: dict[str, str],
    garment_upload: InMemoryUpload | None,
    model_upload: InMemoryUpload | None,
) -> CampaignInputs:
    return CampaignInputs(
        api_key=payload.get("apiKey", "").strip(),
        garment_file=garment_upload,
        render_mode=payload.get("renderMode", "").strip(),
        style_mode=payload.get("styleMode", "").strip(),
        style_desc=payload.get("styleDesc", "").strip(),
        location_mode=payload.get("locationMode", "").strip(),
        location_desc=payload.get("locationDesc", "").strip(),
        model_mode=payload.get("modelMode", "").strip(),
        model_desc=payload.get("modelDesc", "").strip(),
        model_image_file=model_upload,
    )


def get_render_config(render_mode: str) -> dict:
    normalized_mode = render_mode if render_mode in RENDER_MODE_CONFIG else DEFAULT_RENDER_MODE
    return RENDER_MODE_CONFIG[normalized_mode]


def estimate_job_progress(log_count: int, render_mode: str) -> int:
    render_cfg = get_render_config(render_mode)
    expected_logs = 6 + (render_cfg["max_images"] * 2)
    progress = 8 + int((log_count / max(expected_logs, 1)) * 84)
    return max(8, min(progress, 94))


def build_result_manifest(job_id: str, result: CampaignResult) -> dict:
    image_entries = []
    for index, _ in enumerate(result.result_images, start=1):
        image_entries.append(
            {
                "title": f"Look {index}",
                "subtitle": LOOK_SUBTITLES[index - 1] if index - 1 < len(LOOK_SUBTITLES) else "Editorial variation",
                "filename": f"shooting_result_{index}.png",
                "url": f"/api/campaigns/{job_id}/images/{index}",
                "downloadUrl": f"/api/campaigns/{job_id}/images/{index}?download=1",
            }
        )

    return {
        "prompts": result.prompts,
        "modelReferenceUrl": f"/api/campaigns/{job_id}/model-reference",
        "downloadZipUrl": f"/api/campaigns/{job_id}/download.zip",
        "images": image_entries,
    }


def filename_only(path_or_name: str) -> str:
    return os.path.basename(path_or_name)
