import pandas as pd
from pathlib import Path

# Los dos CSV deben estar en la misma carpeta que este programa.
carpeta = Path(__file__).resolve().parent
archivo_exportaciones = carpeta / "EXPORTACIONES ENERO 2026p.csv"
archivo_importaciones = carpeta / "IMPORTACIONES_ENE_2026p.csv"

# 1. Exportaciones por frontera: se utiliza KILNET (peso neto, en kilos).
exportaciones = pd.read_csv(archivo_exportaciones, encoding="utf-8")
exportaciones["KILNET"] = pd.to_numeric(exportaciones["KILNET"], errors="coerce").fillna(0)
resultado_exportaciones = exportaciones.groupby("DESADU")["KILNET"].sum().sort_values(ascending=False)

print("EXPORTACIONES POR FRONTERA (KILOS NETOS)")
print(resultado_exportaciones.to_string(float_format=lambda x: f"{x:,.2f}"))

# 2. Importaciones por frontera en bolivianos.
# En este archivo, ADU corresponde al valor aduanero expresado en bolivianos.
importaciones = pd.read_csv(archivo_importaciones, encoding="utf-8")
importaciones["ADU"] = pd.to_numeric(importaciones["ADU"], errors="coerce").fillna(0)
resultado_importaciones = importaciones.groupby("DESADU")["ADU"].sum().sort_values(ascending=False)

print("\nIMPORTACIONES POR FRONTERA (BOLIVIANOS)")
print(resultado_importaciones.to_string(float_format=lambda x: f"Bs {x:,.2f}"))
