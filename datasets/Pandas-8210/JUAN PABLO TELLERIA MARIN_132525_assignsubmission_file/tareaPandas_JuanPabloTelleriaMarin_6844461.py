import pandas as pd

data1 = pd.read_csv('EXPORTACIONES ENERO 2026p.csv')
data1.columns;
#data1.info();
data1['DESADU'].unique();
kilos_exportados_frontera = data1.groupby('DESADU')['KILBRU'].sum().reset_index()
kilos_exportados_frontera = kilos_exportados_frontera.rename(columns={
    'DESADU':'FRONTERA',
    'KILBRU':'KILOS'
})
print(kilos_exportados_frontera)



data2 = pd.read_csv('IMPORTACIONES_ENE_2026p.csv')
data2.columns;
#data2.info();
data2['DESADU'].unique();
bolivianos_importado_frontera = data2.groupby('DESADU')['PAG'].sum().reset_index()
bolivianos_importado_frontera = bolivianos_importado_frontera.rename(columns={
    'DESADU':'FRONTERA',
    'PAG':'PAGO_BOLIVIANOS'
})
print(bolivianos_importado_frontera)