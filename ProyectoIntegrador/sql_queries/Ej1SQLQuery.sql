/* =========================================================
   EJERCICIO 1 — Ingresos por producto (sin descuento)
   Tablas: dbo.ventas (cantidad) + dbo.productos (precio)
   Pasos:
    1) JOIN ventas↔productos para traer el precio unitario
    2) ingresos = cantidad * precio
    3) GROUP BY por producto
    4) ORDER BY desc
   ========================================================= */
USE ProyectoBootcamp;
GO

SELECT
  p.producto_id,
  p.nombre,
  CAST(SUM(v.cantidad * p.precio) AS DECIMAL(18,2)) AS ingresos  -- 2 decimales
FROM dbo.ventas AS v
JOIN dbo.productos AS p
  ON p.producto_id = v.producto_id
GROUP BY
  p.producto_id, p.nombre
ORDER BY
  ingresos DESC;
