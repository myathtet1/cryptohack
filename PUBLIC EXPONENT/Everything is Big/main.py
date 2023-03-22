from my_library import *
from Crypto.Util.number import long_to_bytes
from rsa.rsaAttacks.wiener.attack import hack_RSA

file = open("output.txt", 'rb')
data = file.readline()
n = int(data.decode()[6:len(data) - 1], 16)
data = file.readline()
e = int(data.decode()[6:len(data) - 1], 16)
data = file.readline()
c = int(data.decode()[6:len(data)], 16)
file.close()
print(n)
print(e)
print(c)
d = hack_RSA(e, n)
pt = pow_2(c, d, n)
print(long_to_bytes(pt))
