import os
import tempfile
import streamlit as st
from script import FashionCampaignAI

DEFAULT_STYLE = (
    "Photorealistic high-fashion campaign with luxury editorial direction, "
    "print-magazine quality art direction, refined cinematic color grading, and elegant visual storytelling. "
    "Mood: confident, modern, and sophisticated."
)

DEFAULT_LOCATION = (
    "A high rooftop at sunset above a dense city skyline, with concrete surfaces, parapets, railings, "
    "architectural service structures, warm low-angle sunlight, and atmospheric haze that enhances depth "
    "for hyperrealistic high-fashion editorial photography."
)

STYLE_PROMPT_PRESETS = {
    "Luxury Editorial Minimalism": (
        "Luxury high-fashion editorial styling with clean visual hierarchy, understated sophistication, "
        "precise tailoring emphasis, restrained neutral palette, controlled body language, polished wardrobe "
        "coordination, and magazine-grade refinement focused on elegance and exclusivity."
    ),
    "Avant-Garde Couture Drama": (
        "Avant-garde couture styling with bold sculptural silhouettes, dramatic proportion play, visual tension "
        "between structure and movement, experimental layering, assertive pose language, and runway-level "
        "editorial intensity with rich textile detail."
    ),
    "90s Supermodel Power": (
        "Iconic 90s supermodel styling with commanding pose language, strong attitude, glossy magazine polish, "
        "high-contrast wardrobe direction, timeless silhouette choices, and bold confidence-driven editorial impact."
    ),
    "Contemporary Quiet Luxury": (
        "Contemporary quiet-luxury styling with minimalist wardrobe storytelling, tactile premium fabrics, "
        "muted tonal harmony, subtle sensuality, clean line work, and an elegant premium mood with refined restraint."
    ),
    "Cinematic Urban Glamour": (
        "Cinematic urban glamour styling with dynamic editorial rhythm, modern aspirational attitude, "
        "premium street-luxury wardrobe combinations, bolder contrasts, expressive movement cues, and impactful "
        "magazine-ready visual energy."
    ),
    "Neo-Noir Night Editorial": (
        "Neo-noir editorial styling with deep black tonal control, sleek monochrome accents, sharp silhouette definition, "
        "dramatic tension, minimal yet precise accessories, and dark cinematic fashion attitude."
    ),
    "Sport-Luxe Precision": (
        "Sport-luxe styling that balances athletic energy with couture refinement, dynamic body language, "
        "technical textile focus, functional layering, clean modern lines, and high-performance luxury attitude."
    ),
    "Romantic Haute Boheme": (
        "Romantic haute-boheme styling with graceful movement, soft yet intentional layering, flowing silhouettes, "
        "organic texture depth, poetic mood, and delicate luxury detailing with elevated editorial softness."
    ),
    "Monochrome Studio Authority": (
        "Monochrome styling direction with assertive silhouette emphasis, disciplined tonal palette, minimal distractions, "
        "sharp tailoring, strong authority-driven pose language, and polished high-fashion editorial clarity."
    ),
    "Futurist Metallic Couture": (
        "Futurist couture styling with metallic accents, clean geometric layering, directional fashion poses, "
        "forward-looking luxury attitude, technical-glam finish, and bold next-generation editorial expression."
    ),
}

