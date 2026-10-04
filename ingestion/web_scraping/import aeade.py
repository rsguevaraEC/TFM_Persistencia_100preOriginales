#download boletines de prensa de la AEADE
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os
import requests

# ============================
# CONFIGURACIÓN INICIAL
# ============================

BASE_URL = "https://www.aeade.net/boletines-de-prensa-venta-de-vehiculos/"
DEST_FOLDER = "boletines_aeade"
os.makedirs(DEST_FOLDER, exist_ok=True)

# Ruta del ChromeDriver
service = Service("C:\\chromedv\\chromedriver.exe")

# Opciones de Chrome
options = Options()
options.add_argument("--headless")            # Ejecutar sin interfaz
options.add_argument("--disable-gpu")         # Evitar errores gráficos
options.add_argument("--no-sandbox")          # Requerido en algunos entornos

# Configurar descargas automáticas
prefs = {
    "download.default_directory": os.path.abspath(DEST_FOLDER),
    "plugins.always_open_pdf_externally": True
}
options.add_experimental_option("prefs", prefs)

# Inicializar Selenium
driver = webdriver.Chrome(service=service, options=options)

# ============================
# SCRAPING DE ENLACES
# ============================

driver.get(BASE_URL)
time.sleep(5)  # Esperar a que cargue el contenido dinámico

# Extraer todos los enlaces del HTML renderizado
links = [
    a.get_attribute("href")
    for a in driver.find_elements("tag name", "a")
    if a.get_attribute("href")
]

# Filtrar enlaces de descarga
pdf_links = [
    l for l in links
    if "sdm_process_download" in l or l.lower().endswith(".pdf")
]

print(f"Se encontraron {len(pdf_links)} enlaces de descarga.")

# ============================
# DESCARGA DE ARCHIVOS
# ============================

for url in pdf_links:
    print(f"Intentando descargar: {url}")

    # Intento 1: Selenium (descarga automática)
    try:
        driver.get(url)
        time.sleep(4)
        print(f"✔ Descarga gestionada por Selenium: {url}")
        continue
    except Exception as e:
        print(f"⚠ Selenium no pudo descargar {url}: {e}")

    # Intento 2: Requests (solo si el servidor entrega PDF directo)
    try:
        filename = url.split("/")[-1]
        filepath = os.path.join(DEST_FOLDER, filename)

        r = requests.get(url)
        if "application/pdf" in r.headers.get("Content-Type", ""):
            with open(filepath, "wb") as f:
                f.write(r.content)
            print(f"✔ Descargado con requests: {filename}")
        else:
            print(f"✖ No es PDF o no disponible: {filename}")

    except Exception as e:
        print(f"✖ Error descargando {url}: {e}")

print("Descarga completada. Archivos guardados en 'boletines_aeade'.")
driver.quit()
