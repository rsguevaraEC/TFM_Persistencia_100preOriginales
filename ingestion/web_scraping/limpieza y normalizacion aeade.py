import pandas as pd

# Cargar archivo real
df = pd.read_csv("boletines_aeade/tablas_aeade/dataset_top20_aeade.csv")

# Extraer el bloque vertical completo
bloque = df.iloc[0, 0]

# Dividir en líneas
lineas = bloque.split("\n")

# Limpiar líneas vacías
lineas = [l.strip() for l in lineas if l.strip()]

# Validación: el número de líneas debe ser múltiplo de 5
if len(lineas) % 5 != 0:
    print("Advertencia: el número de líneas no es múltiplo de 5. Revisar el archivo.")
    
# Agrupar cada 5 líneas: marca + 4 valores
filas = []
for i in range(0, len(lineas), 5):
    grupo = lineas[i:i+5]
    if len(grupo) == 5:
        filas.append(grupo)

# Crear DataFrame
df_final = pd.DataFrame(filas, columns=["marca", "dic_24", "dic_25", "ene_dic_24", "ene_dic_25"])

# Agregar año
df_final["VENTAS_AAAA"] = df.iloc[0, 5]

# Convertir números
for col in ["dic_24", "dic_25", "ene_dic_24", "ene_dic_25"]:
    df_final[col] = df_final[col].astype(int)

# Guardar dataset final
df_final.to_csv("boletines_aeade/tablas_aeade/top20_marcas_normalizado.csv", index=False)

print("Dataset final generado:")
print(df_final.head(10))
