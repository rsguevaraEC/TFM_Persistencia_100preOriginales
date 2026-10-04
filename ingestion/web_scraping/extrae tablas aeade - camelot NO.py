#busca tablas dentro de los boletines de prensa de la AEADE y las guarda en formato CSV
import os
import re
import camelot
import pandas as pd

# Carpeta donde guardas los boletines PDF
PDF_FOLDER = "boletines_aeade"

# Mapeo explícito: archivo PDF real → etiqueta VENTASAAAA
# Aquí defines tú mismo el año correcto de cada archivo
pdfs_a_leer = {
    "Boletin-de-Prensa-Diciembre-2025.pdf": "VENTAS2025",
    "BOLETIN-DE-VENTAS-2020-PARA-PRENSA-ENERO-2021.pdf": "VENTAS2020",
    "BOLETIN-DE-VENTAS-PARA-PRENSA-ENERO-2022.pdf": "VENTAS2021",
    "BOLETIN-DE-VENTAS-PARA-PRENSA-ENERO-2023-V2.pdf": "VENTAS2022",
    "BOLETIN-VENTAS_PRENSA_ENERO-2024.pdf": "VENTAS2023",
    "BOLETIN-VENTAS_PRENSA_ENERO-2025.pdf": "VENTAS2024",
    "Boletin-de-Prensa-Junio-2026.pdf": "VENTAS2026"
}


# Patrones de títulos de tablas internas que debemos extraer (1.1, 1.2, etc.)
patron_tablas = [
    # Grupo A: Marcas
    r"TOP.*20.*MARCAS",
    r"VENTAS.*VEHICULOS.*MARCAS",
    r"AUTOMOVIL.*SUV.*MARCAS",
    r"CAMIONETAS.*PICK.*UP.*MARCAS",
    r"BUS.*VAN.*MARCAS",
    r"CAMIONES.*MARCAS",
    # Grupo B: Modelos por segmento
    r"MODELOS.*SEGMENTO",
    r"\bSUV\b",
    r"CAMIONETA",
    r"AUTOMOVIL",
    r"CAMION",
    r"\bVAN\b",
    r"\bBUS\b"
]


# Carpeta de salida
OUTPUT_FOLDER = os.path.join(PDF_FOLDER, "tablas_aeade")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Limpieza de tablas
def limpiar_tabla(df, etiqueta_pdf, titulo_tabla):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
 
    # Eliminar columnas con porcentajes
    df = df.loc[:, ~df.columns.str.contains("%", case=False)]

    # Eliminar filas vacías o totales
    df = df[~df.apply(lambda x: x.astype(str).str.contains("TOTAL", case=False)).any(axis=1)]
    df = df.dropna(how="all")

    # Agregar metadatos
    df["VENTAS_AAAA"] = etiqueta_pdf
    df["titulo_tabla"] = titulo_tabla
    return df

# Procesamiento
todas_las_tablas = []

for archivo, etiqueta_pdf in pdfs_a_leer.items():
    pdf_path = os.path.join(PDF_FOLDER, archivo)
    print(f"📄 Procesando: {archivo} → {etiqueta_pdf}")

    tablas = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")

    for i, tabla in enumerate(tablas):
        texto_tabla = " ".join(tabla.df.astype(str).values.flatten())

        for patron in patron_tablas:
            if re.search(patron, texto_tabla, re.I):
                df = tabla.df
                df_limpia = limpiar_tabla(df, etiqueta_pdf, patron)
                df_limpia["tabla_numero"] = i + 1
                todas_las_tablas.append(df_limpia)
                break
    print(f"En {archivo}: se detectaron {len(tablas)}")

# Unir y exportar
if todas_las_tablas:
    dataset_final = pd.concat(todas_las_tablas, ignore_index=True)
    dataset_final.to_csv(os.path.join(OUTPUT_FOLDER, "dataset_aeade_filtrado.csv"), index=False)
    print("✅ Dataset generado: dataset_aeade_filtrado.csv")
else:
    print("⚠ No se encontraron tablas relevantes.")
