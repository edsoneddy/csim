n = int(input())

divs = [i for i in range(1, n + 1) if n % i == 0]

ans = {0: ""}

for d in divs:
  nuevos = {}
  for suma, expr in ans.items():
    nueva_suma = suma + d
    if nueva_suma <= n:
      nueva_expr = str(d) if expr == "" else f"{expr}+{d}"
      if nueva_suma not in ans and nueva_suma not in nuevos:
        nuevos[nueva_suma] = nueva_expr
  ans.update(nuevos)

posible = all(i in ans for i in range(1, n + 1))

if posible:
  print("posible")
  for i in range(1, n + 1):
    print(f"{i} | {ans[i]}")
else:
  print("-1")