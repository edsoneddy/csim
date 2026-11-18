entrada = input("Ingrese los numeros separados por espacios: ")
datos = entrada.split()

numeros = []

for dato in datos:
    numeros.append(int(dato))

sumas = []

for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        suma = numeros[i] + numeros[j]
        sumas.append(suma)

cantidades = []

for suma in sumas:
    contador = 0

    for numero in numeros:
        if numero != 0 and suma % numero == 0 and numero != suma:
            contador = contador + 1

    cantidades.append(contador)

print("Lista de sumas:")
print(sumas)

print("Lista de cantidades de divisores:")
print(cantidades)