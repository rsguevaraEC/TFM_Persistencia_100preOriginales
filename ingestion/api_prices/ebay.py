# ==============================
# 0. IMPORTS
# ==============================
import pandas as pd
import requests
import base64
import time
import psycopg2
import csv
import os

# ==============================
# 1. CREDENCIALES
# ==============================
client_id = os.getenv("EBAY_CLIENT_ID")
client_secret = os.getenv("EBAY_CLIENT_SECRET")

# ==============================
# 2. GENERAR TOKEN OAUTH (PRODUCCIÓN)
# ==============================
def obtener_token_ebay():
    print("→ Generando token OAuth...")
    url = "https://api.ebay.com/identity/v1/oauth2/token"

    credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = "grant_type=client_credentials&scope=https://api.ebay.com/oauth/api_scope"
    response = requests.post(url, headers=headers, data=payload.encode("utf-8"))

    print("Código HTTP:", response.status_code)
    print("Respuesta:", response.text)

    token = response.json().get("access_token")
    return token

# ==============================
# 3. FUNCIÓN PARA BUSCAR PRECIOS (PRODUCCIÓN)
# ==============================
def obtener_precio_ebay(codigo, token):

    # Limpiar código OEM antes de buscar
    codigo_limpio = codigo.replace("L-", "").replace("E-", "").replace("CD", "").replace("-", "").strip()

    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={codigo_limpio}"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-ENDUSERCTX": "contextualLocation=country=US"
    }

    print(f"\n→ Buscando código: {codigo}  (limpio: {codigo_limpio})")

    r = requests.get(url, headers=headers)

    # Reintento automático
    if r.status_code in [429, 503]:
        print(f"⚠ eBay temporalmente no disponible para {codigo}. Reintentando en 10 segundos...")
        time.sleep(10)
        return obtener_precio_ebay(codigo, token)

    print(f"   Estado HTTP: {r.status_code}")

    if r.status_code != 200:
        print(f"   ❌ Error buscando {codigo}: {r.text}")
        return None

    data = r.json()

    # Si no hay resultados
    if data.get("total", 0) == 0:
        print(f"   ❌ No se encontró información para: {codigo}")
        return None

    # Extraer el primer ítem
    item = data["itemSummaries"][0]

    try:
        price = item["price"]["value"]
        currency = item["price"]["currency"]
        print(f"   ✔ Precio encontrado: {price} {currency}")
        return f"{price} {currency}"
    except:
        print(f"   ⚠ No se pudo extraer precio para: {codigo}")
        return None

# ==============================
# 4. Función segura para convertir precios
# ==============================

def parse_precio(valor):
    if not valor or valor.strip() == "":
        return None
    valor = valor.replace(" USD", "").strip()
    try:
        return float(valor)
    except ValueError:
        return None


# ==============================
# 5. PROCESAR ARCHIVO CSV
# ==============================
try:
    print("→ Cargando archivo CSV...")
    df = pd.read_csv("orgu.csv")
    print(f"✔ Archivo cargado con éxito: {len(df)} registros localizados.")
except Exception as e:
    print(f"❌ Error crítico al leer 'orgu.csv': {str(e)}")
    exit()

token = obtener_token_ebay()
if not token:
    print("❌ Error Crítico: No se puede continuar sin un token válido.")
    exit()

print("\n→ Iniciando consulta de precios en eBay PRODUCCIÓN...")
precios = []

for idx, fila in df.iterrows():
    codigo = fila["Codigo"]
    precio = obtener_precio_ebay(codigo, token)
    precios.append(precio)
    print(f"Procesado [{idx + 1}/{len(df)}]: Código {codigo} → {precio}")
    time.sleep(1)

df["Precio_USA"] = precios

print("\n→ Exportando archivo final...")
df.to_csv("precios_ebay.csv", index=False, encoding='utf-8')
print("✔ ¡Proceso completado con éxito! Archivo guardado como 'precios_ebay.csv'")


# ==============================
# 6. GRABAR EN POSTGRES
# ==============================
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="ASUS",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

with open('precios_ebay.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:

        precio_usa = parse_precio(row['Precio_USA'])

        cur.execute("""
            INSERT INTO spo.precio_comparativo 
            (codigo, descripcion, precio_usa, fuente, origen_datos)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            row['Codigo'],
            row['Description'],
            precio_usa,
            'ebay',
            'api'
        ))

conn.commit()
cur.close()
conn.close()

print("✔ Inserción completada sin errores.")
