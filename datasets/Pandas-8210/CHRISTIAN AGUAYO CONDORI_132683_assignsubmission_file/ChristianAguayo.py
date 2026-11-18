import pandas as pd

ARCHIVO_IMPORTACIONES = "IMPORTACIONES_ENE_2026p.csv"
ARCHIVO_EXPORTACIONES = "EXPORTACIONES_ENE_2026p.csv"
TIPO_CAMBIO = 6.96

def clasificar_frontera(descripcion):
    if pd.isna(descripcion):
        return "OTROS"
    texto = str(descripcion).upper()
    if "AEROPUERTO" in texto:
        return "AEROPUERTO"
    elif "DESAGUADERO" in texto:
        return "DESAGUADERO"
    elif "PISIGA" in texto:
        return "PISIGA"
    elif "YACUIBA" in texto:
        return "YACUIBA"
    elif "BERMEJO" in texto:
        return "BERMEJO"
    elif "VILLAZON" in texto or "VILLAZÓN" in texto:
        return "VILLAZON"
    elif "PUERTO SUAREZ" in texto or "PUERTO SUÁREZ" in texto:
        return "PUERTO SUAREZ"
    elif "TAMBO QUEMADO" in texto:
        return "TAMBO QUEMADO"
    elif "ARROYO CONCEPCION" in texto or "ARROYO CONCEPCIÓN" in texto:
        return "ARROYO CONCEPCION"
    elif "GUAYARAMERIN" in texto or "GUAYARAMERÍN" in texto:
        return "GUAYARAMERIN"
    elif "AVAROA" in texto:
        return "AVAROA"
    elif "VILLAMONTES" in texto:
        return "VILLAMONTES"
    elif "POSTAL" in texto:
        return "POSTAL"
    elif "INTERIOR" in texto:
        return "INTERIOR"
    else:
        return "OTROS"

importaciones = pd.read_csv(ARCHIVO_IMPORTACIONES, encoding="utf-8")
importaciones["FRONTERA"] = importaciones["DESADU"].apply(clasificar_frontera)
importaciones["ADU_BS"] = importaciones["ADU"] * TIPO_CAMBIO

importaciones_por_frontera = (
    importaciones
    .groupby("FRONTERA", as_index=False)["ADU_BS"]
    .sum()
    .sort_values("ADU_BS", ascending=False)
)

print("=" * 60)
print("Christian Aguayo Condori")
print("IMPORTACIONES POR FRONTERA (en Bolivianos)")
print("=" * 60)
print(importaciones_por_frontera.to_string(index=False))
print(f"\nTOTAL IMPORTADO: Bs {importaciones_por_frontera['ADU_BS'].sum():,.2f}")

try:
    exportaciones = pd.read_csv(ARCHIVO_EXPORTACIONES, encoding="utf-8")
    exportaciones["FRONTERA"] = exportaciones["DESADU"].apply(clasificar_frontera)
    exportaciones_por_frontera = (
        exportaciones
        .groupby("FRONTERA", as_index=False)["KILOS"]
        .sum()
        .sort_values("KILOS", ascending=False)
    )
    print("\n" + "=" * 60)
    print("EXPORTACIONES POR FRONTERA (en Kilos)")
    print("=" * 60)
    print(exportaciones_por_frontera.to_string(index=False))
    print(f"\nTOTAL EXPORTADO: {exportaciones_por_frontera['KILOS'].sum():,.2f} kg")
except FileNotFoundError:
    print("\n" + "=" * 60)
    print("EXPORTACIONES: archivo no encontrado.")
    print("=" * 60)