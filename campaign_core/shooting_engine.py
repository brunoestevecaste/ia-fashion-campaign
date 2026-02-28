import base64
import os
from typing import Callable, Optional

from google.genai import types

from campaign_core.constants import (
    ANALYSIS_MODEL,
    FINAL_ASPECT_RATIO,
    FINAL_IMAGE_SIZE,
    IMAGE_MODEL,
)
from campaign_core.gemini_client import (
    build_client,
    generate_image_4k_via_rest,
    resolve_api_key,
)
from campaign_core.image_utils import (
    detect_mime_type,
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

    def _detect_mime_type(self, image_path):
        return detect_mime_type(image_path)

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

    def _generate_image_4k_via_rest(self, parts, aspect_ratio=FINAL_ASPECT_RATIO):
        return generate_image_4k_via_rest(
            api_key=self.api_key,
            image_model=IMAGE_MODEL,
            parts=parts,
            aspect_ratio=aspect_ratio,
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

    def generate_shoot_prompts(self, style, location):
        self._log("Generando conceptos creativos para el shooting...")

        prompt = build_shoot_prompts_request(style, location)
        response = self.client.models.generate_content(
            model=ANALYSIS_MODEL,
            contents=prompt,
        )

        result = self._extract_json(self._extract_text(response))
        prompts = result.get("prompts")

        if not isinstance(prompts, list) or len(prompts) != 4:
            raise ValueError("El modelo no devolvio exactamente 4 prompts.")
        return prompts

    def execute_shooting(self, prompts, garment_image_path, model_reference_path, output_dir="."):
        self._log("Iniciando sesion de fotos (generando imagenes finales)...")
        generated_files = []
        os.makedirs(output_dir, exist_ok=True)

        garment_bytes, garment_mime = self._prepare_reference_image_jpeg(
            garment_image_path
        )
        model_bytes, model_mime = self._prepare_reference_image_jpeg(
            model_reference_path
        )

        for i, prompt_text in enumerate(prompts):
            self._log(f"   Generando foto {i + 1}/4")

            final_instruction = build_final_image_instruction(prompt_text)

            image_bytes = None
            last_error = None
            for attempt in range(1, 4):
                try:
                    rest_parts = [
                        {"text": "GARMENT_REFERENCE"},
                        {
                            "inlineData": {
                                "mimeType": garment_mime,
                                "data": base64.b64encode(garment_bytes).decode("utf-8"),
                            }
                        },
                        {"text": "MODEL_REFERENCE"},
                        {
                            "inlineData": {
                                "mimeType": model_mime,
                                "data": base64.b64encode(model_bytes).decode("utf-8"),
                            }
                        },
                        {"text": final_instruction},
                    ]
                    image_bytes = self._generate_image_4k_via_rest(
                        rest_parts, aspect_ratio=FINAL_ASPECT_RATIO
                    )
                    break
                except Exception as exc:
                    last_error = exc
                    self._log(
                        f"   Reintento {attempt}/3: fallo al generar imagen 4K para la foto {i + 1}."
                    )

            if image_bytes is None:
                raise RuntimeError(
                    f"No se pudo generar la foto {i + 1} tras 3 intentos. {last_error}"
                )

            output_file = os.path.join(output_dir, f"shooting_result_{i + 1}.png")
            self._save_square_png(
                image_bytes, output_path=output_file, size=FINAL_IMAGE_SIZE
            )
            generated_files.append(output_file)
            self._log(f"   Guardada: {output_file}")

        return generated_files

