from my_library import *
from Crypto.Util.number import long_to_bytes
import gmpy2
from rsa.rsaAttacks.wiener.attack import hack_RSA
from itertools import combinations


def decrypt(grps, e):
    for grp in combinations(zip(grps['n'], grps['c']), e):
        N = 1
        for x in grp:
            N *= x[0]

        M = 0
        for x in grp:
            M += x[1]*inverse_modulo(N//x[0], x[0])*(N//x[0])
        M %= N

        m, exact = gmpy2.iroot(M, 3)
        if exact:
            print(long_to_bytes(m))


file = open("output.txt", 'rb')
n = []
c = []
while True:
    data = file.readline()
    if data:
        if data[0] == 110:
            n.append(int(data.decode()[4:-1], 10))
        elif data[0] == 99:
            c.append(int(data.decode()[4:-1], 10))
    else:
        print("end")
        break
file.close()
groups = {'n': n, 'c': c}
print(decrypt(groups, 3))

