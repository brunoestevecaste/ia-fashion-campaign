import os
import tempfile
from typing import Callable

from campaign_app.models import CampaignInputs, CampaignResult
from campaign_core.constants import DEFAULT_RENDER_MODE, RENDER_MODE_CONFIG
from script import FashionCampaignAI


def run_campaign_pipeline(
    inputs: CampaignInputs,
    logger: Callable[[str], None],
) -> CampaignResult:
    render_mode = inputs.render_mode if inputs.render_mode in RENDER_MODE_CONFIG else DEFAULT_RENDER_MODE
    render_cfg = RENDER_MODE_CONFIG[render_mode]
    logger(
        f"Modo {render_mode}: {render_cfg['max_images']} imagen(es), "
        f"{render_cfg['image_size']} de generacion, salida {render_cfg['output_size']}px."
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        garment_ext = os.path.splitext(inputs.garment_file.name)[1] or ".jpg"
        garment_path = os.path.join(tmp_dir, f"garment_input{garment_ext}")
        with open(garment_path, "wb") as garment_output:
            garment_output.write(inputs.garment_file.getbuffer())

        model_dir = os.path.join(tmp_dir, "model")
        output_dir = os.path.join(tmp_dir, "results")
        os.makedirs(model_dir, exist_ok=True)

        bot = FashionCampaignAI(api_key=inputs.api_key.strip(), logger=logger)
        if inputs.model_mode == "Subir imagen del modelo":
            model_ext = os.path.splitext(inputs.model_image_file.name)[1] or ".jpg"
            model_reference_path = os.path.join(model_dir, f"model_reference_upload{model_ext}")
            with open(model_reference_path, "wb") as model_output:
                model_output.write(inputs.model_image_file.getbuffer())
            logger(f"Usando imagen de modelo subida: {inputs.model_image_file.name}")
        else:
            model_reference_path = bot.get_or_generate_cached_model_reference(
                inputs.model_desc,
                cache_dir=os.path.join(".cache", "model_refs"),
            )

        prompts = bot.generate_shoot_prompts(inputs.style_desc, inputs.location_desc)
        prompts_for_render = prompts[: render_cfg["max_images"]]
        generated_paths = bot.execute_shooting(
            prompts=prompts_for_render,
            garment_image_path=garment_path,
            model_reference_path=model_reference_path,
            output_dir=output_dir,
            max_images=render_cfg["max_images"],
            output_size=render_cfg["output_size"],
            image_size=render_cfg["image_size"],
        )

        with open(model_reference_path, "rb") as model_ref_file:
            model_ref_bytes = model_ref_file.read()

        result_images: list[bytes] = []
        for path in generated_paths:
            with open(path, "rb") as image_file:
                result_images.append(image_file.read())

    return CampaignResult(
        prompts=prompts_for_render,
        model_ref_bytes=model_ref_bytes,
        result_images=result_images,
    )
