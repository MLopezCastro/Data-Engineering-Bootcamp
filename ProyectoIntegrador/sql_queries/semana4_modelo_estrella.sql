-- =============================================
-- 🟦 SEMANA 4 - MODELO DE DATOS ESTRELLA
-- =============================================

-- 🔹 Crear tabla de dimensión CLIENTES
CREATE OR REPLACE TABLE dim_clientes AS
SELECT DISTINCT 
    cliente_id, 
    nombre AS nombre_cliente, 
    email, 
    ciudad, 
    fecha_alta
FROM 'data/data_clean/clientes_clean.csv';

-- 🔹 Crear tabla de dimensión PRODUCTOS
CREATE OR REPLACE TABLE dim_productos AS
SELECT DISTINCT 
    producto_id, 
    nombre AS nombre_producto, 
    categoria, 
    precio
FROM 'data/data_clean/productos_clean.csv';

-- 🔹 Crear tabla de dimensión FECHAS
CREATE OR REPLACE TABLE dim_fechas AS
SELECT DISTINCT 
    fecha_venta,
    EXTRACT(year FROM fecha_venta) AS anio,
    EXTRACT(month FROM fecha_venta) AS mes,
    EXTRACT(day FROM fecha_venta) AS dia
FROM 'data/data_clean/ventas_clean.csv';

-- 🔹 Crear tabla de hechos FACT_VENTAS
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
FROM 'data/data_clean/ventas_clean.csv' v
JOIN dim_productos p ON v.producto_id = p.producto_id;

-- ================================
-- ✅ EXPORTS (archivos de evidencia)
-- ================================
COPY dim_clientes  TO 'outputs/duckdb/dim_clientes.csv'  (HEADER, DELIMITER ',');
COPY dim_productos TO 'outputs/duckdb/dim_productos.csv' (HEADER, DELIMITER ',');
COPY fact_ventas   TO 'outputs/duckdb/fact_ventas.csv'   (HEADER, DELIMITER ',');
COPY dim_fechas TO 'outputs/duckdb/dim_fechas.csv' (HEADER, DELIMITER ',');

-- ================================
-- 🔎 VALIDACIONES (opcional)
-- ================================
-- ¿todas las ventas tienen cliente en la dimensión?
SELECT COUNT(*) AS clientes_faltantes
FROM fact_ventas
WHERE cliente_id NOT IN (SELECT cliente_id FROM dim_clientes);

-- ¿todas las ventas tienen producto en la dimensión?
SELECT COUNT(*) AS productos_faltantes
FROM fact_ventas
WHERE producto_id NOT IN (SELECT producto_id FROM dim_productos);

-- Conteos rápidos
SELECT 
  (SELECT COUNT(*) FROM dim_clientes)   AS filas_dim_clientes,
  (SELECT COUNT(*) FROM dim_productos)  AS filas_dim_productos,
  (SELECT COUNT(*) FROM fact_ventas)    AS filas_fact_ventas;
