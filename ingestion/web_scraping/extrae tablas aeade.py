import fitz
import os

PDF_FOLDER = "boletines_aeade"
IMG_FOLDER = "imagenes_aeade"
os.makedirs(IMG_FOLDER, exist_ok=True)

PDFS = [
    "BOLETIN-DE-VENTAS-2020-PARA-PRENSA-ENERO-2021.pdf",
    "BOLETIN-DE-VENTAS-PARA-PRENSA-ENERO-2022.pdf",
    "BOLETIN-DE-VENTAS-PARA-PRENSA-ENERO-2023-V2.pdf",
    "BOLETIN-VENTAS_PRENSA_ENERO-2024.pdf",
    "BOLETIN-VENTAS_PRENSA_ENERO-2025.pdf",
    "Boletin-de-Prensa-Diciembre-2025.pdf",
    "Boletin-de-Prensa-Agosto-2026.pdf"
]

for pdf in PDFS:
    ruta_pdf = os.path.join(PDF_FOLDER, pdf)
    doc = fitz.open(ruta_pdf)

    print(f"📄 Convirtiendo {pdf}...")

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300)
        ruta_img = os.path.join(IMG_FOLDER, f"{pdf}_page_{i+1}.png")
        pix.save(ruta_img)

    print(f"✔ Imágenes generadas para {pdf}")
