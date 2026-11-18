
numeros = list(map(int, input().split()))

sumas = []

for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        sumas.append(numeros[i] + numeros[j])

print(sumas)

resultado = []

for suma in sumas:
    contador = 0

    for n in numeros:
        if n != 0 and n != suma:
            if suma % n == 0:
                contador += 1

    resultado.append(contador)

print(resultado)
