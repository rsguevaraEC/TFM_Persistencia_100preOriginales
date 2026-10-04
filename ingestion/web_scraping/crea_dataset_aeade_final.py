import os
import re
import json
import pandas as pd

# ============================================================
# 📌 CONFIGURACIÓN DE RUTAS
# ============================================================

ruta = r"C:/Users/Asus/OneDrive/Isabel I/TFM_Persistencia_100preOriginales/proyecto/ingestion/web_scraping/tablas_aeade"
salida = os.path.join(ruta, "dataset_maestro_aeade_final.json")

# ============================================================
# 📌 FUNCIONES AUXILIARES
# ============================================================

def detectar_anios(nombre_archivo):
    """Extrae los dos años del nombre del archivo."""
    match = re.findall(r"(20\d{2})", nombre_archivo)
    return list(map(int, match)) if match else []

def limpiar_dataframe(df):
    """Elimina fila de totales y filas vacías."""
    df = df[~df.iloc[:,0].astype(str).str.contains("Total", case=False, na=False)]
    df = df.dropna(how="all")
    return df

# ============================================================
# 📌 DETECTAR ARCHIVOS CSV VÁLIDOS
# ============================================================

archivos = [f for f in os.listdir(ruta) if f.endswith(".csv")]

archivos_validos = []
for f in archivos:
    anios = detectar_anios(f)
    if len(anios) == 2:
        archivos_validos.append(f)

print("📌 Archivos válidos:", archivos_validos)

# ============================================================
# 📌 CONSTRUIR JSON MAESTRO POR AÑO
# ============================================================

json_final = {}

for archivo in archivos_validos:
    ruta_archivo = os.path.join(ruta, archivo)

    try:
        df = pd.read_csv(ruta_archivo, encoding="utf-8-sig", sep=",", engine="python")

        if df.empty:
            print(f"⚠ CSV vacío: {archivo}")
            continue

        anios = detectar_anios(archivo)
        anio_reciente = max(anios)

        df = limpiar_dataframe(df)

        if df.empty:
            print(f"⚠ CSV sin datos útiles después de limpiar: {archivo}")
            continue

        registros = df.to_dict(orient="records")
        #json_final[str(anio_reciente)] = registros
    
        # Guardar ambos años (anterior y reciente)
        for anio in anios:
            json_final[str(anio)] = registros


        print(f"✅ Migrado año {anio_reciente} desde {archivo}")

    except Exception as e:
        print(f"❌ Error leyendo {archivo}: {e}")

# Guardar JSON maestro
with open(salida, "w", encoding="utf-8") as f:
    json.dump(json_final, f, ensure_ascii=False, indent=4)

print("🎉 JSON maestro creado correctamente en:")
print(salida)

# ============================================================
# 🔥 NORMALIZACIÓN AUTOMÁTICA 
# ============================================================

with open(salida, "r", encoding="utf-8") as f:
    data = json.load(f)

normalizado = []

def procesar_registro(marca, anio, dic, acum, mes_num):
    """Convierte un registro en dos filas normalizadas."""
    if dic is not None:
        normalizado.append({
            "marca": marca,
            "fecha": f"{anio}-{mes_num:02d}-01",
            "ventas": dic,
            "tipo": "mes"
        })
    if acum is not None:
        normalizado.append({
            "marca": marca,
            "fecha": f"{anio}-{mes_num:02d}-28",
            "ventas": acum,
            "tipo": "acumulado"
        })


# ============================================================
# 🔍 PROCESAR AÑO 2019 (DICIEMBRE)
# ============================================================

if "2019" in data:
    for fila in data["2019"]:
        marca = fila.get("Marcas") or fila.get("Marca")

        dic_19 = fila.get("dic-19")
        acum_19 = fila.get("Ene - Dic 2019")

        if dic_19 is not None or acum_19 is not None:
            procesar_registro(marca, 2019, dic_19, acum_19, 12)


# ============================================================
# 🔍 PROCESAR AÑOS 2020–2025 (DICIEMBRE)
# ============================================================

for anio in range(2020, 2026):
    if str(anio) not in data:
        continue

    for fila in data[str(anio)]:
        marca = fila.get("Marcas") or fila.get("Marca")

        dic_actual = fila.get(f"dic-{anio}") or fila.get(f"{anio} Diciembre")
        acum_actual = (
            fila.get(f"Ene - Dic {anio}") or
            fila.get(f"{anio} Ene - Dic") or
            fila.get(f"Ene-Dic {anio}")
        )

        procesar_registro(marca, anio, dic_actual, acum_actual, 12)

# ============================================================
# 🔍 PROCESAR AÑO 2026 (AGOSTO)
# ============================================================

if "2026" in data:
    for fila in data["2026"]:
        marca = fila.get("Marca")

        dic_26 = fila.get("ago-26")
        acum_26 = fila.get("Ene-Ago 26")

        procesar_registro(marca, 2026, dic_26, acum_26, 8)

# ============================================================
# 💾 GUARDAR JSON NORMALIZADO
# ============================================================

salida_normalizado = salida.replace(".json", "_normalizado.json")

with open(salida_normalizado, "w", encoding="utf-8") as f:
    json.dump({"data": normalizado}, f, ensure_ascii=False, indent=4)

print("✅ JSON normalizado creado en:")
print(salida_normalizado)
