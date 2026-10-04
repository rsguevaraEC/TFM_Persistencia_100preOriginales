import pandas as pd
import os

# ============================================================
# CONFIGURACIÓN
# ============================================================

# Carpeta donde guardarás los CSV o TXT de cada año (pueden ser copiados manualmente)
DATA_FOLDER = "tablas_aeade"
os.makedirs(DATA_FOLDER, exist_ok=True)

# ============================================================
# FUNCIÓN PARA CREAR DATAFRAME DE CADA TABLA
# ============================================================

def crear_df(marca, dic_24, dic_25, ene_dic_24, ene_dic_25, etiqueta):
    df = pd.DataFrame({
        "marca": marca,
        "dic_24": dic_24,
        "dic_25": dic_25,
        "ene_dic_24": ene_dic_24,
        "ene_dic_25": ene_dic_25,
        "VENTAS_AAAA": etiqueta
    })
    return df

# ============================================================
# EJEMPLO: TABLA 2025 (VALIDADA CON TU IMAGEN)
# ============================================================

marcas = [
    "KIA","CHEVROLET","HYUNDAI","GWM","TOYOTA","CHERY","RENAULT","SUZUKI","JAC",
    "DONGFENG","SINOTRUK","DFSK","VOLKSWAGEN","BYD","HINO","MAZDA","JETOUR",
    "FOTON","NISSAN","SHINERAY","OTRAS MARCAS"
]

dic_24 = [1254,1431,301,659,499,323,266,337,278,158,203,201,124,118,240,181,162,71,176,185,1534]
dic_25 = [1527,1238,613,1020,564,513,435,236,504,316,378,351,283,386,239,199,381,244,213,171,2557]
ene_dic_24 = [16727,19969,5158,3608,6654,4718,3671,4198,2969,2152,1984,2626,2569,850,2532,2430,1825,1245,2560,2318,17503]
ene_dic_25 = [19141,15671,7554,6678,6123,5660,4810,4534,4047,3479,3459,3320,3181,2916,2699,2637,2289,2077,1772,1769,20689]

df_2025 = crear_df(marcas, dic_24, dic_25, ene_dic_24, ene_dic_25, "VENTAS2025")

# ============================================================
# CARGAR LAS DEMÁS TABLAS (2020–2024, 2026)
# ============================================================
# Puedes copiar manualmente las tablas de cada PDF en este formato y crear los DataFrames igual.
# Ejemplo:
# df_2024 = crear_df(marcas_2024, dic_24_2024, dic_25_2024, ene_dic_24_2024, ene_dic_25_2024, "VENTAS2024")

# ============================================================
# CONCATENAR TODAS LAS TABLAS
# ============================================================

# Si solo tienes 2025 por ahora:
todas = [df_2025]

# Cuando agregues las demás:
# todas = [df_2020, df_2021, df_2022, df_2023, df_2024, df_2025, df_2026]

df_maestro = pd.concat(todas, ignore_index=True)

# ============================================================
# EXPORTAR DATASET MAESTRO
# ============================================================

output_path = os.path.join(DATA_FOLDER, "dataset_top20_maestro.csv")
df_maestro.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"🎉 Dataset maestro generado correctamente: {output_path}")
