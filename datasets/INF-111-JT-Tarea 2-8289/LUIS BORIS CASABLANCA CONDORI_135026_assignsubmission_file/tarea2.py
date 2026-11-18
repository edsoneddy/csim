datos = input().split()
l = []
for elemento in datos:
  l.append(int(elemento))
resultado_de_las_sumas = []
for p in range(len(l)):
  for q in range(p + 1, len(l)):
    total = l[p] + l[q]
    resultado_de_las_sumas.append(total)
d = []
for valor in resultado_de_las_sumas:
  divs = 0
  for divisor in range(1, valor):
    if valor % divisor == 0:
      divs += 1
  d.append(divs)
print(resultado_de_las_sumas)
print(d)