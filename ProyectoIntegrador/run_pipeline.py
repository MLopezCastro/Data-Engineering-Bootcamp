# run_pipeline.py
import os
import logging
from pathlib import Path
import duckdb

BASE = Path(__file__).resolve().parent
os.chdir(BASE)

OUT_DIR = BASE / "outputs" / "duckdb"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = OUT_DIR / "local.duckdb"

LOG_FILE = BASE / "outputs" / "run_pipeline.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("run_pipeline")

SQL_1 = BASE / "duckdb_queries" / "run_all.sql"
SQL_2 = BASE / "sql_queries" / "semana4_modelo_estrella.sql"

def run_sql(con, path: Path):
    if not path.exists():
        raise FileNotFoundError(f"No encuentro el SQL: {path}")
    logger.info(f"Ejecutando SQL: {path}")
    sql_text = path.read_text(encoding="utf-8")
    con.execute(sql_text)
    logger.info(f"OK SQL: {path}")

def main():
    logger.info("== Inicio pipeline completo ==")
    logger.info(f"CWD={Path.cwd()}")
    logger.info(f"DB={DB_PATH}")
    logger.info(f"OUT_DIR={OUT_DIR}")

    con = duckdb.connect(str(DB_PATH))
    run_sql(con, SQL_1)  # Semana 3
    run_sql(con, SQL_2)  # Semana 4

    logger.info("== Pipeline completo OK ==")

    print("OK - Pipeline completo ejecutado.")
    print(f"Log: {LOG_FILE}")
    print(f"DB : {DB_PATH}")
    print(f"Out: {OUT_DIR}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Fallo del pipeline")
        raise
