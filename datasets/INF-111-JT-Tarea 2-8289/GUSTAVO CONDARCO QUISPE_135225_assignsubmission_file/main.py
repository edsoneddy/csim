lista = [1, 2, 4, 5, 6]

sumas = []
for i in range(len(lista)):
  for j in range(i + 1, len(lista)):
    sumas.append(lista[i] + lista[j])

res = []
for s in sumas:
  contador = 0
  for x in lista:
    if s % x == 0 and s != x:
      contador += 1
  res.append(contador)

print(*sumas, sep=", ")
print(*res, sep=", ")