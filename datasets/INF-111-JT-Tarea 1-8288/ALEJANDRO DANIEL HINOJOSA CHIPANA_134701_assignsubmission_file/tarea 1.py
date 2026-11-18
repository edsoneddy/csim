# Sistemas de numeración probables en la antigüedad

# Lectura y validación de la entrada (entero entre 1 y 60)
while True:
    try:
        n = int(input())
    except ValueError:
        print("Error: debe ingresar un número entero.")
        continue
    if n < 1:
        print("Error: el número debe ser mayor o igual que 1.")
    elif n > 60:
        print("Error: el número debe ser menor o igual que 60.")
    else:
        break

# Divisores propios de n (todos los divisores menores que n)
divisores = [d for d in range(1, n) if n % d == 0]

# alcanzables[s] = lista de divisores distintos que suman s
alcanzables = {0: []}
for d in divisores:
    nuevos = {}
    for s, lista in alcanzables.items():
        if s + d not in alcanzables:
            nuevos[s + d] = lista + [d]
    alcanzables.update(nuevos)

# Se deben poder formar todos los números menores que n
if all(k in alcanzables for k in range(1, n)):
    print("posible")
    for k in range(1, n):
        sumandos = sorted(alcanzables[k], reverse=True)
        print(k, "=", "+".join(str(x) for x in sumandos))
    print(n, "=", n)
else:
    print(-1)