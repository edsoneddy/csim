# EZREQUIEL NOCOLAS CHIPANA PACO 
# tarea 2 

def divisores(n):
    d = [1]
    for i in range(2, n):
        if n % i == 0:
            d.append(i)
    if n > 1:
        d.append(n)
    return d


n = int(input())

d = divisores(n)
d = d[::-1]          #mayor a menor
k = len(d)

formas = {}
for Ma in range(1, 2**k):
    Su = 0
    Pa = []
    for j in range(k):
        if Ma & (1 << j):
            Su += d[j]
            Pa.append(str(d[j]))
    if Su not in formas:
        formas[Su] = '+'.join(Pa)

for i in range(1, n + 1):
    if i not in formas:
        print(-1)
        break
else:
    print('posible')
    for i in range(1, n + 1):
        print(f'{i} = {formas[i]}')