# stock_json.py
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
JSON_PATH = OUT_DIR / "stock.json"

# 1) Diccionario inicial
stock = {
    "Manzana": 50,
    "Banana": 30,
    "Pera": 20
}

# 2) Agregar producto nuevo
stock["Naranja"] = 25

# 3) Actualizar cantidad existente (ej: +10 bananas)
stock["Banana"] = stock.get("Banana", 0) + 10  # 40

# 4) Eliminar un producto (ej: Pera)
stock.pop("Pera", None)

# 5) Guardar a JSON (pretty)
with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(stock, f, ensure_ascii=False, indent=2)

# 6) Leer y mostrar contenido
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

print("✅ stock.json generado en:", JSON_PATH)
print(json.dumps(data, ensure_ascii=False, indent=2))
