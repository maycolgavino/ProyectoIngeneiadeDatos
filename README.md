# Proyecto Maderera Perú - Data Pipeline End-to-End (Arquitectura Medallón)

Este repositorio aloja un Pipeline Analítico Avanzado para una maderera peruana. El pipeline ejecuta de principio a fin las 3 capas del modelo Medallón: Simulando transacciones (Bronze), Asegurando la Integridad y Calidad de la data (Silver) y Produciendo reportes de Rentabilidad y Marketing agrupados (Gold).

## 🗂️ Arquitectura del Pipeline y Estructura

El repositorio se divide estratégicamente así:

*   **1. `generador_bronze.py`**: Motor Raw. Simula +100k registros (2023-2025) bajo reglas estrictas de mercado (Inflación, anomalías estacionales). Guarda en `data/bronze/`.
*   **2. `procesador_silver.py`**: Limpieza Orientada a Objetos. Estandariza strings, realiza el *Mega Join* de tickets, inyecta Feature Engineering (Mes, Año, Q) exportando a `data/silver/` (`.parquet`).
*   **3. `procesador_gold.py`**: Datamarts finales. Crea tablas dinámicas maestras listas para Dashboards (Rentabilidad Global y Estrategia Promocional Automática) en `data/gold/`.
*   **▶️ `main_pipeline.py`**: El Orquestador. Dispara secuencialmente y de forma aislada las 3 capas anteriores.
*   **📚 `/docs`**: Justificaciones técnicas, diagramas dictados, diccionario de datos y modelos matemáticos.
*   **🐳 `/ops`**: Contiene el `Dockerfile` optimizado.
*   **🤖 `/.github/workflows`**: Tuberías CI/CD para ejecutar el contenedor *Serverless* en diferentes Proveedores de Nube.

## 🚀 Guía de Deploy Multicloud (Cómo Instalarlo en la Nube)

El proyecto viene Dockerizado y amarrado a **GitHub Actions**, listo para compilarse y ejecutarse automáticamente como un `Batch Job`. Dependiendo de tu Cloud Platform favorito, activa su workflow:

> **NOTA DE VOLUMEN:** Localmente, la memoria va a la carpeta `data/`. Para uso real de Big Data en la nube, el sistema asume que montarás Buckets/Blob Storage hacia esa misma ruta dentro del contenedor.

### 🟣 AMAZON WEB SERVICES (AWS ECS Fargate)
1. En GitHub, ve a `Settings > Secrets` y configura: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `SUBNET_ID`, `SG_ID`.
2. Dirígete a la pestaña **Actions** en Github, selecciona `Deploy to AWS ECS` y dale *Run workflow*.
3. GitHub compilará el código, subirá la imagen al registry (ECR) y ejecutará nuestro `main_pipeline.py` de forma paralela en un contenedor *Fargate* que se apagará al terminar (ahorrando dinero).

### 🟡 GOOGLE CLOUD PLATFORM (Cloud Run Jobs)
1. En GitHub Secrets, configura `GCP_PROJECT_ID` y `GCP_CREDENTIALS` (Service Account Key).
2. Dirígete a la pestaña **Actions** y ejecuta el workflow `Deploy to Google Cloud Run Jobs`.
3. Tu pipeline se empujará al Artifact Registry y se orquestará usando *Cloud Run Jobs* de Google, capaz de manejar hasta 60 minutos de procesamiento ETL puro.

### 🔵 MICROSOFT AZURE (Container Instances)
1. En GitHub Secrets, inyecta: `AZURE_CREDENTIALS`, `ACR_USERNAME`, `ACR_PASSWORD`.
2. Lanza el workflow `Deploy to Azure Container Instances`.
3. Desplegará como un ACI de política *Restart-Never*, ideal para trabajos temporales de Data Quality.

## 🛠️ Guía de Ejecución Local Inmediata

Si quieres correr todo en tu computadora:

```bash
# 1. Crear entorno y activarlo
python -m venv venv
.\venv\Scripts\activate   # Windows

# 2. Instalar el cerebro
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 3. LANZAR LA MAGIA EN UN SOLO CLIC! (Bronze->Silver->Gold)
python main_pipeline.py
```
