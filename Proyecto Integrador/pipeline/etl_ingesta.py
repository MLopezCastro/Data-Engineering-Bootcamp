from pathlib import Path
import re
import pandas as pd
import numpy as np

# === Rutas ===
ROOT = Path(__file__).resolve().parents[1]
RAW  = ROOT / "data" / "data_raw"
CLEAN = ROOT / "data" / "clean"
OUT = ROOT / "outputs"
CLEAN.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

# ---------- Helpers ----------
def parse_date_any(s):
    """Parsea múltiples formatos (yyyy-mm-dd, dd/mm/yyyy, yyyy/mm/dd, compactos, ISO)."""
    return pd.to_datetime(s, errors="coerce", dayfirst=True, utc=False, format=None)

_price_re = re.compile(r"[^\d,.\-]")
def parse_price(x):
    """Convierte precios con símbolos, miles y coma decimal a float. Maneja 'NaN','s/d','-'."""
    if pd.isna(x):
        return np.nan
    s = str(x).strip()
    if s.lower() in {"nan", "s/d", "sd", "-", ""}:
        return np.nan
    s = _price_re.sub("", s)                       # quita $ y letras
    # Si hay coma y punto, asumimos: punto = miles, coma = decimal (formato EU)
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    # Si hay solo coma, asumimos coma decimal
    elif "," in s and "." not in s:
        s = s.replace(",", ".")
    try:
        val = float(s)
    except ValueError:
        return np.nan
    # Precios negativos inválidos -> NaN
    return val if val >= 0 else np.nan

def normalize_city(x):
    if pd.isna(x): return x
    s = str(x).strip()
    m = s.lower()
    mapping = {
        "caba": "CABA", "capital federal": "CABA", "capital federal ": "CABA",
        "cordoba": "Córdoba", "córdoba": "Córdoba",
        "rosario": "Rosario", "mendoza": "Mendoza", "salta": "Salta"
    }
    return mapping.get(m, s.title())

def is_valid_email(e):
    if pd.isna(e): return False
    s = str(e).strip()
    # aceptamos +tag y unicode básico en local-part; rechazamos cosas obvias
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", s))

# ---------- CLIENTES ----------
cli = pd.read_csv(RAW / "clientes.csv", dtype=str)
cli.columns = [c.strip().lower() for c in cli.columns]

# trims
for c in ["nombre","email","ciudad","fecha_alta"]:
    if c in cli: cli[c] = cli[c].astype(str).str.strip()

# normalizaciones
cli["email_limpio"] = cli["email"].str.strip().str.lower()
cli["email_valido"] = cli["email_limpio"].apply(is_valid_email)
cli["ciudad"] = cli["ciudad"].apply(normalize_city)
cli["fecha_alta_parsed"] = parse_date_any(cli["fecha_alta"])

# tipos
cli["cliente_id"] = pd.to_numeric(cli["cliente_id"], errors="coerce").astype("Int64")

# duplicados exactos y por clave
cli["_dup_full"] = cli.duplicated(keep=False)
cli["_dup_cliente_id"] = cli.duplicated(subset=["cliente_id"], keep=False)

# errores fila a fila
cli_err = cli[
    (~cli["email_valido"]) | (cli["cliente_id"].isna()) | (cli["fecha_alta_parsed"].isna())
].copy()
cli_ok = cli[~cli.index.isin(cli_err.index)].copy()

# salida limpia (columnas finales)
cli_ok_final = cli_ok[["cliente_id","nombre","email_limpio","ciudad","fecha_alta_parsed"]].rename(
    columns={"email_limpio":"email","fecha_alta_parsed":"fecha_alta"}
)

# ---------- PRODUCTOS ----------
prod = pd.read_csv(RAW / "productos.csv", dtype=str)
prod.columns = [c.strip().lower() for c in prod.columns]
prod["producto_id"] = pd.to_numeric(prod["producto_id"], errors="coerce").astype("Int64")
prod["nombre"] = prod["nombre"].astype(str).str.strip()
prod["categoria"] = prod["categoria"].astype(str).str.strip().str.title()  # "Smart Home", "Oficina"
prod["precio_raw"] = prod["precio"]
prod["precio"] = prod["precio"].apply(parse_price)

