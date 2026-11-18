"""
Tarea Pandas - INF-111
Estudiante: TACCO LECOÑA CRISTHIAN
Paralelo: B
Estadísticas de comercio exterior del INE (enero 2026).

1. Exportaciones por frontera (aduana) en kilos.
2. Importaciones por frontera (aduana) en bolivianos.

"""
import os
import pandas as pd

CARPETA = os.path.dirname(os.path.abspath(__file__))
ARCH_EXP = os.path.join(CARPETA, "EXPORTACIONES_ENERO_2026p.csv")
ARCH_IMP = os.path.join(CARPETA, "IMPORTACIONES_ENE_2026p.csv")

pd.options.display.float_format = "{:,.2f}".format
pd.options.display.max_rows = None
pd.options.display.width = 120


def main():
    # ---------- 1. EXPORTACIONES: kilos por frontera ----------
    exp = pd.read_csv(ARCH_EXP, encoding="utf-8")
    exp_kilos = (
        exp.groupby("DESADU")[["KILNET", "KILBRU"]]
        .sum()
        .sort_values("KILNET", ascending=False)
    )
    exp_kilos.columns = ["Kilos netos", "Kilos brutos"]
    exp_kilos.index.name = "Frontera"

    print("=" * 70)
    print("1. EXPORTACIONES POR FRONTERA (en kilos)")
    print("=" * 70)
    print(exp_kilos)
    print(f"\nTOTAL exportado: {exp_kilos['Kilos netos'].sum():,.2f} kg netos "
          f"({exp_kilos['Kilos brutos'].sum():,.2f} kg brutos)")

    # ---------- 2. IMPORTACIONES: bolivianos por frontera ----------
    # La columna ADU es el valor en aduana en bolivianos
    # (= valor CIF frontera en $us x tipo de cambio 6.96).
    imp = pd.read_csv(ARCH_IMP, encoding="utf-8")
    imp_bs = (
        imp.groupby("DESADU")["ADU"]
        .sum()
        .sort_values(ascending=False)
        .rename("Bolivianos (Bs)")
    )
    imp_bs.index.name = "Frontera"

    print("\n" + "=" * 70)
    print("2. IMPORTACIONES POR FRONTERA (en bolivianos)")
    print("=" * 70)
    print(imp_bs)
    print(f"\nTOTAL importado: Bs {imp_bs.sum():,.2f}")


if __name__ == "__main__":
    main()