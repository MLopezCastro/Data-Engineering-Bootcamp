# Semana 2 — Lectura y limpieza con pandas (README)

Este repo contiene **3 ejercicios** independientes que simulan tareas típicas de un mini-pipeline de datos. Se trabaja con **CSV**, **diccionarios/JSON** y **APIs públicas**.

---

## 📁 Estructura

```
.
├─ data/
│  └─ ventas_home.csv                # entrada cruda (Ej.1)
├─ outputs/
│  ├─ ventas_home_limpio.csv         # salida limpia (Paso 2 + Paso 3)
│  ├─ resumen_ventas.csv             # agrupado final (Paso 4–5)
│  ├─ stock.json                     # Ej.2
│  └─ todos_completados.json         # Ej.3
├─ cargar_csv.py                     # Ej.1 - Paso 1 (carga y preview)
├─ limpiar.py                        # Ej.1 - Paso 2 (limpieza S/ consigna)
├─ columna_ingresos.py               # Ej.1 - Paso 3 (ingresos)
├─ agrupar_resumen.py                # Ej.1 - Paso 4–5 (groupby + export)
├─ stock_json.py                     # Ej.2 - Diccionarios y JSON
└─ todos_api.py                      # Ej.3 - API pública
```

> **.gitignore:** ignora `.venv/`, `__pycache__/`, etc. (ya incluido).

---

## 🔧 Requisitos / Setup

```bash
# 1) Crear/activar venv (Windows PowerShell)
py -m venv .venv
.\.venv\Scripts\activate

# 2) Instalar dependencias
pip install pandas requests
```

---

## 🧪 Ejercicio 1 — CSV con pandas

**Objetivo:** cargar, limpiar, crear `ingresos`, agrupar y exportar.

### Paso 1 — Carga y exploración

Archivo: `cargar_csv.py`
Acciones: lee `data/ventas_home.csv`, muestra `head()` y `info()`.

```bash
python cargar_csv.py
```

### Paso 2 — Limpieza (sin ingresos)

Archivo: `limpiar.py`
Acciones según consigna:

* Quita espacios extra en `producto`.
* Uniforma `categoria` → {**Fruta**, **Electrónica**, **Indumentaria**} (resto → `Otros`).
* Convierte `precio` de texto a número (soporta `$`, miles y coma decimal).
* Rellena nulos en `cantidad` con `0`.

Salida: `outputs/ventas_home_limpio.csv`

```bash
python limpiar.py
```

> 💡 Si hay un **outlier** (ej. “Camisaco” con precio exagerado), la corrección debe aplicarse **en este paso** antes de guardar (p. ej., reemplazo por mediana de su categoría o exclusión).

### Paso 3 — Columna `ingresos`

Archivo: `columna_ingresos.py`
Acciones: abre `ventas_home_limpio.csv`, agrega `ingresos = precio * cantidad` y **guarda sobre el mismo archivo**.

```bash
python columna_ingresos.py
```

### Pasos 4–5 — Agrupar y exportar resumen

Archivo: `agrupar_resumen.py`
Acciones:

* Agrupa por `categoria`
* Suma `ingresos` y cuenta `productos_distintos`
* Exporta `outputs/resumen_ventas.csv`

```bash
python agrupar_resumen.py
```

**Entregables Ej.1**

* `outputs/ventas_home_limpio.csv`
* `outputs/resumen_ventas.csv`
* Scripts usados (`cargar_csv.py`, `limpiar.py`, `columna_ingresos.py`, `agrupar_resumen.py`)

---

## 📦 Ejercicio 2 — Diccionarios y JSON

**Objetivo:** practicar estructuras básicas y persistencia en JSON.

Archivo: `stock_json.py`
Acciones:

1. Crea un diccionario `stock`.
2. Agrega un producto.
3. Actualiza uno existente.
4. Elimina uno.
5. Guarda en `outputs/stock.json`.
6. Lee el JSON y lo imprime.

```bash
python stock_json.py
```

**Entregables Ej.2**

* `outputs/stock.json`
* `stock_json.py`

---

## 🌐 Ejercicio 3 — API pública (opcional)

**Objetivo:** consumir una API, filtrar y guardar JSON.

Archivo: `todos_api.py`
Fuente: `https://jsonplaceholder.typicode.com/todos`
Acciones:

1. Descarga todos los “todos”.
2. Filtra `completed == True`.
3. Guarda `outputs/todos_completados.json`.

```bash
pip install requests   # si no lo instalaste antes
python todos_api.py
```

**Entregables Ej.3**

* `outputs/todos_completados.json`
* `todos_api.py`

---

## ✅ Checklist de entrega

* [ ] `data/ventas_home.csv` (entrada cruda)
* [ ] `outputs/ventas_home_limpio.csv` (luego de limpieza + ingresos)
* [ ] `outputs/resumen_ventas.csv` (groupby final)
* [ ] `outputs/stock.json`
* [ ] `outputs/todos_completados.json` *(opcional)*
* [ ] Scripts `.py` correspondientes

---

## 🧭 Notas y decisiones

* **Codificación**: los scripts intentan **UTF-8** y, si falla, usan **latin-1**.
* **Normalización de categorías**: se remueven tildes y se mapea a un set fijo.
* **Precios en texto**: se eliminan símbolos y separadores de miles; coma → punto.
* **`cantidad` nula**: se reemplaza por `0` (según consigna).
* **Outliers**: se corrigen/excluyen en **Paso 2** si afectan los totales.

---

