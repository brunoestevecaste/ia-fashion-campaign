from io import BytesIO
import zipfile

import streamlit as st

from campaign_app.config import (
    DEFAULT_LOCATION,
    DEFAULT_MODEL_DESC,
    DEFAULT_STYLE,
    LOCATION_PROMPT_PRESETS,
    MODEL_DESC_PRESETS,
    STYLE_PROMPT_PRESETS,
)
from campaign_app.models import CampaignInputs, CampaignResult


def render_header() -> None:
    st.title("Fashion Campaign Shooting AI")
    st.caption("Genera 4 imagenes editoriales photorealistas en formato cuadrado 4K.")


def render_input_form() -> CampaignInputs:
    api_key = st.text_input(
        "Google API Key",
        type="password",
        help="No se guarda; solo se usa durante esta ejecucion.",
        placeholder="AIza...",
    )

    garment_file = st.file_uploader(
        "Fotografia de la prenda",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=False,
    )

    st.markdown("### Modo de generacion")
    render_mode = st.radio(
        "Selecciona modo",
        options=["Final", "Draft"],
        horizontal=True,
        index=0,
        key="render_mode",
        help="Final: 4 imagenes en 4K (maxima calidad). Draft: 2 imagenes en 1K (menor coste, iteracion rapida).",
    )

    st.markdown("### Estilo de campana")
    style_mode = st.radio(
        "Modo de estilo",
        options=["Preset optimizado", "Prompt personalizado"],
        horizontal=True,
        key="style_mode",
    )
    if style_mode == "Preset optimizado":
        style_preset_name = st.selectbox(
            "Selecciona un estilo por defecto",
            options=list(STYLE_PROMPT_PRESETS.keys()),
            key="style_preset_name",
        )
        style_desc = STYLE_PROMPT_PRESETS[style_preset_name]
    else:
        style_desc = st.text_area(
            "Prompt de estilo personalizado",
            value=DEFAULT_STYLE,
            height=140,
            key="style_prompt_custom",
        )

    st.markdown("### Ubicacion del shooting")
    location_mode = st.radio(
        "Modo de ubicacion",
        options=["Preset optimizado", "Prompt personalizado"],
        horizontal=True,
        key="location_mode",
    )
    if location_mode == "Preset optimizado":
        location_preset_name = st.selectbox(
            "Selecciona una ubicacion por defecto",
            options=list(LOCATION_PROMPT_PRESETS.keys()),
            key="location_preset_name",
        )
        location_desc = LOCATION_PROMPT_PRESETS[location_preset_name]
    else:
        location_desc = st.text_area(
            "Prompt de ubicacion personalizado",
            value=DEFAULT_LOCATION,
            height=140,
            key="location_prompt_custom",
        )

    st.markdown("### Referencia del modelo")
    model_mode = st.radio(
        "Modo de referencia de modelo",
        options=["Preset de descripcion", "Descripcion personalizada", "Subir imagen del modelo"],
        horizontal=True,
        key="model_mode",
    )
    model_image_file = None
    if model_mode == "Preset de descripcion":
        model_preset_name = st.selectbox(
            "Selecciona una descripcion por defecto",
            options=list(MODEL_DESC_PRESETS.keys()),
            key="model_preset_name",
        )
        model_desc = MODEL_DESC_PRESETS[model_preset_name]
    elif model_mode == "Descripcion personalizada":
        model_desc = st.text_area(
            "Descripcion fisica del modelo",
            value=DEFAULT_MODEL_DESC,
            height=180,
            key="model_desc_custom",
        )
    else:
        model_image_file = st.file_uploader(
            "Sube una imagen del modelo",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=False,
            key="model_image_file",
        )
        model_desc = ""

    return CampaignInputs(
        api_key=api_key,
        garment_file=garment_file,
        render_mode=render_mode,
        style_mode=style_mode,
        style_desc=style_desc,
        location_mode=location_mode,
        location_desc=location_desc,
        model_mode=model_mode,
        model_desc=model_desc,
        model_image_file=model_image_file,
    )


def render_results(result: CampaignResult) -> None:
    st.subheader("Prompts generados")
    for idx, prompt in enumerate(result.prompts, start=1):
        st.markdown(f"**Prompt {idx}:** {prompt}")

    st.subheader("Referencia de modelo")
    st.image(result.model_ref_bytes, use_container_width=False)

    st.subheader("Resultados del shooting")
    if result.result_images:
        zip_bytes = _build_campaign_zip(result.result_images)
        st.download_button(
            label="Descargar campana completa (ZIP)",
            data=zip_bytes,
            file_name="fashion_campaign_complete.zip",
            mime="application/zip",
            key="download_campaign_zip",
        )

    cols = st.columns(2)
    for idx, img_bytes in enumerate(result.result_images, start=1):
        col = cols[(idx - 1) % 2]
        with col:
            st.image(img_bytes, caption=f"Foto {idx}", use_container_width=True)
            st.download_button(
                label=f"Descargar foto {idx}",
                data=img_bytes,
                file_name=f"shooting_result_{idx}.png",
                mime="image/png",
                key=f"download_{idx}",
            )


def _build_campaign_zip(images: list[bytes]) -> bytes:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for idx, image_bytes in enumerate(images, start=1):
            zip_file.writestr(f"shooting_result_{idx}.png", image_bytes)
    return zip_buffer.getvalue()
