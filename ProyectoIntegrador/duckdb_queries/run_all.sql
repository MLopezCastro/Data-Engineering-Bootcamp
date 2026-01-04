PPRAGMA threads=4;

-- =========================================
-- 0) Cargar CSV clean a tablas DuckDB
-- =========================================
CREATE OR REPLACE TABLE ventas AS
SELECT * FROM read_csv_auto(
  'data/data_clean/ventas_clean.csv',
  header=TRUE
);

CREATE OR REPLACE TABLE productos AS
SELECT * FROM read_csv_auto(
  'data/data_clean/productos_clean.csv',
  header=TRUE
);

CREATE OR REPLACE TABLE clientes AS
SELECT * FROM read_csv_auto(
  'data/data_clean/clientes_clean.csv',
  header=TRUE
);

-- =========================================
-- 1) SEMANA 4 - MODELO ESTRELLA (DIM + FACT)
-- =========================================

-- DIM CLIENTES
DROP TABLE IF EXISTS dim_clientes;
CREATE TABLE dim_clientes AS
SELECT DISTINCT
  CAST(cliente_id AS INTEGER) AS cliente_id,
  nombre AS nombre_cliente,
  email,
  ciudad,
  fecha_alta
FROM clientes;

-- DIM PRODUCTOS
DROP TABLE IF EXISTS dim_productos;
CREATE TABLE dim_productos AS
SELECT DISTINCT
  CAST(producto_id AS INTEGER) AS producto_id,
  nombre AS nombre_producto,
  categoria,
  CAST(precio AS DOUBLE) AS precio
FROM productos;

-- DIM FECHAS
DROP TABLE IF EXISTS dim_fechas;
CREATE TABLE dim_fechas AS
SELECT DISTINCT
  fecha_venta,
  EXTRACT(year  FROM CAST(fecha_venta AS DATE)) AS anio,
  EXTRACT(month FROM CAST(fecha_venta AS DATE)) AS mes,
  EXTRACT(day   FROM CAST(fecha_venta AS DATE)) AS dia
FROM ventas;

-- FACT VENTAS
DROP TABLE IF EXISTS fact_ventas;
CREATE TABLE fact_ventas AS
SELECT
  CAST(v.venta_id AS INTEGER) AS venta_id,
  CAST(v.cliente_id AS INTEGER) AS cliente_id,
  CAST(v.producto_id AS INTEGER) AS producto_id,
  v.fecha_venta,
  CAST(v.cantidad AS INTEGER) AS cantidad,
  CAST(v.descuento AS DOUBLE) AS descuento,
  p.precio,
  ROUND(CAST(v.cantidad AS DOUBLE) * p.precio * (1 - CAST(v.descuento AS DOUBLE) / 100.0), 2) AS ingreso_total
FROM ventas v
JOIN dim_productos p
  ON CAST(v.producto_id AS INTEGER) = p.producto_id;

-- EXPORTS estrella
COPY dim_clientes  TO 'outputs/duckdb/dim_clientes.csv'  (HEADER, DELIMITER ',');
COPY dim_productos TO 'outputs/duckdb/dim_productos.csv' (HEADER, DELIMITER ',');
COPY dim_fechas    TO 'outputs/duckdb/dim_fechas.csv'    (HEADER, DELIMITER ',');
COPY fact_ventas   TO 'outputs/duckdb/fact_ventas.csv'   (HEADER, DELIMITER ',');

-- =========================================
-- 2) SEMANA 3 - EJ1 / EJ2 / EJ3
-- =========================================

-- EJ1 — Ingresos por producto
DROP TABLE IF EXISTS ej1_ingresos_por_producto;
CREATE TABLE ej1_ingresos_por_producto AS
SELECT
  p.producto_id,
  p.nombre_producto AS nombre,
  ROUND(SUM(CAST(v.cantidad AS DOUBLE) * p.precio), 2) AS ingresos
FROM ventas v
JOIN dim_productos p
  ON CAST(v.producto_id AS INTEGER) = p.producto_id
GROUP BY p.producto_id, p.nombre_producto
ORDER BY ingresos DESC;

COPY ej1_ingresos_por_producto
TO 'outputs/duckdb/ej1_ingresos_por_producto.csv' (HEADER, DELIMITER ',');

-- EJ2 — Productos por encima del promedio
DROP TABLE IF EXISTS ej2_productos_sobre_promedio;
CREATE TABLE ej2_productos_sobre_promedio AS
WITH ingresos_por_producto AS (
  SELECT
    CAST(v.producto_id AS INTEGER) AS producto_id,
    SUM(CAST(v.cantidad AS DECIMAL(18,2)) * p.precio) AS ingresos
  FROM ventas v
  JOIN dim_productos p
    ON CAST(v.producto_id AS INTEGER) = p.producto_id
  GROUP BY CAST(v.producto_id AS INTEGER)
),
promedio AS (
  SELECT AVG(ingresos) AS avg_ingreso FROM ingresos_por_producto
)
SELECT
  ipp.producto_id,
  p.nombre_producto AS nombre,
  ROUND(ipp.ingresos, 2) AS ingresos
FROM ingresos_por_producto ipp
JOIN dim_productos p
  ON p.producto_id = ipp.producto_id
CROSS JOIN promedio pr
WHERE ipp.ingresos > pr.avg_ingreso
ORDER BY ingresos DESC;

COPY ej2_productos_sobre_promedio
TO 'outputs/duckdb/ej2_productos_sobre_promedio.csv' (HEADER, DELIMITER ',');

-- EJ3 — Ventas por región y participación %
DROP TABLE IF EXISTS ej3_region_participacion;
CREATE TABLE ej3_region_participacion AS
WITH ingresos_region AS (
  SELECT
    c.ciudad AS region,
    SUM(CAST(v.cantidad AS DECIMAL(18,2)) * p.precio) AS ingresos
  FROM ventas v
  JOIN dim_clientes c
    ON CAST(v.cliente_id AS INTEGER) = c.cliente_id
  JOIN dim_productos p
    ON CAST(v.producto_id AS INTEGER) = p.producto_id
  GROUP BY c.ciudad
),
total_global AS (
  SELECT SUM(ingresos) AS total FROM ingresos_region
)
SELECT
  ir.region,
  ROUND(ir.ingresos, 2) AS ingresos,
  ROUND(ir.ingresos * 100.0 / tg.total, 2) AS porcentaje
FROM ingresos_region ir
CROSS JOIN total_global tg
ORDER BY porcentaje DESC;

COPY ej3_region_participacion
TO 'outputs/duckdb/ej3_region_participacion.csv' (HEADER, DELIMITER ',');

-- =========================================
-- 3) Checks rápidos (opcional, no exporta)
-- =========================================
-- ¿ventas con cliente faltante?
SELECT COUNT(*) AS clientes_faltantes
FROM fact_ventas
WHERE cliente_id NOT IN (SELECT cliente_id FROM dim_clientes);

-- ¿ventas con producto faltante?
SELECT COUNT(*) AS productos_faltantes
FROM fact_ventas
WHERE producto_id NOT IN (SELECT producto_id FROM dim_productos);
