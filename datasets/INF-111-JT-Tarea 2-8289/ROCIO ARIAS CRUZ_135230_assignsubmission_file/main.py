texto = input("Ingrese los numeros separados por coma: ")

numeros = []

for x in texto.split(","):
    numeros.append(int(x))

sumas = []

for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        suma = numeros[i] + numeros[j]
        sumas.append(suma)
print("Lista de sumas:")
print(sumas)
divisores = []

for suma in sumas:
    cantidad = 0
    
    for num in numeros:
        if num != 0 and num != suma:
            if suma % num == 0:
                cantidad = cantidad + 1

    divisores.append(cantidad)

print("Lista de divisores:")
print(divisores)
