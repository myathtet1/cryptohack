from my_library import *
from Crypto.Util.number import long_to_bytes

file = open("output.txt", 'rb')
data = file.readline()
n = int(data.decode()[3:-1], 10)
data = file.readline()
e = int(data.decode()[3:-1], 10)
data = file.readline()
c = int(data.decode()[3:-1], 10)
file.close()
p = 1
k = n - 1
while k % 2 == 0:
    p = p << 1
    k = k >> 1
p = p - 1
q = n // p
phi = (p - 1) * (q - 1)
d = inverse_modulo(e, phi)
m = pow_2(c, d, n)
print(long_to_bytes(m))
