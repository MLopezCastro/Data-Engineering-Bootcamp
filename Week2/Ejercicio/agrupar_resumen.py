# agrupar_resumen.py
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
INP  = ROOT / "outputs" / "ventas_home_limpio.csv"   # viene de los pasos 2 y 3
OUT  = ROOT / "outputs" / "resumen_ventas.csv"

if not INP.exists():
    raise FileNotFoundError(f"Falta el archivo limpio con 'ingresos': {INP}")

# Cargar
try:
    df = pd.read_csv(INP, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(INP, encoding="latin-1")

# Si por algún motivo no existe 'ingresos', lo calculo en memoria (sin modificar el archivo)
if "ingresos" not in df.columns:
    df["precio"] = pd.to_numeric(df.get("precio"), errors="coerce").fillna(0.0)
    df["cantidad"] = pd.to_numeric(df.get("cantidad"), errors="coerce").fillna(0).astype(int)
    df["ingresos"] = df["precio"] * df["cantidad"]

# Paso 4: agrupar por categoría
resumen = (
    df.groupby("categoria", dropna=False)
      .agg(
          ingresos_total=("ingresos", "sum"),
          productos_distintos=("producto", "nunique")
      )
      .reset_index()
      .sort_values("ingresos_total", ascending=False)
)

# Paso 5: guardar
OUT.parent.mkdir(parents=True, exist_ok=True)
resumen.to_csv(OUT, index=False, encoding="utf-8")
print(f"✅ Resumen generado: {OUT}")
print(resumen)
