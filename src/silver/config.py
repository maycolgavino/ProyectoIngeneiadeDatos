import os

class SilverConfig:
    """Configuraciones globales para el pipeline de Capa Silver."""
    
    # Rutas de entrada (Bronze)
    BRONZE_DIR = 'data/bronze'
    MADERAS_IN = os.path.join(BRONZE_DIR, 'maderas', 'maderas.csv')
    CLIENTES_IN = os.path.join(BRONZE_DIR, 'clientes', 'clientes.csv')
    VENTAS_CABECERA_IN = os.path.join(BRONZE_DIR, 'ventas_cabecera', 'ventas.csv')
    VENTAS_DETALLE_IN = os.path.join(BRONZE_DIR, 'ventas_detalle', 'detalles.csv')
    
    # Rutas de salida (Silver)
    SILVER_DIR = 'data/silver'
    MADERAS_OUT = os.path.join(SILVER_DIR, 'dim_maderas')
    CLIENTES_OUT = os.path.join(SILVER_DIR, 'dim_clientes')
    VENTAS_UNIFICADAS_OUT = os.path.join(SILVER_DIR, 'fact_ventas_marketing')
    
    @classmethod
    def setup_directories(cls):
        """Asegura que los directorios donde se guardará la data Silver existan."""
        os.makedirs(cls.MADERAS_OUT, exist_ok=True)
        os.makedirs(cls.CLIENTES_OUT, exist_ok=True)
        os.makedirs(cls.VENTAS_UNIFICADAS_OUT, exist_ok=True)
