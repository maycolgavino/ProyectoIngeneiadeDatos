# Capa Silver (Data Quality) - Justificación Técnica

Este documento explica las "mejores decisiones" tomadas para la reestructuración del pipeline al avanzar hacia la Capa Silver (donde la Data Científica queda pulida para que Negocios la pueda consumir).

## 1. Modularidad y OOP (Programación Orientada a Objetos)

**¿Qué hicimos?**
En lugar de tener un mega-script de 500 líneas (como ocurre con el generador de Bronze), dividimos la lógica en archivos separados (`src/silver/config.py`, `src/silver/transformers.py`) y un orquestador principal (`procesador_silver.py`). Además, aplicamos una clase pura para heredar métodos de limpieza (`DataCleaner`) a la clase principal de negocio (`SilverTransformer`).

**¿Por qué y Para qué?**
*   **Mantenibilidad de Pipeline:** En Ingeniería de Datos moderna, si una regla para limpiar Clientes falla, no quieres romper la regla que cruza Ventas. La modularidad aísla los componentes.
*   **OOP (Orientado a Objetos):** Al encapsular los DF (Dataframes) como procesos internos de métodos de clase, mañana podrías inyectar configuración asíncrona o heredar validadores de Data Quality mucho más sencillo.

## 2. Unificación Fact_Ventas (El Mega Join transaccional)

**¿Qué hicimos?**
Eliminamos la tabla `ventas.csv` (cabeceras). En vez de propagar 2 archivos distintos hacia reportes, *unificamos* el Detalle y la Cabecera en la salida Silver (`fact_ventas_marketing`).

**¿Por qué y Para qué?**
*   **Modelado Dimensional Star-Schema:** Las herramientas de visualización (ej. Power BI, Tableau, Looker) trabajan pésimo con relaciones Cabecera-Detalle y tienden a duplicar las filas causándote errores millonarios de suma. Unir (Join) el `id_venta`, `fecha` y `cliente` hacia nivel "Línea de Detalle" (Hecho puro) crea una *Wide Table* imbatible que responde rapidísimamente a las métricas del negocio.

## 3. Feature Engineering de Calendario de Marketing

**¿Qué hicimos?**
Durante el Join de la Capa Silver extrajimos de la fecha de venta los componentes: `anio`, `mes`, `nombre_mes`, `trimestre` (Q1, Q2, etc.) y `es_fin_de_semana` pre-cacheados como columnas.

**¿Por qué y Para qué?**
*   Tú querías la data para que marketing entienda picos mensuales/bimestrales. Hacer que una base de datos calcule `DATE_TRUNC`, `DATE_PART()` o `FORMAT()` sobre +100 mil registros en el vuelo cada vez que alguien abre un reporte es costoso (fuego quemando billetes en GCP/AWS) y súper lento.
*   Cálculo Directo: Precomputar en Silver el "Trimestre" y el "Mes" significa que el reporte solo lee los renglones directamente sin usar nada de procesador analítico, el filtrado es casi del 100% eficiente y marketing no tiene que ser técnico creando funciones DAX o SQL para sacar el trimestre.

## 4. Almacenamiento "Parquet" (Columnar)

**¿Qué hicimos?**
La capa Bronze escribía CSVs legibles. La capa Silver ahora escribe archivos con extensión `.parquet`.

**¿Por qué y Para qué?**
*   El CSV guarda TODO como texto, el PARQUET guarda los tipos de datos reales (`float64`, `int32`, `datetime`). 
*   **Compresión y Costos:** El formato columnar de Apache Parquet ahorra espacio drástico (usualmente pesa 80% a 90% menos que un CSV), lo cual ahorra costos de Storage en los DataLakes (S3) y lo más importante: reduce drásticamente el tiempo de Input/Output al cargar de vuelta el archivo hacia Pandas al analizar modelos.
