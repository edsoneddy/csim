n = int(input())
divisores = []
for d in range(1, n + 1):
    if n % d == 0:
        divisores.append(d)
divisores.reverse()
cumple = True
formas = []
for num in range(1, n + 1):
    x = num
    suma = ""
    for d in divisores:
        if d <= x:
            x = x - d
            suma = suma + str(d) + "+"
        if x == 0:
            break
    if x != 0:
        cumple = False
    else:
        formas.append(suma[:-1])
if cumple:
    print("posible")
    for num in range(1, n + 1):
        print(num, "=", formas[num - 1])
else:
    print(-1)
    
