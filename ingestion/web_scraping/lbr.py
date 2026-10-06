import requests

# Ejemplo: URL directa del archivo de datos de una oleada (puedes extraerla usando F12 en su web)
url_latinobarometro = "https://www.latinobarometro.org/documents/LAT-2024/latinobarometro-2024-csv-v20250817.zip" 

# Nombre con el que quieres guardar el archivo localmente
archivo_destino = "data_raw\latinobarometro_2024.zip"

print("Iniciando descarga de datos...")
response = requests.get(url_latinobarometro, stream=True)

if response.status_code == 200:
    with open(archivo_destino, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"¡Descarga completada con éxito! Guardado como: {archivo_destino}")
else:
    print(f"Error en la descarga. Código de estado: {response.status_code}")