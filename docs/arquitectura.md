# Arquitectura del Pipeline de Datos (Medallón)

Este proyecto aplica los principios de la **Arquitectura Medallón** (Medallion Architecture), diseñado para proveer simulaciones robustas enfocadas a analítica de Marketing y Ventas en el sector maderero.

## 1. Visión General del Pipeline

El pipeline actual abarca la **Ingesta de Datos** (Capa Bronze). Está programado en **Python**, diseñado localmente interactuando con procesos `Batch`, y es escalable a la nube mediante Contenedores (Docker) disparados por cron-jobs en Serverless (ECS Fargate/Cloud Run Jobs).

## 2. Capa Bronze (Raw Data)

El script `generador_bronze.py` funge como los sistemas de origen transaccional (ERP) de la empresa maderera. 

### Lógica Comercial y Reglas Aleatorias
*   **Volumen:** Genera más de 100,000 registros transaccionales (Detalles de Venta).
*   **Temporalidad:** Base histórica desde Enero 2023 hasta finales de 2025.
*   **Límites Estándar:** 
    * El máximo de compra por línea de detalle es de **200 piezas**.
    * La venta total máxima permitida diaria/por cliente estándar es tapada algorítmicamente a **$30,000**.
*   **Anomalías de Marketing ('Días Buenos'):** Existe una probabilidad calculada constante de `~15%` de que un día explote comercialmente (representando el Black Friday, Remates, etc.). En estos escenarios los límites se eluden, levantando la cantidad a 800 ítems y topes de facturación de hasta $150,000.
*   **Fluctuación de Precios:** Todos los cortes de madera incrementan su precio anual basado en una inflación pseudo-aleatoria de entre `5% a 8%` anual con respecto a la base del 2023.
*   **Estrategia de Descuentos:** Compras al por mayor (>50 unidades) disparan promociones aleatorias de `1% al 12% off`.

## 3. Despliegue Multi-Cloud (CI/CD)

El proyecto incluye directrices para Integración y Despliegue continuo hacia las nubes líderes:

Dado que este generador produce archivos robustos (`CSV`), al llevar la arquitectura a la nube estos deberán alojarse en **Data Lakes** como:
*   AWS: **S3 (Simple Storage Service)**
*   GCP: **GCS (Google Cloud Storage)**
*   Azure: **Blob Storage**

El aprovisionamiento del código hacia estos entornos se hace empaquetando todo en un contenedor `Docker` a través de **GitHub Actions**.
