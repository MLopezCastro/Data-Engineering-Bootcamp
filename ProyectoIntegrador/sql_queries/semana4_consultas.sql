-- Conteos rápidos
SELECT COUNT(*) FROM dim_clientes;
SELECT COUNT(*) FROM dim_productos;
SELECT COUNT(*) FROM fact_ventas;

-- 1) Ingresos por categoría
SELECT p.categoria, ROUND(SUM(f.cantidad * p.precio * (1 - f.descuento/100.0)),2) AS ingresos
FROM fact_ventas f
JOIN dim_productos p ON f.producto_id = p.producto_id
GROUP BY p.categoria
ORDER BY ingresos DESC;

-- 2) Ingresos por mes (usando dim_fechas)
SELECT df.anio, df.mes,
       ROUND(SUM(f.cantidad * p.precio * (1 - f.descuento/100.0)),2) AS ingresos
FROM fact_ventas f
JOIN dim_productos p ON f.producto_id = p.producto_id
JOIN dim_fechas df ON f.fecha_venta = df.fecha_venta
GROUP BY df.anio, df.mes
ORDER BY df.anio, df.mes;

-- 3) Top 10 productos por ingresos
SELECT p.nombre_producto,
       ROUND(SUM(f.cantidad * p.precio * (1 - f.descuento/100.0)),2) AS ingresos
FROM fact_ventas f
JOIN dim_productos p ON f.producto_id = p.producto_id
GROUP BY p.nombre_producto
ORDER BY ingresos DESC
LIMIT 10;
