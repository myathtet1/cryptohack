from pwn import *
import json
import gmpy2
from my_library import inverse_modulo, pow_2, gcd
from Crypto.Util.number import long_to_bytes, bytes_to_long

r = remote("socket.cryptohack.org", 13386)


def factorize(n):
    if n < 2:
        return 1
    product = 1
    for i in range(1, n + 1):
        product *= i
    return product


chap = []
for i in range(12):
    chap.append(factorize(11) // (factorize(i) * factorize(11 - i)))

print(r.recvline())
send = {'option': 'get_flag'}
send = json.dumps(send).encode()
arr_a = []
arr_b = []
n = 0
for _ in range(1024):
    if _ % 100 == 0:
        print(_)
    r.sendline(send)
    data = r.recvline().decode()
    data = json.loads(data)
    encrypted_flag = data["encrypted_flag"]
    n = data["modulus"]
    a = data["padding"][0]
    b = data["padding"][1]
    ar = []
    for i in range(12):
        num = chap[i] * pow_2(a, 11 - i, n) * pow_2(b, i, n) % n
        ar.append(num)
    arr_a.append(ar)
    arr_b.append(encrypted_flag)
while len(arr_a) > 1:
    print(len(arr_a))
    n_a = []
    n_b = []
    for i in range(0, len(arr_a), 2):
        ar = []
        for j in range(1, len(arr_a[i]), 1):
            num = (arr_a[i][j] * arr_a[i + 1][0] - arr_a[i + 1][j] * arr_a[i][0]) % n
            ar.append(num)
        n_a.append(ar)
        c = (arr_b[i] * arr_a[i + 1][0] - arr_b[i + 1] * arr_a[i][0]) % n
        n_b.append(c)
    arr_a = n_a
    arr_b = n_b
print(long_to_bytes((arr_b[0] - arr_a[0][1]) * inverse_modulo(arr_a[0][0], n) % n))
