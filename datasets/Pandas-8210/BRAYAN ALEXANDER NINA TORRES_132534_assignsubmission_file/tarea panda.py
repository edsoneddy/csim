import pandas as pd

def calcular_exportaciones():
    archivo = 'EXPORTACIONES ENERO 2026p.csv'    
    try:
        df = pd.read_csv(archivo, encoding='utf-8')
        resultado = df.groupby('DESADU')['KILNET'].sum()
        
        print("=== 1. EXPORTACIONES POR FRONTERA (EN KILOS) ===")
        print(resultado.to_string())
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'. Asegúrate de que esté en la misma carpeta.")

if __name__ == '__main__':
    calcular_exportaciones()
