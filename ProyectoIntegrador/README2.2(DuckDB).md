

# README 2.2 — Alternativa con DuckDB (SQL directo sobre CSV)

## 🎯 Objetivo

Correr **las mismas consultas** pero usando **DuckDB**, que ejecuta SQL **directo sobre los CSV limpios** sin necesidad de un servidor.

---

## 📁 Estructura usada

```
ProyectoIntegrador/
├─ data/
│  └─ data_clean/
│     ├─ clientes_clean.csv
│     ├─ productos_clean.csv
│     └─ ventas_clean.csv
├─ duckdb_queries/
│  └─ run_all.sql           # script SQL que crea tablas y corre Ej1/Ej2/Ej3
├─ outputs/
│  └─ duckdb/
│     ├─ ej1_ingresos_por_producto.csv
│     ├─ ej2_productos_sobre_promedio.csv
│     ├─ ej3_region_participacion.csv
│     └─ local.duckdb       # base embebida opcional con las tablas
└─ run_duckdb.py            # runner en Python para ejecutar run_all.sql
```

---

## 🔧 Instalación rápida

1. Activar venv e instalar dependencias (ya están en `requirements.txt`):

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. (Si no existen) crear carpetas:

```powershell
mkdir .\duckdb_queries -Force
mkdir .\outputs\duckdb -Force
```

---

## ▶️ Cómo correr

### Opción A — Runner en Python (recomendada)

Desde la raíz del proyecto:

```powershell
python .\run_duckdb.py
```

Salida esperada:

* CSVs generados en `outputs/duckdb/` (**ej1**, **ej2**, **ej3**).
* Archivo `outputs/duckdb/local.duckdb` con las tablas materializadas (opcional).

### Opción B — Solo DuckDB (si tenés el CLI)

```powershell
duckdb -init .\duckdb_queries\run_all.sql
```

---

## 🧠 ¿Qué hace `duckdb_queries/run_all.sql`?

1. **Carga CSV limpios** como **tablas** DuckDB (usa `read_csv_auto` para inferir tipos).
2. Ejecuta las 3 consultas y **materializa** resultados con `CREATE TABLE ... AS SELECT`.
3. **Exporta** cada resultado a CSV (UTF-8) en `outputs/duckdb/`.

Puntos clave:

* No hay que crear esquemas a mano; DuckDB infiere tipos (con los formatos de fecha indicados).
* Las consultas son **las mismas** que en SQL Server, adaptadas a sintaxis DuckDB.
* **No aplica descuento** (como pidió la entrega).

  > Si querés incluirlo después: reemplazá `p.precio` por
  > `p.precio * (1 - v.descuento/100.0)` en cada `SUM(...)`.

---

## 📤 Resultados de entrega (DuckDB)

* `outputs/duckdb/ej1_ingresos_por_producto.csv`
* `outputs/duckdb/ej2_productos_sobre_promedio.csv`
* `outputs/duckdb/ej3_region_participacion.csv`

Ver rápido en PowerShell (forzando UTF-8 para acentos):

```powershell
Get-Content -Encoding utf8 .\outputs\duckdb\ej1_ingresos_por_producto.csv -TotalCount 20
Get-Content -Encoding utf8 .\outputs\duckdb\ej2_productos_sobre_promedio.csv -TotalCount 20
Get-Content -Encoding utf8 .\outputs\duckdb\ej3_region_participacion.csv -TotalCount 20
```

---

## 🗄️ ¿Qué es `local.duckdb`?

Es un **archivo de base de datos** DuckDB que guarda:

* las tablas de entrada (`ventas`, `productos`, `clientes`) y
* las tablas de salida (`ej1_*`, `ej2_*`, `ej3_*`).

Sirve para reabrir y consultar sin re-leer CSV. Es **opcional**:

* Inspeccionar:

  ```powershell
  python - << 'PY'
  import duckdb
  con = duckdb.connect('outputs/duckdb/local.duckdb')
  print(con.sql('SHOW TABLES').df())
  print(con.sql('SELECT * FROM ej1_ingresos_por_producto LIMIT 5').df())
  PY
  ```
* Si no querés persistirlo, en `run_duckdb.py` usá:

  ```python
  duckdb.connect(database=':memory:')
  ```

---

## 🧪 Consultas implementadas (resumen)

* **Ej1 — Ingresos por producto:** `SUM(v.cantidad * p.precio)` agrupado por producto.
* **Ej2 — Encima del promedio:** CTE con ingresos por producto + CTE de `AVG(ingresos)` y filtro `> promedio`.
* **Ej3 — Región y % participación:** ingresos por `clientes.ciudad` y `ingresos * 100 / total`.

> Las versiones completas están dentro de `duckdb_queries/run_all.sql`.

---

## 🧩 Diferencias vs SQL Server

| Aspecto         | SQL Server               | DuckDB                                       |
| --------------- | ------------------------ | -------------------------------------------- |
| Tipo            | Servidor (service)       | Embebido (librería/CLI)                      |
| Fuente de datos | Tablas cargadas por BULK | CSV/Parquet directo o tablas efímeras        |
| Persistencia    | DB en instancia          | Archivo `.duckdb` opcional                   |
| Uso típico      | ETL/OLTP/BI              | Análisis local/notebooks, exploración rápida |

Ambas versiones coexisten en el repo:

* **SQL Server** en `sql_queries/`
* **DuckDB** en `duckdb_queries/` + `run_duckdb.py` + `outputs/duckdb/`

---

## 🛠️ Troubleshooting

* **Acentos raros en consola**: leer CSV con `-Encoding utf8` (ver arriba).
* **Rutas**: en Windows, en SQL usás `C:\...`; en DuckDB (SQL) uso rutas **relativas** `data/data_clean/...` (se resuelven desde la raíz del repo).
* **“No module named duckdb”**: instalar `pip install duckdb` en el **venv** activo.
* **“syntax error near CREATE”**: en DuckDB, usá `CREATE TABLE ... AS WITH ... SELECT` (ya aplicado en `run_all.sql`).

---

## 🧷 Reproducible de punta a punta (solo DuckDB)

```powershell
# 1) Asegurar data limpia (ya creada por tu ETL en data/data_clean/)
# 2) Instalar
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 3) Ejecutar
python .\run_duckdb.py

# 4) Revisar salidas
Get-ChildItem .\outputs\duckdb\
```

