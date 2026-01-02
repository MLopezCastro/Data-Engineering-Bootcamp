# pipeline/validaciones.py
from pathlib import Path
import pandas as pd
import logging
from datetime import datetime

BASE = Path(__file__).resolve().parents[1]          # root del proyecto
CLEAN = BASE / "data" / "data_clean"
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

LOG_FILE = OUT / "validaciones.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("validaciones")

def fail(msg: str):
    logger.error(msg)
    raise Exception(msg)

def main():
    logger.info("== Inicio validaciones ==")

    # ---------- Cargar datasets limpios ----------
    clientes = pd.read_csv(CLEAN / "clientes_clean.csv")
    productos = pd.read_csv(CLEAN / "productos_clean.csv")
    ventas = pd.read_csv(CLEAN / "ventas_clean.csv")

    errores = 0

    # ========== VALIDACIONES CLIENTES ==========
    # 1) PK no nula y única
    if clientes["cliente_id"].isna().any():
        errores += 1
        logger.warning("Clientes: cliente_id contiene nulos.")
    if clientes["cliente_id"].duplicated().any():
        errores += 1
        logger.warning("Clientes: cliente_id contiene duplicados.")

    # 2) Email no nulo (en limpio debería venir bien)
    if clientes["email"].isna().any():
        errores += 1
        logger.warning("Clientes: email contiene nulos.")

    # ========== VALIDACIONES PRODUCTOS ==========
    if productos["producto_id"].isna().any():
        errores += 1
        logger.warning("Productos: producto_id contiene nulos.")
    if productos["producto_id"].duplicated().any():
        errores += 1
        logger.warning("Productos: producto_id contiene duplicados.")
    # precio > 0 (o >=0 si permitís 0)
    if (productos["precio"] <= 0).any():
        errores += 1
        logger.warning("Productos: hay precios <= 0.")

    # ========== VALIDACIONES VENTAS ==========
    # Tipos / parseo de fecha
    ventas["fecha_venta"] = pd.to_datetime(ventas["fecha_venta"], errors="coerce")
    if ventas["fecha_venta"].isna().any():
        errores += 1
        logger.warning("Ventas: fecha_venta inválida (NaT) en dataset limpio.")

    # fechas futuras
    hoy = pd.Timestamp(datetime.today().date())
    if (ventas["fecha_venta"] > hoy).any():
        errores += 1
        logger.warning("Ventas: hay fechas futuras.")

    # cantidad > 0
    if (ventas["cantidad"] <= 0).any():
        errores += 1
        logger.warning("Ventas: hay cantidad <= 0.")

    # descuento 0-100
    if (~ventas["descuento"].between(0, 100)).any():
        errores += 1
        logger.warning("Ventas: hay descuentos fuera de rango 0-100.")

    # duplicados de venta_id
    if ventas["venta_id"].duplicated().any():
        errores += 1
        logger.warning("Ventas: hay venta_id duplicados.")

    # integridad referencial (FKs)
    cli_ids = set(clientes["cliente_id"].astype(int).tolist())
    prod_ids = set(productos["producto_id"].astype(int).tolist())

    fk_cli_bad = ~ventas["cliente_id"].astype(int).isin(cli_ids)
    fk_prod_bad = ~ventas["producto_id"].astype(int).isin(prod_ids)

    if fk_cli_bad.any():
        errores += 1
        logger.warning(f"Ventas: {fk_cli_bad.sum()} registros con cliente_id sin match en dim_clientes.")
    if fk_prod_bad.any():
        errores += 1
        logger.warning(f"Ventas: {fk_prod_bad.sum()} registros con producto_id sin match en dim_productos.")

    # ---------- Resultado ----------
    if errores == 0:
        logger.info("✅ Validaciones PASADAS (0 errores).")
        print(f"OK - Validaciones PASADAS. Log: {LOG_FILE}")
    else:
        fail(f"❌ Validaciones FALLIDAS. Errores encontrados: {errores}. Revisar {LOG_FILE}")

if __name__ == "__main__":
    main()
