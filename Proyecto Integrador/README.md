Te entiendo Marcelo 😓.
El problema es este: en **Markdown**, cada vez que usamos comillas triples ``` o indentamos como código, GitHub lo muestra como **bloques separados**.

Si vos querés que TODO tu README se vea como **un único bloque corrido, sin cortes de estilo**, la única forma es **escribirlo todo en texto plano** (sin backticks, sin bloques de código).

Acá te paso el `README.md` completo, armado en puro texto continuo. Si lo copiás así, en GitHub se va a ver todo junto, sin “bloques de código” partidos:

---

# 📦 Proyecto Integrador – Bootcamp Data Engineering

Empresa simulada: VentasOnline SA
Objetivo: construir un pipeline ETL que procese CSV crudos de clientes, productos y ventas, aplique limpieza, JOIN, validaciones y exporte un dataset listo para análisis.

---

## 📂 Dataset (crudo)

Ubicación: data/data_raw/

* clientes.csv
* productos.csv
* ventas.csv

---

## 🔄 Pipeline (diagrama simplificado)

clientes.csv  → Limpieza clientes  \
productos.csv → Limpieza productos  ---> JOIN ventas + productos + clientes → Validaciones de datos → Export CSV/Parquet → Automatizacion (Semana 5)
ventas.csv    → Limpieza ventas   /

---

## 🔹 Actividad 3 – Supuestos del sistema

Como Data Engineer único en la empresa, defino los siguientes supuestos:

* Los archivos CSV llegan una vez por día por correo (6 AM).
* Los archivos pueden venir vacíos, duplicados o con errores de formato.
* Los IDs de cliente y producto son únicos y sirven como claves de unión.
* Si un cliente tiene email inválido, igual se carga pero se marca como pendiente.
* El negocio necesita reportes diarios de ingresos y ventas por producto.
* Los archivos históricos no cambian: una vez cargados, se consideran fijos y no se reescriben.

---

## 📸 Flujo detallado (ASCII)

[CSV crudos] → [Lectura con pandas] → [Limpieza + Validaciones] → [JOIN clientes + productos + ventas] → [Parquet/CSV limpio] → [Dashboard BI]

---

## ✅ Checklist de avance

* Lectura de CSV (pandas)
* Limpieza por dataset (tipos, fechas, precios, nulos)
* JOIN final (ventas + productos + clientes)
* Validaciones (nulos, duplicados, FKs, rangos)
* Export limpio (data/clean/ en CSV o Parquet)
* Automatización (cron/Step Functions) – Semana 5

---

## 🚀 Cómo correr:

1. Crear entorno virtual: python -m venv venv
2. Activar: venv\Scripts\activate
3. Instalar dependencias: pip install -r requirements.txt
4. Ejecutar: python pipeline/etl_local.py

---

