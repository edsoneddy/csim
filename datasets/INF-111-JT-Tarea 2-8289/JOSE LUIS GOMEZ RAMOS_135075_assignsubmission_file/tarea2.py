# Leemos la línea y la separamos por espacios
entrada = input()
partes = entrada.split()

# Convertimos cada pedacito a número entero uno por uno
lista = []
for x in partes:
    lista.append(int(x))

# Sacamos la suma de cada par de números de la lista
sumas = []
for i in range(len(lista)):
    for j in range(i + 1, len(lista)):
        s = lista[i] + lista[j]
        sumas.append(s)

# Verificamos cuántos números de la lista dividen a la suma (que no sean iguales)
divisores = []
for s in sumas:
    cont = 0
    for num in lista:
        if s % num == 0 and num != s:
            cont = cont + 1
    divisores.append(cont)

# Mostramos los resultados en pantalla
print(sumas)
print(divisores)