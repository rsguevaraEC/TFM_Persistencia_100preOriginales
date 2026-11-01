import psycopg2
import pandas as pd
import json
from datetime import datetime
import random

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
subset_cols = ["persona_id_cliente", "correo_electronico", "telefono_movil"]
subset_cols = [c for c in subset_cols if c in df.columns]

df = df.drop_duplicates(subset=subset_cols, keep="first")

# ================================
# OBTENER CLIENTES EXISTENTES
# ================================
cur.execute("SELECT id_cliente FROM spo.clientes;")
ids_clientes = [row[0] for row in cur.fetchall()]

if not ids_clientes:
    raise ValueError("⚠ No existen clientes en spo.clientes. Inserta clientes primero.")

# ================================
# FUNCIÓN: DIVIDIR NOMBRE COMPLETO
# ================================
def dividir_nombre_completo(nombre_completo):
    partes = str(nombre_completo).strip().split()
    if len(partes) == 0:
        return "", ""
    if len(partes) == 1:
        return partes[0], ""
    if len(partes) == 2:
        return partes[0], partes[1]
    return " ".join(partes[:-2]), " ".join(partes[-2:])

# ================================
# FUNCIÓN: CONVERTIR FECHA
# ================================
def convertir_fecha(fecha_str):
    try:
        return datetime.strptime(fecha_str, "%d/%m/%Y")
    except:
        # Si la fecha no sirve, generar una aleatoria entre julio y octubre 2025
        return datetime(
            2025,
            random.choice([7, 8, 9, 10]),
            random.randint(1, 28),
            random.randint(0, 23),
            random.randint(0, 59)
        )

# ================================
# FUNCIÓN: INSERTAR LEAD
# ================================
def insertar_lead(row):
    try:
        nombre, apellido = dividir_nombre_completo(row.get("nombre_cliente"))

        metadata = json.dumps({
            "origen": "import_csv",
            "archivo": "data.csv"
        })

        contexto = json.dumps({
            "interes": random.choice(["Automotriz", "Consumo", "Educación", "Tecnología"])
        })

        fecha_registro = convertir_fecha(row.get("fec_comprobante"))
        fecha_actualizacion = fecha_registro

        cur.execute("""
            INSERT INTO spo.leads (
                lead_identificacion, lead_nombre, lead_apellido, lead_email,
                lead_telefono, lead_direccion, lead_ciudad, lead_pais,
                lead_fuente, lead_estado, lead_metadata, lead_contexto,
                fecha_registro, id_cliente, fecha_actualizacion
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            str(row.get("persona_id_cliente")),
            nombre,
            apellido,
            str(row.get("correo_electronico")),
            str(row.get("telefono_movil")),
            None,
            str(row.get("ciudad")),
            "Ecuador",
            random.choice(["Facebook", "Instagram", "Web", "Referido", "Evento"]),
            random.choice(["Nuevo", "Contactado", "Calificado", "Descartado"]),
            metadata,
            contexto,
            fecha_registro,
            random.choice(ids_clientes),
            fecha_actualizacion
        ))

    except Exception as e:
        print(f"Error en registro {row.get('persona_id_cliente')}: {e}")
        conn.rollback()  # ← CLAVE PARA EVITAR TRANSACCIÓN ABORTADA

# ================================
# INSERTAR TODOS LOS REGISTROS
# ================================
for _, row in df.iterrows():
    insertar_lead(row)

conn.commit()
cur.close()
conn.close()

print(f"✔ {len(df)} leads procesados e insertados correctamente (con rollback en errores).")
