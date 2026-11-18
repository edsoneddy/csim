import pandas as pd
# EXPORTACIONES POR CADA FRONTERA EN KILOS BRUTOS
expor = pd.read_csv('EXPORTACIONES ENERO 2026p.csv', encoding='utf-8')
tablas_exp = expor.groupby('DESADU')
pd.options.display.float_format = "{:.2f} kilos brutos".format
print(tablas_exp['KILBRU'].sum())
print("\n" + "="*50 + "\n")

# IMPORTACIONES POR CADA FRONTERA EN BOLIVIANOS
impor = pd.read_csv('IMPORTACIONES_ENE_2026p.csv', encoding='utf-8')
tablas_imp = impor.groupby('DESADU')
pd.options.display.float_format = "{:.2f} bolivianos".format
print(tablas_imp['ADU'].sum())