# pipeline/generar_raw.py
# Genera CSV sintéticos en data/data_raw/ con 10k+ clientes, 500+ productos y 200k ventas.
# Luego corré tu etl_ingesta.py para producir data_clean/*

from pathlib import Path
import random, math, csv
from datetime import datetime, timedelta

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "data_raw"
RAW.mkdir(parents=True, exist_ok=True)

# ---------- Parámetros (ajustá si querés) ----------
N_CLIENTES  = 10_000
N_PRODUCTOS = 500
N_VENTAS    = 200_000
SEED        = 42

random.seed(SEED)

# ---------- Catálogos básicos ----------
CATS = ["Gaming","Oficina","Audio","Accesorios","Smart Home","Redes","Computación","Video"]
REGIONES = ["CABA","Córdoba","Rosario","Mendoza","Salta","Tucumán","Neuquén","Santa Fe","Chubut","San Luis"]

def rand_date(start="2023-01-01", end="2023-12-31"):
    d0 = datetime.fromisoformat(start)
    d1 = datetime.fromisoformat(end)
    delta = (d1 - d0).days
    return (d0 + timedelta(days=random.randint(0, delta))).date().isoformat()

def precio_base_por_cat(cat):
    bases = {
        "Gaming": (20000, 350000),
        "Oficina": (5000, 120000),
        "Audio": (4000, 180000),
        "Accesorios": (1500, 40000),
        "Smart Home": (6000, 200000),
        "Redes": (5000, 180000),
        "Computación": (12000, 800000),
        "Video": (10000, 600000),
    }
    lo, hi = bases[cat]
    # distrib. log-normal para tener colas largas
    r = random.random()
    val = lo * math.exp(r * math.log(hi / lo))
    # redondeo a .00
    return round(val / 10) * 10

# ---------- 1) productos.csv ----------
prod_path = RAW / "productos.csv"
with prod_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["producto_id","nombre","categoria","precio"])
    for i in range(1, N_PRODUCTOS+1):
        cat = random.choice(CATS)
        nombre = f"Prod {i:04d}"
        precio = precio_base_por_cat(cat)
        w.writerow([100 + i, nombre, cat, f"{precio:.2f}"])

# ---------- 2) clientes.csv ----------
def nombre_fake(i):
    return f"Cliente{i:05d}"

cli_path = RAW / "clientes.csv"
with cli_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["cliente_id","nombre","email","ciudad","fecha_alta"])
    for i in range(1, N_CLIENTES+1):
        nom = nombre_fake(i)
        email = f"{nom.lower()}@example.com"
        ciudad = random.choice(REGIONES)
        alta = rand_date("2020-01-01","2023-12-31")
        w.writerow([i, nom, email, ciudad, alta])

# ---------- 3) ventas.csv ----------
ven_path = RAW / "ventas.csv"
with ven_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["venta_id","cliente_id","producto_id","fecha_venta","cantidad","descuento"])
    for i in range(1, N_VENTAS+1):
        cliente_id  = random.randint(1, N_CLIENTES)
        producto_id = 100 + random.randint(1, N_PRODUCTOS)
        fecha = rand_date("2023-01-01","2023-12-31")
        # cantidades con bias a 1–3
        cantidad = random.choices([1,2,3,4,5],[0.45,0.25,0.18,0.08,0.04])[0]
        # descuento 0–20% con mayoría en 0–5
        descuento = random.choices([0,2,5,10,15,20],[0.55,0.15,0.15,0.10,0.04,0.01])[0]
        w.writerow([i, cliente_id, producto_id, fecha, cantidad, descuento])

print("OK - Generados data_raw/productos.csv, clientes.csv y ventas.csv")
