# cambio_usd_hoy_fallback.py
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import date
import pandas as pd

# === CONFIG POSTGRES ===
PG_HOST = "localhost"
PG_PORT = "5433"
PG_DB = "postgres"
PG_USER = "postgres"
PG_PASS = "ASUS"

# === PAÍSES A PROCESAR (códigos normalizados) ===
paises = ["BRA", "COL", "ECU"]  # añade o quita según necesites

# === MAPA DE MONEDAS ISO ===
monedas = {
    "BRA": "BRL",
    "COL": "COP",
    "ARG": "ARS",
    "BOL": "BOB",
    "CHL": "CLP",
    "PER": "PEN",
    "PRY": "PYG",
    "URY": "UYU",
    # ECU se trata como USD
}

# === FECHA HOY ===
hoy = date.today().strftime("%Y-%m-%d")

# === FUNCIONES PARA CONSULTAR PROVEEDORES ===
def trm_exchangerate_host(moneda):
    """Proveedor principal: exchangerate.host (endpoint latest)."""
    url = f"https://api.exchangerate.host/latest?base={moneda}&symbols=USD"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "rates" in data and "USD" in data["rates"]:
            rate = data["rates"]["USD"]
            if rate and rate != 0:
                return float(rate)
    except Exception:
        return None
    return None

def trm_open_er_api(moneda):
    """Fallback: open.er-api.com (sin clave)."""
    url = f"https://open.er-api.com/v6/latest/{moneda}"
    try:
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        data = r.json()
        # estructura: { "result":"success", "rates": { "USD": 0.19, ... } }
        if isinstance(data, dict) and "rates" in data and "USD" in data["rates"]:
            rate = data["rates"]["USD"]
            if rate and rate != 0:
                return float(rate)
    except Exception:
        return None
    return None

def obtener_trm_con_fallback(pais):
    """Intenta proveedores en orden y devuelve la TRM o None."""
    if pais == "ECU":
        return 1.0
    moneda = monedas.get(pais)
    if not moneda:
        print(f"⚠ Moneda no definida para {pais}")
        return None

    # 1) Proveedor principal
    rate = trm_exchangerate_host(moneda)
    if rate:
        return rate

    # 2) Fallback
    rate = trm_open_er_api(moneda)
    if rate:
        return rate

    # Si quieres, aquí puedes añadir más proveedores
    print(f"⚠ No se obtuvo TRM para {pais} desde los proveedores configurados")
    return None

# === RECOLECTAR TRMs (sin tocar la BD aún) ===
filas = []
errores = []
for p in paises:
    trm = obtener_trm_con_fallback(p)
    if trm is None:
        errores.append(p)
    else:
        # valor_local y valor_usd quedan NULL; solo guardamos la TRM del día
        filas.append((p, hoy, None, trm, None))

# === Si no hay TRMs válidas, abortar para no truncar la tabla ===
if not filas:
    print("✖ No se obtuvo ninguna TRM válida. No se modificará spo.cambio_usd.")
    if errores:
        print("Países sin TRM:", errores)
    raise SystemExit(1)

# === CONEXIÓN A POSTGRES Y TRUNCATE + INSERT EN TRANSACCIÓN ===
conn = psycopg2.connect(
    host=PG_HOST, port=PG_PORT, database=PG_DB, user=PG_USER, password=PG_PASS
)
conn.set_client_encoding('UTF8')
cur = conn.cursor()

try:
    # TRUNCATE y reiniciar serial
    cur.execute("TRUNCATE TABLE spo.cambio_usd RESTART IDENTITY;")

    insert_sql = """
    INSERT INTO spo.cambio_usd (pais, fecha, valor_local, trm_usd, valor_usd)
    VALUES %s
    """
    execute_values(cur, insert_sql, filas)
    conn.commit()
    print(f"✔ Tabla spo.cambio_usd actualizada con {len(filas)} filas. Fecha: {hoy}")
    if errores:
        print(f"⚠ No se obtuvieron TRM para: {errores}")
except Exception as e:
    conn.rollback()
    print("✖ Error durante TRUNCATE/INSERT:", e)
finally:
    cur.close()
    conn.close()
