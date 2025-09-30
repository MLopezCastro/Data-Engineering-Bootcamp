# columna_ingresos.py
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
IN_OUT = ROOT / "outputs" / "ventas_home_limpio.csv"  # viene del Paso 2 y se actualiza acá

if not IN_OUT.exists():
    raise FileNotFoundError(f"No encuentro el archivo limpio del Paso 2: {IN_OUT}")

# Cargar robusto
try:
    df = pd.read_csv(IN_OUT, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(IN_OUT, encoding="latin-1")

# Asegurar tipos (por si el Paso 2 no forzó numéricos)
df["precio"] = pd.to_numeric(df["precio"], errors="coerce").fillna(0.0)
df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce").fillna(0).astype(int)

# PASO 3: crear ingresos = precio * cantidad
df["ingresos"] = df["precio"] * df["cantidad"]

# Guardar (sobrescribe el limpio con la nueva columna)
df.to_csv(IN_OUT, index=False, encoding="utf-8")

print("✅ Paso 3 OK — columna 'ingresos' creada")
print(f"Archivo actualizado: {IN_OUT}")
print(df.head(10).to_string(index=False))
