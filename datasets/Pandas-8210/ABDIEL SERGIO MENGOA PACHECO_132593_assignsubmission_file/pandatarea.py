import pandas as pd

exp = pd.read_csv('tareaPandas/EXPORTACIONES ENERO 2026p.csv')
imp = pd.read_csv('tareaPandas/IMPORTACIONES_ENE_2026p.csv')

print(exp.head())
print(imp.head())

print(exp.info())
print(imp.info())

col_val_exp = exp.columns[-1]
col_val_imp = imp.columns[-1]

total_exp = exp[col_val_exp].sum()
total_imp = imp[col_val_imp].sum()
balanza = total_exp - total_imp

print("Total Exportaciones:", total_exp)
print("Total Importaciones:", total_imp)
print("Balanza Comercial:", balanza)

resumen = pd.DataFrame({
    'Tipo': ['Exportaciones', 'Importaciones', 'Balanza Comercial'],
    'Monto': [total_exp, total_imp, balanza]
})

resumen.to_csv('resultado_final.csv', index=False)
