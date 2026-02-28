from campaign_app.models import CampaignInputs


def validate_inputs(inputs: CampaignInputs) -> list[str]:
    missing_fields: list[str] = []

    if not inputs.api_key.strip():
        missing_fields.append("API key de Google")
    if inputs.garment_file is None:
        missing_fields.append("fotografia de la prenda")
    if inputs.style_mode == "Prompt personalizado" and not inputs.style_desc.strip():
        missing_fields.append("descripcion del estilo")
    if inputs.location_mode == "Prompt personalizado" and not inputs.location_desc.strip():
        missing_fields.append("descripcion de la ubicacion")
    if inputs.model_mode in {"Preset de descripcion", "Descripcion personalizada"} and not inputs.model_desc.strip():
        missing_fields.append("descripcion fisica del modelo")
    if inputs.model_mode == "Subir imagen del modelo" and inputs.model_image_file is None:
        missing_fields.append("imagen del modelo")

    return missing_fields

