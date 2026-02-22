# Fashion Campaign Streamlit App

Aplicacion Streamlit para generar shootings de moda con Gemini.

## Requisitos
- Python 3.10+
- API Key de Google Gemini

## Ejecutar en local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Despliegue en Streamlit Community Cloud
1. Sube este proyecto a un repositorio de GitHub.
2. Entra en https://share.streamlit.io/ y pulsa **New app**.
3. Selecciona tu repositorio, rama y archivo principal: `app.py`.
4. Despliega la app.
5. Cada usuario debe introducir su propia Google API Key en la interfaz.

## Estructura minima del proyecto
- `app.py`: interfaz Streamlit.
- `script.py`: logica de generacion de imagenes.
- `requirements.txt`: dependencias para despliegue.
- `.streamlit/config.toml`: configuracion visual/servidor de Streamlit.
- `.gitignore`: exclusiones para no subir archivos locales innecesarios.

## Subir a GitHub (comandos)
```bash
git init
git add .
git commit -m "Prepare Streamlit app for deployment"
git branch -M main
git remote add origin <URL_DE_TU_REPO>
git push -u origin main
```
