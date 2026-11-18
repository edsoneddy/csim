import pandas as pd

exp = pd.read_csv("EXPORTACIONES ENERO 2026p.csv")
imp = pd.read_csv("IMPORTACIONES_ENE_2026p.csv")

print("Exportaciones por frontera (kilos)")
print(exp.groupby("DESADU")["KILNET"].sum().sort_values(ascending=False))

imp["DESADU"] = imp["DESADU"].apply(lambda x: x.encode("latin-1").decode("cp850"))

imp = imp[imp["DESADU"].str.startswith(("Frontera", "Aeropuerto"))]

print("\nImportaciones por frontera (bolivianos)")
print(imp.groupby("DESADU")["ADU"].sum().sort_values(ascending=False))
