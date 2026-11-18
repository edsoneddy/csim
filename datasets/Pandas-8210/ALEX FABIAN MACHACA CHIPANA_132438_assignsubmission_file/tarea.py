import pandas as pd

# Cargar archivos
exp = pd.read_csv('EXPORTACIONES ENERO 2026p.csv')
imp = pd.read_csv('IMPORTACIONES_ENE_2026p.csv')

# 1. Total exportado por frontera en kilos
totales_exp = exp.groupby('DESADU')['KILBRU'].sum()
print("EXPORTACIONES EN KILOS:")
print(totales_exp)

print("-" * 40)

# 2. Total importado por frontera en bolivianos
totales_imp = imp.groupby('DESADU')['ADU'].sum()
print("IMPORTACIONES EN BOLIVIANOS:")
print(totales_imp)