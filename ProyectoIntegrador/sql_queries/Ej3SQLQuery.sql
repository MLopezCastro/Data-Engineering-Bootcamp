/* =========================================================
   EJERCICIO 3 — Ventas por región y participación %
   Idea:
     CTE #1 (ingresos_region): suma por región (usamos clientes.ciudad como 'region')
     CTE #2 (total_global)   : suma de todos los ingresos
     Select final            : region, ingresos y % sobre el total
   ========================================================= */
USE ProyectoBootcamp;
GO

WITH ingresos_region AS (
  SELECT
      c.ciudad AS region,
      SUM(CAST(v.cantidad AS DECIMAL(18,2)) * p.precio) AS ingresos
  FROM dbo.ventas v
  JOIN dbo.clientes  c ON c.cliente_id  = v.cliente_id
  JOIN dbo.productos p ON p.producto_id = v.producto_id
  GROUP BY c.ciudad
),
total_global AS (
  SELECT SUM(ingresos) AS total
  FROM ingresos_region
)
SELECT
    ir.region,
    CAST(ir.ingresos AS DECIMAL(18,2))            AS ingresos,
    CAST(ir.ingresos * 100.0 / tg.total AS DECIMAL(6,2)) AS porcentaje
FROM ingresos_region AS ir
CROSS JOIN total_global AS tg
ORDER BY porcentaje DESC;
