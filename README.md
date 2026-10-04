Sistema de Persistencia del TFM 100preOriginales

Este repositorio contiene el desarrollo ténico del sistema de persistencia. Incluye el modelo fí­sico en PostgreSQL, los datasets iniciales, los scripts de ingesta de datos externos y la documentación necesaria para reproducir el entorno en local.
# 🏗️ **1. Arquitectura General del Proceso de Ingestión información automotriz**

Este proyecto integra dos fuentes principales:

1. **Boletines de ventas de vehículos (AEADE)**  
   - Publicados en formato PDF  
   - Contienen tablas de ventas por marca y año  
   - Requieren scraping, descarga, extracción y normalización

2. **Market Review (Power BI)**  
   - Sistema interno con datos de inventario, repuestos, rotación y precios  
   - Exportado desde Power BI en formato CSV  
   - Requiere limpieza, estandarización y carga en PostgreSQL

Ambas fuentes se integran en un **pipeline ETL** que produce un dataset consolidado para análisis predictivo.

---

# 🚗 **2. Ingestión de Boletines AEADE (Web Scraping + PDF Parsing)**

## **2.1. Obtención de enlaces de boletines**

Los boletines se encuentran en:

```
https://www.aeade.net/boletines-de-prensa-venta-de-vehiculos/
```

### **Proceso:**
- Se utiliza **Selenium** para navegar la página y extraer enlaces PDF.
- Se filtran enlaces que contienen `sdm_process_download`.
- Se descargan automáticamente todos los boletines disponibles.

### **Script principal:**
```
proyecto/ingestion/web_scraping/import_aeade.py
```

---

## **2.2. Descarga de PDFs**

Cada enlace se procesa con:

- `requests.get()`  
- Validación de tipo MIME (`application/pdf`)  
- Guardado en carpeta local:

```
proyecto/ingestion/web_scraping/boletines_aeade/
```

---

## **2.3. Extracción de tablas desde PDF**

Se utiliza:

- **tabula-py**  
- **camelot**  
- **pandas**

### Objetivo:
Convertir cada tabla del boletín en un CSV estructurado.

Salida:

```
boletines_aeade/tablas_aeade/
```

---

## **2.4. Normalización de tablas**

Se aplica:

- Limpieza de nombres de marcas  
- Conversión de columnas numéricas  
- Eliminación de caracteres especiales  
- Unificación de estructura entre boletines

Script:

```
limpieza_aeade.py
```

---

## **2.5. Generación del dataset maestro AEADE**

Se consolidan todas las tablas en:

```
dataset_maestro_aeade_limpio.csv
```

Incluye:

- marca  
- año  
- unidades  
- origen_pdf  
- número de tabla  

---

# 🔧 **3. Ingestión de Market Review desde Power BI**

## **3.1. Exportación desde Power BI**

Desde el panel de Power BI se exportan:

- Inventario  
- Repuestos  
- Rotación  
- Precios  
- Equivalencias  

Formato: **CSV**

Archivos típicos:

```
Orgu.csv
Orgu - Original.csv
precios_partsgeek.csv
```

---

## **3.2. Limpieza y normalización**

Se aplican rutinas Python:

- Eliminación de duplicados  
- Normalización de códigos de repuestos  
- Conversión de precios  
- Unificación de marcas  
- Integración con precios externos (PartsGeek)

Script:

```
cargar_powerbi_market_review.py
```

---

## **3.3. Generación del dataset Market Review**

Salida:

```
market_review_limpio.csv
```

Incluye:

- marca  
- año  
- repuestos  
- rotación  
- equivalencias  
- precios comparativos  

---

# 🗄️ **4. Carga en PostgreSQL (Persistencia)**

## **4.1. Conexión a la base de datos**

```
host="localhost"
database="postgres"
user="postgres"
password="A"
```

---

## **4.2. Inserción en tablas del esquema `spo`**

Tablas:

- `spo.aeade_boletines`  
- `spo.aeade_boletines_json`  
- `spo.market_review`  
- `spo.precio_comparativo`  
- `spo.inveec`  
- `spo.factura_cabecera`  
- `spo.factura_detalle`  

Scripts:

```
graba_json_en_bdd.py
graba_en_bdd.py
```

---

# 🔗 **5. Integración de ambas fuentes**

Se genera el dataset final:

```
df_total
```

Con columnas:

- marca  
- año  
- unidades (AEADE)  
- repuestos (Market Review)  
- crec_vehiculos  
- crec_repuestos  
- ratio_repuestos  
- clase (multiclase)  
- PC1, PC2 (PCA)  

Este dataset alimenta:

- modelos supervisados  
- modelos no supervisados  
- proyecciones  
- análisis de market share  

---

# 📊 **6. Estructura del repositorio**

```
TFM_Persistencia_100preOriginales/
│
├── ingestion/
│   ├── web_scraping/
│   ├── powerbi/
│   └── limpieza/
│
├── database/
│   ├── scripts_sql/
│   └── carga/
│
├── notebooks/
│   ├── aeade_ingestion.ipynb
│   ├── aeade_marketreview.ipynb
│   ├── modelos_predictivos.ipynb
│   └── pca_cluster.ipynb
│
├── models/
│   ├── randomforest/
│   ├── prophet/
│   └── pca/
│
├── docs/
│   ├── metodologia.md
│   ├── conclusiones.md
│   ├── limitaciones.md
│   └── arquitectura.md
│
└── README.md
```

---

# 🏁 **7. Estado actual del pipeline**

✔ Scraping AEADE  
✔ Parsing PDF  
✔ Normalización  
✔ Exportación Power BI  
✔ Limpieza Market Review  
✔ Carga PostgreSQL  
✔ Integración AEADE + Market Review  
✔ Modelos predictivos  
✔ PCA  
✔ Market share  
✔ Conclusiones y limitaciones  
