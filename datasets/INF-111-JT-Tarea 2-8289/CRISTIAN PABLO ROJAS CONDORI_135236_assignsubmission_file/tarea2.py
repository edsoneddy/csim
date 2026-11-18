numeros = list(map(int, input().split()))

sumas = []
for i in range(len(numeros)):
  for j in range(i + 1, len(numeros)):
    sumas.append(numeros[i] + numeros[j])

divis = []
for s in sumas:
  contador = 0
  for num in numeros:
    if s % num == 0 and num != s:
      contador += 1
  divis.append(contador)

print("Lista de sumas:", sumas)
print("Lista de divisores:", divis)