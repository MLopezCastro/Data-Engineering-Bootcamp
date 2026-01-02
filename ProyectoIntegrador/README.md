
---

# 📦 Proyecto Integrador – Bootcamp Data Engineering

**Empresa simulada:** *VentasOnline SA*

## 🎯 Objetivo del proyecto

Diseñar e implementar un **pipeline de datos end-to-end** que procese archivos CSV crudos de clientes, productos y ventas, aplique limpieza, transformaciones, validaciones de calidad y automatización, y genere datasets listos para análisis.

El proyecto simula el trabajo real de un **Data Engineer junior**, desde la ingesta hasta la confiabilidad del output.

---

## 📂 Datasets de entrada (crudos)

Ubicación: `data/data_raw/`

* `clientes.csv`
* `productos.csv`
* `ventas.csv`

Los archivos pueden contener errores reales como:

* valores nulos
* formatos inconsistentes
* duplicados
* tipos incorrectos

---

## 🔄 Arquitectura del pipeline (visión general)

```
[CSV crudos]
      ↓
[Limpieza y normalización con pandas]
      ↓
[Datos limpios (data_clean)]
      ↓
[Transformaciones SQL + DuckDB]
      ↓
[Modelo estrella (fact + dims)]
      ↓
[Validaciones de calidad (quality gate)]
      ↓
[Outputs finales + logs]
      ↓
[Ejecución automatizada]
```

---

## 🟦 Semana 1 – Diseño del pipeline

* Definición del flujo completo de datos
* Identificación de etapas: ingesta, limpieza, transformación, validación, output
* Selección de herramientas (Python, pandas, DuckDB)

### Supuestos del sistema

* Los archivos CSV llegan una vez por día (6 AM)
* Pueden venir vacíos, duplicados o con errores de formato
* Los IDs de cliente y producto son únicos y sirven como claves
* El negocio necesita reportes diarios de ingresos y ventas por producto
* Los datos históricos no se reescriben

---

## 🟦 Semana 2 – Limpieza de datos con pandas

Se implementó un proceso de limpieza para cada dataset:

### Principales tareas

* Normalización de texto
* Parseo robusto de fechas y precios
* Conversión de tipos
* Detección de duplicados
* Separación de registros inválidos

### Outputs

* `data/data_clean/clientes_clean.csv`
* `data/data_clean/productos_clean.csv`
* `data/data_clean/ventas_clean.csv`
* Archivos de errores (`outputs/errores_*.csv`)
* `outputs/reporte_calidad.csv`

---

## 🟦 Semana 3 – Transformaciones con SQL (DuckDB)

Se utilizaron consultas SQL ejecutadas con **DuckDB** para:

* Leer directamente archivos CSV limpios
* Unir ventas con productos y clientes
* Calcular métricas como ingresos
* Generar tablas intermedias para análisis

Scripts ubicados en:

```
duckdb_queries/
```

---

## 🟦 Semana 4 – Modelado de datos (Esquema Estrella)

Se implementó un **modelo analítico en estrella**:

### Tablas creadas

* `fact_ventas`
* `dim_clientes`
* `dim_productos`
* `dim_fechas`

El modelo permite analizar:

* ingresos por producto y categoría
* ventas por cliente o ciudad
* descuentos y volúmenes

Script principal:

```
sql_queries/semana4_modelo_estrella.sql
```

---

## 🟦 Semana 5 – Automatización del pipeline

Se creó un **script orquestador** que ejecuta todo el flujo de forma automática.

### Script principal

```
run_pipeline.py
```

### Funciones

* Ejecuta transformaciones SQL (Semana 3)
* Ejecuta el modelo estrella (Semana 4)
* Ejecuta validaciones de calidad (Semana 6)
* Registra logs de ejecución
* Puede ejecutarse manualmente o mediante Task Scheduler

### Logs

* `outputs/run_pipeline.log`

---

## 🟦 Semana 6 – Validación de calidad de datos

Se implementó una etapa de **validación automática** como *quality gate*.

### Script

```
pipeline/validaciones.py
```

### Validaciones realizadas

* Valores nulos en campos críticos
* Duplicados en claves
* Rangos inválidos (cantidad ≤ 0, descuento fuera de 0–100)
* Fechas futuras
* Consistencia general de datos

### Comportamiento

* Si las validaciones fallan, el pipeline se detiene
* Los errores quedan registrados en logs y archivos CSV

### Outputs

* `outputs/validaciones.log`
* `outputs/reporte_calidad.csv`
* `outputs/errores_clientes.csv`
* `outputs/errores_productos.csv`
* `outputs/errores_ventas.csv`

---

## ▶️ Cómo ejecutar el proyecto

```powershell
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar pipeline completo
python run_pipeline.py
```

---

## 📁 Estructura del repositorio

```
ProyectoIntegrador/
├─ data/
│  ├─ data_raw/
│  └─ data_clean/
├─ pipeline/
│  ├─ generar_raw.py
│  ├─ etl_ingesta.py
│  └─ validaciones.py
├─ duckdb_queries/
├─ sql_queries/
├─ outputs/
├─ run_pipeline.py
└─ README.md
```

---

## 🔎 Extensión opcional – SQL Server

Como ejercicio adicional, se cargaron los datos limpios en **SQL Server** utilizando `BULK INSERT`, se definieron llaves foráneas y se resolvieron consultas analíticas con CTEs.

Este paso no forma parte del pipeline principal del TP, pero demuestra capacidad de trabajo con motores de base de datos relacionales.

Scripts disponibles en:

```
sql_queries/
```

---

## ✅ Estado final

* Pipeline completo y funcional
* Automatizado
* Con validaciones de calidad
* Logs y trazabilidad
* Listo para análisis o BI

---

### 🧠 Conclusión

Este proyecto integra los conceptos centrales del bootcamp y replica un flujo real de ingeniería de datos, desde datos crudos hasta outputs confiables y automatizados.

---


