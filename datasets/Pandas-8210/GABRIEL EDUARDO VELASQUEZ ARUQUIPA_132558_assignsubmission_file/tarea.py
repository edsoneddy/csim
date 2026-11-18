import pandas as pd
exportaciones = pd.read_csv("EXPORTACIONES_ENERO_2026p.csv")
importaciones = pd.read_csv("IMPORTACIONES_ENE_2026p.csv")
print("Exportaciones por frontera (kilos):")
resultado1 = exportaciones.groupby("DESADU")["KILNET"].sum()
print(resultado1)
print("Importaciones por frontera (bolivianos):")
resultado2 = importaciones.groupby("DESADU")["ADU"].sum()
print(resultado2)
