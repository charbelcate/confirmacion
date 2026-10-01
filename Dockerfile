# Imagen para desplegar el piloto "Camino a la Primera Comunión" en un VPS
# (pensada para Easypanel, pero sirve para cualquier plataforma que corra
# contenedores Docker). Ver "Guía de despliegue en VPS" para el paso a
# paso completo (dominio, HTTPS, volúmenes persistentes, etc.).

FROM python:3.11-slim

# build-essential: por si alguna dependencia de requirements.txt necesita
# compilar algo al instalar (no debería hacer falta con las versiones
# fijadas, pero evita errores confusos si tu VPS usa otra arquitectura).
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

COPY backend/ backend/
COPY frontend/ frontend/

# Carpeta donde sentence-transformers guarda el modelo ya descargado (unos
# cientos de MB). Se monta como volumen en producción para no volver a
# descargarlo en cada redeploy (ver guía de despliegue).
ENV HF_HOME=/app/backend/.cache/huggingface
# Evita que Python bufferee la salida, para que los logs aparezcan de
# inmediato en el panel de Easypanel (o en `docker logs`).
ENV PYTHONUNBUFFERED=1

WORKDIR /app/backend
EXPOSE 5000

# Servidor de producción (gunicorn) en vez del servidor de desarrollo de
# Flask. 2 workers alcanza de sobra para un piloto de catequesis; puedes
# subirlo si tienes muchos niños conectados a la vez y tu VPS tiene CPU
# de sobra.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