LOCATION_PROMPT_PRESETS = {
    "Sunset Rooftop Skyline": (
        "High rooftop at sunset above a dense metropolitan skyline, with concrete textures, railings, service "
        "structures, warm low-angle sun, long shadows, and layered atmospheric urban depth."
    ),
    "Brutalist Museum Forecourt": (
        "Open-air brutalist museum forecourt with monumental concrete geometry, strong linear perspective, "
        "clean negative space, hard edges, and directional daylight with sculpted shadows."
    ),
    "Historic European Avenue": (
        "Historic European avenue with classic facades, stone pavement, wrought-iron details, subtle street reflections, "
        "deep perspective lines, and soft natural light across architectural surfaces."
    ),
    "Industrial Loft Daylight": (
        "Large industrial loft with tall steel-frame windows, textured walls, polished concrete flooring, "
        "soft directional daylight, and natural interior depth with gentle light falloff."
    ),
    "Coastal Cliff Golden Hour": (
        "Coastal cliff landscape at golden hour with textured rock formations, clean horizon separation, "
        "salt-air haze, warm highlights, and expansive natural depth."
    ),
    "Art Deco Hotel Lobby": (
        "Grand art deco hotel lobby with geometric symmetry, polished stone floors, brass accents, patterned walls, "
        "warm ambient interior light, and layered architectural depth."
    ),
    "Desert Modernist Villa": (
        "Desert modernist villa with travertine and concrete planes, open volumes, dry atmosphere, "
        "sun-sculpted shadows, and clean architectural transitions."
    ),
    "Tokyo Neon Backstreet": (
        "Narrow Tokyo backstreet at blue hour with neon signage glow, wet asphalt reflections, dense vertical details, "
        "tight urban perspective, and layered city ambience."
    ),
    "Marble Gallery Hall": (
        "Large marble gallery hall with monumental columns, pristine stone surfaces, soft directional top light, "
        "subtle reflections, and calm museum-scale symmetry."
    ),
    "Rainy Financial District Night": (
        "Modern financial district at night after rain, reflective pavement, glass-and-steel facades, light bloom, "
        "misty air, and deep metropolitan perspective."
    ),
    "Botanical Glasshouse": (
        "Historic botanical glasshouse with iron framework, diffused daylight through glass panels, layered greenery, "
        "subtle humidity haze, and rich organic depth."
    ),
}

DEFAULT_MODEL_DESC = (
    "Young woman with radiant, natural beauty. She has a symmetrical oval face with smooth white skin "
    "covered in delicate freckles across her nose and cheeks. Her eyes are almond-shaped, light hazel-green "
    "with a soft, captivating gaze, framed by defined eyebrows that are full and natural. Her nose is small "
    "and proportionate, with subtle definition. She has full, well-shaped lips with a soft natural pink tone. "
    "Her hair is curly, voluminous, and black with platinum blond undertones, styled half-up and half-down, "
    "with loose curls framing her forehead and temples. The curls are defined and bouncy, adding texture around her head."
)

