import sdmx
import pandas as pd

# Cliente oficial del FMI
IMF = sdmx.Client('IMF_DATA')

# Dataset WEO (World Economic Outlook)
dataset = 'WEO'

# Países en formato FMI
paises = ["ARG", "BOL", "BRA", "CHL", "COL", "ECU", "PRY", "PER", "URY"]

# Indicador: PIB real (NGDP_R)
indicador = "NGDP_R"

dfs = []

for pais in paises:
    key = f"{pais}.{indicador}"
    print("Consultando:", key)

    data_msg = IMF.data(
        dataset,
        key=key,
        params={"startPeriod": 2000}
    )

    df = sdmx.to_pandas(data_msg)
    df = df.reset_index()
    df["country"] = pais
    dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)
df_final.to_csv("data_raw/imf_weo_sdmx.csv", index=False)

print(df_final.head())
