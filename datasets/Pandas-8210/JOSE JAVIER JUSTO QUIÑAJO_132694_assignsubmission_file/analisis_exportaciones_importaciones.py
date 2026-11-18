import pandas as pd

# 1. Indicamos los nombres de los archivos CSV
archivo_exportaciones = "EXPORTACIONES ENERO 2026p.csv"
archivo_importaciones = "IMPORTACIONES_ENE_2026p.csv"

print("Cargando los datos, por favor espera...")

# 2. Leemos los archivos con pandas
df_expo = pd.read_csv(archivo_exportaciones, encoding="utf-8")
df_impo = pd.read_csv(archivo_importaciones, encoding="utf-8")

# 3. Sumar las exportaciones por frontera (kilos netos)
# Agrupamos por la columna 'DESADU' y sumamos 'KILNET'
expo_por_frontera = df_expo.groupby("DESADU")["KILNET"].sum()

# Ordenamos de mayor a menor
expo_por_frontera = expo_por_frontera.sort_values(ascending=False)

print("\n--- EXPORTACIONES POR FRONTERA (Kilos Netos) ---")
print(expo_por_frontera)


# 4. Sumar las importaciones por frontera (valor aduanero en bolivianos)
# Agrupamos por 'DESADU' y sumamos la columna 'ADU'
impo_por_frontera = df_impo.groupby("DESADU")["ADU"].sum()

# Ordenamos de mayor a menor
impo_por_frontera = impo_por_frontera.sort_values(ascending=False)

print("\n--- IMPORTACIONES POR FRONTERA (Bolivianos) ---")
# Mostramos los resultados uno por uno con un formato de dinero sencillo
for frontera, valor in impo_por_frontera.items():
    print(f"{frontera}: {valor:,.2f} Bs")
