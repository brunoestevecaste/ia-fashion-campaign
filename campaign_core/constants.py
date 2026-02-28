import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ANALYSIS_MODEL_FLASH = "gemini-3-flash-preview"
ANALYSIS_MODEL_PRO = "gemini-3-pro-preview"
# Backward compatibility alias
ANALYSIS_MODEL = ANALYSIS_MODEL_PRO
IMAGE_MODEL = "gemini-3-pro-image-preview"
FINAL_IMAGE_SIZE = 4096
FINAL_ASPECT_RATIO = "1:1"

DEFAULT_RENDER_MODE = "Final"
RENDER_MODE_CONFIG = {
    "Draft": {
        "max_images": 2,
        "image_size": "1K",
        "output_size": 1024,
    },
    "Final": {
        "max_images": 4,
        "image_size": "4K",
        "output_size": 4096,
    },
}
