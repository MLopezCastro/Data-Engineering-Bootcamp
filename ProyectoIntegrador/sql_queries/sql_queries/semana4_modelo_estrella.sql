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
