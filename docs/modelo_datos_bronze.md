# Modelo de Datos (Capa Bronze)

El script generador extrae 4 conjuntos de datos (`datasets`) simulando dos maestros y dos transaccionales. Aquí definimos el esquema de cada archivo CSV alojado en `data/bronze/`.

## 1. Maestros
Definen las entidades descriptivas.

### `maderas.csv`
Almacena el catálogo de productos disponibles en la maderera.
*   `id_madera` (String): Código único secuencial (Ej: M-00001).
*   `especie` (String): Tornillo, Huimba, Caimotillo, etc.
*   `espesor_pulg` (Float): Espesor nominal en pulgadas.
*   `ancho_pulg` (Float): Ancho nominal en pulgadas.
*   `largo_pies` (Float): Largo nominal en pies.
*   `pies_cuadrados` (Float): Volumen estandarizado calculado como `(espesor * ancho * largo) / 12`.
*   `descripcion` (String): Descripción amigable del corte.
*   `precio_pt_referencial` (Float): Precio referencial del pie tabular (PT) base del año 2023.

### `clientes.csv`
Padrón de empresas compradoras simuladas en Perú.
*   `id_cliente` (String): Identificador interno.
*   `nombre_empresa` (String): Razón social comercial.
*   `ruc` (String): Número simulado de 11 dígitos iniciando siempre en 20.
*   `departamento` (String): Región geográfica predominante (Ej: Lima, Arequipa).
*   `fecha_registro` (Date): Fecha de alta del cliente en el sistema.

## 2. Transaccionales
Simulan la facturación a lo largo del tiempo.

### `ventas.csv`
Cabecera y totalizados de la factura comercial.
*   `id_venta` (String): Código secuencial identificador (Ej: V-000001).
*   `id_cliente` (String): Foreign Key hacia la dimensión Cliente.
*   `fecha_venta` (Date/Time): Marca de tiempo de la operación.
*   `total_venta` (Float): Total a pagar del ticket calculado en base a todos los detalles.

### `detalles.csv`
Granularidad final. Cada producto facturado por línea.
*   `id_detalle` (Integer): Correlativo absoluto único.
*   `id_venta` (String): Foreign Key que lo amarra a una boleta específica.
*   `id_madera` (String): Foreign Key de la madera elegida del inventario.
*   `descripcion_snapshot` (String): Copia transaccional de la descripción de la madera al momento de compra (Data Warehouse Slowly Changing Dimensions fallback).
*   `cantidad_piezas` (Integer): Cantidad despachada.
*   `precio_pt_base` (Float): Precio por Pie Tabular aplicando el índice de inflación anual sobre el precio referencial.
*   `descuento_pct` (Float): Porcentaje de descuento por promociones (0% a 12%).
*   `precio_pt_aplicado` (Float): Precio con el descuento deducido.
*   `subtotal` (Float): Monto total sin IGV calculado como `pies_cuadrados * cantidad * precio_aplicado`.
