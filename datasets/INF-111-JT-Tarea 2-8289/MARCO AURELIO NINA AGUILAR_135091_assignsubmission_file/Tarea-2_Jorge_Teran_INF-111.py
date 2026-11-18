def main():
    entrada = input("Ingrese la lista de números separados por espacios: ")
    numeros = [int(x) for x in entrada.split()]

    sumas = []
    for i in range(len(numeros)):
        for j in range(i + 1, len(numeros)):
            sumas.append(numeros[i] + numeros[j])

    print("\nLista de sumas de dos números:")
    print(sumas)

    divisores = []
    for s in sumas:
        cuenta = 0
        for n in numeros:
            if n != 0 and n != s and s % n == 0:
                cuenta += 1
        divisores.append(cuenta)

    print("\nLista de números de divisores:")
    print(divisores)

if __name__ == "__main__":
    main()
