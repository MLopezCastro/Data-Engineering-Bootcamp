/* =========================================================
   EJERCICIO 2 — Productos por encima del promedio
   Idea:
     CTE #1  -> ingresos por producto
     CTE #2  -> promedio global de esos ingresos
     Select  -> filtra los > promedio y muestra nombre + ingresos
   ========================================================= */

USE ProyectoBootcamp;

WITH ingresos_por_producto AS (
  SELECT
      v.producto_id,
      SUM(CAST(v.cantidad AS DECIMAL(18,2)) * p.precio) AS ingresos
  FROM dbo.ventas v
  JOIN dbo.productos p ON p.producto_id = v.producto_id
  GROUP BY v.producto_id
),
promedio AS (
  SELECT AVG(ingresos) AS avg_ingreso
  FROM ingresos_por_producto
)
SELECT
    ipp.producto_id,
    p.nombre,
    CAST(ipp.ingresos AS DECIMAL(18,2)) AS ingresos
FROM ingresos_por_producto ipp
JOIN dbo.productos p ON p.producto_id = ipp.producto_id
CROSS JOIN promedio pr
WHERE ipp.ingresos > pr.avg_ingreso
ORDER BY ingresos DESC;

