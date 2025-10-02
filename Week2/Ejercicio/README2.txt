# README 2 — Cómo correr el pipeline (desde cero, rápido)

> Proyecto: `Week2/Ejercicio` (Windows + VS Code + PowerShell)

## 1) Seleccionar e **activar** el venv

1. Abrí la carpeta `Week2/Ejercicio` en VS Code.
2. `Ctrl + Shift + P` → **Python: Select Interpreter** → elegí `.\.venv\Scripts\python.exe`.
3. **Terminal nueva**: `Ctrl + ñ`. Debe verse `(.venv)` al inicio del prompt.

   * Si no aparece, activalo manual:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
   .\.venv\Scripts\Activate.ps1
   ```

## 2) Instalar/actualizar dependencias

Con `(.venv)` activo y **parado en `Ejercicio`**:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> Si no existe `requirements.txt`, crealo con:

```
pandas>=2.2,<3
requests>=2.33,<3
```

Verificación rápida:

```powershell
python -c "import pandas, numpy; print('OK', pandas.__version__, numpy.__version__)"
```

## 3) Orden de ejecución de los scripts

Ejecutar **en este orden** (cada línea por separado):

```powershell
python .\cargar_csv.py            # toma data cruda / valida existencia
python .\limpiar.py               # genera outputs\ventas_home_limpio.csv
python .\agrupar_resumen.py       # genera outputs\resumen_ventas.csv
python .\columna_ingresos.py      # agrega métricas/ingresos al resumen
python .\stock_json.py            # genera/actualiza outputs\stock.json
python .\todos_api.py             # genera outputs\todos_completados.json
```

## 4) Atajos útiles (opcional)

* **Run all**: crear `run_all.ps1` y pegar:

  ```powershell
  .\.venv\Scripts\activate
  pip install -r requirements.txt
  python .\cargar_csv.py
  python .\limpiar.py
  python .\agrupar_resumen.py
  python .\columna_ingresos.py
  python .\stock_json.py
  python .\todos_api.py
  ```

  Ejecutar:

  ```powershell
  powershell -ExecutionPolicy Bypass -File .\run_all.ps1
  ```

## 5) Troubleshooting ultra-rápido

* No aparece `(.venv)`: terminal nueva o `.\.venv\Scripts\Activate.ps1`.
* Error con **numpy/pandas**: evitar carpetas/archivos llamados `numpy` o `pandas` en el proyecto.
* Siempre correr desde la carpeta `Ejercicio` (donde están los `.py`).
