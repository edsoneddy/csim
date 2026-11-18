# Para la entrada de datos
entrada_usuario = input()
lista_numeros = [int(x) for x in entrada_usuario.replace(",", " ").split()]

# Para calcular las sumas por pares usamos while
lista_de_sumas = []
indice_primero = 0
while indice_primero < len(lista_numeros) - 1:
    indice_segundo = indice_primero + 1
    while indice_segundo < len(lista_numeros):
        suma_par = lista_numeros[indice_primero] + lista_numeros[indice_segundo]
        lista_de_sumas.append(suma_par)
        indice_segundo = indice_segundo + 1
    indice_primero = indice_primero + 1

# Para calcular la cantidad de divisores usamos la estructura for 
conteo_divisores = []
for suma_par in lista_de_sumas:
    cantidad_divisores = 0
    for numero_divisor in lista_numeros:
        if suma_par != numero_divisor and suma_par % numero_divisor == 0:
            cantidad_divisores += 1
    conteo_divisores.append(cantidad_divisores)

# Para imprimir los 2 resultados que pide el ejercicio sumas y divisores 
print(lista_de_sumas)
print(conteo_divisores)