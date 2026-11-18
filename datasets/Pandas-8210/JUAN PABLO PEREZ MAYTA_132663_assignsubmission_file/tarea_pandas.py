import pandas as pd

df = pd.read_excel('exportaciones_enero_2026.xlsx')

total_fob = df['VALOR FOB'].sum()
total_peso = df['PESO NETO'].sum()
total_operaciones = len(df)

print(total_fob)
print(total_peso)
print(total_operaciones)

por_departamento = df.groupby('DEPARTAMENTO DE ORIGEN')['VALOR FOB'].sum()
print(por_departamento)

por_pais = df.groupby('PAÍS DESTINO')['VALOR FOB'].sum()
top_5_paises = por_pais.sort_values(ascending=False).head(5)
print(top_5_paises)

top_5_paises.to_excel('Resultado_Exportaciones.xlsx')
