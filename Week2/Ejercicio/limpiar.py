# limpiar.py
from pathlib import Path
import pandas as pd
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
CSV_IN  = ROOT / "data" / "ventas_home.csv"
CSV_OUT = ROOT / "outputs" / "ventas_home_limpio.csv"
CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

# 1) Cargar CSV
try:
    df = pd.read_csv(CSV_IN, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(CSV_IN, encoding="latin-1")

# 2) Limpiar
# 2.1 Quitar espacios extra en producto
df["producto"] = (
    df["producto"].astype(str)
      .str.replace(r"\s+", " ", regex=True)
      .str.strip()
)

# 2.2 Uniformar categoria (Fruta, Electrónica, Indumentaria)
def sin_tildes(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", str(s)) if not unicodedata.combining(c))

cat_norm = (df["categoria"].astype(str)
            .str.strip().str.lower()
            .map(sin_tildes))

mapa = {
    "fruta": "Fruta",
    "frutas": "Fruta",
    "electronica": "Electrónica",
    "electronic": "Electrónica",
    "indumentaria": "Indumentaria",
}
df["categoria"] = cat_norm.map(lambda x: mapa.get(x, "Otros"))

# 2.3 Reemplazar precios en texto por números
def to_number(x):
    if pd.isna(x): return pd.NA
    s = str(x).strip().replace("$", "").replace("USD", "").replace("ARS", "")
    s = re.sub(r"[.\s](?=\d{3}(?:\D|$))", "", s)  # quita separadores de miles
    s = s.replace(",", ".")                        # coma decimal -> punto
    try: return float(s)
    except: return pd.NA

df["precio"] = df["precio"].map(to_number)

# 2.4 Rellenar nulos en cantidad con 0
df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)

# Guardar dataset limpio SIN ingresos
df.to_csv(CSV_OUT, index=False, encoding="utf-8")
print(f"✅ Archivo limpio (sin ingresos) guardado en: {CSV_OUT}")
