import psycopg2
import pandas as pd

# ================================
# CONEXIÓN A POSTGRES
# ================================
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="ASUS",
    port="5433"
)
cur = conn.cursor()

# ================================
# CARGAR CSV
# ================================
df = pd.read_csv("c:/temp/data.csv", dtype=str)

# Normalizar encabezados
df.columns = [c.strip().lower() for c in df.columns]

# Reemplazar NaN por vacío
df = df.fillna("")

# ================================
# ELIMINAR DUPLICADOS
# ================================
subset_cols = ["persona_id_cliente"]
df = df.drop_duplicates(subset=subset_cols, keep="first")

# ================================
# ACTUALIZAR PROVINCIA EN LEADS
# ================================
def actualizar_provincia(row):
    try:
        identificacion = str(row.get("persona_id_cliente"))
        provincia = str(row.get("provincia"))

        cur.execute("""
            UPDATE spo.leads
            SET provincia = %s
            WHERE lead_identificacion = %s
        """, (provincia, identificacion))

    except Exception as e:
        print(f"Error actualizando {identificacion}: {e}")
        conn.rollback()  # ← evita abortar toda la transacción

# ================================
# PROCESAR TODAS LAS FILAS
# ================================
for _, row in df.iterrows():
    actualizar_provincia(row)

conn.commit()
cur.close()
conn.close()

print("✔ Provincia actualizada correctamente en spo.leads.")
