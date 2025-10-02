# 📦 Proyecto Integrador – Bootcamp Data Engineering

Empresa simulada: **VentasOnline SA**.  
Objetivo: construir un **pipeline ETL** que procese CSV crudos de **clientes**, **productos** y **ventas**, aplique **limpieza**, **JOIN**, **validaciones** y exporte un dataset **listo para análisis**.

---

## 📂 Dataset (crudo)
Ubicación: `data/data_raw/`
- `clientes.csv`
- `productos.csv`
- `ventas.csv`

---

## 🔄 Pipeline (diagrama simplificado)

```mermaid
flowchart TB
    A[clientes.csv] --> A1[Limpieza clientes]
    B[productos.csv] --> B1[Limpieza productos]
    C[ventas.csv] --> C1[Limpieza ventas]
    A1 --> J[JOIN ventas + productos + clientes]
    B1 --> J
    C1 --> J
    J --> Q[Validaciones de datos]
    Q --> O[Export CSV o Parquet]
    O --> AUTO[Automatizacion - Semana 5]


