import pandas as pd
#exportaciones
print("==========================================")
print("       ANÁLISIS DE EXPORTACIONES          ")
print("==========================================")

expor = pd.read_csv('EXPORTACIONES ENERO 2026p.csv')
grupo_expor = expor.groupby('DESADU')
#suma de kilos brutos
pd.options.display.float_format = "{:,.2f} kilos brutos".format
print("\n--- SUMA DE KILOS BRUTOS POR ADUANA ---")
print(grupo_expor['KILBRU'].sum())
#suma de Kilos netos 
pd.options.display.float_format = "{:,.2f} kilos netos".format
print("\n--- SUMA DE KILOS NETOS POR ADUANA ---")
print(grupo_expor['KILNET'].sum())
#importaciones
print("\n==========================================")
print("       ANÁLISIS DE IMPORTACIONES          ")
print("==========================================")

impor = pd.read_csv('IMPORTACIONES_ENE_2026p.csv')
impor['KILOS'] = pd.to_numeric(impor['KILOS'], errors='coerce')
grupo_impor = impor.groupby('DESADU')
#suma de kilos brutos
pd.options.display.float_format = "{:,.2f} kilos brutos".format
print("\n--- SUMA DE KILOS BRUTOS (IMPORTACIONES) ---")
print(grupo_impor['KILOS'].sum())
#suma de kilos netos
pd.options.display.float_format = "{:,.2f} kilos netos".format
print("\n--- SUMA DE KILOS NETOS (IMPORTACIONES) ---")
print(grupo_impor['KILOS'].sum())
