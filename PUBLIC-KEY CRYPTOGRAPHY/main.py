import hashlib
import Crypto.Util.number


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


def hash_function(flag):
    return Crypto.Util.number.bytes_to_long(hashlib.sha256(flag.encode()).digest())


e = 65537
file = open("private.key")
str_N = file.readline()
N = int(str_N[4:len(str_N) - 1])
str_d = file.readline()
d = int(str_d[4:len(str_d) - 1])
file.close()
flag = "crypto{Immut4ble_m3ssag1ng}"
hash_value = hash_function(flag)
S = pow_2(hash_value, d, N)
M = Crypto.Util.number.bytes_to_long(flag.encode())
C = pow_2(M, e, N)
m = pow_2(C, d, N)
s = pow_2(S, e, N)
assert hash_function(Crypto.Util.number.long_to_bytes(m).decode()) == s
print(Crypto.Util.number.long_to_bytes(m))
