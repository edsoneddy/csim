def divis(n):
    d=[]
    for i in range(1,n):
        if n%i==0:
            d.append(i)
    return d
def formar(numero,d):
    suma=[]
    resto=numero
    for i in range(len(d)-1,-1,-1):
        if d[i]<=resto:
            suma.append(d[i])
            resto-=d[i]
    return suma, resto
n=int(input())
if n<1 or n>60:
    print(-1)
else:
    d=divis(n)
    resultados=[]
    posible=True
    for numero in range(1,n):
        suma, resto= formar(numero,d)
        if resto !=0:
            posible= False
            break
        resultados.append(suma)
    if posible:
        print("posible")
        for numero in range(1,n):
            print(numero,"+".join(map(str, resultados[numero -1])))
        print(n,n)
    else:
        print(-1)