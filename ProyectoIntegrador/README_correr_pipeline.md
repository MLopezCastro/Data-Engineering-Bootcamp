
Puntos clave (importantes):

* `run_pipeline.py` **NO** corre `etl_clean.py` ni `etl_ingesta.py`.
* `run_pipeline.py` hace:

  1. Ejecuta **DuckDB SQL Semana 3**: `duckdb_queries/run_all.sql`
  2. Ejecuta **DuckDB SQL Semana 4**: `sql_queries/semana4_modelo_estrella.sql`
  3. Corre **quality gate Semana 6**: `pipeline/validaciones.py` (sobre `data/data_clean/*.csv`)
* Por eso, **antes** de `run_pipeline.py`, vos tenés que garantizar que `data/data_clean/*.csv` está actualizado (o corriendo `etl_clean.py` o editándolo vos a mano, pero lo correcto es `etl_clean.py`).

A continuación te dejo el README corregido, “cerrado”, con tus nombres reales.

---

## README_correr_pipeline.md (versión definitiva)

````markdown
# Cómo correr el pipeline (RAW → CLEAN → Validaciones → DuckDB)

Este proyecto tiene 3 capas prácticas:
1) **RAW / CLEAN (CSV)**: datos en `data/data_raw/` y `data/data_clean/`
2) **Quality Gate (Semana 6)**: `pipeline/validaciones.py` valida los CSV CLEAN
3) **DuckDB (Semanas 3 y 4)**: `run_pipeline.py` ejecuta SQL en DuckDB + valida

---

## Estructura relevante

- `data/`
  - `data_raw/`   (inputs)
  - `data_clean/` (outputs clean)
- `pipeline/`
  - `generar_raw.py`
  - `etl_clean.py`
  - `etl_ingesta.py`
  - `validaciones.py`
- `duckdb_queries/`
  - `run_all.sql` (Semana 3)
- `sql_queries/`
  - `semana4_modelo_estrella.sql` (Semana 4)
- `run_pipeline.py` (runner principal: DuckDB + Validaciones)
- `run_duckdb.py` (runner opcional para ejecutar un SQL de DuckDB manualmente)
- `outputs/`
  - `validaciones.log`
  - `run_pipeline.log`
  - `duckdb/local.duckdb`
  - `duckdb/*.csv` (dimensiones, fact y ejercicios exportados)

---

## 0) Activar entorno (PowerShell)

Desde la raíz del proyecto:

```powershell
.\venv\Scripts\Activate.ps1
python --version
````

Si falta algo:

```powershell
pip install -r requirements.txt
```

---

## 1) Flujo OFICIAL cuando modificás RAW

### Paso 1 — (Opcional) Generar raw “de prueba”

Si querés regenerar datos raw sintéticos (si aplica a tu proyecto):

```powershell
python pipeline\generar_raw.py
```

### Paso 2 — ETL CLEAN (raw → clean)

Esto es lo que actualiza:

* `data/data_clean/clientes_clean.csv`
* `data/data_clean/productos_clean.csv`
* `data/data_clean/ventas_clean.csv`

```powershell
python pipeline\etl_clean.py
```

### Paso 3 — Validaciones (Semana 6)

Valida que los CSV clean tengan calidad e integridad.

```powershell
python pipeline\validaciones.py
```

Log:

* `outputs\validaciones.log`

Si falla: corregís raw o la lógica de clean, y repetís Paso 2 y 3.

### Paso 4 — DuckDB + Modelo Estrella + Quality Gate (RUN PRINCIPAL)

Este es el runner “macro” que:

* Ejecuta `duckdb_queries/run_all.sql` (Semana 3)
* Ejecuta `sql_queries/semana4_modelo_estrella.sql` (Semana 4)
* Corre `pipeline/validaciones.py` como **quality gate**

```powershell
python run_pipeline.py
```

Outputs:

* DB: `outputs/duckdb/local.duckdb`
* CSVs: `outputs/duckdb/*.csv`
* Log: `outputs/run_pipeline.log`

---

## 2) Flujo rápido si SOLO tocaste CLEAN (y NO raw)

Si editaste directamente `data/data_clean/*.csv` (no recomendado, pero sirve para test):

```powershell
python pipeline\validaciones.py
python run_pipeline.py
```

---

## 3) Correr SOLO DuckDB (sin el runner macro)

Si querés ejecutar un SQL puntual de DuckDB sin correr Semana 4 ni validaciones:

```powershell
python run_duckdb.py duckdb_queries\run_all.sql
```

(El runner principal recomendado es `run_pipeline.py`.)

---

## 4) Checks rápidos (para no volverse loco)

### 4.1 Verificar que existen los CSV CLEAN

```powershell
python -c "from pathlib import Path; p=Path('data/data_clean'); print([x.name for x in p.glob('*.csv')])"
```

### 4.2 Verificar que el pipeline generó dims/fact en outputs/duckdb

```powershell
python -c "from pathlib import Path; p=Path('outputs/duckdb'); print(sorted([x.name for x in p.glob('*.csv')]))"
```

### 4.3 Buscar un registro puntual en una dim exportada

Ejemplo: producto_id 601 en `dim_productos.csv`

```powershell
python -c "import pandas as pd; df=pd.read_csv('outputs/duckdb/dim_productos.csv'); print(df[df['producto_id'].astype(str).eq('601')].to_string(index=False))"
```

---

## 5) Resumen mínimo (lo que hacés el 90% de las veces)

Si cambiaste RAW:

```powershell
.\venv\Scripts\Activate.ps1
python pipeline\etl_clean.py
python pipeline\validaciones.py
python run_pipeline.py
```

Listo.

```

---

### Nota final sobre tu duda “¿primero raw → clean → validaciones → run?”
Con tu `run_pipeline.py`, la respuesta correcta es:

- **Sí**, pero con esta precisión:  
  **run_pipeline.py** = DuckDB (Sem 3 + Sem 4) + corre **validaciones** como gate.  
  Entonces **antes** de `run_pipeline.py`, vos **tenés** que correr `etl_clean.py` si cambiaste raw.

---

