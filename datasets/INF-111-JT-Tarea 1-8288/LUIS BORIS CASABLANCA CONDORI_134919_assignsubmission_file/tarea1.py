n = int(input())

div = []
for d in range(1, n + 1):
  if n % d == 0:
    div.append(d)
div.reverse()
cumple = True
tabla_de_resultados = []
for i in range(1, n + 1):
  x = i
  divisores_usados = []
  for d in div:
    if d <= x:
      x = x - d
      divisores_usados.append(str(d))
    if x == 0:
      break
  if x != 0:
    cumple = False
    break
  else:
    tabla_de_resultados.append((i, "+".join(divisores_usados)))

if cumple:
  print("posible")
  print("Numero" " Suma de divisores")
  for num, suma in tabla_de_resultados:
    print(f"{num}    " f"{suma}")
else:
  print("-1")