#limpia y normaliza el dataset maestro de la AEADE
import os
import pandas as pd

# ============================
# CONFIGURACIÓN
# ============================

INPUT_FOLDER = "boletines_aeade/tablas_aeade"
INPUT_FILE = os.path.join(INPUT_FOLDER, "dataset_maestro_aeade.csv")

OUTPUT_FILE = os.path.join(INPUT_FOLDER, "dataset_maestro_aeade_limpio.csv")

print("Iniciando limpieza del dataset maestro...\n")

# ============================
# CARGAR DATASET
# ============================

df = pd.read_csv(INPUT_FILE)

print(f"Dataset original: {df.shape[0]} filas, {df.shape[1]} columnas\n")

# ============================
# LIMPIEZA DE ENCABEZADOS
# ============================

# Normalizar nombres de columnas
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

# ============================
# ELIMINAR FILAS VACÍAS
# ============================

df.replace("", pd.NA, inplace=True)
df.dropna(how="all", inplace=True)

print(f"Después de eliminar filas vacías: {df.shape[0]} filas\n")

# ============================
# CONVERSIÓN DE NÚMEROS
# ============================

def convertir_numero(valor):
    try:
        # Quitar símbolos comunes
        valor = str(valor).replace(",", "").replace("%", "").strip()
        return float(valor)
    except:
        return valor

for col in df.columns:
    df[col] = df[col].apply(convertir_numero)

# ============================
# DETECTAR COLUMNAS NUMÉRICAS
# ============================

columnas_numericas = df.select_dtypes(include=["float", "int"]).columns.tolist()
print("Columnas numéricas detectadas:")
for c in columnas_numericas:
    print(f" - {c}")
print()

# ============================
# ELIMINAR FILAS CON SOLO TEXTO
# ============================

df = df.dropna(subset=columnas_numericas, how="all")

print(f"Después de eliminar filas sin datos numéricos: {df.shape[0]} filas\n")

# ============================
# GUARDAR DATASET LIMPIO
# ============================

df.to_csv(OUTPUT_FILE, index=False)
print(f"✔ Dataset limpio generado: {OUTPUT_FILE}")

print("\nLimpieza completada.")
