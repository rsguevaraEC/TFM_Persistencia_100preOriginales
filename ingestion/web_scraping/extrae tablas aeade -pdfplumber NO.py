#busca tablas dentro de los boletines de prensa de la AEADE y las guarda en formato CSV
import pdfplumber
import pandas as pd
import os
import re

PDF_FOLDER = "boletines_aeade"
OUTPUT_FOLDER = os.path.join(PDF_FOLDER, "tablas_aeade")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

pdfs_a_leer = {
    "Boletin-de-Prensa-Diciembre-2025.pdf": "VENTAS2025",
    "BOLETIN-DE-VENTAS-2020-PARA-PRENSA-ENERO-2021.pdf": "VENTAS2020",
    "BOLETIN-DE-VENTAS-PARA-PRENSA-ENERO-2022.pdf": "VENTAS2021",
    "BOLETIN-DE-VENTAS-PARA-PRENSA-ENERO-2023-V2.pdf": "VENTAS2022",
    "BOLETIN-VENTAS_PRENSA_ENERO-2024.pdf": "VENTAS2023",
    "BOLETIN-VENTAS_PRENSA_ENERO-2025.pdf": "VENTAS2024",
    "Boletin-de-Prensa-Junio-2026.pdf": "VENTAS2026"
}

# Patrones que identifican la tabla TOP 20
patrones_top20 = [
    r"TOP\s*20",
    r"MARCAS\s*DE\s*VEHICULOS",
    r"VENTAS\s*DE\s*VEHICULOS\s*POR\s*MARCAS"
]

def es_encabezado_top20(texto):
    texto = texto.upper()
    return any(re.search(p, texto) for p in patrones_top20)

def extraer_tabla(pdf_path):
    tablas_detectadas = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lineas = text.split("\n")

            # Buscar encabezado TOP 20
            for idx, linea in enumerate(lineas):
                if es_encabezado_top20(linea):
                    # Extraer las siguientes líneas como tabla
                    tabla_lineas = lineas[idx+1: idx+40]  # 40 líneas es suficiente

                    filas = []
                    for l in tabla_lineas:
                        # Separar por múltiples espacios
                        partes = re.split(r"\s{2,}", l.strip())
                        if len(partes) >= 2:
                            filas.append(partes)

                    if len(filas) > 3:
                        df = pd.DataFrame(filas)
                        tablas_detectadas.append(df)

    return tablas_detectadas

# Procesar PDFs
todas = []

for archivo, etiqueta in pdfs_a_leer.items():
    pdf_path = os.path.join(PDF_FOLDER, archivo)
    print(f"Procesando {archivo} → {etiqueta}")

    tablas = extraer_tabla(pdf_path)

    for t in tablas:
        t["VENTAS_AAAA"] = etiqueta
        todas.append(t)

# Exportar
if todas:
    df_final = pd.concat(todas, ignore_index=True)
    df_final.to_csv(os.path.join(OUTPUT_FOLDER, "top20_marcas.csv"), index=False)
    print("CSV generado: top20_marcas.csv")
else:
    print("No se detectaron tablas TOP 20.")
