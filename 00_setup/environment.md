# Configuración del Entorno de Desarrollo (Fase 0)

Este documento detalla la infraestructura local y las herramientas utilizadas para el desarrollo de este portfolio de MLOps.

## 1. Lenguaje y Gestión de Entornos
- **Python:** Versión 3.10.x
- **Gestor de Entornos:** Anaconda / Conda
- **Entorno Virtual:** `data-env`
  - *Comando de activación:* `conda activate data-env`

## 2. Infraestructura Local (Docker)
Se utiliza Docker Desktop para levantar servicios esenciales sin instalar dependencias directamente en el sistema operativo.

### Base de Datos Relacional (Postgres)
- **Imagen:** `postgres:15`
- **Puerto:** `5432`
- **Uso:** Almacenamiento de metadatos de modelos, usuarios y datos estructurados.

### Almacenamiento de Objetos (S3 Local - MinIO)
- **Imagen:** `minio/minio`
- **Puerto API:** `9000`
- **Puerto Consola:** `9001`
- **Uso:** Almacenamiento de datasets (Raw/Processed) y artefactos de modelos (archivos .pkl, .h5).

## 3. Herramientas de Desarrollo (IDE)
- **Editor:** Visual Studio Code (VSCode)
- **Extensiones clave:**
  - Python (Microsoft)
  - Jupyter (Microsoft)
  - Docker (Microsoft)

## 4. Servicios Cloud (Free Tiers)
- **Hugging Face:** Repositorio de modelos y Spaces.
- **Pinecone:** Base de datos vectorial para proyectos de RAG e IA Generativa.