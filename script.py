import os

from campaign_core.constants import (
    ANALYSIS_MODEL,
    FINAL_ASPECT_RATIO,
    FINAL_IMAGE_SIZE,
    GEMINI_API_KEY,
    IMAGE_MODEL,
)
from campaign_core.shooting_engine import FashionCampaignAI

__all__ = [
    "FashionCampaignAI",
    "GEMINI_API_KEY",
    "ANALYSIS_MODEL",
    "IMAGE_MODEL",
    "FINAL_IMAGE_SIZE",
    "FINAL_ASPECT_RATIO",
]


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

