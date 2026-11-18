entrada = input().replace(",", " ").split()
numeros = list(map(int, entrada))

sumas = []

for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        sumas.append(numeros[i] + numeros[j])

print(sumas)

cantidades = []

for suma in sumas:
    contador = 0

    for numero in numeros:
        if numero != 0 and numero != suma and suma % numero == 0:
            contador += 1

    cantidades.append(contador)

print(cantidades)