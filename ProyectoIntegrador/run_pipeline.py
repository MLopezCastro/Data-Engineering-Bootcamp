# run_pipeline.py
import os
import sys
import logging
import subprocess
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

# Semana 6 (validaciones)
VALIDACIONES_PY = BASE / "pipeline" / "validaciones.py"


def run_sql(con: duckdb.DuckDBPyConnection, path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"No encuentro el SQL: {path}")
    logger.info(f"Ejecutando SQL: {path}")
    sql_text = path.read_text(encoding="utf-8")
    con.execute(sql_text)
    logger.info(f"OK SQL: {path}")


def run_validaciones() -> None:
    """
    Ejecuta las validaciones de calidad (Semana 6) como quality gate.
    - Si falla, levanta excepción y corta el pipeline.
    - El detalle queda en outputs/validaciones.log (lo gestiona validaciones.py).
    """
    if not VALIDACIONES_PY.exists():
        raise FileNotFoundError(f"No encuentro el script de validaciones: {VALIDACIONES_PY}")

    logger.info(f"Ejecutando validaciones: {VALIDACIONES_PY}")

    # Usar el mismo python con el que se ejecuta este script (venv / task scheduler)
    py_exec = sys.executable

    # Ejecutar y capturar salida (por si querés verla en consola / logs)
    result = subprocess.run(
        [py_exec, str(VALIDACIONES_PY)],
        cwd=str(BASE),
        capture_output=True,
        text=True
    )

    # Loguear stdout/stderr para auditoría (sin romper tu log principal)
    if result.stdout:
        logger.info("STDOUT validaciones:\n" + result.stdout.strip())
    if result.stderr:
        logger.warning("STDERR validaciones:\n" + result.stderr.strip())

    if result.returncode != 0:
        raise RuntimeError(
            f"Validaciones FALLIDAS (returncode={result.returncode}). "
            f"Revisar outputs/validaciones.log"
        )

    logger.info("Validaciones OK (Semana 6).")


def main() -> None:
    logger.info("== Inicio pipeline completo ==")
    logger.info(f"CWD={Path.cwd()}")
    logger.info(f"DB={DB_PATH}")
    logger.info(f"OUT_DIR={OUT_DIR}")

    # Ejecutar SQL
    con = duckdb.connect(str(DB_PATH))
    run_sql(con, SQL_1)   # Semana 3
    run_sql(con, SQL_2)   # Semana 4

    # Quality gate (Semana 6)
    run_validaciones()

    logger.info("== Pipeline completo OK ==")

    print("OK - Pipeline completo ejecutado.")
    print(f"Log: {LOG_FILE}")
    print(f"DB : {DB_PATH}")
    print(f"Out: {OUT_DIR}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Fallo del pipeline")
        raise
