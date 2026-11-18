n = int(input())

div = []

for d in range(1, n + 1):
    if n % d == 0:
        div.append(d)
        
div.reverse()
cumple = True
formas = {}
for x in range(1, n + 1):
    aux = x
    suma = []

    for d in div:
        if d <= aux:
            aux = aux - d
            suma.append(d)
            if aux == 0:
                break
    if aux != 0:
        cumple = False
    else:
        formas[x] = suma
if cumple:
    print("posible")
    for x in range(1, n + 1):
        print(x, "=", " + ".join(map(str, formas[x])))
else:
    print(-1)