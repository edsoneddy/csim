numeros= list(map(int, input().split()))
sumas=[]
divisores=[]
for i in range(len(numeros)):
    for j in range(i+1, len(numeros)):
        suma=numeros[i]+numeros[j]
        sumas.append(suma)
        cantidad=0
        for numero in numeros:
            if numero != 0 and numero != suma and suma % numero == 0:
                cantidad +=1
        divisores.append(cantidad)
print(sumas)
print(divisores)