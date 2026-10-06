import requests
import pandas as pd

paises = ["ARG", "BOL", "BRA", "CHL", "COL", "ECU", "PRY", "PER", "URY"]
indicadores = {
    "NY.GDP.PCAP.CD": "pib_per_capita",
    "NY.GDP.MKTP.KD.ZG": "crecimiento_pib",
    "FP.CPI.TOTL.ZG": "inflacion",
    "SL.UEM.TOTL.ZS": "desempleo",
    "SP.URB.TOTL.IN.ZS": "poblacion_urbana"
}

def obtener_indicador(pais, indicador):
    url = f"http://api.worldbank.org/v2/country/{pais}/indicator/{indicador}?format=json&per_page=2000"
    r = requests.get(url).json()
    datos = r[1]
    df = pd.DataFrame(datos)
    df = df[["country", "date", "value"]]
    df["country"] = pais
    return df

df_total = pd.DataFrame()

for pais in paises:
    for ind, nombre in indicadores.items():
        df = obtener_indicador(pais, ind)
        df["indicator"] = nombre
        df_total = pd.concat([df_total, df], ignore_index=True)

df_total.to_csv("data_raw/worldbank_raw.csv", index=False)
