import os
import tempfile

import streamlit as st

from script import FashionCampaignAI

DEFAULT_STYLE = (
    "Hyperrealistic high-fashion streetwear campaign with a premium editorial direction; "
    "cinematic golden-hour color grading, elevated urban styling, and refined magazine-quality composition. "
    "Mood: confident, modern, and sophisticated."
)

DEFAULT_LOCATION = (
    "A high rooftop at sunset above a dense city skyline, with concrete surfaces, parapets, railings, "
    "architectural service structures, warm low-angle sunlight, and atmospheric haze that enhances depth "
    "for hyperrealistic high-fashion editorial photography."
)

DEFAULT_MODEL_DESC = (
    "Young woman with radiant, natural beauty. She has a symmetrical oval face with smooth white skin "
    "covered in delicate freckles across her nose and cheeks. Her eyes are almond-shaped, light hazel-green "
    "with a soft, captivating gaze, framed by defined eyebrows that are full and natural. Her nose is small "
    "and proportionate, with subtle definition. She has full, well-shaped lips with a soft natural pink tone. "
    "Her hair is curly, voluminous, and black with platinum blond undertones, styled half-up and half-down, "
    "with loose curls framing her forehead and temples. The curls are defined and bouncy, adding texture around her head."
)

st.set_page_config(page_title="Fashion Campaign Generator", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #2e231f;
        --ink: #dcc4a4;
        --panel: color-mix(in srgb, var(--ink) 92%, var(--bg) 8%);
        --panel-text: var(--bg);
        --surface: color-mix(in srgb, var(--bg) 84%, var(--ink) 16%);
        --surface-soft: color-mix(in srgb, var(--bg) 90%, var(--ink) 10%);
        --stroke: color-mix(in srgb, var(--ink) 62%, var(--bg) 38%);
        --stroke-strong: color-mix(in srgb, var(--ink) 80%, var(--bg) 20%);
    }

    .stApp {
        background: radial-gradient(circle at 20% 0%, var(--surface) 0%, var(--bg) 60%);
        color: var(--ink);
    }

    .main .block-container {
        background: var(--surface-soft);
        border: 1px solid var(--stroke-strong);
        border-radius: 18px;
        padding: 1.5rem 1.25rem 2rem;
    }

    h1, h2, h3, h4, h5, h6, p, label, small {
        color: var(--ink) !important;
    }

    [data-testid="stSidebar"] {
        background: var(--surface);
        border-right: 1px solid var(--stroke-strong);
    }

    [data-testid="stForm"] {
        background: color-mix(in srgb, var(--bg) 86%, var(--ink) 14%);
        border: 1px solid var(--stroke);
        border-radius: 16px;
        padding: 1rem 1rem 0.5rem;
    }

    [data-testid="stTextInputRootElement"] > div,
    [data-testid="stTextArea"] textarea,
    [data-testid="stFileUploaderDropzone"] {
        background: var(--panel) !important;
        color: var(--panel-text) !important;
        border-radius: 12px !important;
        border: 2px solid var(--stroke-strong) !important;
    }

    [data-testid="stTextInputRootElement"] input,
    [data-testid="stTextArea"] textarea {
        color: var(--panel-text) !important;
        caret-color: var(--panel-text) !important;
    }

    [data-testid="stTextInputRootElement"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {
        color: color-mix(in srgb, var(--bg) 78%, var(--ink) 22%) !important;
        opacity: 1 !important;
    }

    [data-testid="stTextInputRootElement"] > div:focus-within,
    [data-testid="stTextArea"] textarea:focus,
    [data-testid="stFileUploaderDropzone"]:focus-within {
        border-color: var(--stroke-strong) !important;
        box-shadow: 0 0 0 2px color-mix(in srgb, var(--ink) 60%, transparent) !important;
    }

    .stButton button,
    .stDownloadButton button {
        background: var(--ink) !important;
        color: var(--bg) !important;
        border: 2px solid var(--ink) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        background: color-mix(in srgb, var(--ink) 80%, var(--bg) 20%) !important;
        color: var(--bg) !important;
    }

    .stButton button:focus,
    .stDownloadButton button:focus {
        box-shadow: 0 0 0 3px color-mix(in srgb, var(--ink) 55%, transparent) !important;
    }

    [data-testid="stStatusWidget"] {
        background: color-mix(in srgb, var(--bg) 82%, var(--ink) 18%);
        border: 1px solid var(--stroke-strong);
        border-radius: 12px;
    }

    [data-testid="stAlert"] {
        background: color-mix(in srgb, var(--bg) 80%, var(--ink) 20%) !important;
        border: 1px solid var(--stroke-strong) !important;
    }

    [data-testid="stAlert"] * {
        color: var(--ink) !important;
    }

    [data-testid="stCodeBlock"] {
        background: color-mix(in srgb, var(--bg) 78%, var(--ink) 22%) !important;
        color: var(--ink) !important;
        border: 1px solid var(--stroke-strong) !important;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Fashion Campaign Shooting AI")
st.caption("Genera 4 imagenes editoriales a partir de la prenda y tus indicaciones creativas.")

with st.form("campaign_form"):
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

    style_desc = st.text_area("Descripcion del estilo de shooting", value=DEFAULT_STYLE, height=120)
    location_desc = st.text_area("Descripcion de la ubicacion", value=DEFAULT_LOCATION, height=120)
    model_desc = st.text_area("Descripcion fisica del modelo", value=DEFAULT_MODEL_DESC, height=180)

    submitted = st.form_submit_button("Generar shooting")

if submitted:
    missing_fields = []
    if not api_key.strip():
        missing_fields.append("API key de Google")
    if garment_file is None:
        missing_fields.append("fotografia de la prenda")
    if not style_desc.strip():
        missing_fields.append("descripcion del estilo")
    if not location_desc.strip():
        missing_fields.append("descripcion de la ubicacion")
    if not model_desc.strip():
        missing_fields.append("descripcion fisica del modelo")

    if missing_fields:
        st.error(f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        st.stop()

    log_messages = []
    log_placeholder = st.empty()

    def ui_logger(message: str):
        log_messages.append(message)
        log_placeholder.code("\n".join(log_messages), language="text")

    with st.status("Ejecutando pipeline de generacion...", expanded=True) as status:
        try:
            with tempfile.TemporaryDirectory() as tmp_dir:
                garment_ext = os.path.splitext(garment_file.name)[1] or ".jpg"
                garment_path = os.path.join(tmp_dir, f"garment_input{garment_ext}")
                with open(garment_path, "wb") as f:
                    f.write(garment_file.getbuffer())

                model_dir = os.path.join(tmp_dir, "model")
                output_dir = os.path.join(tmp_dir, "results")

                bot = FashionCampaignAI(api_key=api_key.strip(), logger=ui_logger)
                model_reference_path = bot.get_or_generate_single_model_reference(
                    model_desc,
                    model_dir=model_dir,
                )
                prompts = bot.generate_shoot_prompts(style_desc, location_desc)
                generated_paths = bot.execute_shooting(
                    prompts=prompts,
                    garment_image_path=garment_path,
                    model_reference_path=model_reference_path,
                    output_dir=output_dir,
                )

                with open(model_reference_path, "rb") as model_ref_file:
                    model_ref_bytes = model_ref_file.read()

                result_images = []
                for path in generated_paths:
                    with open(path, "rb") as image_file:
                        result_images.append(image_file.read())

            status.update(label="Shooting completado", state="complete")
        except Exception as exc:
            status.update(label="Error durante la generacion", state="error")
            st.error(f"No se pudo completar el shooting: {exc}")
            st.stop()

    st.subheader("Prompts generados")
    for idx, prompt in enumerate(prompts, start=1):
        st.markdown(f"**Prompt {idx}:** {prompt}")

    st.subheader("Referencia de modelo")
    st.image(model_ref_bytes, use_container_width=False)

    st.subheader("Resultados del shooting")
    cols = st.columns(2)
    for idx, img_bytes in enumerate(result_images, start=1):
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
