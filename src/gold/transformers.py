import pandas as pd
import numpy as np

class GoldTransformer:
    """
    Motor de pre-cálculo para la Capa Gold (Datamarts).
    Consolida las métricas finales que usarán los analistas de BI, para que el dashboard vuele.
    """
    
    def process_dm_rentabilidad(self, df_fact: pd.DataFrame, df_maderas: pd.DataFrame) -> pd.DataFrame:
        """
        Datamart de Rentabilidad General.
        Agrupa y resume ingresos por Período de Tiempo (Año/Trimestre/Mes) y por Especie.
        """
        print(" -> Generando Datamart: Rentabilidad por Especie...")
        
        # Enriquecer la fact (que tiene id_madera) con la especie pura de dim_maderas
        df_join = pd.merge(
            df_fact, 
            df_maderas[['id_madera', 'especie']], 
            on='id_madera', 
            how='left'
        )
        
        # Agrupación profunda por jerarquía de tiempo y especie
        dm_rentabilidad = df_join.groupby(
            ['anio', 'trimestre', 'mes', 'nombre_mes', 'especie']
        ).agg(
            ingresos_totales=('subtotal', 'sum'),
            volumen_piezas_vendidas=('cantidad_piezas', 'sum'),
            transacciones_totales=('id_venta', 'count')
        ).reset_index()
        
        # ORDENAR de forma natural por calendario
        dm_rentabilidad = dm_rentabilidad.sort_values(by=['anio', 'mes', 'ingresos_totales'], ascending=[True, True, False])
        
        return dm_rentabilidad

    def process_dm_promociones(self, df_fact: pd.DataFrame, df_maderas: pd.DataFrame) -> pd.DataFrame:
        """
        Datamart de Marketing/Promociones.
        Identifica en base a rendimiento histórico (por mes y producto) qué elementos 
        deben ser "Gancho" y cuáles deben ir en liquidación "3x1".
        """
        print(" -> Generando Datamart Inteligente: Recomendador de Estrategia Promocional...")
        
        df_join = pd.merge(df_fact, df_maderas[['id_madera', 'especie']], on='id_madera', how='left')
        
        # Queremos saber el comportamiento por Mes y por Corte de Madera Exacto
        grouped = df_join.groupby(['mes', 'nombre_mes', 'especie', 'id_madera', 'descripcion_snapshot']).agg(
            total_piezas_vendidas=('cantidad_piezas', 'sum'),
            ingresos_totales=('subtotal', 'sum'),
            veces_vendido=('id_venta', 'count')
        ).reset_index()
        
        def asignar_estrategia(group_df):
            """Analiza la curva de ventas dentro de una Especie en un Mes y clasifica extremos."""
            # Si se ha vendido muy poquito (extremo inferior 10%)
            umbral_hueso = group_df['total_piezas_vendidas'].quantile(0.10)
            # Si se ha vendido brutalmente bien (extremo superior 90%)
            umbral_estrella = group_df['total_piezas_vendidas'].quantile(0.90)
            
            condiciones = [
                group_df['total_piezas_vendidas'] <= umbral_hueso,
                group_df['total_piezas_vendidas'] >= umbral_estrella
            ]
            etiquetas = [
                'Liquidación 3x1 (Hueso Histórico)', 
                'Campaña Gancho (Estrella / Loss Leader)'
            ]
            
            group_df['recomendacion_marketing'] = np.select(condiciones, etiquetas, default='Normal (Sin Promo Sugerida)')
            return group_df
            
        # Aplicamos el análisis agrupando por cada Mes y Especie independientemente.
        # Es decir, comparamos los Cortes de Tornillo de Junio sólo contra otros Cortes de Tornillo de Junio.
        dm_promo = grouped.groupby(['mes', 'especie'], group_keys=False).apply(asignar_estrategia)
        
        # Organizamos la tabla
        dm_promo = dm_promo.sort_values(by=['mes', 'especie', 'total_piezas_vendidas'], ascending=[True, True, False])
        
        return dm_promo
