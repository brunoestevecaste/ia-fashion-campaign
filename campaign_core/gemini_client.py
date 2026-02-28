import base64

import requests
from google import genai

from campaign_core.constants import GEMINI_API_KEY


def resolve_api_key(api_key=None):
    resolved = api_key or GEMINI_API_KEY
    if not resolved:
        raise ValueError(
            "Falta la API key. Pasala como parametro o define la variable de entorno GEMINI_API_KEY."
        )
    return resolved


def build_client(api_key):
    return genai.Client(api_key=api_key)


def generate_image_via_rest(api_key, image_model, parts, aspect_ratio, image_size="4K"):
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{image_model}:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size,
            },
        },
    }

    response = requests.post(url, json=payload, timeout=180)
    if not response.ok:
        raise RuntimeError(
            f"Error REST {response.status_code} en generacion {image_size}: {response.text[:400]}"
        )

    data = response.json()
    for candidate in data.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            inline_data = part.get("inlineData")
            if inline_data and inline_data.get("data"):
                return base64.b64decode(inline_data["data"])

    raise RuntimeError(
        f"La API REST no devolvio imagen {image_size} ({aspect_ratio}) en la respuesta."
    )


def generate_image_4k_via_rest(api_key, image_model, parts, aspect_ratio):
    return generate_image_via_rest(
        api_key=api_key,
        image_model=image_model,
        parts=parts,
        aspect_ratio=aspect_ratio,
        image_size="4K",
    )
