def inverse_modulo(x, n):
    n_const = n
    a_p = []
    a_q = []
    i = 0
    r = n % x
    while r != 0:
        a_q.append(n//x)
        if i == 0 or i == 1:
            a_p.append(i)
        else:
            a_p.append((a_p[i-2] - a_p[i-1] * a_q[i-2]) % n_const)
        n = x
        x = r
        r = n % x
        i += 1
    for x in range(i, i+2):
        a_p.append((a_p[x - 2] - a_p[x - 1] * a_q[x - 2]) % n_const)
    return a_p[i+1]


inverse_modulo(26513, 32321)
print((1 - 26513 * inverse_modulo(26513, 32321)) / 32321)
# print(inverse_modulo(15, 26))
