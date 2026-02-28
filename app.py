import streamlit as st

from campaign_app.pipeline import run_campaign_pipeline
from campaign_app.theme import apply_theme, configure_page
from campaign_app.ui import render_header, render_input_form, render_results
from campaign_app.validation import validate_inputs


def main() -> None:
    configure_page()
    apply_theme()
    render_header()

    if "campaign_result" not in st.session_state:
        st.session_state["campaign_result"] = None

    inputs = render_input_form()
    submitted = st.button("Generar shooting")

    if submitted:
        missing_fields = validate_inputs(inputs)
        if missing_fields:
            st.error(f"Faltan campos obligatorios: {', '.join(missing_fields)}")
        else:
            log_messages: list[str] = []
            log_placeholder = st.empty()

            def ui_logger(message: str) -> None:
                log_messages.append(message)
                log_placeholder.code("\n".join(log_messages), language="text")

            with st.status("Ejecutando pipeline de generacion...", expanded=True) as status:
                try:
                    result = run_campaign_pipeline(inputs, logger=ui_logger)
                    st.session_state["campaign_result"] = result
                    status.update(label="Shooting completado", state="complete")
                except Exception as exc:
                    status.update(label="Error durante la generacion", state="error")
                    st.error(f"No se pudo completar el shooting: {exc}")

    if st.session_state["campaign_result"] is not None:
        render_results(st.session_state["campaign_result"])


if __name__ == "__main__":
    main()
