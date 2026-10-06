import requests
import pandas as pd

def descargar_bcb(codigo):
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json"
    r = requests.get(url).json()

    # Validación: si no devuelve lista, no procesar
    if not isinstance(r, list) or len(r) == 0:
        print(f"⚠️ Código {codigo} no tiene datos o no existe.")
        return pd.DataFrame()  # DataFrame vacío

    df = pd.DataFrame(r)
    df["valor"] = df["valor"].astype(float)
    return df


indicadores = {
    "selic": 432,
    "credito_personas": 25466,
    "ibcbr": 24363,
    "pib": 4380,
    "ipca": 433,
    "ingreso_real": 28763,
    "usd_brl": 1,
    "confianza": 4390
}

dfs = []

for nombre, codigo in indicadores.items():
    df = descargar_bcb(codigo)
    df["indicador"] = nombre
    dfs.append(df)

df_total = pd.concat(dfs, ignore_index=True)
df_total.to_csv("data_raw/brasil_indicadores_vehiculos.csv", index=False)

print(df_total.head())


df = pd.read_csv("data_raw/brasil_indicadores_vehiculos.csv")
print(df.head())
print(df["indicador"].unique())
