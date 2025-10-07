# pipeline/generar_raw.py
from pathlib import Path
import random, math, csv, re, unicodedata
from datetime import datetime, timedelta
from faker import Faker

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "data_raw"
RAW.mkdir(parents=True, exist_ok=True)

# -------- Parámetros ----------
N_CLIENTES  = 10_000
N_PRODUCTOS = 500
N_VENTAS    = 200_000
SEED        = 42

random.seed(SEED)
fake = Faker("es_AR")
Faker.seed(SEED)

CATS = ["Gaming","Oficina","Audio","Accesorios","Smart Home","Redes","Computación","Video"]
REGIONES = ["CABA","Córdoba","Rosario","Mendoza","Salta","Tucumán","Neuquén","Santa Fe","Chubut","San Luis"]
DOMAINS = ["gmail.com","hotmail.com","outlook.com","yahoo.com"]

def rand_date(start="2023-01-01", end="2023-12-31"):
    d0 = datetime.fromisoformat(start); d1 = datetime.fromisoformat(end)
    return (d0 + (d1-d0)*random.random()).date().isoformat()

def precio_por_cat(cat):
    bases = {
        "Gaming": (20000, 350000), "Oficina": (5000, 120000),
        "Audio": (4000, 180000), "Accesorios": (1500, 40000),
        "Smart Home": (6000, 200000), "Redes": (5000, 180000),
        "Computación": (12000, 800000), "Video": (10000, 600000),
    }
    lo, hi = bases[cat]
    r = random.random()
    val = lo * math.exp(r * math.log(hi/lo))
    return round(val/10)*10

def slugify(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-zA-Z0-9]+','', s).lower()

# ---------- productos.csv ----------
with (RAW / "productos.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["producto_id","nombre","categoria","precio"])
    for i in range(1, N_PRODUCTOS+1):
        cat = random.choice(CATS)
        nombre = f"{cat} Item {i:04d}"
        precio = precio_por_cat(cat)
        w.writerow([100+i, nombre, cat, f"{precio:.2f}"])

# ---------- clientes.csv ----------
with (RAW / "clientes.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["cliente_id","nombre","email","ciudad","fecha_alta"])
    for i in range(1, N_CLIENTES+1):
        fn = fake.first_name(); ln = fake.last_name()
        nombre = f"{fn} {ln}"
        email = f"{slugify(fn)}.{slugify(ln)}+{i}@{random.choice(DOMAINS)}"
        ciudad = random.choice(REGIONES)
        alta = rand_date("2020-01-01","2023-12-31")
        w.writerow([i, nombre, email, ciudad, alta])

# ---------- ventas.csv ----------
with (RAW / "ventas.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f); w.writerow(["venta_id","cliente_id","producto_id","fecha_venta","cantidad","descuento"])
    for i in range(1, N_VENTAS+1):
        w.writerow([
            i,
            random.randint(1, N_CLIENTES),
            100 + random.randint(1, N_PRODUCTOS),
            rand_date("2023-01-01","2023-12-31"),
            random.choices([1,2,3,4,5],[0.45,0.25,0.18,0.08,0.04])[0],
            random.choices([0,2,5,10,15,20],[0.55,0.15,0.15,0.10,0.04,0.01])[0]
        ])

print("RAW OK: productos.csv, clientes.csv, ventas.csv con datos realistas.")
