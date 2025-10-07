
---

# README2 — SQL aplicado (dataset ampliado + carga en SQL Server + queries)

## 0) Resumen

* Generé **más filas** con `pipeline/generar_raw.py` (usa Faker) y limpié con `pipeline/etl_ingesta.py`.
* Cargué en **SQL Server** las **3 tablas con todas las columnas** usando **BULK INSERT**.
* Dejé las **consultas** pedidas (sin aplicar descuento) listas para ejecutar.

---

## 1) Generación y limpieza de datos

**Parámetros (editables) en `pipeline/generar_raw.py`**

```python
N_CLIENTES  = 10_000
N_PRODUCTOS = 500
N_VENTAS    = 200_000
```

**Comandos**

```powershell
# activar venv e instalar deps
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install pandas numpy Faker

# generar raw y limpiar a *_clean.csv
python .\pipeline\generar_raw.py
python .\pipeline\etl_ingesta.py

# copiar los clean a una carpeta simple para BULK
New-Item -ItemType Directory -Path "C:\Temp\week3" -Force | Out-Null
Copy-Item ".\data\data_clean\*.csv" "C:\Temp\week3\" -Force
```

**Archivos usados para cargar**

* `data/data_clean/productos_clean.csv` — `producto_id,nombre,categoria,precio`
* `data/data_clean/clientes_clean.csv` — `cliente_id,nombre,email,ciudad,fecha_alta`
* `data/data_clean/ventas_clean.csv` — `venta_id,cliente_id,producto_id,fecha_venta,cantidad,descuento`

---

## 2) SQL Server — scripts y orden de ejecución

> Base: `ProyectoBootcamp`.

1. **Creación + BULK:** `sql_queries/InicialSQLQuery1.sql`

   * Borra si existen y crea **dbo.productos**, **dbo.clientes**, **dbo.ventas** con **todas las columnas**.
   * Hace `BULK INSERT` desde `C:\Temp\week3\*.csv`.
   * Incluye chequeos de conteo.

2. **Llaves y checks:** `sql_queries/LlavesForaneasSQLQuery.sql`

   * `FK_ventas_clientes (ventas.cliente_id → clientes.cliente_id)`
   * `FK_ventas_productos (ventas.producto_id → productos.producto_id)`
   * `CHECK cantidad > 0`
   * `CHECK descuento BETWEEN 0 AND 100`

> Nota: si el BULK falla por el fin de línea, cambiar `ROWTERMINATOR='0x0a'`.

---

## 3) Consultas (sin descuento)

### 3.1 `sql_queries/Ej1SQLQuery.sql` — Ingresos por producto

```sql
/* JOIN ventas↔productos; ingresos=cantidad*precio; GROUP BY; ORDER BY desc */
USE ProyectoBootcamp;
GO

SELECT
  p.producto_id,
  p.nombre,
  CAST(SUM(v.cantidad * p.precio) AS DECIMAL(18,2)) AS ingresos
FROM dbo.ventas AS v
JOIN dbo.productos AS p
  ON p.producto_id = v.producto_id
GROUP BY p.producto_id, p.nombre
ORDER BY ingresos DESC;
```

### 3.2 `sql_queries/Ej2SQLQuery.sql` — Productos por encima del promedio (CTEs)

```sql
/* CTE1: ingresos por producto; CTE2: promedio global; filtro > promedio */
USE ProyectoBootcamp;

WITH ingresos_por_producto AS (
  SELECT v.producto_id,
         SUM(CAST(v.cantidad AS DECIMAL(18,2)) * p.precio) AS ingresos
  FROM dbo.ventas v
  JOIN dbo.productos p ON p.producto_id = v.producto_id
  GROUP BY v.producto_id
),
promedio AS (
  SELECT AVG(ingresos) AS avg_ingreso
  FROM ingresos_por_producto
)
SELECT ipp.producto_id, p.nombre,
       CAST(ipp.ingresos AS DECIMAL(18,2)) AS ingresos
FROM ingresos_por_producto ipp
JOIN dbo.productos p ON p.producto_id = ipp.producto_id
CROSS JOIN promedio pr
WHERE ipp.ingresos > pr.avg_ingreso
ORDER BY ingresos DESC;
```

### 3.3 `sql_queries/Ej3SQLQuery.sql` — Ventas por región y participación %

```sql
/* CTE1: ingresos por región (clientes.ciudad como 'region');
   CTE2: total global; select final con % */
USE ProyectoBootcamp;
GO

WITH ingresos_region AS (
  SELECT c.ciudad AS region,
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
  CAST(ir.ingresos AS DECIMAL(18,2)) AS ingresos,
  CAST(ir.ingresos * 100.0 / tg.total AS DECIMAL(6,2)) AS porcentaje
FROM ingresos_region ir
CROSS JOIN total_global tg
ORDER BY porcentaje DESC;
```

> Si en algún momento querés **aplicar el descuento** de `ventas`, cambia `p.precio` por
> `p.precio * (1 - ISNULL(v.descuento,0)/100.0)` en cada `SUM(...)`.

---

## 4) Estructura relevante del repo

```
ProyectoIntegrador/
├─ data/
│  ├─ data_raw/
│  └─ data_clean/
├─ pipeline/
│  ├─ generar_raw.py
│  └─ etl_ingesta.py
├─ sql_queries/
│  ├─ InicialSQLQuery1.sql
│  ├─ LlavesForaneasSQLQuery.sql
│  ├─ Ej1SQLQuery.sql
│  ├─ Ej2SQLQuery.sql
│  └─ Ej3SQLQuery.sql
└─ README2.md
```

---

## 5) Runbook rápido

1. `python pipeline/generar_raw.py`
2. `python pipeline/etl_ingesta.py`
3. `Copy-Item .\data\data_clean\*.csv C:\Temp\week3\ -Force`
4. Ejecutar **InicialSQLQuery1.sql** → crea y carga tablas
5. Ejecutar **LlavesForaneasSQLQuery.sql**
6. Ejecutar **Ej1SQLQuery.sql**, **Ej2SQLQuery.sql**, **Ej3SQLQuery.sql** para la entrega.

