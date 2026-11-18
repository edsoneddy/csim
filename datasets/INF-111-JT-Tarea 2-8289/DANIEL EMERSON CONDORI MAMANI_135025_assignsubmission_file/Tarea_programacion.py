
numeros = []
sumas = []
cantidad_numeros = 0


entrada = input("Ingrese los numeros separados por espacios: ")

numeros = list(map(int, entrada.split()))

cantidad_numeros = len(numeros)



print("\nLista de sumas de dos numeros:")

for i in range(0, cantidad_numeros):

    for j in range(i + 1, cantidad_numeros):

        suma = numeros[i] + numeros[j]

        sumas.append(suma)



print(sumas)




print("\nCantidad de divisores de cada suma:")

for i in range(0, len(sumas)):

    contador = 0

    suma_actual = sumas[i]

    for j in range(0, cantidad_numeros):

        numero_actual = numeros[j]


        if numero_actual != suma_actual:

            if suma_actual % numero_actual == 0:

                contador = contador + 1

    print(contador, end=" ")

print()
