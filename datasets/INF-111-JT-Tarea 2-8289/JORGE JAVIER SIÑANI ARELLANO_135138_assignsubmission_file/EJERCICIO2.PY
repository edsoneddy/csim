
numeros = list(map(int, input().split()))

sumas = []

for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        suma = numeros[i] + numeros[j]
        sumas.append(suma)

print(sumas)

divisores = []

for suma in sumas:
    cantidad = 0

    for numero in numeros:
        if numero != suma and suma % numero == 0:
            cantidad += 1

    divisores.append(cantidad)

print(divisores)
