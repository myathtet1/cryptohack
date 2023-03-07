from Crypto.PublicKey import RSA

file = open("privacy.pem", 'rb')

data = file.read()
key = RSA.import_key(data)

print(key.d)

