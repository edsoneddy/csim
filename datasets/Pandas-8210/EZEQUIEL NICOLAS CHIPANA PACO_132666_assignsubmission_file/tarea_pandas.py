import pandas as pd

exportaciones = pd.read_csv("EXPORTACIONES ENERO 2026p.csv", encoding="utf-8")
importaciones = pd.read_csv("IMPORTACIONES_ENE_2026p.csv", encoding="utf-8")

exp_por_frontera = exportaciones.groupby("DESADU")["KILNET"].sum()
exp_por_frontera = exp_por_frontera.sort_values(ascending=False)

imp_por_frontera = importaciones.groupby("DESADU")["FOB"].sum()
imp_por_frontera = imp_por_frontera.sort_values(ascending=False)

print("EXPORTACIONES POR FRONTERA (en kilos)")
print("-------------------------------------")
for frontera, kilos in exp_por_frontera.items():
    print(frontera, ":", round(kilos, 2), "kilos")

print()
print("IMPORTACIONES POR FRONTERA (en bolivianos)")
print("------------------------------------------")
for frontera, bolivianos in imp_por_frontera.items():
    print(frontera, ":", round(bolivianos, 2), "Bs")