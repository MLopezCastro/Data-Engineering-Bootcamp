# run_duckdb.py
import sys, os
from pathlib import Path
import duckdb

# Root del proyecto = carpeta donde está este .py
BASE = Path(__file__).resolve().parent

# 1) Elegir qué SQL ejecutar: arg o default (run_all.sql)
if len(sys.argv) > 1:
    sql_path = Path(sys.argv[1]).resolve()
else:
    sql_path = BASE / "duckdb_queries" / "run_all.sql"

if not sql_path.exists():
    raise FileNotFoundError(f"No encuentro el SQL: {sql_path}")

# 2) Fijar working directory al root del proyecto (para rutas relativas en el SQL)
os.chdir(BASE)

# 3) Asegurar carpeta de salida y DB persistente
out_dir = BASE / "outputs" / "duckdb"
out_dir.mkdir(parents=True, exist_ok=True)
db_path = out_dir / "local.duckdb"

# 4) Ejecutar
sql_text = Path(sql_path).read_text(encoding="utf-8")
con = duckdb.connect(str(db_path))   # crea/abre outputs/duckdb/local.duckdb
con.execute(sql_text)

# 5) Info útil
print("OK - DuckDB ejecutado.")
print(f"SQL: {sql_path}")
print(f"CWD: {Path.cwd()}")
print(f"DB : {db_path}")
print(f"Outputs esperados en: {out_dir}")
