import random


def pow_2(a, p, mod):
    if a % mod == 0:
        return 0
    if p == 0:
        return 1
    if p == 1:
        return a % mod
    so_nhan_du = 1
    while True:
        if p % 2 == 0:
            p = p >> 1
        else:
            p = (p-1) >> 1
            so_nhan_du = (so_nhan_du * a) % mod
        a = (a**2) % mod
        if p == 1:
            return (a * so_nhan_du) % mod


def inverse_modulo(k, n):
    p_0 = 0
    p_1 = 1
    count = 0
    q_0 = 0
    q_1 = 0
    a = k
    b = n
    while True:
        if count > 1:
            p_2 = (p_0 - p_1 * q_0) % n
            if p_2 < 0:
                p_2 += n
            p_0 = p_1
            p_1 = p_2
            q_0 = q_1
            q_1 = b // a
        else:
            if count == 0:
                q_0 = b // a
            else:
                q_1 = b // a
        num = b % a
        if num == 0:
            p_1 = (p_0 - p_1 * q_0) % n
            if p_1 < 0:
                p_1 += n
            break
        b = a
        a = num
        count += 1
    return p_1


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def compute_2p(p, n, a):
    k = gcd(2 * p[1], n)
    if k > 1:
        return [-1, k]
    lamda = inverse_modulo(2 * p[1], n)
    lamda = (lamda * (3 * (p[0] ** 2) + a)) % n
    x = (lamda ** 2 - 2 * p[0]) % n
    y = (lamda * (p[0] - x) - p[1]) % n
    return [x, y]


def compute_sum(p, q, n, a):
    if p[0] == 0 and p[1] == 0:
        return q
    if q[0] == 0 and q[1] == 0:
        return p
    if p[0] == q[0] and p[1] == q[1]:
        return compute_2p(p, n, a)
    if p[0] == q[0] and p[0] == 0 - q[0]:
        return [0, 0]
    k = gcd(q[0] - p[0], n)
    if k > 1:
        return [-1, k]
    minus = (q[0] - p[0]) % n
    if minus < 0:
        minus += n
    lamda = inverse_modulo(q[0] - p[0], n)
    if lamda * minus % n == n - 1:
        lamda = n - lamda
    lamda = (lamda * (q[1] - p[1])) % n
    x = (lamda ** 2 - p[0] - q[0]) % n
    y = (lamda * (p[0] - x) - p[1]) % n
    return [x, y]


def compute_minus(p, q, n, a):
    y = -q[1] % n
    if y < 0:
        y += n
    return compute_sum(p, [q[0], y], n, a)


def compute_kp(k, p, n, a):
    remain = [0, 0]
    while k > 1:
        if p[0] == -1:
            return p
        if k % 2 == 0:
            p = compute_2p(p, n, a)
            k = k >> 1
        else:
            remain = compute_sum(remain, p, n, a)
            k = k - 1
    p = compute_sum(p, remain, n, a)
    return p


def order(n, p):
    index = 1
    k = n
    while index < p:
        if k == 1:
            return index
        index += 1
        k = k * n % p


def multiply_vectors(u, v):
    sol = 0
    for i in range(len(u)):
        sol += u[i] * v[i]
    return sol


def square_of_size(u):
    return multiply_vectors(u, u)


def minus_vector(u, v):
    arr = []
    for i in range(len(u)):
        arr.append(u[i] - v[i])
    return arr


def multiply_number(u, n):
    arr = []
    for i in range(len(u)):
        arr.append(u[i] * n)
    return arr


def gram_schmidt(v):
    u = []
    for i in range(0, 4):
        arr = [v[i][j] for j in range(4)]
        for j in range(i):
            arr = minus_vector(arr, multiply_number(u[j], multiply_vectors(u[j], v[i]) / square_of_size(u[j])))
        u.append(arr)
    return u


def gaussian_reduction(u, v):
    while True:
        if square_of_size(v) < square_of_size(u):
            u, v = v, u
        m = multiply_vectors(u, v) // multiply_vectors(u, u)
        if m == 0:
            break
        v = minus_vector(v, multiply_number(u, m))
    return u, v


def inverse_modulo2(x, n):
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


def double_montgomery_curve(p, a, b, mod):
    alpha = inverse_modulo(2 * b * p[1], mod)
    if (alpha * 2 * b * p[1]) % mod == mod - 1:
        alpha = mod - alpha
    alpha = ((3 * p[0] ** 2 + 2 * a * p[0] + 1) * alpha) % mod
    x = (b * alpha ** 2 - a - 2 * p[0]) % mod
    y = (alpha * (p[0] - x) - p[1]) % mod
    return [x, y]


def add_montgomery_curve(p, q, a, b, mod):
    if p[0] == 0 and p[1] == 0:
        return q
    if q[0] == 0 and q[1] == 0:
        return p
    if p[0] == q[0] and p[1] == q[1]:
        return double_montgomery_curve(p, a, b, mod)
    alpha = inverse_modulo((q[0] - p[0]), mod)
    if (alpha * (q[0] - p[0])) % mod == mod - 1:
        alpha = mod - alpha
    alpha = (q[1] - p[1]) * alpha
    alpha = alpha % mod
    x = (b * alpha ** 2 - a - p[0] - q[0]) % mod
    y = (alpha * (p[0] - x) - p[1]) % mod
    return [x, y]


def add_multi_montgomery_curve(k, p, a, b, mod):
    remain = [0, 0]
    while k > 1:
        if k % 2 == 0:
            p = double_montgomery_curve(p, a, b, mod)
            k = k >> 1
        else:
            remain = add_montgomery_curve(p, remain, a, b, mod)
            k = k - 1
    p = add_montgomery_curve(p, remain, a, b, mod)
    return p

