import json
from io import BytesIO

from PIL import Image


def detect_mime_type(image_path):
    lower_path = image_path.lower()
    if lower_path.endswith(".png"):
        return "image/png"
    if lower_path.endswith(".webp"):
        return "image/webp"
    return "image/jpeg"


def extract_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No se pudo extraer JSON valido de la respuesta.")
        return json.loads(text[start : end + 1])


def extract_image_bytes(response):
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


def extract_text(response):
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


def save_square_png(image_bytes, output_path, size=1024):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    width, height = image.size
    side = min(width, height)
    left = (width - side) // 2
    top = (height - side) // 2
    square = image.crop((left, top, left + side, top + side))
    square = square.resize((size, size), Image.Resampling.LANCZOS)
    square.save(output_path, format="PNG")
    return output_path


def prepare_reference_image_jpeg(image_path, max_side=1280, quality=90):
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

