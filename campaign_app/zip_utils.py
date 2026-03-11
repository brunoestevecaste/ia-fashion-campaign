from io import BytesIO
import zipfile


def build_campaign_zip(images: list[bytes]) -> bytes:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for idx, image_bytes in enumerate(images, start=1):
            zip_file.writestr(f"shooting_result_{idx}.png", image_bytes)
    return zip_buffer.getvalue()
