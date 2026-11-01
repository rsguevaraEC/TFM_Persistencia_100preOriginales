# cambio_usd_hoy_multi.py
import os
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import date

# === CONFIG POSTGRES ===
PG_HOST = "localhost"
PG_PORT = "5433"
PG_DB = "postgres"
PG_USER = "postgres"
PG_PASS = "ASUS"

# === Lista de países: si quieres tomarla desde la BD, ver nota abajo ===
paises = ["BRA", "COL", "ECU", "ARG", "BOL", "CHL", "PER", "PRY", "URY"]

# === Mapa moneda ISO ===
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

hoy = date.today().strftime("%Y-%m-%d")

# === LEE ACCESS KEY (opcional) para exchangerate.host desde variable de entorno ===
EXR_KEY = os.getenv("EXR_KEY")  # define EXR_KEY en tu entorno si la tienes

# === PROVEEDOR 1: exchangerate.host (con opción access_key) ===
def trm_exchangerate_host(moneda):
    # intento directo base=MONEDA
    params = {"base": moneda, "symbols": "USD"}
    if EXR_KEY:
        params["access_key"] = EXR_KEY
    url = "https://api.exchangerate.host/latest"
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "rates" in data and "USD" in data["rates"]:
            rate = data["rates"]["USD"]
            if rate and rate != 0:
                return float(rate)
    except Exception:
        pass
    # intento inverso: base=USD -> moneda  => TRM = 1 / rate_usd_to_moneda
    try:
        params2 = {"base": "USD", "symbols": moneda}
        if EXR_KEY:
            params2["access_key"] = EXR_KEY
        r2 = requests.get(url, params=params2, timeout=8)
        r2.raise_for_status()
        d2 = r2.json()
        if isinstance(d2, dict) and "rates" in d2 and moneda in d2["rates"]:
            r_usd_to_mon = d2["rates"][moneda]
            if r_usd_to_mon and r_usd_to_mon != 0:
                return float(1.0 / r_usd_to_mon)
    except Exception:
        pass
    return None

# === PROVEEDOR 2: open.er-api.com (estructura rates) ===
def trm_open_er_api(moneda):
    # intento directo: endpoint devuelve rates con base=moneda en la ruta
    try:
        url = f"https://open.er-api.com/v6/latest/{moneda}"
        r = requests.get(url, timeout=8)
        r.raise_for_status()
        data = r.json()
        if isinstance(data, dict) and "rates" in data and "USD" in data["rates"]:
            rate = data["rates"]["USD"]
            if rate and rate != 0:
                return float(rate)
    except Exception:
        pass
    # intento inverso: pedir latest/USD y buscar moneda
    try:
        url2 = "https://open.er-api.com/v6/latest/USD"
        r2 = requests.get(url2, timeout=8)
        r2.raise_for_status()
        d2 = r2.json()
        if isinstance(d2, dict) and "rates" in d2 and moneda in d2["rates"]:
            r_usd_to_mon = d2["rates"][moneda]
            if r_usd_to_mon and r_usd_to_mon != 0:
                return float(1.0 / r_usd_to_mon)
    except Exception:
        pass
    return None

# === Añade aquí más proveedores si quieres ===

def obtener_trm_con_fallback(pais):
    if pais == "ECU":
        return 1.0
    moneda = monedas.get(pais)
    if not moneda:
        print(f"⚠ Moneda no definida para {pais}")
        return None

    # 1) exchangerate.host (con key si la tienes)
    rate = trm_exchangerate_host(moneda)
    if rate:
        return rate

    # 2) open.er-api.com
    rate = trm_open_er_api(moneda)
    if rate:
        return rate

    # 3) si quieres, añadir más proveedores aquí

    print(f"⚠ No se obtuvo TRM para {pais} desde los proveedores configurados")
    return None

def main():
    filas = []
    errores = []
    for p in paises:
        trm = obtener_trm_con_fallback(p)
        if trm is None:
            errores.append(p)
        else:
            filas.append((p, hoy, None, trm, None))

    if not filas:
        print("✖ No se obtuvo ninguna TRM válida. No se modificará spo.cambio_usd.")
        if errores:
            print("Países sin TRM:", errores)
        return

    conn = psycopg2.connect(host=PG_HOST, port=PG_PORT, database=PG_DB, user=PG_USER, password=PG_PASS)
    conn.set_client_encoding('UTF8')
    cur = conn.cursor()
    try:
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

if __name__ == "__main__":
    main()
