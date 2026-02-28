import streamlit as st


THEME_CSS = """
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
"""


def configure_page() -> None:
    st.set_page_config(page_title="Fashion Campaign Generator", layout="wide")


def apply_theme() -> None:
    st.markdown(THEME_CSS, unsafe_allow_html=True)

