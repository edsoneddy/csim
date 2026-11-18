import pandas

exportar = pandas.read_csv('EXPORTACIONES ENERO 2026p.csv')
importar = pandas.read_csv('IMPORTACIONES_ENE_2026p.csv')

print("1. EXPORTACIONES POR FRONTERA (EN KILOS)")
tablas_de_exportar = exportar.groupby('DESADU')['KILNET'].sum()
print(tablas_de_exportar)

print("=========================================================")

print("2. IMPORTACIONES POR FRONTERA (EN BOLIVIANOS)")
tablas_de_importar = importar.groupby('DESADU')['ADU'].sum()
print(tablas_de_importar)