
import pandas as pd


exportaciones = pd.read_csv("EXPORTACIONES ENERO 2026p.csv", encoding="utf-8")
importaciones = pd.read_csv("IMPORTACIONES_ENE_2026p.csv", encoding="utf-8")


exportaciones["KILNET"] = pd.to_numeric(
    exportaciones["KILNET"], errors="coerce"
).fillna(0)

total_exportaciones = exportaciones.groupby("DESADU")["KILNET"].sum()

print("EXPORTACIONES POR FRONTERA (kilos netos)")
print(total_exportaciones.to_string())


importaciones["ADU"] = pd.to_numeric(
    importaciones["ADU"], errors="coerce"
).fillna(0)

total_importaciones = importaciones.groupby("DESADU")["ADU"].sum()

print("\nIMPORTACIONES POR FRONTERA (bolivianos)")
print(total_importaciones.to_string())
