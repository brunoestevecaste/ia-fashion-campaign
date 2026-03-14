import base64
import random
import time
from typing import Optional

import requests
from google import genai

from campaign_core.constants import GEMINI_API_KEY
from campaign_app.security import redact_sensitive_text


RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}


def resolve_api_key(api_key=None):
    resolved = api_key or GEMINI_API_KEY
    if not resolved:
        raise ValueError(
            "Falta la API key. Pasala como parametro o define la variable de entorno GEMINI_API_KEY."
        )
    return resolved


def build_client(api_key):
    return genai.Client(api_key=api_key)


def _sleep_with_backoff(attempt: int, base_seconds: float) -> None:
    delay = base_seconds * (2 ** (attempt - 1))
    jitter = random.uniform(0, min(1.0, delay * 0.2))
    time.sleep(delay + jitter)


def _safe_error_text(value) -> str:
    return redact_sensitive_text(str(value))


def generate_image_via_rest(
    api_key,
    image_model,
    parts,
    aspect_ratio,
    image_size="4K",
    timeout_seconds=180,
    max_retries=3,
    backoff_base_seconds=1.0,
    session: Optional[requests.Session] = None,
):
    if max_retries < 1:
        raise ValueError("max_retries debe ser >= 1.")

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

    managed_session = session or requests.Session()
    should_close_session = session is None
    last_error = None

    try:
        for attempt in range(1, max_retries + 1):
            try:
                response = managed_session.post(url, json=payload, timeout=timeout_seconds)
            except requests.RequestException as exc:
                last_error = exc
                if attempt == max_retries:
                    raise RuntimeError(
                        "Error de conexion al generar imagen "
                        f"{image_size} tras {max_retries} intentos: {_safe_error_text(exc)}"
                    ) from exc
                _sleep_with_backoff(attempt=attempt, base_seconds=backoff_base_seconds)
                continue

            if response.ok:
                try:
                    data = response.json()
                except ValueError as exc:
                    last_error = exc
                    if attempt == max_retries:
                        raise RuntimeError(
                            f"Respuesta JSON invalida en generacion {image_size} tras {max_retries} intentos."
                        ) from exc
                    _sleep_with_backoff(attempt=attempt, base_seconds=backoff_base_seconds)
                    continue

                for candidate in data.get("candidates", []):
                    content = candidate.get("content", {})
                    for part in content.get("parts", []):
                        inline_data = part.get("inlineData")
                        if inline_data and inline_data.get("data"):
                            return base64.b64decode(inline_data["data"])

                last_error = RuntimeError(
                    f"La API REST no devolvio imagen {image_size} ({aspect_ratio}) en la respuesta."
                )
                if attempt == max_retries:
                    raise last_error
                _sleep_with_backoff(attempt=attempt, base_seconds=backoff_base_seconds)
                continue

            last_error = RuntimeError(
                "Error REST "
                f"{response.status_code} en generacion {image_size}: {_safe_error_text(response.text[:400])}"
            )
            if response.status_code not in RETRYABLE_STATUS_CODES or attempt == max_retries:
                raise last_error
            _sleep_with_backoff(attempt=attempt, base_seconds=backoff_base_seconds)
    finally:
        if should_close_session:
            managed_session.close()

    raise RuntimeError(
        "No se pudo generar imagen "
        f"{image_size} tras {max_retries} intentos. Error final: {_safe_error_text(last_error)}"
    )
