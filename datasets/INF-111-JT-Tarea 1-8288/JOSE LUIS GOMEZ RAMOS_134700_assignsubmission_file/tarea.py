# Leemos el número que ingresa por teclado
n = int(input())

# Paso 1: Encontramos todos los divisores exactos del número
divisores = []
for d in range(1, n + 1):
    if n % d == 0:
        divisores.append(d)

# Damos la vuelta a la lista para empezar probando desde el divisor más grande
divisores.reverse()

# Paso 2: Verificamos si se pueden formar todos los números desde 1 hasta n-1
es_posible = True
for x in range(1, n):
    resto = x
    for d in divisores:
        if d <= resto:
            resto = resto - d
        if resto == 0:
            break
    # Si sobra algo, significa que no se pudo formar este número
    if resto != 0:
        es_posible = False

# Paso 3: Imprimimos usando un if-else directo
if es_posible:
    print("posible")
    print("Numero | Suma de divisores")
    
    # Si es posible, recorremos del 1 al n para mostrar cómo se forma cada uno
    for i in range(1, n + 1):
        resto = i
        suma_actual = []
        for d in divisores:
            if d <= resto:
                resto -= d
                suma_actual.append(str(d))
            if resto == 0:
                break
        # Mostramos la tablita con el número y su respectiva suma
        print(f"{i} | {' + '.join(suma_actual)}")
else:
    print("-1")