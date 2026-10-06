import pandas as pd
import os

# ---------------------------------------------------------
# CONFIGURACIÓN DE RUTAS
# ---------------------------------------------------------
DATA_DIR = "data_raw"
OUTPUT_FILE = os.path.join(DATA_DIR, "union_final.csv")

# ---------------------------------------------------------
# FUNCIONES DE LIMPIEZA
# ---------------------------------------------------------

def clean_brasil(df):
    df = df.copy()
    df.rename(columns={"data": "fecha", "valor": "valor"}, inplace=True)
    df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%Y", errors="coerce")
    df["pais"] = "Brasil"
    df["fuente"] = "Banco Central de Brasil (BCB) – Indicadores de crédito"
    return df[["pais", "fecha", "indicador", "valor", "fuente"]]


def clean_colombia(df):
    df = df.copy()
    df.rename(columns={"vigenciadesde": "fecha", "valor": "valor"}, inplace=True)
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
    df["pais"] = "Colombia"
    df["fuente"] = "Banco de la República – TRM e ISE"
    return df[["pais", "fecha", "indicador", "valor", "fuente"]]


def clean_imf(df):
    df = df.copy()
    df.rename(columns={"TIME_PERIOD": "fecha", "value": "valor", "INDICATOR": "indicador", "COUNTRY": "pais"}, inplace=True)
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y", errors="coerce")
    df["fuente"] = "Fondo Monetario Internacional (IMF) – World Economic Outlook SDMX"
    return df[["pais", "fecha", "indicador", "valor", "fuente"]]


def clean_worldbank(df):
    df = df.copy()
    df.rename(columns={"date": "fecha", "value": "valor", "indicator": "indicador", "country": "pais"}, inplace=True)
    df["fecha"] = pd.to_datetime(df["fecha"], format="%Y", errors="coerce")
    df["fuente"] = "Banco Mundial – API de Indicadores Globales"
    return df[["pais", "fecha", "indicador", "valor", "fuente"]]


def clean_latinobarometro(df):
    df = df.copy()
    df.rename(columns={"pais_sigla": "pais"}, inplace=True)
    df["fecha"] = pd.to_datetime("2024-01-01")
    df["fuente"] = "Latinobarómetro 2024 – Opinión pública económica y social"

    variables = [
        "situacion_laboral",
        "miedo_desempleo",
        "percepcion_eco_pais",
        "percepcion_eco_hogar",
        "justicia_ingresos",
        "progreso_pais",
        "eco_pais_pasado",
        "eco_pais_futuro",
        "genero",
        "edad"
    ]

    df_long = df.melt(
        id_vars=["pais", "fecha", "fuente"],
        value_vars=variables,
        var_name="indicador",
        value_name="valor"
    )

    return df_long[["pais", "fecha", "indicador", "valor", "fuente"]]


# ---------------------------------------------------------
# CARGA DE ARCHIVOS
# ---------------------------------------------------------
print("Cargando archivos...")

df_brasil = pd.read_csv(os.path.join(DATA_DIR, "brasil_indicadores_vehiculos.csv"))
df_colombia = pd.read_csv(os.path.join(DATA_DIR, "colombia_indicadores_vehiculos.csv"))
df_imf = pd.read_csv(os.path.join(DATA_DIR, "imf_weo_sdmx.csv"))
df_worldbank = pd.read_csv(os.path.join(DATA_DIR, "worldbank_raw.csv"))
df_latino = pd.read_csv(os.path.join(DATA_DIR, "latinobarometro_2024_economico_sudamerica.csv"), encoding="latin1")

print("✔ Todos los archivos cargados correctamente.")

# ---------------------------------------------------------
# LIMPIEZA Y UNIÓN
# ---------------------------------------------------------
datasets = [
    clean_brasil(df_brasil),
    clean_colombia(df_colombia),
    clean_imf(df_imf),
    clean_worldbank(df_worldbank),
    clean_latinobarometro(df_latino)
]

df_final = pd.concat(datasets, ignore_index=True)

# ---------------------------------------------------------
# EXPORTACIÓN
# ---------------------------------------------------------
df_final.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

print(f"\n📁 Archivo final generado: {OUTPUT_FILE}")
print("✔ Filas totales:", len(df_final))
print("✔ Columnas:", list(df_final.columns))
print("\nFuentes incluidas:")
print(df_final["fuente"].unique())
