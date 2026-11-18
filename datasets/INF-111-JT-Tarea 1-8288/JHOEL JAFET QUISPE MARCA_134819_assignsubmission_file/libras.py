n = int(input())

divisores = []
for d in range(n, 0, -1):
    if n % d == 0:
        divisores.append(d)

k = len(divisores)

formas = [None] * (n + 1)

for combinacion in range(1, 2 ** k):
    suma = 0
    texto = ""
    for i in range(k):
        if (combinacion // 2 ** i) % 2 == 1:
            suma += divisores[i]
            if texto == "":
                texto = str(divisores[i])
            else:
                texto = texto + "+" + str(divisores[i])
    if suma <= n and formas[suma] is None:
        formas[suma] = texto

posible = True
for numero in range(1, n + 1):
    if formas[numero] is None:
        posible = False

if posible:
    print("posible")
    for numero in range(1, n + 1):
        print(numero, formas[numero])
else:
    print(-1)