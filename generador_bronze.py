import os
import random
from datetime import datetime, timedelta
import pandas as pd
from faker import Faker

# Configurar Faker (Usamos es_ES o es_MX ya que 'es_PE' no siempre está disponible en Faker)
fake = Faker('es_ES')

# Parámetros del proyecto
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2025, 12, 31)
NUM_CLIENTES = 500
NUM_VENTAS_MIN = 25000  # Estimación de ventas (cabecera)
NUM_DETALLES_TARGET = 100000  # Target de detalles

# Especies de madera peruanas y sus precios referenciales por pie tabular (PT)
# Precio semilla para introducir variabilidad luego.
ESPECIES_MADERA = {
    'Tornillo': 4.5,
    'Huimba': 2.8,
    'Caimotillo': 3.5,
    'Caoba': 12.0,
    'Cedro': 9.0,
    'Copaiba': 3.2,
    'Moena': 3.0,
    'Pino': 2.5,
    'Cumala': 2.2,
    'Pumaquiro': 5.0
}

ESPESORES = [1, 1.5, 2, 2.5, 3, 3.5, 4]
ANCHOS = list(range(1, 13))  # 1 a 12
LARGOS = list(range(6, 31, 2))  # 6, 8, 10... 30

def asegurar_directorios():
    """Crea la estructura de carpetas Medallón si no existe."""
    os.makedirs('data/bronze/maderas', exist_ok=True)
    os.makedirs('data/bronze/clientes', exist_ok=True)
    os.makedirs('data/bronze/ventas_cabecera', exist_ok=True)
    os.makedirs('data/bronze/ventas_detalle', exist_ok=True)

def generar_maderas():
    """Genera el catálogo de maderas combinando especies y dimensiones."""
    print("Generando catálogo de Maderas...")
    maderas = []
    id_counter = 1
    for especie, precio_base in ESPECIES_MADERA.items():
        # Tomar un sample aleatorio de dimensiones para no generar TODAS las combinaciones (serían miles por especie)
        # y hacerlo más realista (no todas las medidas existen siempre)
        for _ in range(50): 
            espesor = random.choice(ESPESORES)
            ancho = random.choice(ANCHOS)
            largo = random.choice(LARGOS)
            
            pies_cuadrados = (espesor * ancho * largo) / 12.0
            descripcion = f"{especie} {espesor}x{ancho}x{largo}'"
            
            # Existe una posibilidad de colisión si se repite la misma dimensión para la misma especie, lo ideal sería un set
            maderas.append({
                'id_madera': f"M-{str(id_counter).zfill(5)}",
                'especie': especie,
                'espesor_pulg': espesor,
                'ancho_pulg': ancho,
                'largo_pies': largo,
                'pies_cuadrados': round(pies_cuadrados, 2),
                'descripcion': descripcion,
                'precio_pt_referencial': round(precio_base * random.uniform(0.9, 1.1), 2)
            })
            id_counter += 1
            
    # Eliminar duplicados si los hubiera
    df_maderas = pd.DataFrame(maderas).drop_duplicates(subset=['especie', 'espesor_pulg', 'ancho_pulg', 'largo_pies'])
    # Reasignar IDs tras de-duplicar
    df_maderas = df_maderas.reset_index(drop=True)
    df_maderas['id_madera'] = ['M-' + str(i+1).zfill(5) for i in range(len(df_maderas))]
    
    df_maderas.to_csv('data/bronze/maderas/maderas.csv', index=False)
    print(f"-> {len(df_maderas)} maderas generadas.")
    return df_maderas

def generar_clientes():
    """Genera una lista de clientes ficticios en Perú."""
    print("Generando Clientes...")
    clientes = []
    deptos = ['Lima', 'Arequipa', 'Piura', 'La Libertad', 'Cusco', 'Junín', 'Lambayeque', 'Loreto', 'Ica', 'Cajamarca']
    
    for i in range(1, NUM_CLIENTES + 1):
        clientes.append({
            'id_cliente': f"C-{str(i).zfill(4)}",
            'nombre_empresa': fake.company(),
            'ruc': '20' + str(fake.random_number(digits=9, fix_len=True)),
            'departamento': random.choices(deptos, weights=[40, 10, 8, 8, 7, 6, 6, 5, 5, 5])[0], # Pesos dando preferencia a Lima
            'fecha_registro': fake.date_between(start_date=START_DATE - timedelta(days=365), end_date=END_DATE)
        })
        
    df_clientes = pd.DataFrame(clientes)
    df_clientes.to_csv('data/bronze/clientes/clientes.csv', index=False)
    print(f"-> {len(df_clientes)} clientes generados.")
    return df_clientes