MODEL_DESC_PRESETS = {
    "Freckled Natural Muse": DEFAULT_MODEL_DESC,
    "Androgynous Runway Edge": (
        "Young androgynous model with a sharp jawline and high cheekbones, neutral warm-beige skin tone, deep-set "
        "dark brown eyes, naturally full brows, straight nose bridge, and medium lips with subtle definition. Hair is "
        "short, dark, and slightly wet-textured, brushed back from the forehead. Overall look is modern, bold, and "
        "editorial with clean facial structure and minimal styling."
    ),
    "Afro-Textured Editorial Icon": (
        "Young woman with deep brown skin and luminous undertones, oval face, expressive almond-shaped eyes, softly "
        "arched brows, balanced nose profile, and full naturally defined lips. Hair is a voluminous, well-defined afro "
        "with rich texture and shape. The look feels powerful, elegant, and unmistakably high-fashion with realistic "
        "skin detail and strong editorial presence."
    ),
    "Mediterranean Classic Beauty": (
        "Young woman with olive skin, symmetrical face, hazel eyes, thick dark eyebrows, softly contoured straight nose, "
        "and full lips with a natural rose tone. Hair is long, dark chestnut, and glossy with soft waves parted at the center. "
        "Overall appearance is timeless, sophisticated, and suitable for premium fashion editorials."
    ),
    "East Asian Minimal Elegance": (
        "Young woman with porcelain-neutral skin tone, refined oval face, dark almond-shaped eyes, straight brows, "
        "small balanced nose, and softly sculpted lips. Hair is straight, jet black, and shoulder-length with a precise "
        "center part. The look is understated, modern, and highly editorial with clean, elegant facial harmony."
    ),
    "Mature Silver-Hair Authority": (
        "Mature woman with radiant fair skin showing natural texture, striking high cheekbones, grey-green eyes, "
        "defined eyebrows, elegant nose line, and balanced lips with subtle neutral tone. Hair is silver, shoulder-length, "
        "and styled in soft polished waves. Overall look conveys confidence, luxury, and iconic fashion authority."
    ),
    "Latin Curly Glamour": (
        "Young Latina model with warm golden-olive skin, bright brown eyes, softly arched eyebrows, refined nose bridge, "
        "and naturally full lips. Hair is long, dark brown, and densely curly with controlled volume and healthy shine. "
        "The face is expressive and magnetic, with a glamorous yet realistic high-fashion editorial presence."
    ),
    "Classic Tailored Male Lead": (
        "Young man with defined jawline, balanced oval face, medium-light warm skin tone, deep brown eyes, "
        "thick natural eyebrows, straight nose bridge, and medium full lips. Hair is short, dark brown, neatly "
        "textured with subtle volume on top. Overall look is elegant, confident, and ideal for premium editorial menswear."
    ),
    "Athletic Modern Male": (
        "Young man with athletic build, medium tan skin, sharp cheekbone structure, dark hazel eyes, straight brows, "
        "proportionate nose, and natural lip definition. Hair is short black with clean sides and slightly tousled top. "
        "The appearance feels modern, energetic, and polished for contemporary high-fashion campaigns."
    ),
    "Mature Silver-Hair Gentleman": (
        "Mature man with refined facial structure, fair-to-neutral skin tone with realistic texture, light grey eyes, "
        "well-groomed brows, straight nose line, and subtle beard shadow. Hair is silver, medium-short, combed back "
        "with natural volume. The look conveys authority, sophistication, and timeless luxury."
    ),
    "Afro-Textured Male Icon": (
        "Young Black man with deep brown skin, strong jawline, expressive dark eyes, natural thick brows, and full lips. "
        "Hair is a defined short afro with dense texture and clean shape. Overall presence is bold, elegant, and strongly "
        "editorial with high realism."
    ),
    "East Asian Sharp Menswear": (
        "Young East Asian man with clear neutral skin tone, structured face, almond-shaped dark eyes, straight brows, "
        "balanced nose, and clean lip line. Hair is straight jet black, short on the sides with controlled top volume. "
        "The look is precise, contemporary, and ideal for minimalist luxury menswear editorials."
    ),
}

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
st.caption("Genera 4 imagenes editoriales photorealistas en formato cuadrado 4K.")

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

submitted = st.button("Generar shooting")

if submitted:
    missing_fields = []
    if not api_key.strip():
        missing_fields.append("API key de Google")
    if garment_file is None:
        missing_fields.append("fotografia de la prenda")
    if style_mode == "Prompt personalizado" and not style_desc.strip():
        missing_fields.append("descripcion del estilo")
    if location_mode == "Prompt personalizado" and not location_desc.strip():
        missing_fields.append("descripcion de la ubicacion")
    if model_mode in {"Preset de descripcion", "Descripcion personalizada"} and not model_desc.strip():
        missing_fields.append("descripcion fisica del modelo")
    if model_mode == "Subir imagen del modelo" and model_image_file is None:
        missing_fields.append("imagen del modelo")

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
                os.makedirs(model_dir, exist_ok=True)

                bot = FashionCampaignAI(api_key=api_key.strip(), logger=ui_logger)
                if model_mode == "Subir imagen del modelo":
                    model_ext = os.path.splitext(model_image_file.name)[1] or ".jpg"
                    model_reference_path = os.path.join(model_dir, f"model_reference_upload{model_ext}")
                    with open(model_reference_path, "wb") as model_file:
                        model_file.write(model_image_file.getbuffer())
                    ui_logger(f"Usando imagen de modelo subida: {model_image_file.name}")
                else:
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
