# Proyecto: 5 Fuentes y Obtención de Datos

Este repositorio contiene el desarrollo del proyecto de análisis y visualización de fuentes de datos económicas y sociales en Sudamérica.  
El objetivo es integrar y documentar indicadores provenientes de organismos internacionales y regionales, garantizando la reproducibilidad del proceso.

## 📂 Estructura del repositorio
data_raw/  → Archivos de datos y gráficos generados

             desde los archivos resultado de las Api o web scraping hasta la generación de archivos resumen
             la subcarpeta \itbaro, es donde se descomprime el archivo latinobarometro_2024.zip
             
bcb.py     → Información del Banco Central de Brasil 

bcc.py     → Información del Banco Central de Colombia

fmi.py     → Información del Fondo monetario internacional

lbr.py     → Descargar el archivo Zip y extraer los archivos del Latinobarómetro, este debe ser ejecutado primero.
lbr2.py    → Trabaja con el archivo interno, depura y crea el archivo final de Latinobarómetro.

wb.py      → Información del Banco Mundial

clean_union.py   → Limpieza, estrucuturación y unificación de datasets en uno solo

resumen.py       → Generación de resumen estadístico y gráficos

README.md        → Presentación del proyecto


## ✅ Verificación de ejecución

Los scripts fueron ejecutados localmente en Visual Studio Code con Python 3.12.  
Los resultados generados se encuentran en la carpeta `data_raw/`, incluyendo:

- `grafico_conteo_fuentes.png` → gráfico de cantidad de registros por fuente  
- `grafico_proporcion_fuentes.png` → gráfico de proporción de registros  
- `resumen_estadistico.csv` → resumen estadístico del dataset unificado  

Para reproducir el análisis:
```bash
pip install -r requirements.txt
python resumen.py

Cada uno de los programas PY corren por separado, al final se debe correr el programa   

      clean_union.py que genera el archivo data_raw\union_final.csv

Después para generar los gráficos y tablas de resultado se ejecuta el programa
      
      resumen.py
