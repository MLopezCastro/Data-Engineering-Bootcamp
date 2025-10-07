# run_duckdb.py
import duckdb, pathlib

base = pathlib.Path(__file__).resolve().parent
sql_path = base / "duckdb_queries" / "run_all.sql"

# DB local (archivo) y carpeta de salida ya usadas en el SQL
db_path = base / "outputs" / "duckdb" / "local.duckdb"
db_path.parent.mkdir(parents=True, exist_ok=True)

sql_text = sql_path.read_text(encoding="utf-8")

con = duckdb.connect(str(db_path))   # crea/abre local.duckdb
con.execute(sql_text)                 # ejecuta todo el script
print(f"OK - DuckDB ejecutado. CSVs en: {db_path.parent}")
