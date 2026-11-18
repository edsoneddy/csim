n = int(input())

divisores = []

for numero in range(1, n + 1):
    if n % numero == 0:
        divisores.append(numero)

divisores.sort(reverse=True)

sumas = {0: []}

for divisor in divisores:
    anteriores = list(sumas.keys())

    for actual in anteriores:
        nueva = actual + divisor

        if nueva <= n and nueva not in sumas:
            sumas[nueva] = sumas[actual] + [divisor]

posible = True

for numero in range(1, n + 1):
    if numero not in sumas:
        posible = False
        break

if not posible:
    print(-1)
else:
    print("posible")

    for numero in range(1, n + 1):
        expresion = "+".join(map(str, sumas[numero]))
        print(numero, expresion)