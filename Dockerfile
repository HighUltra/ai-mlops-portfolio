# --- ETAPA 1: Builder (La cocina pesada) ---
FROM python:3.10-slim AS builder

WORKDIR /app

# Instalamos herramientas necesarias para compilar algunas librerías de IA
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalamos las librerías en una carpeta local para luego moverlas
RUN pip install --user --no-cache-dir -r requirements.txt


# --- ETAPA 2: Runner (La caja limpia y ligera) ---
FROM python:3.10-slim

WORKDIR /app

# Copiamos solo las librerías instaladas desde el 'builder'
COPY --from=builder /root/.local /root/.local
# Copiamos todo tu código y modelos al contenedor
COPY . .

# Configuramos variables de entorno para que Python encuentre todo
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app

# Exponemos el puerto 8000 (el de FastAPI)
EXPOSE 8000

# El comando que arranca tu API automáticamente al prender el contenedor
CMD ["python", "-m", "App.main"]