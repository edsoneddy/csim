numero = int(input("Ingrese un numero menor o igual a 60: "))

if numero < 1 or numero > 60:
    print("Ingrese un numero entre 1 y 60")
else:
    divisores = []

    for i in range(1, numero):
        if numero % i == 0:
            divisores.append(i)

    formas = [None] * numero
    formas[0] = []

    for divisor in divisores:
        for suma in range(numero - 1, divisor - 1, -1):
            if formas[suma] == None:
                if formas[suma - divisor] != None:
                    formas[suma] = formas[suma - divisor] + [divisor]

    posible = True

    for i in range(1, numero):
        if formas[i] == None:
            posible = False

    if posible:
        print("posible")

        for i in range(1, numero):
            expresion = ""

            for divisor in formas[i]:
                if expresion == "":
                    expresion = str(divisor)
                else:
                    expresion = expresion + " + " + str(divisor)

            print(i, "=", expresion)
    else:
        print(-1)
        