#graba en la base de datos PostgreSQL el dataset maestro de la AEADE - modelo estructural
import os
import pandas as pd
import psycopg2
from psycopg2 import sql

# ============================
# CONFIGURACIÓN
# ============================

INPUT_FOLDER = "boletines_aeade/tablas_aeade"
INPUT_FILE = os.path.join(INPUT_FOLDER, "dataset_maestro_aeade_limpio.csv")

# Conexión a PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="ASUS",
    port="5433"
)

cursor = conn.cursor()

SCHEMA_NAME = "spo"
TABLE_NAME = "aeade_boletines"

# ============================
# CARGAR DATASET
# ============================

df = pd.read_csv(INPUT_FILE)
print(f"Dataset cargado: {df.shape[0]} filas, {df.shape[1]} columnas")

# ============================
# CREAR TABLA DINÁMICAMENTE
# ============================

column_defs = []
for col in df.columns:
    if df[col].dtype in ["float64", "int64"]:
        column_defs.append(sql.SQL("{} DOUBLE PRECISION").format(sql.Identifier(col)))
    else:
        column_defs.append(sql.SQL("{} TEXT").format(sql.Identifier(col)))

create_table_query = sql.SQL("""
    CREATE TABLE IF NOT EXISTS {}.{} (
        id SERIAL PRIMARY KEY,
        {}
    );
""").format(
    sql.Identifier(SCHEMA_NAME),
    sql.Identifier(TABLE_NAME),
    sql.SQL(", ").join(column_defs)
)

cursor.execute(create_table_query)
conn.commit()
print(f"✔ Tabla '{SCHEMA_NAME}.{TABLE_NAME}' creada o ya existente.")

# ============================
# INSERTAR DATOS
# ============================

cols = list(df.columns)

insert_query = sql.SQL("""
    INSERT INTO {}.{} ({})
    VALUES ({})
""").format(
    sql.Identifier(SCHEMA_NAME),
    sql.Identifier(TABLE_NAME),
    sql.SQL(", ").join(map(sql.Identifier, cols)),
    sql.SQL(", ").join(sql.Placeholder() * len(cols))
)

for _, row in df.iterrows():
    cursor.execute(insert_query, tuple(row.values))

conn.commit()
print(f"✔ {df.shape[0]} registros insertados en '{SCHEMA_NAME}.{TABLE_NAME}'.")

# ============================
# CERRAR CONEXIÓN
# ============================

cursor.close()
conn.close()
print("Proceso completado.")
