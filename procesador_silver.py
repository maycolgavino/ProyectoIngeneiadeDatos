import os
import pandas as pd
from src.silver.config import SilverConfig
from src.silver.transformers import SilverTransformer

def main():
    """Ejecutor principal de la capa Silver (Pipeline de Datos)."""
    
    # 1. Asegurar directorios de salida
    SilverConfig.setup_directories()
    
    print("\n[ETAPA 1: LECTURA / EXTRACTION]")
    # Simulamos el 'Extraction' de la Capa Bronze (Archivos crudos CSV)
    # En la vida real, sacaríamos esto con boto3 (AWS S3) o google-cloud-storage
    df_maderas_crudo = pd.read_csv(SilverConfig.MADERAS_IN)
    df_clientes_crudo = pd.read_csv(SilverConfig.CLIENTES_IN)
    df_ventas_cabecera = pd.read_csv(SilverConfig.VENTAS_CABECERA_IN)
    df_ventas_detalle = pd.read_csv(SilverConfig.VENTAS_DETALLE_IN)
    
    print("\n[ETAPA 2: TRANSFORMACIÓN CON OOP]")
    # Instanciamos nuestra clase transormadora
    transformer = SilverTransformer()
    
    # Invocamos métodos especializados (encapsulación del proceso)
    df_clientes_silver = transformer.process_clientes(df_clientes_crudo)
    df_maderas_silver = transformer.process_maderas(df_maderas_crudo)
    df_fact_ventas = transformer.process_ventas_marketing(df_ventas_cabecera, df_ventas_detalle)
    
    print("\n[ETAPA 3: CARGA / LOAD (Exportación a Parquet)]")
    # Para la Analítica Moderna 'Silver', se usa el Standard Parquet porque
    # la compresión de texto repetitivo reduce espacio 10 a 1 y guarda Data-types exactos.
    # Así ahorramos miles de dólares en consultas a la Nube.
    
    df_clientes_silver.to_parquet(
        os.path.join(SilverConfig.CLIENTES_OUT, 'clientes.parquet'),
        index=False, engine='pyarrow', compression='snappy'
    )
    
    df_maderas_silver.to_parquet(
        os.path.join(SilverConfig.MADERAS_OUT, 'maderas.parquet'),
        index=False, engine='pyarrow', compression='snappy'
    )
    
    df_fact_ventas.to_parquet(
        os.path.join(SilverConfig.VENTAS_UNIFICADAS_OUT, 'fact_ventas.parquet'),
        index=False, engine='pyarrow', compression='snappy'
    )
    
    print(f"-> Operación Silver Exitosa. Puedes consultar tus Dataframes optimizados en: {SilverConfig.SILVER_DIR}/")

if __name__ == '__main__':
    main()
