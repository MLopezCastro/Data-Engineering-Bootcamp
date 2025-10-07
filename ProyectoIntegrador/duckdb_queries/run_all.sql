PRAGMA threads=4;

-- Cargar CSV a tablas DuckDB
CREATE OR REPLACE TABLE ventas AS
SELECT * FROM read_csv_auto('data/data_clean/ventas_clean.csv', header=TRUE, dateformat='%Y-%m-%d');

CREATE OR REPLACE TABLE productos AS
SELECT * FROM read_csv_auto('data/data_clean/productos_clean.csv', header=TRUE);

CREATE OR REPLACE TABLE clientes AS
SELECT * FROM read_csv_auto('data/data_clean/clientes_clean.csv', header=TRUE, dateformat='%Y-%m-%d');

-- =========================
-- EJ1 — Ingresos por producto
-- =========================
DROP TABLE IF EXISTS ej1_ingresos_por_producto;
CREATE TABLE ej1_ingresos_por_producto AS
SELECT
  p.producto_id,
  p.nombre,
  ROUND(SUM(v.cantidad * p.precio), 2) AS ingresos
FROM ventas v
JOIN productos p USING (producto_id)
GROUP BY p.producto_id, p.nombre
ORDER BY ingresos DESC;

COPY ej1_ingresos_por_producto
TO 'outputs/duckdb/ej1_ingresos_por_producto.csv' (HEADER, DELIMITER ',');

-- =========================================
-- EJ2 — Productos por encima del promedio
-- =========================================
DROP TABLE IF EXISTS ej2_productos_sobre_promedio;
CREATE TABLE ej2_productos_sobre_promedio AS
WITH ingresos_por_producto AS (
  SELECT v.producto_id,
         SUM(CAST(v.cantidad AS DECIMAL(18,2)) * p.precio) AS ingresos
  FROM ventas v
  JOIN productos p USING (producto_id)
  GROUP BY v.producto_id
),
promedio AS (
  SELECT AVG(ingresos) AS avg_ingreso FROM ingresos_por_producto
)
SELECT
  ipp.producto_id,
  p.nombre,
  ROUND(ipp.ingresos, 2) AS ingresos
FROM ingresos_por_producto ipp
JOIN productos p ON p.producto_id = ipp.producto_id
CROSS JOIN promedio pr
WHERE ipp.ingresos > pr.avg_ingreso
ORDER BY ingresos DESC;

COPY ej2_productos_sobre_promedio
TO 'outputs/duckdb/ej2_productos_sobre_promedio.csv' (HEADER, DELIMITER ',');

-- =========================================
-- EJ3 — Ventas por región y participación %
-- =========================================
DROP TABLE IF EXISTS ej3_region_participacion;
CREATE TABLE ej3_region_participacion AS
WITH ingresos_region AS (
  SELECT
    c.ciudad AS region,
    SUM(CAST(v.cantidad AS DECIMAL(18,2)) * p.precio) AS ingresos
  FROM ventas v
  JOIN clientes  c USING (cliente_id)
  JOIN productos p USING (producto_id)
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
