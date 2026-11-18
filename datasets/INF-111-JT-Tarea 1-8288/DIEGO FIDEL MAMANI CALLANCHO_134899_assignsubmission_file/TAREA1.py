
n = int(input())

divisores = []

for i in range(1, n):
    if n % i == 0:
        divisores.append(i)

alcance = 0
posible = True

for d in divisores:
    if d > alcance + 1:
        posible = False
        break
    alcance = alcance + d

if alcance < n - 1:
    posible = False

if posible:
    print("posible")

    for numero in range(1, n):
        resto = numero
        suma = []

        for d in divisores[::-1]:
            if d <= resto:
                suma.append(str(d))
                resto = resto - d

        print(str(numero) + " = " + "+".join(suma))

else:
    print(-1)
