# cargar_csv.py
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
CSV = ROOT / "data" / "ventas_home.csv"

if not CSV.exists():
    raise FileNotFoundError(f"No encuentro el archivo: {CSV}")

# UTF-8 primero; si falla, probamos latin-1 (útil por tildes)
try:
    df = pd.read_csv(CSV, encoding="utf-8")
except UnicodeDecodeError:
    df = pd.read_csv(CSV, encoding="latin-1")

print("✅ Cargado OK")
print("Ruta:", CSV)
print("Shape:", df.shape)               # (filas, columnas)
print("\nPrimeras filas:")
print(df.head(10).to_string(index=False))
print("\nInfo del DataFrame:")
print(df.info())
