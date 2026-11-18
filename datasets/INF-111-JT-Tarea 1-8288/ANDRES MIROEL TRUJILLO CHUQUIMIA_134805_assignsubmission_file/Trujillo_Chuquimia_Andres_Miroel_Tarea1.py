n = int(input())
posible = True
txt = ""
for k in range(1, n):
    falta = k
    sum = ""
    for d in range(n - 1, 0, -1):
        if n % d == 0 and d <= falta:
            falta = falta - d
            sum = sum + str(d) + "+"
    if falta != 0:
        posible = False
    txt= txt + str(k) + " = " + sum[:-1] + "\n"
if posible:
    print("posible")
    print(txt)
else:
    print(-1)