import pandas as pd
pd.options.display.float_format='{:,.2f}'.format
df_importaciones = pd.read_csv('IMPORTACIONES_ENE_2026p.csv',encoding='utf-8')
df_exportaciones= pd.read_csv('EXPORTACIONES ENERO 2026p.csv',encoding='utf-8')
#exportaciones en kilos
df_exportaciones['Frontera']=df_exportaciones['DESADU']
df_exportaciones['Kilos']=df_exportaciones['KILNET']
resul_exp=df_exportaciones.groupby(by='Frontera',as_index=False,sort=False)['Kilos'].sum()
#importaciones en bolivianos
df_importaciones['Bolivianos']= df_importaciones['ADU']
df_importaciones['Frontera']=df_importaciones['DESADU']
resul_imp=df_importaciones.groupby(by='Frontera',as_index=False,sort=False)['Bolivianos'].sum()
print("Exportaciones en kilos")
print(resul_exp)
print("\nImportaciones en Bolivianos")
print(resul_imp)