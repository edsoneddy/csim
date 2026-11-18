import pandas as pd

def main():
    print("==================================================")
    print(" EXPORTACIONES POR FRONTERA (EN KILOS)")
    print("==================================================")
    df_exp = pd.read_csv("EXPORTACIONES ENERO 2026p.csv")
    
    exp_por_frontera = df_exp.groupby("DESADU")[["KILBRU", "KILNET"]].sum()
    print(exp_por_frontera.to_string())
    
    print("\n" + "=" * 50)
    print(" IMPORTACIONES POR FRONTERA (EN BOLIVIANOS)")
    print("==================================================")
    
    df_imp = pd.read_csv("IMPORTACIONES_ENE_2026p.csv")
    
    imp_por_frontera = df_imp.groupby("DESADU")["ADU"].sum().reset_index()
    imp_por_frontera.columns = ["Frontera (Aduana)", "Valor Total (Bolivianos)"]
    print(imp_por_frontera.to_string(index=False))

if __name__ == "__main__":
    main()
