import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random

# ==============================
# 1. User Agents reales (rotación)
# ==============================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
]

# ==============================
# 2. Función para obtener precio en PartsGeek
# ==============================
def obtener_precio_partsgeek(codigo):

    url = f"https://www.partsgeek.com/brands/oem.html?keywords={codigo}"

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.partsgeek.com/",
        "Connection": "keep-alive"
    }

    print(f"\n→ Buscando en PartsGeek: {codigo}")

    try:
        r = requests.get(url, headers=headers, timeout=12)
    except Exception as e:
        print(f"   ❌ Error de conexión: {str(e)}")
        return None

    # Manejo de bloqueos
    if r.status_code == 403:
        print(f"   ❌ PartsGeek bloqueó la solicitud (403). Reintentando con otro User-Agent...")
        time.sleep(5)
        return obtener_precio_partsgeek(codigo)

    if r.status_code != 200:
        print(f"   ❌ Error HTTP {r.status_code} en PartsGeek")
        return None

    # Detectar si no hay resultados
    if "No results found" in r.text:
        print(f"   ❌ No se encontró en PartsGeek")
        return None

    soup = BeautifulSoup(r.text, "html.parser")

    # Buscar el primer precio
    price_tag = soup.find("span", class_="price")

    if not price_tag:
        print(f"   ⚠ No se encontró precio en PartsGeek")
        return None

    price = price_tag.text.strip()
    print(f"   ✔ Precio PartsGeek: {price}")

    return price

# ==============================
# 3. Leer archivo CSV
# ==============================
try:
    print("→ Cargando archivo CSV...")
    df = pd.read_csv("orgu.csv")
    print(f"✔ Archivo cargado: {len(df)} registros.")
except Exception as e:
    print(f"❌ Error al leer 'orgu.csv': {str(e)}")
    exit()

# ==============================
# 4. Procesar cada código
# ==============================
precios_pg = []

for idx, fila in df.iterrows():
    codigo = fila["Codigo"]

    precio_pg = obtener_precio_partsgeek(codigo)
    precios_pg.append(precio_pg)

    print(f"✔ Procesado [{idx + 1}/{len(df)}]: {codigo} → PartsGeek: {precio_pg}")

    # Pausa aleatoria para evitar detección
    time.sleep(random.uniform(1.5, 3.5))

# ==============================
# 5. Exportar resultados
# ==============================
df["Precio_PartsGeek"] = precios_pg

df.to_csv("orgu_precios_partsgeek.csv", index=False, encoding='utf-8')
print("\n✔ Archivo final guardado como 'orgu_precios_partsgeek.csv'")
