FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias base de Python y optimizaciones
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Instalar dependencias de la aplicación
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY generador_bronze.py .

# Crear estructura de carpetas necesaria independientemente del mount
RUN mkdir -p data/bronze/maderas data/bronze/clientes data/bronze/ventas_cabecera data/bronze/ventas_detalle

# Por defecto, ejecuta TODO EL PIPELINE ORQUESTADO (Bronze -> Silver -> Gold)
CMD ["python", "main_pipeline.py"]
