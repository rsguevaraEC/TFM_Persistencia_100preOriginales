# Carga del dataset maestro AEADE en PostgreSQL (JSONB)

import json
import pandas as pd
import psycopg2
from psycopg2 import sql
from datetime import datetime
import numpy as np

# ============================
# CONFIGURACIÓN
# ============================

DATASET_FILE = "boletines_aeade\\tablas_aeade\\sondataset_aeade_filtrado.csv"

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="ASUS",
    port="5433"
)

cursor = conn.cursor()

SCHEMA_NAME = "spo"
TABLE_NAME = "aeade_boletines_json"

# ============================
# CREAR TABLA JSONB (si no existe)
# ============================

create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {}.{} (
        id SERIAL PRIMARY KEY,
        origen_pdf TEXT,
        tabla_numero INT,
        fecha_carga TIMESTAMP,
        contenido_json JSONB
    );
""").format(
    sql.Identifier(SCHEMA_NAME),
    sql.Identifier(TABLE_NAME)
)

cursor.execute(create_table_query)
conn.commit()
print(f"✔ Tabla {SCHEMA_NAME}.{TABLE_NAME} lista.")

# ============================
# CARGAR DATASET MAESTRO
# ============================

df = pd.read_csv(DATASET_FILE)

# Limpieza de valores
df = df.replace([np.nan, np.inf, -np.inf], None)

print(f"📄 Dataset cargado: {DATASET_FILE}")
print(f"📊 Total de registros: {len(df)}")

# ============================
# INSERTAR REGISTROS JSONB
# ============================

insertados = 0

insert_query = sql.SQL("""
    INSERT INTO {}.{} (origen_pdf, tabla_numero, fecha_carga, contenido_json)
    VALUES (%s, %s, %s, %s)
""").format(
    sql.Identifier(SCHEMA_NAME),
    sql.Identifier(TABLE_NAME)
)

for idx, row in df.iterrows():

    # Convertir fila completa a JSON
    contenido_json = json.dumps(row.to_dict(), ensure_ascii=False)

    # Metadatos
    origen_pdf = row.get("VENTAS_AAAA", "DESCONOCIDO")
    tabla_numero = row.get("tabla_numero", idx + 1)
    fecha_carga = datetime.now()

    cursor.execute(insert_query, (
        origen_pdf,
        tabla_numero,
        fecha_carga,
        contenido_json
    ))

    insertados += 1

print(f"✔ Registros insertados: {insertados}")

conn.commit()
cursor.close()
conn.close()

print("\n✅ Proceso completado: dataset maestro cargado en JSONB.")
