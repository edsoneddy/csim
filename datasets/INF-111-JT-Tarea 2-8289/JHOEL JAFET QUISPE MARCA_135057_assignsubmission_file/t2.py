texto = input().split()

lista = []
for t in texto:
    lista.append(int(t))

sumas = []
for i in range(len(lista)):
    for j in range(i + 1, len(lista)):
        sumas.append(lista[i] + lista[j])

divisores = []
for s in sumas:
    cantidad = 0
    for x in lista:
        if x != s and s % x == 0:
            cantidad += 1
    divisores.append(cantidad)

salida = ""
for s in sumas:
    if salida == "":
        salida = str(s)
    else:
        salida = salida + ", " + str(s)
print(salida)

salida = ""
for d in divisores:
    if salida == "":
        salida = str(d)
    else:
        salida = salida + ", " + str(d)
print(salida)
