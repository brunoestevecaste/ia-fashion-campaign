from dataclasses import dataclass
from typing import Any


@dataclass
class CampaignInputs:
    api_key: str
    garment_file: Any
    style_mode: str
    style_desc: str
    location_mode: str
    location_desc: str
    model_mode: str
    model_desc: str
    model_image_file: Any


@dataclass
class CampaignResult:
    prompts: list[str]
    model_ref_bytes: bytes
    result_images: list[bytes]

