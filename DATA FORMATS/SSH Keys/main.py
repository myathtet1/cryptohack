from Crypto.PublicKey import RSA

file = open("bruce.pub", 'rb')
data = file.read()
key = RSA.import_key(data)
print(key.n)