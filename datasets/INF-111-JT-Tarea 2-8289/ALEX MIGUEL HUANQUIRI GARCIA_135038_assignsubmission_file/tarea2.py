numeros = list(map(int, input("Ingrese los numeros separados por un espacio: ").split()))
sumas = []
for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        sumas.append(numeros[i] + numeros[j])
divisores = []
for numero in sumas:
    cantidad = 0
    for n in numeros:
        if n != numero and numero % n == 0:
            cantidad += 1
    divisores.append(cantidad)
print(sumas)
print(divisores)