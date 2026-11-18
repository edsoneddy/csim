def buscar(divisores, objetivo, inicio=0):
    if objetivo == 0:
        return []
    for i in range(inicio, len(divisores)):
        d = divisores[i]
        if d > objetivo:
            break
        resultado = buscar(divisores, objetivo - d, i + 1)
        if resultado is not None:
            return [d] + resultado
    return None
def resolver(n):
    divisores = [i for i in range(1, n) if n % i == 0]
    soluciones = []
    for numero in range(1, n):
        resultado = buscar(divisores, numero)
        if resultado is None:
            print(-1)
            return
        soluciones.append(resultado)
    soluciones.append([n])
    print("posible")
    for i, solucion in enumerate(soluciones, 1):
        print(i, "("+" + ".join(map(str, solucion))+")")
while True:
    n = int(input("Ingrese el numero: "))
    if 1 <= n <= 60:
        resolver(n)
        break
    else:
        print("El numero debe ser menor o igual a 60")
        continue
