import os

class GoldConfig:
    """Configuración de rutas para los Datamarts de la Capa Gold."""
    
    # Rutas de entrada (Extraídas desde la Capa Silver)
    SILVER_DIR = 'data/silver'
    FACT_VENTAS_IN = os.path.join(SILVER_DIR, 'fact_ventas_marketing', 'fact_ventas.parquet')
    DIM_MADERAS_IN = os.path.join(SILVER_DIR, 'dim_maderas', 'maderas.parquet')
    
    # Rutas de salida para Datamarts Finales (Gold)
    GOLD_DIR = 'data/gold'
    DM_RENTABILIDAD_OUT = os.path.join(GOLD_DIR, 'dm_rentabilidad')
    DM_PROMOCIONES_OUT = os.path.join(GOLD_DIR, 'dm_promociones')
    
    @classmethod
    def setup_directories(cls):
        """Prepara las carpetas de negocio Gold."""
        os.makedirs(cls.DM_RENTABILIDAD_OUT, exist_ok=True)
        os.makedirs(cls.DM_PROMOCIONES_OUT, exist_ok=True)
