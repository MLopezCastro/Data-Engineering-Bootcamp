# 📦 Proyecto Integrador – Bootcamp Data Engineering

Este proyecto simula el trabajo de un Data Engineer en una empresa de e-commerce (*VentasOnline SA*).  
El objetivo es construir un **pipeline ETL** que procese datos crudos de clientes, productos y ventas, y los deje listos para análisis.

---

## 📂 Dataset
Archivos CSV crudos ubicados en `data/data_raw/`:
- `clientes.csv`
- `productos.csv`
- `ventas.csv`

---

## 🔄 Pipeline (diagrama)

```mermaid
flowchart LR
  %% --- Fuentes ---
  subgraph S[Fuentes (CSV)]
    C1([clientes.csv])
    P1([productos.csv])
    V1([ventas.csv])
  end

  %% --- Limpieza ---
  subgraph T[Transformación / Limpieza]
    C2[Limpiar clientes<br/>(trim, email, fecha)]
    P2[Limpiar productos<br/>(precio → número, categoría)]
    V2[Limpiar ventas<br/>(cantidad/desc, fecha)]
  end

  %% --- Integración / Calidad / Salida ---
  J[JOIN<br/>ventas + productos + clientes]
  Q[Validaciones de calidad<br/>(nulos, duplicados, FKs, rangos)]
  O[[Export limpio<br/>(CSV / Parquet)]]
  A{{Automatización<br/>(Semana 5)}}

  %% Flujos
  C1 --> C2
  P1 --> P2
  V1 --> V2
  C2 --> J
  P2 --> J
  V2 --> J
  J  --> Q
  Q  --> O
  O  -.-> A
