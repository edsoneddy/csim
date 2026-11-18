def obtener_divisores(n):
    divisores = []

    for i in range(1, n + 1):
        if n % i == 0:
            divisores.append(i)

    return divisores


def generar_sumas(n, divisores):
    combinaciones = [[]]

    for d in divisores:
        nuevas = []

        for c in combinaciones:
            nueva = c + [d]
            nuevas.append(nueva)

        for c in nuevas:
            combinaciones.append(c)

    resultados = [None] * (n + 1)

    for c in combinaciones:
        suma = 0

        for d in c:
            suma += d

        if suma <= n:
            if resultados[suma] == None:
                resultados[suma] = c

    return resultados


def main():
    n = int(input())

    divisores = obtener_divisores(n)
    resultados = generar_sumas(n, divisores)

    posible = True

    for i in range(1, n + 1):
        if resultados[i] == None:
            posible = False

    if posible == False:
        print("-1")
    else:
        print("posible")

        for i in range(1, n + 1):
            suma = resultados[i]
            texto = ""

            for j in range(len(suma)):
                if j > 0:
                    texto += "+"

                texto += str(suma[j])

            print(i, "|", texto)


if __name__ == "__main__":
    main()
