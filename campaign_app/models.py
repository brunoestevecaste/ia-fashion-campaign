from dataclasses import dataclass
from typing import Optional

from streamlit.runtime.uploaded_file_manager import UploadedFile


@dataclass
class CampaignInputs:
    api_key: str
    garment_file: Optional[UploadedFile]
    render_mode: str
    style_mode: str
    style_desc: str
    location_mode: str
    location_desc: str
    model_mode: str
    model_desc: str
    model_image_file: Optional[UploadedFile]


@dataclass
class CampaignResult:
    prompts: list[str]
    model_ref_bytes: bytes
    result_images: list[bytes]
