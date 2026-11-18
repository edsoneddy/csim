n = int(input())
d = [x for x in range(1, n) if n % x == 0]

def f(r, i):
  if r == 0:
    return []
  if r < 0 or i >= len(d):
    return None
  res = f(r - d[i], i + 1)
  return [d[i]] + res if res is not None else f(r, i + 1)

res = []
for i in range(1, n + 1):
  comb = [n] if i == n else f(i, 0)
  if comb is None:
    print("-1")
    break
  res.append((i, comb))
else:
  print("posible")
  for num, s in res:
    txt = str(s[0])
    for x in s[1:]:
      txt += "+" + str(x)
    print(f"{num} | {txt}")
