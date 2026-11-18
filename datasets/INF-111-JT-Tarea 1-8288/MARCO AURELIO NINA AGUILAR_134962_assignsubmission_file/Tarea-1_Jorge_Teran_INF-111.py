def resolver(n):
    divs = [d for d in range(1, n + 1) if n % d == 0]

    alcanzable = {0: []}
    for d in divs:
        nuevos = {}
        for s, usados in alcanzable.items():
            t = s + d
            if t <= n and t not in alcanzable and t not in nuevos:
                nuevos[t] = usados + [d]
        alcanzable.update(nuevos)

    for x in range(1, n + 1):
        if x not in alcanzable:
            print(-1)
            return

    print("posible")
    for x in range(1, n + 1):
        suma = sorted(alcanzable[x], reverse=True)
        print(x, "+".join(map(str, suma)))


if __name__ == "__main__":
    resolver(int(input()))
