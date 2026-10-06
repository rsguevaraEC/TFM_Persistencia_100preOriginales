import pandas as pd

# ============================================================
# 1. TRM – Tipo de cambio COP/USD
# ============================================================

df_trm = pd.read_json("https://www.datos.gov.co/resource/ceyp-9c7c.json")
df_trm = df_trm[["valor", "vigenciadesde"]]
df_trm["indicador"] = "trm"
print("✔ TRM descargado")

# ============================================================
# 2. ISE – Actividad económica
# ============================================================

df_ise = pd.read_json("https://www.datos.gov.co/resource/32sa-8pi3.json")
df_ise = df_ise[["valor", "vigenciadesde"]]
df_ise["indicador"] = "ise"
print("✔ ISE descargado")

# ============================================================
# 3. Unificación
# ============================================================

df_total = pd.concat([df_trm, df_ise], ignore_index=True)

df_total.to_csv("data_raw/colombia_indicadores_vehiculos.csv", index=False)

print("📁 Archivo generado: colombia_indicadores_vehiculos.csv")
print(df_total.head())
