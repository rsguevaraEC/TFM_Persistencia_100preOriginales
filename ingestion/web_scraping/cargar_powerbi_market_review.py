import pandas as pd
import psycopg2
from psycopg2 import sql

# ============================================================
# 📌 CONFIGURACIÓN DE CONEXIÓN
# ============================================================

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="ASUS",
    port="5433"
)
cursor = conn.cursor()

# ============================================================
# 📌 RUTA DEL ARCHIVO CSV EXPORTADO DESDE POWER BI
# ============================================================

ruta_csv = r"C:/Users/Asus/OneDrive/Isabel I/TFM_Persistencia_100preOriginales/proyecto/ingestion/web_scraping/tablas_aeade/powerbi_market_review.csv"

# ============================================================
# 📌 LEER Y LIMPIAR EL CSV
# ============================================================

df = pd.read_csv(ruta_csv, encoding="utf-8-sig", sep=",")
df = df.replace("-", None)

# Normalizar nombres de columnas para PostgreSQL
df.columns = [c.strip().lower().replace(" ", "_").replace("/", "_") for c in df.columns]

# Convertir fechas al formato correcto
if "fecha" in df.columns:
    df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")

print(f"📊 Total de filas a insertar: {len(df)}")

# ============================================================
# 📌 CREAR TABLA EN POSTGRESQL (si no existe)
# ============================================================

create_table_query = sql.SQL("""
CREATE TABLE IF NOT EXISTS spo.market_review (
    id SERIAL PRIMARY KEY,
    anio INT,
    mes INT,
    marca TEXT,
    familia TEXT,
    modelo TEXT,
    llavemodelo INT,
    segmento TEXT,
    provincia TEXT,
    zonas TEXT,
    segmento_ford TEXT,
    subsegmento_ford TEXT,
    segmento_kia TEXT,
    subsegaa TEXT,
    subsegbb TEXT,
    trasmision TEXT,
    tipo_combustible TEXT,
    precio NUMERIC(18,2),
    unidades INT,
    grupo TEXT,
    fuente TEXT,
    qm TEXT,
    assa TEXT,
    fecha DATE
);
""")

cursor.execute(create_table_query)
conn.commit()
print("✔ Tabla spo.market_review creada o ya existente.")

# ============================================================
# 📌 INSERTAR REGISTROS
# ============================================================

insert_query = """
INSERT INTO spo.market_review (
    anio, mes, marca, familia, modelo, llavemodelo, segmento, provincia, zonas,
    segmento_ford, subsegmento_ford, segmento_kia, subsegaa, subsegbb,
    trasmision, tipo_combustible, precio, unidades, grupo, fuente, qm, assa, fecha
)
VALUES (
    %(año)s, %(mes)s, %(marca)s, %(familia)s, %(modelo)s, %(llavemodelo)s, %(segmento)s, %(provincia)s, %(zonas)s,
    %(segmento_ford)s, %(subsegmento_ford)s, %(segmento_kia)s, %(subsegaa)s, %(subsegbb)s,
    %(trasmisión)s, %(tipo_combustible)s, %(precio)s, %(unidades)s, %(grupo)s, %(fuente)s, %(qm)s, %(assa)s, %(fecha)s
)
ON CONFLICT DO NOTHING;
"""

for _, fila in df.iterrows():
    cursor.execute(insert_query, fila.to_dict())

conn.commit()
cursor.close()
conn.close()

print("🎉 Datos cargados correctamente en spo.market_review")
