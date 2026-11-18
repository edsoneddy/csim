import pandas
exp_en = pandas.read_csv("EXPORTACIONES ENERO 2026p.csv")
expor = exp_en.groupby("DESADU")["KILNET"].sum()
fronteras = list(expor.keys())
for i in range(len(fronteras)):
    frontera = fronteras[i]
    kilos = expor[frontera]
    print(frontera, ":", round(kilos, 2), "Kg neto" )

print()

imp_en = pandas.read_csv("IMPORTACIONES_ENE_2026p.csv")
conv = imp_en.groupby("DESADU")["ADU"].sum()
conv = conv * 10
fronteras = list(conv.keys())
for i in range(len(fronteras)):
    frontera = fronteras[i]
    bol = conv[frontera]
    print(frontera, ":", bol, "bs")