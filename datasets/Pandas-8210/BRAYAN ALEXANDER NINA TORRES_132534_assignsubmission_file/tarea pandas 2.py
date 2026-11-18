import pandas as pd
def calcular_importaciones():    
    archivo = 'IMPORTACIONES_ENE_2026p.csv'    
    try:
        df = pd.read_csv(archivo, encoding='utf-8')
        resultado = df.groupby('DESADU')['ADU'].sum()
        
        print("=== 2. IMPORTACIONES POR FRONTERA (EN BOLIVIANOS) ===")
        print(resultado.to_string())
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'. Asegúrate de que esté en la misma carpeta.")
if __name__ == '__main__':
    calcular_importaciones()
