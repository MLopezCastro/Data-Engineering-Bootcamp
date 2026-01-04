from pathlib import Path
import duckdb

SQL = r"""
PRAGMA threads=4;

-- 1) Cargar clean a tablas
CREATE OR REPLACE TABLE clientes AS
SELECT * FROM read_csv_auto('data/data_clean/clientes_clean.csv', header=true);

CREATE OR REPLACE TABLE productos AS
SELECT * FROM read_csv_auto('data/data_clean/productos_clean.csv', header=true);

CREATE OR REPLACE TABLE ventas AS
SELECT * FROM read_csv_auto('data/data_clean/ventas_clean.csv', header=true);

-- 2) Modelo estrella
CREATE OR REPLACE TABLE dim_clientes AS
SELECT DISTINCT
  CAST(cliente_id AS INTEGER) AS cliente_id,
  nombre AS nombre_cliente,
  email,
  ciudad,
  fecha_alta
FROM clientes;

CREATE OR REPLACE TABLE dim_productos AS
SELECT DISTINCT
  CAST(producto_id AS INTEGER) AS producto_id,
  nombre AS nombre_producto,
  categoria,
  CAST(precio AS DOUBLE) AS precio
FROM productos;

CREATE OR REPLACE TABLE dim_fechas AS
SELECT DISTINCT
  fecha_venta,
  EXTRACT(year FROM CAST(fecha_venta AS DATE))  AS anio,
  EXTRACT(month FROM CAST(fecha_venta AS DATE)) AS mes,
  EXTRACT(day FROM CAST(fecha_venta AS DATE))   AS dia
FROM ventas;

CREATE OR REPLACE TABLE fact_ventas AS
SELECT
  CAST(v.venta_id AS INTEGER) AS venta_id,
  CAST(v.cliente_id AS INTEGER) AS cliente_id,
  CAST(v.producto_id AS INTEGER) AS producto_id,
  v.fecha_venta,
  CAST(v.cantidad AS INTEGER) AS cantidad,
  CAST(v.descuento AS DOUBLE) AS descuento,
  p.precio,
  ROUND(CAST(v.cantidad AS DOUBLE) * p.precio * (1 - CAST(v.descuento AS DOUBLE)/100.0), 2) AS ingreso_total
FROM ventas v
JOIN dim_productos p
  ON CAST(v.producto_id AS INTEGER) = p.producto_id;

-- 3) Export evidencias
COPY dim_clientes  TO 'outputs/duckdb/dim_clientes.csv'  (HEADER, DELIMITER ',');
COPY dim_productos TO 'outputs/duckdb/dim_productos.csv' (HEADER, DELIMITER ',');
COPY dim_fechas    TO 'outputs/duckdb/dim_fechas.csv'    (HEADER, DELIMITER ',');
COPY fact_ventas   TO 'outputs/duckdb/fact_ventas.csv'   (HEADER, DELIMITER ',');
"""

def main():
    out = Path("outputs") / "duckdb"
    out.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(out / "local.duckdb"))
    con.execute(SQL)
    con.close()

    print("OK - DIMs + fact exportadas en outputs/duckdb/")

if __name__ == "__main__":
    main()
