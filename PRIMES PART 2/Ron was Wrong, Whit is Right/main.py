from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from my_library import gcd, inverse_modulo

c = []
n = []
e = []
for i in range(1, 51):
    file = open(f"keys_and_messages/keys_and_messages/{i}.pem", 'rb')
    data = file.read()
    key = RSA.import_key(data)
    n.append(key.n)
    e.append(key.e)
    file.close()
    file = open(f"keys_and_messages/keys_and_messages/{i}.ciphertext", 'rb')
    c.append(file.read())
    file.close()
p = 0
index = 0
for i in range(len(n)):
    visited = False
    for j in range(i + 1, len(n)):
        num = gcd(n[i], n[j])
        if num != 1:
            p = num
            index = i
            visited = True
            break
    if visited:
        break
q = n[index] // p
phi = (p - 1) * (q - 1)
d = inverse_modulo(e[index], phi)
key = RSA.construct((n[index], e[index], d))
cipher = PKCS1_OAEP.new(key)
# print(index)
# print(p)
# print(q)
# print(n[index] - p * q)
print(cipher.decrypt(bytes.fromhex(c[index].decode())))
