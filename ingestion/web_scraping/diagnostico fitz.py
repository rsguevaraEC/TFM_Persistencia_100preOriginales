import pymupdf as fitz

pdf = "boletines_aeade/BOLETIN-DE-VENTAS-PARA-PRENSA-ENERO-2023-V2.pdf"
doc = fitz.open(pdf)

for page in doc:
    print("\n=== Página ===")
    blocks = page.get_text("blocks")
    for b in blocks:
        print(b)
