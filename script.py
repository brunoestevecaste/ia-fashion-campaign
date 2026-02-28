import base64
import json
import os
from io import BytesIO
from typing import Callable, Optional

from PIL import Image
from google import genai
from google.genai import types
import requests

# --- CONFIGURACION ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ANALYSIS_MODEL = "gemini-3-pro-preview"
IMAGE_MODEL = "gemini-3-pro-image-preview"
FINAL_IMAGE_SIZE = 4096
FINAL_ASPECT_RATIO = "1:1"


class FashionCampaignAI:
    def __init__(self, api_key: Optional[str] = None, logger: Optional[Callable[[str], None]] = None):
        api_key = api_key or GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "Falta la API key. Pasala como parametro o define la variable de entorno GEMINI_API_KEY."
            )
        self.api_key = api_key
        self.logger = logger
        self.client = genai.Client(api_key=api_key)

    def _log(self, message):
        if self.logger:
            self.logger(message)
            return
        print(message)

    def _detect_mime_type(self, image_path):
        lower_path = image_path.lower()
        if lower_path.endswith(".png"):
            return "image/png"
        if lower_path.endswith(".webp"):
            return "image/webp"
        return "image/jpeg"

    def _extract_json(self, text):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start = text.find("{")
            end = text.rfind("}")
            if start == -1 or end == -1 or end <= start:
                raise ValueError("No se pudo extraer JSON valido de la respuesta.")
            return json.loads(text[start : end + 1])

    def _extract_image_bytes(self, response):
        for candidate in response.candidates or []:
            for part in candidate.content.parts or []:
                if part.inline_data and part.inline_data.data:
                    return part.inline_data.data

        diag = []
        for idx, candidate in enumerate(response.candidates or [], start=1):
            finish_reason = getattr(candidate, "finish_reason", None)
            if finish_reason:
                diag.append(f"candidate_{idx}.finish_reason={finish_reason}")
            content = getattr(candidate, "content", None)
            if content:
                text_parts = []
                for part in content.parts or []:
                    text_value = getattr(part, "text", None)
                    if text_value:
                        text_parts.append(text_value.strip())
                if text_parts:
                    diag.append(
                        f"candidate_{idx}.text={(' '.join(text_parts))[:240]}"
                    )

        diag_msg = " | ".join(diag) if diag else "sin detalles del candidato"
        raise RuntimeError(f"La respuesta no incluyo una imagen. Diagnostico: {diag_msg}")

    def _extract_text(self, response):
        text_parts = []
        for candidate in response.candidates or []:
            content = getattr(candidate, "content", None)
            if not content:
                continue
            for part in content.parts or []:
                text_value = getattr(part, "text", None)
                if text_value:
                    text_parts.append(text_value)
        return "\n".join(text_parts).strip()

    def _save_square_png(self, image_bytes, output_path, size=1024):
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
        width, height = image.size
        side = min(width, height)
        left = (width - side) // 2
        top = (height - side) // 2
        square = image.crop((left, top, left + side, top + side))
        square = square.resize((size, size), Image.Resampling.LANCZOS)
        square.save(output_path, format="PNG")
        return output_path

    def _prepare_reference_image_jpeg(self, image_path, max_side=1280, quality=90):
        image = Image.open(image_path).convert("RGB")
        width, height = image.size
        longest_side = max(width, height)

        if longest_side > max_side:
            scale = max_side / float(longest_side)
            new_width = max(1, int(width * scale))
            new_height = max(1, int(height * scale))
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=quality, optimize=True)
        return buffer.getvalue(), "image/jpeg"

    def _generate_image_4k_via_rest(self, parts, aspect_ratio=FINAL_ASPECT_RATIO):
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{IMAGE_MODEL}:generateContent?key={self.api_key}"
        )
        payload = {
            "contents": [{"role": "user", "parts": parts}],
            "generationConfig": {
                "responseModalities": ["IMAGE"],
                "imageConfig": {
                    "aspectRatio": aspect_ratio,
                    "imageSize": "4K",
                },
            },
        }

        response = requests.post(url, json=payload, timeout=180)
        if not response.ok:
            raise RuntimeError(
                f"Error REST {response.status_code} en generacion 4K: {response.text[:400]}"
            )

        data = response.json()
        for candidate in data.get("candidates", []):
            content = candidate.get("content", {})
            for part in content.get("parts", []):
                inline_data = part.get("inlineData")
                if inline_data and inline_data.get("data"):
                    return base64.b64decode(inline_data["data"])

        raise RuntimeError(
            f"La API REST no devolvio imagen 4K ({aspect_ratio}) en la respuesta."
        )

    def generate_model_reference(self, model_desc, output_path="model_reference.png"):
        self._log("Generando imagen de referencia del modelo...")

        prompt = f"""
Create a photorealistic CLOSE-UP model reference image for identity consistency.

Model description:
{model_desc}

Requirements:
- Tight close-up portrait, front-facing.
- Neutral expression, even studio lighting, clean plain background.
- No dramatic pose, no accessories covering face, no text or watermark.
- Fashion casting style, realistic skin texture.
- Composition (1:1).
"""

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

        prompt = f"""
You are a world-class high-fashion creative director and Vogue-level editorial photographer.

CAMPAIGN INPUT:
- Style: {style}
- Location: {location}

TASK:
Generate exactly 4 highly detailed image prompts in ENGLISH for a high-fashion photorealistic campaign.
The final generation system will receive:
1) A garment reference photo.
2) A single model reference photo.

So your prompts must focus on scene direction only:
- composition
- camera language
- pose
- mood
- lighting
- editorial storytelling
- background atmosphere

Creative constraints:
- Respect and amplify the user inputs for style and location.
- Keep all 4 prompts visually coherent as one campaign narrative.
- Every prompt must target SQUARE framing (1:1) and print-ready 4K detail.
- The look must be strictly photorealistic (no illustration, no CGI, no surreal distortion).
- Include premium fashion-photography language: lens choice, camera height/angle, body language,
  fabric behavior, skin and hair micro-texture, and nuanced lighting behavior.

Visual direction must be consistent across all prompts:
- high-fashion streetwear attitude
- cinematic editorial lighting with sculpted highlights and dimensional shadows
- controlled contrast, realistic atmospheric depth, and refined color grading
- high micro-detail in skin, fabrics, hair, and architectural textures
- strictly hyperrealistic fashion photography (no stylized or illustrative look)
- premium high-fashion editorial quality suitable for print magazine

Use these mandatory variations:
1) full body + walking pose
2) medium shot + seated pose
3) low-angle shot + static pose
4) detail shot + in-motion pose

For each prompt, explicitly include:
- framing and shot scale
- focal length (in mm)
- camera perspective
- lighting direction and quality
- emotional tone
- environment cues derived from the location input

Return ONLY valid JSON using this exact format:
{{
  "prompts": ["prompt 1", "prompt 2", "prompt 3", "prompt 4"]
}}
"""

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

            final_instruction = f"""
You will receive reference images:
1) GARMENT_REFERENCE: preserve garment identity exactly (shape, details, colors, materials).
2) MODEL_REFERENCE: preserve facial identity, hairstyle, and overall model look.

Generate ONE photorealistic high-fashion campaign image using this direction:
{prompt_text}

Hard constraints:
- Keep the same garment and same model identity from references.
- Output must be square (1:1), native 4K (4096x4096).
- No text, logo, watermark, or frame.
- Strictly hyperrealistic quality, suitable for a top-tier fashion magazine.
- Preserve physically plausible anatomy, realistic skin detail, and true-to-life fabric rendering.
- Maintain a premium high-fashion editorial atmosphere aligned with the prompt direction.
"""

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


