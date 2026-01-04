# pipeline/etl_clean.py
import os
from pathlib import Path
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
os.chdir(BASE)

RAW = BASE / "data" / "data_raw"
CLEAN = BASE / "data" / "data_clean"
CLEAN.mkdir(parents=True, exist_ok=True)

def clean_clientes():
    df = pd.read_csv(RAW / "clientes.csv")

    # Normalización básica
    df.columns = [c.strip() for c in df.columns]
    df["cliente_id"] = pd.to_numeric(df["cliente_id"], errors="coerce").astype("Int64")

    # fecha_alta a datetime (acepta varios formatos)
    df["fecha_alta"] = pd.to_datetime(df["fecha_alta"], errors="coerce")

    # Reglas mínimas: cliente_id no puede ser nulo
    df = df.dropna(subset=["cliente_id"])

    # Opcional: quitar duplicados por id
    df = df.drop_duplicates(subset=["cliente_id"], keep="last")

    df.to_csv(CLEAN / "clientes_clean.csv", index=False)

def clean_productos():
    df = pd.read_csv(RAW / "productos.csv")
    df.columns = [c.strip() for c in df.columns]
    df["producto_id"] = pd.to_numeric(df["producto_id"], errors="coerce").astype("Int64")
    df["precio"] = pd.to_numeric(df["precio"], errors="coerce")

    df = df.dropna(subset=["producto_id"])
    df = df.drop_duplicates(subset=["producto_id"], keep="last")

    df.to_csv(CLEAN / "productos_clean.csv", index=False)

def clean_ventas():
    df = pd.read_csv(RAW / "ventas.csv")
    df.columns = [c.strip() for c in df.columns]

    df["venta_id"] = pd.to_numeric(df["venta_id"], errors="coerce").astype("Int64")
    df["cliente_id"] = pd.to_numeric(df["cliente_id"], errors="coerce").astype("Int64")
    df["producto_id"] = pd.to_numeric(df["producto_id"], errors="coerce").astype("Int64")

    df["fecha_venta"] = pd.to_datetime(df["fecha_venta"], errors="coerce")
    df["cantidad"] = pd.to_numeric(df["cantidad"], errors="coerce")
    df["descuento"] = pd.to_numeric(df["descuento"], errors="coerce").fillna(0)

    # Reglas mínimas (campos críticos)
    df = df.dropna(subset=["venta_id", "cliente_id", "producto_id", "fecha_venta", "cantidad"])
    df = df[df["cantidad"] > 0]
    df = df[df["descuento"].between(0, 100)]

    df = df.drop_duplicates(subset=["venta_id"], keep="last")

    df.to_csv(CLEAN / "ventas_clean.csv", index=False)

def main():
    clean_clientes()
    clean_productos()
    clean_ventas()
    print("OK - ETL CLEAN generado en data/data_clean/")

if __name__ == "__main__":
    main()
