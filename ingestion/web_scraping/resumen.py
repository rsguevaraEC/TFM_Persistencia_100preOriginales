import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------
# 1. Cargar archivo final ya unificado
# ---------------------------------------------------------
df = pd.read_csv("data_raw/union_final.csv")

print("✔ Archivo final cargado correctamente")
print(df.head())

# ---------------------------------------------------------
# 2. Resumen estadístico general
# ---------------------------------------------------------
print("\n================ RESUMEN ESTADÍSTICO ================\n")

# describe() sin datetime_is_numeric
resumen = df.describe(include="all")

print(resumen)

# Guardar resumen en CSV
resumen.to_csv("data_raw/resumen_estadistico.csv", index=True)
print("\n✔ Resumen estadístico guardado en data_raw/resumen_estadistico.csv")

# ---------------------------------------------------------
# 3. Tabla resumen por fuente
# ---------------------------------------------------------
print("\n================ RESUMEN POR FUENTE ================\n")

tabla_fuente = df["fuente"].value_counts().reset_index()
tabla_fuente.columns = ["fuente", "cantidad_registros"]

print(tabla_fuente)

tabla_fuente.to_csv("data_raw/resumen_por_fuente.csv", index=False)
print("\n✔ Tabla por fuente guardada en data_raw/resumen_por_fuente.csv")

# ---------------------------------------------------------
# 4. Gráfico alternativo: barras del tamaño de cada dataset
# ---------------------------------------------------------
# Sort the data by 'cantidad_registros' for better visualization
tabla_fuente_sorted = tabla_fuente.sort_values(by='cantidad_registros', ascending=False)

plt.figure(figsize=(12, 8)) # Increase figure size for better readability
sns.barplot(data=tabla_fuente_sorted, y='fuente', x='cantidad_registros', palette='viridis')
plt.title('Cantidad de Registros por Fuente de Datos')
plt.xlabel('Cantidad de Registros')
plt.ylabel('Fuente de Datos')
plt.tight_layout() # Adjust layout to prevent labels from being cut off
plt.savefig('data_raw/grafico_conteo_fuentes.png')
plt.show()
plt.close() # Close the figure to free up memory

print('✔ Gráfico de conteo de fuentes guardado en data_raw/grafico_conteo_fuentes.png')

# ---------------------------------------------------------------
# 5. Gráfico adicional: proporción de registros tabla porcentual
# --------------------------------------------------------------

# Cargar el dataset final
df_final = pd.read_csv("data_raw/union_final.csv", encoding="utf-8-sig")

# Calcular proporción por fuente
fuente_counts = df_final["fuente"].value_counts(normalize=True) * 100

# Configuración del gráfico
plt.figure(figsize=(10, 6))
bars = plt.barh(fuente_counts.index, fuente_counts, color=plt.cm.PuBuGn(range(len(fuente_counts))))

# Etiquetas y formato
plt.title("Proporción de registros por fuente", fontsize=14, fontweight="bold", pad=20)
plt.xlabel("Porcentaje de registros (%)", fontsize=12)
plt.ylabel("Fuente de datos", fontsize=12)
plt.grid(axis="x", linestyle="--", alpha=0.6)

# Mostrar valores sobre las barras
for bar in bars:
    plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
             f"{bar.get_width():.1f}%", va="center", fontsize=10)

plt.tight_layout()
plt.savefig("data_raw/grafico_proporcion_fuentes_barras.png", dpi=300)
print('✔ Gráfico de proporciones guardado en data_raw/grafico_proporcion_fuentes_barras.png')
plt.show()
plt.close()
