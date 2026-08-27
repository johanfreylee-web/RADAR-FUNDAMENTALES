# Radar Value Investing — Cómo publicarlo

Tenés 2 archivos: `app.py` (la app) y `requirements.txt` (dependencias).
La forma más simple y gratuita de tener tu URL pública es **Streamlit Community Cloud**.

## Paso 1: Crear cuenta en GitHub (si no tenés)
1. Andá a https://github.com y creá una cuenta gratis.

## Paso 2: Subir los archivos a un repositorio
1. En GitHub, hacé clic en **"New repository"**.
2. Ponele un nombre, ej: `radar-fundamentales`.
3. Marcalo como **Public**.
4. Creá el repo, y luego subí `app.py` y `requirements.txt` con el botón **"Add file" → "Upload files"** (arrastralos directo, sin necesidad de usar terminal/git).

## Paso 3: Desplegar en Streamlit Cloud
1. Andá a https://share.streamlit.io y entrá con tu cuenta de GitHub (botón "Sign in with GitHub").
2. Hacé clic en **"New app"**.
3. Seleccioná el repositorio `radar-fundamentales`, la rama `main`, y el archivo principal `app.py`.
4. Hacé clic en **"Deploy"**.
5. Esperá 1-2 minutos. Te va a dar una URL tipo `https://radar-fundamentales-tuusuario.streamlit.app`.

Esa URL ya es pública y funcional: entrás, escribís los tickers, apretás "Correr análisis" y ves los resultados.

## Paso 4 (opcional): Actualizar la app en el futuro
Si querés cambiar algo del código, editá `app.py` directo en GitHub (lápiz ✏️ arriba a la derecha del archivo) y Streamlit Cloud lo redespliega solo en segundos.

---

### Notas importantes
- **yfinance depende de Yahoo Finance**: a veces bloquea temporalmente si hay muchas consultas seguidas. Si ves errores tipo "Too Many Requests", esperá unos minutos.
- La app ahora te deja ajustar **WACC, crecimiento y umbral de oportunidad** desde el panel lateral, sin tocar código.
- Es un modelo simplificado con fines educativos — no es asesoramiento financiero.
