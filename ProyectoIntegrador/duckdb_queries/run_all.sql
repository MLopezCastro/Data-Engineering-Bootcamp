PRAGMA threads=4;

-- 0) Cargar clean a tablas
CREATE OR REPLACE TABLE ventas AS
SELECT * FROM read_csv_auto('data/data_clean/ventas_clean.csv', header=true);

CREATE OR REPLACE TABLE productos AS
SELECT * FROM read_csv_auto('data/data_clean/productos_clean.csv', header=true);

CREATE OR REPLACE TABLE clientes AS
SELECT * FROM read_csv_auto('data/data_clean/clientes_clean.csv', header=true);

-- 1) STAR SCHEMA
CREATE OR REPLACE TABLE dim_clientes AS
SELECT DISTINCT
  cliente_id,
  nombre AS nombre_cliente,
  email,
  ciudad,
  fecha_alta
FROM clientes;

CREATE OR REPLACE TABLE dim_productos AS
SELECT DISTINCT
  producto_id,
  nombre AS nombre_producto,
  categoria,
  precio
FROM productos;

CREATE OR REPLACE TABLE dim_fechas AS
SELECT DISTINCT
  fecha_venta,
  EXTRACT(year FROM fecha_venta) AS anio,
  EXTRACT(month FROM fecha_venta) AS mes,
  EXTRACT(day FROM fecha_venta) AS dia
FROM ventas;

CREATE OR REPLACE TABLE fact_ventas AS
SELECT
  v.venta_id,
  v.cliente_id,
  v.producto_id,
  v.fecha_venta,
  v.cantidad,
  v.descuento,
  p.precio,
  ROUND(v.cantidad * p.precio * (1 - v.descuento / 100.0), 2) AS ingreso_total
FROM ventas v
JOIN dim_productos p USING (producto_id);

-- 2) EXPORTS
COPY dim_clientes  TO 'outputs/duckdb/dim_clientes.csv'  (HEADER);
COPY dim_productos TO 'outputs/duckdb/dim_productos.csv' (HEADER);
COPY dim_fechas    TO 'outputs/duckdb/dim_fechas.csv'    (HEADER);
COPY fact_ventas   TO 'outputs/duckdb/fact_ventas.csv'   (HEADER);

-- 3) EJERCICIOS
CREATE OR REPLACE TABLE ej1_ingresos_por_producto AS
SELECT
  p.producto_id,
  p.nombre,
  ROUND(SUM(v.cantidad * p.precio), 2) AS ingresos
FROM ventas v
JOIN productos p USING (producto_id)
GROUP BY p.producto_id, p.nombre
ORDER BY ingresos DESC;

COPY ej1_ingresos_por_producto
TO 'outputs/duckdb/ej1_ingresos_por_producto.csv' (HEADER);

-- (dejás ej2/ej3 como ya los tenías)
