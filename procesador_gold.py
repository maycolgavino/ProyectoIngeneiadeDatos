import os
import pandas as pd
from src.gold.config import GoldConfig
from src.gold.transformers import GoldTransformer

def main():
    """Ejecutor principal de la capa Gold (Construcción de Datamarts)."""
    
    print("\n[ETAPA 1: LECTURA DE CAPA SILVER / SINGLE SOURCE OF TRUTH]")
    GoldConfig.setup_directories()
    
    # Cargamos Parquets optimizados (Ultra rápidos)
    df_fact_ventas = pd.read_parquet(GoldConfig.FACT_VENTAS_IN)
    df_dim_maderas = pd.read_parquet(GoldConfig.DIM_MADERAS_IN)
    
    print("\n[ETAPA 2: TRANSFORMACIÓN GOLD / CREACIÓN DE DATAMARTS]")
    transformer = GoldTransformer()
    
    dm_rentabilidad = transformer.process_dm_rentabilidad(df_fact_ventas, df_dim_maderas)
    dm_promociones = transformer.process_dm_promociones(df_fact_ventas, df_dim_maderas)
    
    print("\n[ETAPA 3: EXPORTACIÓN CUBOS ANALÍTICOS (GOLD)]")
    dm_rentabilidad.to_csv(os.path.join(GoldConfig.DM_RENTABILIDAD_OUT, 'rentabilidad.csv'), index=False)
    dm_promociones.to_csv(os.path.join(GoldConfig.DM_PROMOCIONES_OUT, 'estrategia_promociones.csv'), index=False)
    
    # También exportamos en Parquet por si se ingestan en PowerBI via Dataflows
    dm_rentabilidad.to_parquet(os.path.join(GoldConfig.DM_RENTABILIDAD_OUT, 'rentabilidad.parquet'), index=False)
    dm_promociones.to_parquet(os.path.join(GoldConfig.DM_PROMOCIONES_OUT, 'estrategia_promociones.parquet'), index=False)

    print(f"-> Operación Gold Exitosa. Datamarts listos para consumo BI en: {GoldConfig.GOLD_DIR}/")

if __name__ == '__main__':
    main()
