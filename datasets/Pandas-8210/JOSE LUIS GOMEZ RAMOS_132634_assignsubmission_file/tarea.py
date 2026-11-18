import pandas as pd

# 1. Cargamos los archivos CSV de la carpeta
print("Cargando datos...")
df_exp = pd.read_csv("EXPORTACIONES ENERO 2026p.csv")
df_imp = pd.read_csv("IMPORTACIONES_ENE_2026p.csv")

print("\n--- 1. EXPORTACIONES POR FRONTERA (EN KILOS) ---")
# Sacamos las aduanas/fronteras sin repetir para revisar una por una
fronteras_exp = df_exp['DESADU'].unique()

for frontera in fronteras_exp:
    # Filtramos las filas que corresponden solo a esta frontera
    datos_frontera = df_exp[df_exp['DESADU'] == frontera]
    
    # Sumamos los kilos netos de todo lo filtrado
    total_kilos = datos_frontera['KILNET'].sum()
    
    # Imprimimos el total de esta frontera
    print(f"Frontera: {frontera} ---> Kilos: {total_kilos}")


print("\n--- 2. IMPORTACIONES POR FRONTERA (EN BOLIVIANOS) ---")
# Hacemos lo mismo para el archivo de importaciones
fronteras_imp = df_imp['DESADU'].unique()

for frontera in fronteras_imp:
    # Filtramos por cada frontera
    datos_frontera_imp = df_imp[df_imp['DESADU'] == frontera]
    
    # Sumamos la columna de pagos en bolivianos
    total_bolivianos = datos_frontera_imp['PAG'].sum()
    
    # Mostramos el resultado
    print(f"Frontera: {frontera} ---> Bolivianos: {total_bolivianos}")