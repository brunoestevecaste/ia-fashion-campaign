# Fashion Campaign Streamlit App

Prueba la app aqui: https://ia-fashion-campaign.streamlit.app/

Este proyecto es una aplicacion de generacion visual para campañas de moda que transforma una entrada simple (foto de prenda + direccion creativa) en un shooting editorial completo asistido por IA. El sistema recibe una fotografia real de la prenda, una descripcion del estilo deseado, una descripcion de la ubicacion y una descripcion fisica del modelo, y a partir de ello ejecuta un flujo automatizado que mantiene consistencia visual entre todas las imagenes producidas.

La aplicacion genera primero una referencia de modelo (si no existe una unica imagen de referencia), luego construye cuatro prompts creativos coherentes con la direccion artistica indicada, y finalmente produce cuatro imagenes finales en formato cuadrado 4K con enfoque editorial. El resultado es un mini shooting de moda listo para exploracion creativa, presentacion interna o iteracion rapida de conceptos de campana, manteniendo la identidad de la prenda y del modelo en todas las tomas.

En la interfaz puedes elegir estilos y ubicaciones desde presets optimizados (curados para calidad editorial) o escribir tus propios prompts personalizados para cada uno.
Para el modelo, puedes seleccionar descripciones fisicas por defecto, escribir una descripcion personalizada o subir directamente una imagen de referencia.
Tambien puedes elegir modo `Final` (4 imagenes 4K) o modo `Draft` (2 imagenes 1K) para iterar con menor coste.
Al finalizar, puedes descargar cada imagen por separado o la campaña completa en un archivo ZIP.

El valor principal del proyecto es reducir de forma drástica el tiempo y el coste de preproduccion visual: permite pasar de una idea a propuestas visuales de alta calidad en minutos, sin depender de una sesion fotografica completa en la fase inicial. Tambien aporta consistencia, velocidad de prueba y capacidad de experimentar multiples direcciones narrativas con menos friccion, ayudando a equipos de marketing, branding y contenido a validar conceptos antes de invertir en produccion final.

## Estructura del proyecto

- `app.py`: punto de entrada de Streamlit y orquestacion de alto nivel.
- `script.py`: fachada/entrypoint compatible que expone `FashionCampaignAI`.
- `campaign_app/config.py`: presets y constantes de la UI.
- `campaign_app/theme.py`: configuracion de pagina y estilos CSS.
- `campaign_app/ui.py`: render de inputs y resultados en Streamlit.
- `campaign_app/validation.py`: validacion de campos de entrada.
- `campaign_app/pipeline.py`: ejecucion del pipeline end-to-end usando `FashionCampaignAI`.
- `campaign_app/models.py`: modelos de datos (`CampaignInputs`, `CampaignResult`).
- `campaign_core/gemini_client.py`: cliente Gemini y llamada REST para imagen 4K.
- `campaign_core/prompts.py`: plantillas de prompts para referencia, conceptos y render final.
- `campaign_core/image_utils.py`: utilidades de parsing y procesamiento de imagen.
- `campaign_core/shooting_engine.py`: implementacion principal de `FashionCampaignAI`.
- `campaign_core/constants.py`: constantes de modelos y configuracion global del motor.

## Optimizaciones de coste incluidas

- Estrategia `flash-first` para generar prompts y fallback automatico a `pro` si la salida no es valida.
- Cache persistente de referencias de modelo por descripcion en `.cache/model_refs`.
- Modo `Draft` para reducir llamadas y resolucion durante iteraciones creativas.
