import psycopg2
import csv

# Función segura para convertir precios
def parse_precio(valor):
    if not valor or valor.strip() == "":
        return None
    valor = valor.replace(" USD", "").strip()
    try:
        return float(valor)
    except ValueError:
        return None

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
