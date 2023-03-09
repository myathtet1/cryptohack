def pow_2(a, p, mod):
    if a % mod == 0:
        return 0
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

