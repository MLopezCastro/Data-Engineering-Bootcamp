# todos_api.py
from pathlib import Path
import json
import requests

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_PATH = OUT_DIR / "todos_completados.json"

URL = "https://jsonplaceholder.typicode.com/todos"  # endpoint público

# 1) Hacer la solicitud HTTP GET
resp = requests.get(URL, timeout=30)  # timeout por si no responde
resp.raise_for_status()               # si no es 200 OK, lanza error

# 2) Convertir la respuesta JSON (texto) a objetos Python (lista/dict)
todos = resp.json()                   # ahora es una lista de dicts

# 3) Filtrar solo los completados
completados = [t for t in todos if t.get("completed") is True]

# 4) Guardar el resultado en disco como JSON bonito
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(completados, f, ensure_ascii=False, indent=2)

print(f"OK → completados: {len(completados)}")
print(f"Guardado en: {OUT_PATH}")
