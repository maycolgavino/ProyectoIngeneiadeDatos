import pandas as pd

def analizar_promociones_huimba():
    print("=== Análisis de Marketing: Candidatos 3x1 para 'HUIMBA' en Junio ===")
    
    # 1. Cargar las ventas consolidadas (Capa Silver)
    df_ventas = pd.read_parquet('data/silver/fact_ventas_marketing/fact_ventas.parquet')
    
    # 2. Filtrar por el mes de Junio (mes == 6)
    df_junio = df_ventas[df_ventas['mes'] == 6]
    
    # 3. Filtrar por la especie Huimba (usando el snapshot de la descripción)
    df_huimba_junio = df_junio[df_junio['descripcion_snapshot'].str.contains('Huimba', case=False, na=False)]
    
    # 4. Agrupar por producto (madera) para ver el rendimiento histórico total de Junio
    rendimiento = df_huimba_junio.groupby(['id_madera', 'descripcion_snapshot']).agg(
        total_piezas_vendidas=('cantidad_piezas', 'sum'),
        ingresos_totales=('subtotal', 'sum'),
        veces_vendido=('id_venta', 'count')
    ).reset_index()
    
    if rendimiento.empty:
        print("No se encontraron ventas de Huimba en Junio en el historial.")
        return
        
    print(f"Total de productos Huimba distintos vendidos en Junio: {len(rendimiento)}")
    
    # ESTRATEGIA 1: Los menos vendidos (Huesos / Huesitos)
    # Ideal para 3x1 porque necesitamos rotar este inventario que no se mueve en Junior.
    menos_vendidos = rendimiento.sort_values(by='total_piezas_vendidas', ascending=True).head(5)
    
    print("\n[ESTRATEGIA 1] - Productos de Mínima Rotación (Ideales para liquidar stock en 3x1):")
    for _, row in menos_vendidos.iterrows():
        print(f"- {row['descripcion_snapshot']} (ID: {row['id_madera']})")
        print(f"  Vendido solo {row['total_piezas_vendidas']} piezas en {row['veces_vendido']} transacciones. Ingreso: ${row['ingresos_totales']:,.2f}")

    # ESTRATEGIA 2: Los más vendidos (Anzuelos)
    # Ideal para 3x1 si queremos atraer volumen masivo sacrificando margen (loss leader).
    mas_vendidos = rendimiento.sort_values(by='total_piezas_vendidas', ascending=False).head(3)
    
    print("\n[ESTRATEGIA 2] - Productos Estrella (Ideales para campañas gancho 'Loss Leader'):")
    for _, row in mas_vendidos.iterrows():
        print(f"- {row['descripcion_snapshot']} (ID: {row['id_madera']})")
        print(f"  {row['total_piezas_vendidas']} piezas vendidas a lo largo de {row['veces_vendido']} transacciones. Ingreso: ${row['ingresos_totales']:,.2f}")

if __name__ == '__main__':
    analizar_promociones_huimba()
