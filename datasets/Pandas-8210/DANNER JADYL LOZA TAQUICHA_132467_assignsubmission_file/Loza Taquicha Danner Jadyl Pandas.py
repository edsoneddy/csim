import pandas as pd

exp = pd.read_csv("EXPORTACIONES ENERO 2026p.csv")
imp = pd.read_csv("IMPORTACIONES_ENE_2026p.csv")

kilos = exp.groupby("DESADU")["KILNET"].sum()
print("Exportaciones por frontera (kilos)")
print(kilos)
print()

bs = imp.groupby("DESADU")["ADU"].sum()
print("Importaciones por frontera (bolivianos)")
print(bs)
