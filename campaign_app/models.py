from dataclasses import dataclass
from typing import Optional, Protocol


class UploadedAsset(Protocol):
    name: str

    def getbuffer(self):
        ...


@dataclass
class CampaignInputs:
    api_key: str
    garment_file: Optional[UploadedAsset]
    render_mode: str
    style_mode: str
    style_desc: str
    location_mode: str
    location_desc: str
    model_mode: str
    model_desc: str
    model_image_file: Optional[UploadedAsset]


@dataclass
class CampaignResult:
    prompts: list[str]
    model_ref_bytes: bytes
    model_ref_mime: str
    result_images: list[bytes]
    zip_bytes: bytes = b""
