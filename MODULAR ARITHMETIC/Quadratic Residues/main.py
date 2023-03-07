p = 29
ints = [14, 6, 11]

power = (p - 1) / 2
num = None
for i in ints:
    if i ** power % p == 1:
        num = i
        break
for i in range(p):
    if i * i % p == num:
        print(i)
        break