prod["_dup_full"] = prod.duplicated(keep=False)
prod["_dup_producto_id"] = prod.duplicated(subset=["producto_id"], keep=False)
prod["precio_invalido"] = prod["precio"].isna()

prod_err = prod[prod["producto_id"].isna() | prod["precio_invalido"] | prod["_dup_producto_id"]].copy()
# para duplicados por producto_id, nos quedamos con el último registro válido
prod_sorted = prod.sort_values(["producto_id","precio_invalido"])
prod_ok = prod_sorted.drop_duplicates(subset=["producto_id"], keep="first")
prod_ok_final = prod_ok[["producto_id","nombre","categoria","precio"]]

# ---------- VENTAS ----------
ven = pd.read_csv(RAW / "ventas.csv", dtype=str)
ven.columns = [c.strip().lower() for c in ven.columns]
for c in ["venta_id","cliente_id","producto_id","cantidad","descuento"]:
    ven[c] = pd.to_numeric(ven[c], errors="coerce")

ven["fecha_venta_parsed"] = parse_date_any(ven["fecha_venta"])

# reglas
ven["cantidad_valida"] = ven["cantidad"].notna() & (ven["cantidad"] > 0)
ven["desc_valido"] = ven["descuento"].notna() & (ven["descuento"].between(0,100))
ven["_dup_venta"] = ven.duplicated(subset=["venta_id"], keep=False)

# FK checks (contra OK finales de clientes y productos)
cli_ids = set(cli_ok_final["cliente_id"].dropna().astype(int))
prod_ids = set(prod_ok_final["producto_id"].dropna().astype(int))
ven["fk_cliente_ok"] = ven["cliente_id"].apply(lambda x: int(x) in cli_ids if not pd.isna(x) else False)
ven["fk_producto_ok"] = ven["producto_id"].apply(lambda x: int(x) in prod_ids if not pd.isna(x) else False)

ven_err = ven[
    ven["_dup_venta"] |
    ven["fecha_venta_parsed"].isna() |
    (~ven["cantidad_valida"]) |
    (~ven["desc_valido"]) |
    (~ven["fk_cliente_ok"]) |
    (~ven["fk_producto_ok"])
].copy()

ven_ok = ven[~ven.index.isin(ven_err.index)].copy()
ven_ok_final = ven_ok[["venta_id","cliente_id","producto_id","fecha_venta_parsed","cantidad","descuento"]].rename(
    columns={"fecha_venta_parsed":"fecha_venta"}
)

# ---------- Exports ----------
cli_ok_final.to_csv(CLEAN / "clientes_clean.csv", index=False)
prod_ok_final.to_csv(CLEAN / "productos_clean.csv", index=False)
ven_ok_final.to_csv(CLEAN / "ventas_clean.csv", index=False)

# errores detallados
cli_err.to_csv(OUT / "errores_clientes.csv", index=False)
prod_err.to_csv(OUT / "errores_productos.csv", index=False)
ven_err.to_csv(OUT / "errores_ventas.csv", index=False)

# resumen de calidad
quality = pd.DataFrame([
    {"tabla":"clientes","filas_raw":len(cli),"filas_ok":len(cli_ok_final),"errores":len(cli_err)},
    {"tabla":"productos","filas_raw":len(prod),"filas_ok":len(prod_ok_final),"errores":len(prod_err)},
    {"tabla":"ventas","filas_raw":len(ven),"filas_ok":len(ven_ok_final),"errores":len(ven_err)},
])
quality.to_csv(OUT / "reporte_calidad.csv", index=False)

print("OK - Limpios en data/clean, errores en outputs/, resumen en outputs/reporte_calidad.csv")
