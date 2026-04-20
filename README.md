# Proyecto Maderera Perú - Data Engineering Pipeline

Este proyecto simula un pipeline de datos transaccionales para una empresa maderera en Perú, utilizando la Arquitectura Medallón (Bronze, Silver, Gold). Su objetivo principal es proveer data volumétrica (+100k registros entre 2023 y 2025) para la creación de reportes gerenciales tácticos enfocados en proyecciones y estrategias de Marketing (estacionalidad y tendencias de consumo por especies).

## Estructura

El pipeline se divide en scripts para estructurar el datalake:

*   `generador_bronze.py`: Ingesta/Simulación. Genera las tablas maestras (Maderas, Clientes) y los hechos transaccionales (Ventas y Detalles) guardándolos en `data/bronze/` en formato CSV. Utiliza `Faker` para simular empresas y distribución geográfica en Perú.

## Requisitos

*   Python 3.8+
*   Pandas
*   Faker

## Instalación

1.  Crear entorno virtual: `python -m venv venv`
2.  Activar entorno virtual: `.\venv\Scripts\activate` (Windows)
3.  Instalar dependencias: `pip install -r requirements.txt`

## Ejecución

1.  Para generar la capa Raw (Bronze):
    ```bash
    python generador_bronze.py
    ```
