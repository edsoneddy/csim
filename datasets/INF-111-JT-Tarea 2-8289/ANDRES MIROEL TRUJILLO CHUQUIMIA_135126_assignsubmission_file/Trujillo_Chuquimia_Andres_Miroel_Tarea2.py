txt = input()
par = txt.split()
numeros = []
for p in par:
    numeros.append(int(p))
suma = []
for i in range(len(numeros)):
    for j in range(i + 1, len(numeros)):
        suma.append(numeros[i] + numeros[j])
for s in suma:
    print(s, end=" ")
for s in suma:
    contador = 0
    for x in numeros:
        if s % x == 0 and x != s:
            contador = contador + 1
    print(contador, end=" ")
