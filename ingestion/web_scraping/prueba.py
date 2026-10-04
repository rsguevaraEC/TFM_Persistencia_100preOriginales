import pandas as pd
df = pd.read_csv(r"C:/Users/Asus/OneDrive/Isabel I/TFM_Persistencia_100preOriginales/proyecto/ingestion/web_scraping/tablas_aeade/2019-2020.csv", encoding="latin1", sep=";")
print(df.head())