def main():
    garment_image_path = "mi_prenda.webp"
    user_style = (
        "Hyperrealistic high-fashion streetwear campaign with a premium editorial direction; "
        "cinematic golden-hour color grading, elevated urban styling, and refined magazine-quality composition. "
        "Mood: confident, modern, and sophisticated."
    )
    user_location = (
        "A high rooftop at sunset above a dense city skyline, with concrete surfaces, parapets, railings, "
        "architectural service structures, warm low-angle sunlight, and atmospheric haze that enhances depth "
        "for hyperrealistic high-fashion editorial photography."
    )
    user_model_desc = (
        "Young woman with radiant, natural beauty. She has a symmetrical oval face with smooth white skin "
        "covered in delicate freckles across her nose and cheeks. Her eyes are almond-shaped, light hazel-green "
        "with a soft, captivating gaze, framed by defined eyebrows that are full and natural. Her nose is small "
        "and proportionate, with subtle definition. She has full, well-shaped lips with a soft natural pink tone. "
        "Her hair is curly, voluminous, and black with platinum blond undertones, styled half-up and half-down, "
        "with loose curls framing her forehead and temples. The curls are defined and bouncy, adding texture around her head. "
    )

    if not os.path.exists(garment_image_path):
        print(f"Error: coloca una imagen llamada '{garment_image_path}' en esta carpeta.")
        return

    bot = FashionCampaignAI()

    model_reference_path = bot.get_or_generate_single_model_reference(
        user_model_desc, model_dir="model"
    )

    prompts_list = bot.generate_shoot_prompts(user_style, user_location)
    files = bot.execute_shooting(
        prompts=prompts_list,
        garment_image_path=garment_image_path,
        model_reference_path=model_reference_path,
    )

    print(f"\nShooting finalizado. Imagenes generadas: {files}")


if __name__ == "__main__":
    main()
