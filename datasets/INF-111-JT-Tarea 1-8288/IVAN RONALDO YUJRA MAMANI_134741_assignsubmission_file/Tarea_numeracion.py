''' Tarea numeración - INF-111 (13 de mayo de 2025)
'''
n = int(input())

divisores = []
for d in range(n - 1, 0, -1):
    if n % d == 0:
        divisores.append(d)

formas = {0: []}
for d in divisores:
    sumas_actuales = list(formas.keys())
    for s in sumas_actuales:
        nueva_suma = s + d
        if nueva_suma not in formas:
            formas[nueva_suma] = formas[s] + [d]

se_puede = True
for numero in range(1, n):
    if numero not in formas:
        se_puede = False

if se_puede:
    print("posible")
    for numero in range(1, n):
        texto = ""
        for d in formas[numero]:
            if texto != "":
                texto = texto + "+"
            texto = texto + str(d)
        print(f"{numero} = {texto}")
else:
    print(-1)
