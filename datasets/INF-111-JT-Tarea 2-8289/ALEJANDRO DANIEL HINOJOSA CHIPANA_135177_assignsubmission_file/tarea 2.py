# Leer y validar la lista de numeros
while True:
    try:
        numeros = list(map(int, input().split()))

        if len(numeros) < 2:
            print("Error: ingrese al menos dos números.")
            continue

        break

    except ValueError:
        print("Error: ingrese solo números enteros separados por espacios.")
sumas = []
cantidades = []


for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        suma = numeros[i] + numeros[j]
        sumas.append(suma)


for suma in sumas:
    contador = 0

    for numero in numeros:
        if numero != suma and numero != 0:
            if suma % numero == 0:
                contador += 1

    cantidades.append(contador)

# Mostrar los resultados
print("Lista de sumas:")
print(sumas)

print("Lista de divisores:")
print(cantidades)