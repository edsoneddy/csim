import pandas
 
print("\nEXPORTACIONES POR FRONTERA (En Kilos)")
exporta = pandas.read_csv("EXPORTACIONES ENERO 2026p.csv")
tablas = exporta.groupby("DESADU")
pandas.options.display.float_format = "{:.2f} kilos".format
print(tablas["KILBRU"].sum())

print("\nIMPORTACIONES POR FRONTERA (En Bolivianos Bs.)")
pandas.options.display.float_format = '{:.2f}'.format
importa= pandas.read_csv("IMPORTACIONES_ENE_2026p.csv")
tablas=importa.groupby("DESADU")
def cambio (x):
    return x * 6.97
#El tipo de cambio actual es de 11.84, pero está redondeada a 11.9 para que sea más fácil de calcular
tabla_final = tablas["FOB"].sum().reset_index(name = "SUMA")
tabla_final["SUMA"] = tabla_final["SUMA"].apply(cambio)
print(tabla_final)



