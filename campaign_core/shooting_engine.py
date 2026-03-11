import base64
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import os
from typing import Callable, Optional

from google.genai import types

from campaign_core.constants import (
    ANALYSIS_MODEL_FLASH,
    ANALYSIS_MODEL_PRO,
    FINAL_ASPECT_RATIO,
    FINAL_IMAGE_SIZE,
    IMAGE_MODEL,
)
from campaign_core.gemini_client import (
    build_client,
    generate_image_via_rest,
    resolve_api_key,
)
from campaign_core.image_utils import (
    extract_image_bytes,
    extract_json,
    extract_text,
    prepare_reference_image_jpeg,
    save_square_png,
)
from campaign_core.prompts import (
    build_final_image_instruction,
    build_model_reference_prompt,
    build_shoot_prompts_request,
)


class FashionCampaignAI:
    def __init__(self, api_key: Optional[str] = None, logger: Optional[Callable[[str], None]] = None):
        self.api_key = resolve_api_key(api_key)
        self.logger = logger
        self.client = build_client(api_key=self.api_key)

    def _log(self, message):
        if self.logger:
            self.logger(message)
            return
        print(message)

    def _extract_json(self, text):
        return extract_json(text)

    def _extract_image_bytes(self, response):
        return extract_image_bytes(response)

    def _extract_text(self, response):
        return extract_text(response)

    def _save_square_png(self, image_bytes, output_path, size=1024):
        return save_square_png(image_bytes, output_path=output_path, size=size)

    def _prepare_reference_image_jpeg(self, image_path, max_side=1280, quality=90):
        return prepare_reference_image_jpeg(
            image_path=image_path,
            max_side=max_side,
            quality=quality,
        )

    def _generate_image_via_rest(self, parts, aspect_ratio=FINAL_ASPECT_RATIO, image_size="4K"):
        return generate_image_via_rest(
            api_key=self.api_key,
            image_model=IMAGE_MODEL,
            parts=parts,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        )

    def generate_model_reference(self, model_desc, output_path="model_reference.png"):
        self._log("Generando imagen de referencia del modelo...")

        prompt = build_model_reference_prompt(model_desc)
        response = self.client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
        image_bytes = self._extract_image_bytes(response)
        return self._save_square_png(image_bytes, output_path=output_path)

    def get_or_generate_single_model_reference(
        self, model_desc, model_dir="model"
    ) -> str:
        os.makedirs(model_dir, exist_ok=True)
        allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

        model_reference_paths = []
        for filename in sorted(os.listdir(model_dir)):
            file_path = os.path.join(model_dir, filename)
            _, ext = os.path.splitext(filename.lower())
            if os.path.isfile(file_path) and ext in allowed_extensions:
                model_reference_paths.append(file_path)

        if len(model_reference_paths) > 1:
            raise ValueError(
                f"La carpeta '{model_dir}' debe contener una sola imagen de referencia. "
                f"Encontradas: {len(model_reference_paths)}"
            )

        if len(model_reference_paths) == 1:
            self._log(f"Usando imagen de referencia en '{model_reference_paths[0]}'.")
            return model_reference_paths[0]

        generated_path = os.path.join(model_dir, "model_reference_generated.png")
        self.generate_model_reference(model_desc, output_path=generated_path)
        self._log(f"No habia imagenes en '{model_dir}'. Referencia generada: {generated_path}")
        return generated_path

    def get_or_generate_cached_model_reference(
        self,
        model_desc,
        cache_dir=".cache/model_refs",
    ) -> str:
        os.makedirs(cache_dir, exist_ok=True)
        cache_key = hashlib.sha256(
            f"{IMAGE_MODEL}\n{model_desc.strip()}".encode("utf-8")
        ).hexdigest()[:24]
        cached_path = os.path.join(cache_dir, f"model_ref_{cache_key}.png")

        if os.path.exists(cached_path):
            self._log(f"Usando referencia de modelo cacheada: {cached_path}")
            return cached_path

        self._log("No existe cache de referencia de modelo. Generando y guardando en cache...")
        self.generate_model_reference(model_desc, output_path=cached_path)
        self._log(f"Referencia de modelo cacheada en: {cached_path}")
        return cached_path

    def generate_shoot_prompts(self, style, location, prompt_count=4):
        self._log("Generando conceptos creativos para el shooting...")

        prompt = build_shoot_prompts_request(style, location, prompt_count=prompt_count)
        flash_error = None

        try:
            return self._generate_shoot_prompts_with_model(
                prompt=prompt,
                model_name=ANALYSIS_MODEL_FLASH,
                expected_prompt_count=prompt_count,
            )
        except Exception as exc:
            flash_error = exc
            self._log(
                "El modelo flash no devolvio prompts validos. Reintentando con modelo pro..."
            )

        try:
            return self._generate_shoot_prompts_with_model(
                prompt=prompt,
                model_name=ANALYSIS_MODEL_PRO,
                expected_prompt_count=prompt_count,
            )
        except Exception as pro_error:
            raise RuntimeError(
                "No se pudieron generar prompts validos. "
                f"Flash error: {flash_error} | Pro error: {pro_error}"
            )

    def _generate_shoot_prompts_with_model(self, prompt, model_name, expected_prompt_count):
        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        result = self._extract_json(self._extract_text(response))
        prompts = result.get("prompts")
        if not isinstance(prompts, list):
            raise ValueError(
                f"El modelo {model_name} no devolvio una lista de prompts valida."
            )
        if len(prompts) < expected_prompt_count:
            raise ValueError(
                f"El modelo {model_name} no devolvio al menos {expected_prompt_count} prompts."
            )
        if len(prompts) > expected_prompt_count:
            self._log(
                f"El modelo {model_name} devolvio {len(prompts)} prompts; se usaran los primeros {expected_prompt_count}."
            )
        return prompts[:expected_prompt_count]

    def execute_shooting(
        self,
        prompts,
        garment_image_path,
        model_reference_path,
        output_dir=".",
        max_images=4,
        output_size=FINAL_IMAGE_SIZE,
        image_size="4K",
        parallel_workers=None,
    ):
        self._log("Iniciando sesion de fotos (generando imagenes finales)...")
        os.makedirs(output_dir, exist_ok=True)

        garment_bytes, garment_mime = self._prepare_reference_image_jpeg(
            garment_image_path
        )
        model_bytes, model_mime = self._prepare_reference_image_jpeg(
            model_reference_path
        )
        garment_b64 = base64.b64encode(garment_bytes).decode("utf-8")
        model_b64 = base64.b64encode(model_bytes).decode("utf-8")

        selected_prompts = prompts[:max_images]
        total_images = len(selected_prompts)
        if total_images == 0:
            return []

        if parallel_workers is None:
            worker_count = 1 if total_images == 1 else max(2, min(4, total_images))
        else:
            bounded_workers = max(1, min(4, parallel_workers, total_images))
            worker_count = bounded_workers if total_images == 1 else max(2, bounded_workers)
        self._log(f"Generacion paralela activada: {worker_count} worker(s).")

        generated_files: list[Optional[str]] = [None] * total_images

        def _generate_and_save(index: int, prompt_text: str):
            final_instruction = build_final_image_instruction(prompt_text)
            rest_parts = [
                {"text": "GARMENT_REFERENCE"},
                {
                    "inlineData": {
                        "mimeType": garment_mime,
                        "data": garment_b64,
                    }
                },
                {"text": "MODEL_REFERENCE"},
                {
                    "inlineData": {
                        "mimeType": model_mime,
                        "data": model_b64,
                    }
                },
                {"text": final_instruction},
            ]
            image_bytes = self._generate_image_via_rest(
                rest_parts,
                aspect_ratio=FINAL_ASPECT_RATIO,
                image_size=image_size,
            )
            output_file = os.path.join(output_dir, f"shooting_result_{index + 1}.png")
            self._save_square_png(
                image_bytes, output_path=output_file, size=output_size
            )
            return index, output_file

        if worker_count == 1:
            for idx, prompt_text in enumerate(selected_prompts):
                self._log(f"   Generando foto {idx + 1}/{total_images}")
                _, output_path = _generate_and_save(idx, prompt_text)
                generated_files[idx] = output_path
                self._log(f"   Guardada: {output_path}")
            return [path for path in generated_files if path is not None]

        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            future_to_index = {}
            for idx, prompt_text in enumerate(selected_prompts):
                self._log(f"   Encolada foto {idx + 1}/{total_images}")
                future = executor.submit(_generate_and_save, idx, prompt_text)
                future_to_index[future] = idx

            for future in as_completed(future_to_index):
                idx = future_to_index[future]
                try:
                    _, output_path = future.result()
                except Exception as exc:
                    for pending_future in future_to_index:
                        pending_future.cancel()
                    raise RuntimeError(
                        f"No se pudo generar la foto {idx + 1}/{total_images}. {exc}"
                    ) from exc
                generated_files[idx] = output_path
                self._log(f"   Guardada foto {idx + 1}/{total_images}: {output_path}")

        return [path for path in generated_files if path is not None]