def generar_ventas(df_maderas, df_clientes):
    """Genera las ventas y sus detalles correspondientes (> 100k registros)."""
    print("Generando Ventas (Cabeceras y Detalles)... Esto puede tardar unos segundos.")
    ventas = []
    detalles = []
    
    id_venta_counter = 1
    id_detalle_counter = 1
    
    total_days = (END_DATE - START_DATE).days
    
    # Calcular promedio de detalles por venta para llegar al target de 100k
    # Si queremos 100,000 detalles y tenemos 25,000 ventas, son ~4 detalles por venta.
    
    for i in range(NUM_VENTAS_MIN):
        # Distribución de fechas
        # Para simular tendencias de marketing, agregamos más probabilidad a ciertos meses (ej. Verano o Diciembre)
        random_day = START_DATE + timedelta(days=random.randint(0, total_days))
        
        # Simular una pequeña estacionalidad (bump si es noviembre o diciembre)
        if random_day.month in [11, 12]:
             # 30% propensión a duplicar ventas en estos meses
             if random.random() < 0.3:
                 random_day = START_DATE + timedelta(days=random.randint(0, total_days))
                 
        cliente_id = random.choice(df_clientes['id_cliente'].tolist())
        
        # Simulamos 50-60 días súper rentables al año (probabilidad del ~15%) que rompen el tope de 30k y 200 items
        es_dia_bueno = random.random() < 0.15
        limite_presupuesto = 150000 if es_dia_bueno else 29999
        limite_cantidad_item = 800 if es_dia_bueno else 200
        
        num_items_en_venta = random.randint(1, 8) # Entre 1 y 8 líneas de detalle por venta
        venta_total_monto = 0
        
        for _ in range(num_items_en_venta):
            madera = df_maderas.sample(1).iloc[0]
            
            # Calculamos la inflación y precios base
            inflacion = 1.0 + ((random_day.year - 2023) * random.uniform(0.05, 0.08)) # 5% a 8% más caro cada año
            precio_unit_base = madera['precio_pt_referencial'] * inflacion
            
            # Límite para que la venta total no sobrepase el presupuesto establecido
            precio_base_por_pieza = madera['pies_cuadrados'] * precio_unit_base
            presupuesto_sobrante = limite_presupuesto - venta_total_monto
            if presupuesto_sobrante <= 0:
                break
                
            max_posible_por_presupuesto = int(presupuesto_sobrante // precio_base_por_pieza)
            if max_posible_por_presupuesto < 1:
                break
                
            cantidad = random.randint(1, min(limite_cantidad_item, max_posible_por_presupuesto))
            
            # Ajustamos la regla del descuento para cantidades >= 50 ya que el tope bajó a 200
            descuento_porcentual = random.uniform(0.01, 0.12) if cantidad >= 50 else 0.0
            descuento_factor = 1.0 - descuento_porcentual
            
            precio_unit_aplicado = precio_unit_base * descuento_factor
            
            # Cálculos de línea
            subtotal = madera['pies_cuadrados'] * cantidad * precio_unit_aplicado
            
            detalles.append({
                'id_detalle': id_detalle_counter,
                'id_venta': f"V-{str(id_venta_counter).zfill(6)}",
                'id_madera': madera['id_madera'],
                'descripcion_snapshot': madera['descripcion'],
                'cantidad_piezas': cantidad,
                'precio_pt_base': round(precio_unit_base, 2),
                'descuento_pct': round(descuento_porcentual * 100, 2),
                'precio_pt_aplicado': round(precio_unit_aplicado, 2),
                'subtotal': round(subtotal, 2)
            })
            
            venta_total_monto += subtotal
            id_detalle_counter += 1
            
        ventas.append({
            'id_venta': f"V-{str(id_venta_counter).zfill(6)}",
            'id_cliente': cliente_id,
            'fecha_venta': random_day,
            'total_venta': round(venta_total_monto, 2)
        })
        
        id_venta_counter += 1
        
        if len(detalles) >= NUM_DETALLES_TARGET:
            break

    df_ventas = pd.DataFrame(ventas)
    df_detalles = pd.DataFrame(detalles)
    
    # Ordenar por fecha cronológicamente
    df_ventas = df_ventas.sort_values(by='fecha_venta').reset_index(drop=True)
    
    df_ventas.to_csv('data/bronze/ventas_cabecera/ventas.csv', index=False)
    # PyArrow se usa internamente en Pandas para engine='pyarrow' si se desea pero CSV normal es suficiente.
    df_detalles.to_csv('data/bronze/ventas_detalle/detalles.csv', index=False)
    
    print(f"-> {len(df_ventas)} ventas generadas.")
    print(f"-> {len(df_detalles)} detalles de venta generados.")

if __name__ == '__main__':
    asegurar_directorios()
    df_maderas = generar_maderas()
    df_clientes = generar_clientes()
    generar_ventas(df_maderas, df_clientes)
    print("¡Generación de Capa Bronze completada!")
