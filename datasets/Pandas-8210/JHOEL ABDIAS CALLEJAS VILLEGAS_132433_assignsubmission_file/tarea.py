import pandas as pd

# Leer los archivos CSV
exportaciones = pd.read_csv("EXPORTACIONES ENERO 2026p.csv")
importaciones = pd.read_csv("IMPORTACIONES_ENE_2026p.csv")

# Sumamos los kilogramos exportados por frontera
total_exportaciones = exportaciones.groupby("DESADU")["KILNET"].sum()

# Sumamos los bolivianos importados por frontera
total_importaciones = importaciones.groupby("DESADU")["ADU"].sum()

# exportaciones
print("EXPORTACIONES POR FRONTERA (KG)")
print(total_exportaciones)

# importaciones
print("IMPORTACIONES POR FRONTERA (BS)")
print(total_importaciones)