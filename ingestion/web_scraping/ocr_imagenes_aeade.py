import os
import pytesseract
from PIL import Image
import re

# Ruta de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMG_FOLDER = "imagenes_aeade"
TXT_FOLDER = "texto_aeade"
os.makedirs(TXT_FOLDER, exist_ok=True)

# Patrón del encabezado TOP 20
patrones_top20 = [
    r"TOP\s*20",
    r"MARCAS",
    r"VEHICULOS",
    r"VENDIDAS"
]

def contiene_top20(texto):
    texto_u = texto.upper()
    return any(re.search(p, texto_u) for p in patrones_top20)

# ============================================================
# OCR sobre cada imagen
# ============================================================

for archivo in os.listdir(IMG_FOLDER):
    if not archivo.lower().endswith(".png"):
        continue

    ruta_img = os.path.join(IMG_FOLDER, archivo)
    print(f"📄 OCR: {archivo}")

    img = Image.open(ruta_img)

    # OCR en inglés (funciona mejor con texto impreso)
    texto = pytesseract.image_to_string(img, lang="eng")

    ruta_txt = os.path.join(TXT_FOLDER, archivo.replace(".png", ".txt"))
    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write(texto)

    # Detección rápida de si la página contiene la tabla TOP 20
    if contiene_top20(texto):
        print(f"   ✔ Esta página contiene la tabla TOP 20")
    else:
        print(f"   ⚠ No contiene TOP 20")
