from my_library import *
from Crypto.Util.number import long_to_bytes

file = open("output.txt")
data = file.readline()
s = data.split("My private key: (")[1][:-2].split(', ')
n = int(s[0], 10)
d = int(s[1], 10)
data = file.readline()
s = data.split('My Friend\'s public keys: [')[1][:-2]
arr = s.split(', ')
friend_keys = []
for i in range(len(arr)):
    if i % 2 == 1:
        friend_keys.append(int(arr[i][:-1], 10))
data = file.readline()
s = data.split('Encrypted flag: ')[1][:-1]
cipher = int(s, 10)
file.close()
e = int('10001', 16)
p, q = factorize_2(n, e, d)
phi = (p - 1) * (q - 1)
for i in range(len(friend_keys) - 1, -1, -1):
    inv = inverse_modulo(friend_keys[i], phi)
    cipher = pow_2(cipher, inv, n)
print(long_to_bytes(cipher))
