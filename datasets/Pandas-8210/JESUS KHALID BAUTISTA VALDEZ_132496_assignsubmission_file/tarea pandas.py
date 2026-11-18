import pandas as pd

# Archivos CSV: deben estar en la misma carpeta que este programa.
archivo_exportaciones = "EXPORTACIONES ENERO 2026p.csv"
archivo_importaciones = "IMPORTACIONES_ENE_2026p.csv"

# Leer los datos
exportaciones = pd.read_csv(archivo_exportaciones, encoding="utf-8")
importaciones = pd.read_csv(archivo_importaciones, encoding="utf-8")

# 1. Exportaciones por frontera en kilos netos
exportaciones_por_frontera = (
    exportaciones.groupby("DESADU")["KILNET"]
    .sum()
    .sort_values(ascending=False)
)

print("\nEXPORTACIONES POR FRONTERA (KILOS NETOS)")
print(exportaciones_por_frontera.to_string())

# 2. Importaciones por frontera en bolivianos
# En el archivo de importaciones, la columna ADU contiene el valor aduanero.
importaciones_por_frontera = (
    importaciones.groupby("DESADU")["ADU"]
    .sum()
    .sort_values(ascending=False)
)

print("\nIMPORTACIONES POR FRONTERA (BOLIVIANOS)")
print(importaciones_por_frontera.map(lambda x: f"{x:,.2f} Bs").to_string())
