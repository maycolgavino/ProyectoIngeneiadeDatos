import pandas as pd

class DataCleaner:
    """
    Clase base orientada a objetos para albergar funciones de limpieza genéricas.
    Es provechoso usar OOP porque nos permite heredar lógicas o aislar estado si el pipeline crece.
    """
    @staticmethod
    def clean_text_column(series: pd.Series) -> pd.Series:
        """Remueve espacios en blanco dobles y pasa el texto a MAYÚSCULAS para evitar duplicados lógicos."""
        return series.str.strip().str.replace(r'\s+', ' ', regex=True).str.upper()

class SilverTransformer(DataCleaner):
    """
    Motor Táctico de Transformación. 
    Se encarga de procesar los DataFrames que vienen desde 'Bronze' y cruzarlos/limpiarlos.
    Hereda de DataCleaner para reutilizar métodos.
    """
    
    def __init__(self):
        # Esta clase inicializa el estado del transformador. Si quisiéramos inyectar configs, se harían aquí.
        print("Iniciando Motor de Transformación Capa Silver (OOP)...")

    def process_clientes(self, df_clientes: pd.DataFrame) -> pd.DataFrame:
        """Limpia la dimensión de clientes."""
        print(" -> Procesando Dimensión Clientes...")
        df = df_clientes.copy()
        
        # 1. Estandarizamos textos para el analista
        df['nombre_empresa'] = self.clean_text_column(df['nombre_empresa'])
        df['departamento'] = self.clean_text_column(df['departamento'])
        
        # 2. Rellenamos vacíos por seguridad (Buenas prácticas en DWH)
        df['departamento'] = df['departamento'].fillna('DESCONOCIDO')
        
        # 3. Forzamos formato (RUC como string puro)
        df['ruc'] = df['ruc'].astype(str)
        
        return df

    def process_maderas(self, df_maderas: pd.DataFrame) -> pd.DataFrame:
        """Enriquece el catálogo de maderas con agrupaciones analíticas."""
        print(" -> Procesando Dimensión Maderas...")
        df = df_maderas.copy()
        
        df['especie'] = self.clean_text_column(df['especie'])
        
        # 1. Feature Engineering: Agrupar por categoría de volumen (Útil para saber qué se vente más)
        def categorizar_volumen(pt):
            if pt < 5: return 'Corte Ligero'
            if pt <= 15: return 'Corte Estándar'
            return 'Corte Pesado / Vigas'
            
        df['categoria_volumen'] = df['pies_cuadrados'].apply(categorizar_volumen)
        return df

    def process_ventas_marketing(self, df_cabecera: pd.DataFrame, df_detalle: pd.DataFrame) -> pd.DataFrame:
        """
        Une (Join) Cabecera y Detalle, e inyecta Variables de Dimensión de Tiempo (Data Time).
        Súper importante para los reportes de Estrategia de Marketing pedidos (Trimestres, Meses, etc).
        """
        print(" -> Generando Dataset Consolidado Fact Ventas Marketing...")
        
        # 1. Join Principal: Inner Join usando 'id_venta' de llave foránea
        df_join = pd.merge(df_detalle, df_cabecera, on='id_venta', how='inner')
        
        # 2. Parseo estricto a formato Fecha de la columna 'fecha_venta'
        df_join['fecha_venta'] = pd.to_datetime(df_join['fecha_venta'])
        
        # 3. Feature Engineering de Calendario / Marketing Series de Tiempo
        # Al extraer esto acá, el BI o PowerBI no debe calcularlo pesado al vuelo, ya viene masticado.
        df_join['anio'] = df_join['fecha_venta'].dt.year
        df_join['mes'] = df_join['fecha_venta'].dt.month
        df_join['nombre_mes'] = df_join['fecha_venta'].dt.strftime('%B') # Ej: January, February...
        df_join['trimestre'] = 'Q' + df_join['fecha_venta'].dt.quarter.astype(str)
        # Es fin de semana si el día de la semana es 5 (Sábado) o 6 (Domingo)
        df_join['es_fin_de_semana'] = df_join['fecha_venta'].dt.dayofweek.isin([5, 6])
        
        # Quitamos la columna de total_venta de la cabecera porque queremos totalizar los subtotales usando BI
        # df_join = df_join.drop(columns=['total_venta']) # Opcional: limpiar la tabla plana

        return df_join
