from Crypto.PublicKey import RSA
from cryptography import x509
file = open("mykey.pem", 'rb')

data = file.read()
key = RSA.import_key(data)

decimal = key
print(key)

file2 = open("2048b.der", 'rb')

data2 = file2.read()

key2 = RSA.import_key(data2)

print(key2.n)