from pathlib import Path
import pandas as pd

carpeta = Path(__file__).resolve().parent
carpeta_datos = Path.home() / "Downloads" / "tareaPandas" / "tareaPandas"

archivo_exportaciones = carpeta / "EXPORTACIONES ENERO 2026p.csv"
archivo_importaciones = carpeta / "IMPORTACIONES_ENE_2026p.csv"

if not archivo_exportaciones.exists():
    archivo_exportaciones = carpeta_datos / "EXPORTACIONES ENERO 2026p.csv"
if not archivo_importaciones.exists():
    archivo_importaciones = carpeta_datos / "IMPORTACIONES_ENE_2026p.csv"

exportaciones = pd.read_csv(archivo_exportaciones, encoding="utf-8")
importaciones = pd.read_csv(archivo_importaciones, encoding="utf-8")

exportaciones["KILBRU"] = pd.to_numeric(exportaciones["KILBRU"], errors="coerce").fillna(0)
importaciones["ADU"] = pd.to_numeric(importaciones["ADU"], errors="coerce").fillna(0)

kilos_por_frontera = exportaciones.groupby("DESADU")["KILBRU"].sum().sort_index()
bolivianos_por_frontera = importaciones.groupby("DESADU")["ADU"].sum().sort_index()

print("EXPORTACIONES POR FRONTERA (kilos brutos)")
for frontera, total in kilos_por_frontera.items():
    print(f"{frontera}: {total:,.2f} kg")

print("\nIMPORTACIONES POR FRONTERA (bolivianos)")
for frontera, total in bolivianos_por_frontera.items():
    print(f"{frontera}: Bs {total:,.2f}")