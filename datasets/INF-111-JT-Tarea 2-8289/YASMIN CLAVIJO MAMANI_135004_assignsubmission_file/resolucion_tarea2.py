### Leer la lista por teclado
lista = list(map(int, input("Ingrese la lista de numeros: ").split()))
### Sumas de todos los pares de numeros
sumas = []
i = 0
while i < len(lista) - 1:
    j = i + 1
    while j < len(lista):
        suma = lista[i] + lista[j]
        sumas.append(suma)
        j = j + 1
    i = i + 1
### Cantidad de divisores propios
resultado = []
for suma in sumas:
    contador = 0
    for divisor in lista:
        if suma != divisor and suma % divisor == 0:
            contador += 1
    resultado.append(contador)

print(sumas)
print(resultado) 
