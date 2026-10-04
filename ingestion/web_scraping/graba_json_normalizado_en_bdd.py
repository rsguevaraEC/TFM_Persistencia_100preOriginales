import json
import psycopg2

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
# 📌 RUTA DEL JSON NORMALIZADO
# ============================================================

ruta_json = r"C:/Users/Asus/OneDrive/Isabel I/TFM_Persistencia_100preOriginales/proyecto/ingestion/web_scraping/tablas_aeade/dataset_maestro_aeade_final_normalizado.json"

# ============================================================
# 📌 CREAR TABLA EN POSTGRESQL
# ============================================================

cursor.execute("""
    CREATE TABLE IF NOT EXISTS spo.aeade_ventas_normalizado (
        marca TEXT NOT NULL,
        fecha DATE NOT NULL,
        ventas INTEGER,
        tipo TEXT,
        PRIMARY KEY (marca, fecha)
    );
""")

conn.commit()
print("✔ Tabla spo.aeade_ventas_normalizado creada o ya existente.")

# ============================================================
# 📌 CARGAR JSON NORMALIZADO
# ============================================================

with open(ruta_json, "r", encoding="utf-8") as f:
    data = json.load(f)

registros = data["data"]
print(f"📌 Registros a insertar: {len(registros)}")

# ============================================================
# 📌 INSERTAR REGISTROS EN POSTGRESQL
# ============================================================

insert_query = """
    INSERT INTO spo.aeade_ventas_normalizado (marca, fecha, ventas, tipo)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (marca, fecha) DO UPDATE SET
        ventas = EXCLUDED.ventas,
        tipo = EXCLUDED.tipo;
"""

for fila in registros:
    cursor.execute(insert_query, (
        fila["marca"],
        fila["fecha"],
        fila["ventas"],
        fila["tipo"]
    ))

conn.commit()
print("✔ Inserción completada correctamente.")

# ============================================================
# 📌 CERRAR CONEXIÓN
# ============================================================

cursor.close()
conn.close()
print("🎉 Proceso finalizado. Datos listos en PostgreSQL.")
