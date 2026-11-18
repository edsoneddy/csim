''' Tarea sumas - INF-111 (21 de julio de 2023)
'''
numeros = input().split()

lista = []
for x in numeros:
    lista.append(int(x))

sumas = []
for i in range(len(lista)):
    for j in range(i + 1, len(lista)):
        sumas.append(lista[i] + lista[j])

print(*sumas)

cantidades = []
for s in sumas:
    contador = 0
    for d in lista:
        if d != s and s % d == 0:
            contador = contador + 1
    cantidades.append(contador)

print(*cantidades)
