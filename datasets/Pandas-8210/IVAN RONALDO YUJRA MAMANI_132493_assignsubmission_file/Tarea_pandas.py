''' Tarea Pandas - INF-111
Requiere EXPORTACIONES.csv e IMPORTACIONES.csv en la misma carpeta que este programa.
(se excluyen reexportaciones y efectos personales del archivo "EXPORTACIONES.csv").
'''
import pandas as pd

exp = pd.read_csv("EXPORTACIONES.csv", encoding="utf-8")
imp = pd.read_csv("IMPORTACIONES.csv", encoding="utf-8")

es_exportacion = exp["FLUJO"] == "1 EXPORTACIONES"
exp = exp[es_exportacion]

print("Exportaciones por frontera (kilos)")
kilos = exp.groupby("DESADU")[["KILNET", "KILBRU"]].sum()
for frontera, fila in kilos.iterrows():
    print(f"{frontera}: neto {fila['KILNET']:,.2f} | bruto {fila['KILBRU']:,.2f}")

print("Importaciones por frontera (bolivianos)")
bolivianos = imp.groupby("DESADU")["ADU"].sum()
for frontera, total in bolivianos.items():
    print(f"{frontera}: {total:,}")