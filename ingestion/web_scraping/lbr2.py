import zipfile
import pandas as pd
import os

# ==============================================================================
# 1. CONFIGURACIÓN DE CARPETAS Y RUTAS LOCALES (Tu PC)
# ==============================================================================
carpeta_origen = "data_raw"
nombre_zip = "latinobarometro_2024.zip"  
archivo_zip_completo = os.path.join(carpeta_origen, nombre_zip)

carpeta_extraccion = os.path.join(carpeta_origen, "ltbaro")

# Nombre del nuevo archivo CSV que indicas
archivo_csv_interno = "Latinobarometro_2024_Csv_esp_v20250817.csv"
archivo_csv_completo = os.path.join(carpeta_extraccion, archivo_csv_interno)


# ==============================================================================
# 2. DESCOMPRESIÓN AUTOMÁTICA DEL ARCHIVO ZIP
# ==============================================================================
if os.path.exists(archivo_zip_completo):
    print(f"Buscando archivo ZIP en: {archivo_zip_completo}...")
    print("Descomprimiendo archivos en data_raw\\ltbaro...")
    with zipfile.ZipFile(archivo_zip_completo, 'r') as zip_ref:
        zip_ref.extractall(carpeta_extraccion)
    print("¡Archivos extraídos correctamente!\n")
else:
    print(f"Error: No se encontró el archivo ZIP en la ruta '{archivo_zip_completo}'")


# ==============================================================================
# 3. DICCIONARIO DE CÓDIGOS PARA FILTRAR SUDAMÉRICA
# ==============================================================================
codigos_paises = {
    32: "ARG",   # Argentina
    68: "BOL",   # Bolivia
    76: "BRA",   # Brasil
    152: "CHL",  # Chile
    170: "COL",  # Colombia
    218: "ECU",  # Ecuador
    600: "PRY",  # Paraguay
    604: "PER",  # Perú
    858: "URY"   # Uruguay
}


# ==============================================================================
# 4. LECTURA, FILTRADO Y PROCESAMIENTO REVISADO
# ==============================================================================
if os.path.exists(archivo_csv_completo):
    print(f"Cargando el archivo local: {archivo_csv_interno}...")
    
    # Diagnóstico automático del separador del CSV (';' o ',')
    df_test = pd.read_csv(archivo_csv_completo, nrows=2)
    separador = ';' if len(df_test.columns) <= 1 else ','
    print(f"-> Separador detectado: '{separador}'")
    
    # Carga completa del archivo original en Pandas
    df = pd.read_csv(archivo_csv_completo, sep=separador, low_memory=False)
    
    # Normalizar cabeceras (Minúsculas y sin espacios fantasmas)
    df.columns = df.columns.str.lower().str.strip()
    
    # Columna base de país en este nuevo archivo
    columna_pais = 'idenpa'
    
    if columna_pais in df.columns:
        print(f"-> ¡Columna de control '{columna_pais}' localizada exitosamente!")
        
        # Primero filtramos las filas por tus países de interés de Sudamérica
        codigos_numericos = list(codigos_paises.keys())
        df_sudamerica = df[df[columna_pais].isin(codigos_numericos)].copy()
        
        # ==========================================================================
        # 5. MAPEO EXCLUSIVO DE VARIABLES CON LA NUEVA NOMENCLATURA 2024
        # ==========================================================================
        columnas_interes = {
            'idenpa': 'idenpa',
            'numinves': 'id_encuesta',
            's18.a': 'situacion_laboral',     # Nueva nomenclatura con punto '.'
            's4': 'miedo_desempleo',           # Nueva variable fija del cuestionario
            'p6stgbs': 'percepcion_eco_pais',
            'p9stgbs': 'percepcion_eco_hogar',
            'p17st': 'justicia_ingresos',
            'p2st': 'progreso_pais',
            'p7stgbs': 'eco_pais_pasado',
            'p8st': 'eco_pais_futuro',
            'reg': 'provincia_estado',
            'tamciud': 'tamano_ciudad',        # Nueva nomenclatura con 'd' al final
            'sexo': 'genero',
            'edad': 'edad'
        }
        
        # Validamos cuáles de estas variables en minúsculas existen en el DataFrame
        columnas_validas = {orig: nuevo for orig, nuevo in columnas_interes.items() if orig in df_sudamerica.columns}
        
        print(f"-> Columnas localizadas para exportar: {len(columnas_validas)} de {len(columnas_interes)}")
        
        if len(columnas_validas) > 0:
            # Extraemos las columnas seleccionadas
            df_final = df_sudamerica[list(columnas_validas.keys())].copy()
            
            # Renombramos a tus variables descriptivas en español
            df_final.rename(columns=columnas_validas, inplace=True)
            
            # Crear la columna calculada con las siglas legibles (ARG, ECU, etc.)
            df_final['pais_sigla'] = df_final['idenpa'].map(codigos_paises)
            
            # Reordenar las columnas para dejar los datos geográficos al inicio
            columnas_ordenadas = ['pais_sigla', 'provincia_estado', 'tamano_ciudad'] + \
                                 [col for col in df_final.columns if col not in ['pais_sigla', 'provincia_estado', 'tamano_ciudad', 'idenpa']]
            df_exportar = df_final[columnas_ordenadas]
            
            # ==========================================================================
            # 6. SALIDA EN CONSOLA Y EXPORTACIÓN FINAL
            # ==========================================================================
            print("\n" + "="*50)
            print("   PROCESAMIENTO POR PAÍS COMPLETADO EXITOSAMENTE")
            print("="*50)
            print(df_exportar['pais_sigla'].value_counts())
            print("-"*50)
            print(f"Total de registros filtrados para Sudamérica: {df_exportar.shape[0]}")
            print(f"Columnas optimizadas integradas: {df_exportar.shape[1]}")
            print("="*50)
            
            # Guardar el archivo estructurado directamente en la raíz de tu proyecto
            archivo_salida = "data_raw\latinobarometro_2024_economico_sudamerica.csv"
            df_exportar.to_csv(archivo_salida, index=False, encoding='utf-8')
            print(f"\n¡Éxito! Tu dataset limpio y filtrado se guardó como: '{archivo_salida}'")
        else:
            print("\nERROR: No se pudo mapear ninguna variable de la lista.")
    else:
        print(f"\nERROR: No se encontró la columna '{columna_pais}' en el archivo.")
else:
    print(f"Error Crítico: No se encontró el archivo CSV en la ruta especificada: {archivo_csv_completo}")