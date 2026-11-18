## CRISTHIAN TACCO LECOÑA
numeros = list(map(int, input("Ingrese la lista de numeros: ").split()))

sumas = []
for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        sumas.append(numeros[i] + numeros[j])

print("Sumas:", sumas)

divisores = []
for s in sumas:
    cantidad = 0
    for n in numeros:
        if s % n == 0 and n != s:
            cantidad += 1
    divisores.append(cantidad)

print("Divisores:", divisores)
