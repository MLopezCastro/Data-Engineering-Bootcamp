# pipeline/validaciones.py
from pathlib import Path
import logging
import pandas as pd
from datetime import datetime


BASE = Path(__file__).resolve().parents[1]      # root del proyecto
CLEAN = BASE / "data" / "data_clean"
OUT = BASE / "outputs"
OUT.mkdir(parents=True, exist_ok=True)

LOG_FILE = OUT / "validaciones.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("validaciones")


def _req_file(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"No existe: {path}")


def _warn(cond: bool, msg: str) -> int:
    """Suma 1 error si cond=True y loguea warning."""
    if cond:
        logger.warning(msg)
        return 1
    return 0


def _error_and_raise(total_errores: int) -> None:
    logger.error(f"❌ Validaciones FALLIDAS. Errores encontrados: {total_errores}.")
    raise Exception(f"Validaciones FALLIDAS ({total_errores}). Revisar: {LOG_FILE}")


def main() -> None:
    logger.info("== Inicio validaciones (Semana 6) ==")

    # ---------- Archivos requeridos ----------
    f_cli = CLEAN / "clientes_clean.csv"
    f_pro = CLEAN / "productos_clean.csv"
    f_ven = CLEAN / "ventas_clean.csv"
    _req_file(f_cli)
    _req_file(f_pro)
    _req_file(f_ven)

    # ---------- Carga ----------
    clientes = pd.read_csv(f_cli)
    productos = pd.read_csv(f_pro)
    ventas = pd.read_csv(f_ven)

    errores = 0

    # =========================
    # CLIENTES
    # =========================
    expected_cli = {"cliente_id", "nombre", "email", "ciudad", "fecha_alta"}
    errores += _warn(set(clientes.columns) != expected_cli,
                     f"Clientes: columnas inesperadas. Esperado={expected_cli}, Actual={set(clientes.columns)}")

    errores += _warn(clientes["cliente_id"].isna().any(),
                     "Clientes: cliente_id contiene nulos.")
    errores += _warn(clientes["cliente_id"].duplicated().any(),
                     "Clientes: cliente_id contiene duplicados.")

    errores += _warn(clientes["email"].isna().any(),
                     "Clientes: email contiene nulos.")
    errores += _warn((clientes["email"].astype(str).str.strip() == "").any(),
                     "Clientes: email contiene strings vacíos.")

    # fecha_alta parseable + no futura (opcional)
    cli_fecha = pd.to_datetime(clientes["fecha_alta"], errors="coerce", dayfirst=True)
    errores += _warn(cli_fecha.isna().any(),
                     "Clientes: fecha_alta contiene valores no parseables.")
    hoy = pd.Timestamp(datetime.today().date())
    errores += _warn((cli_fecha > hoy).any(),
                     "Clientes: fecha_alta contiene fechas futuras.")

    # =========================
    # PRODUCTOS
    # =========================
    expected_pro = {"producto_id", "nombre", "categoria", "precio"}
    errores += _warn(set(productos.columns) != expected_pro,
                     f"Productos: columnas inesperadas. Esperado={expected_pro}, Actual={set(productos.columns)}")

    errores += _warn(productos["producto_id"].isna().any(),
                     "Productos: producto_id contiene nulos.")
    errores += _warn(productos["producto_id"].duplicated().any(),
                     "Productos: producto_id contiene duplicados.")

    # precio numérico y > 0
    precio_num = pd.to_numeric(productos["precio"], errors="coerce")
    errores += _warn(precio_num.isna().any(),
                     "Productos: precio tiene valores no numéricos.")
    errores += _warn((precio_num <= 0).any(),
                     "Productos: hay precios <= 0 (regla: precio debe ser > 0).")

    # =========================
    # VENTAS
    # =========================
    expected_ven = {"venta_id", "cliente_id", "producto_id", "fecha_venta", "cantidad", "descuento"}
    errores += _warn(set(ventas.columns) != expected_ven,
                     f"Ventas: columnas inesperadas. Esperado={expected_ven}, Actual={set(ventas.columns)}")

    # PK duplicada
    errores += _warn(ventas["venta_id"].isna().any(),
                     "Ventas: venta_id contiene nulos.")
    errores += _warn(ventas["venta_id"].duplicated().any(),
                     "Ventas: venta_id contiene duplicados.")

    # fecha_venta válida + no futura
    ven_fecha = pd.to_datetime(ventas["fecha_venta"], errors="coerce", dayfirst=True)
    errores += _warn(ven_fecha.isna().any(),
                     "Ventas: fecha_venta contiene valores no parseables.")
    errores += _warn((ven_fecha > hoy).any(),
                     "Ventas: fecha_venta contiene fechas futuras.")

    # cantidad > 0
    cant = pd.to_numeric(ventas["cantidad"], errors="coerce")
    errores += _warn(cant.isna().any(),
                     "Ventas: cantidad tiene valores no numéricos.")
    errores += _warn((cant <= 0).any(),
                     "Ventas: hay cantidad <= 0.")

    # descuento 0-100
    desc = pd.to_numeric(ventas["descuento"], errors="coerce")
    errores += _warn(desc.isna().any(),
                     "Ventas: descuento tiene valores no numéricos.")
    errores += _warn((~desc.between(0, 100)).any(),
                     "Ventas: hay descuentos fuera de rango (0-100).")

    # Integridad referencial (FKs)
    cli_ids = set(pd.to_numeric(clientes["cliente_id"], errors="coerce").dropna().astype(int))
    pro_ids = set(pd.to_numeric(productos["producto_id"], errors="coerce").dropna().astype(int))

    ven_cli = pd.to_numeric(ventas["cliente_id"], errors="coerce")
    ven_pro = pd.to_numeric(ventas["producto_id"], errors="coerce")

    errores += _warn(ven_cli.isna().any(),
                     "Ventas: cliente_id tiene valores no numéricos o nulos.")
    errores += _warn(ven_pro.isna().any(),
                     "Ventas: producto_id tiene valores no numéricos o nulos.")

    fk_cli_bad = ven_cli.dropna().astype(int).apply(lambda x: x not in cli_ids)
    fk_pro_bad = ven_pro.dropna().astype(int).apply(lambda x: x not in pro_ids)

    errores += _warn(fk_cli_bad.any(),
                     f"Ventas: {int(fk_cli_bad.sum())} registros con cliente_id sin match en dim_clientes.")
    errores += _warn(fk_pro_bad.any(),
                     f"Ventas: {int(fk_pro_bad.sum())} registros con producto_id sin match en dim_productos.")

    # ---------- Resultado ----------
    if errores == 0:
        logger.info("✅ Validaciones PASADAS (0 errores).")
        print(f"OK - Validaciones PASADAS. Log: {LOG_FILE}")
    else:
        _error_and_raise(errores)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Fallo en validaciones")
        raise
