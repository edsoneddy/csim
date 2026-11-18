import pandas as pd

# Leer el archivo de exportaciones
df = pd.read_excel("exportaciones_enero_2026.xlsx")

# Calcular los totales generales
total_fob = df["VALOR FOB"].sum()
total_peso = df["PESO NETO"].sum()
total_operaciones = len(df)

print("TOTAL VALOR FOB:", total_fob)
print("TOTAL PESO NETO:", total_peso)
print("TOTAL DE OPERACIONES:", total_operaciones)

# Calcular el valor FOB total por departamento de origen
por_departamento = df.groupby("DEPARTAMENTO DE ORIGEN")["VALOR FOB"].sum()
print("\nVALOR FOB POR DEPARTAMENTO DE ORIGEN:")
print(por_departamento)

# Obtener los cinco países de destino con mayor valor FOB
por_pais = df.groupby("PAÍS DESTINO")["VALOR FOB"].sum()
top_5_paises = por_pais.sort_values(ascending=False).head(5)
print("\nTOP 5 PAÍSES DE DESTINO POR VALOR FOB:")
print(top_5_paises)

# Guardar los resultados en un archivo Excel
top_5_paises.to_excel("Resultado_Exportaciones.xlsx")

print("\nLos resultados se guardaron en Resultado_Exportaciones.xlsx")
