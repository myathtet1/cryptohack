import os

import requests
import json


def encrypt():
    r = requests.get("https://aes.cryptohack.org/ecbcbcwtf/encrypt_flag/")
    return (json.loads(r.text))['ciphertext']


def decrypt(ciphertext):
    url = "https://aes.cryptohack.org/ecbcbcwtf/decrypt/" + ciphertext + "/"
    r = requests.get(url)
    return (json.loads(r.text))['plaintext']


encrypted = encrypt()
decrypted = decrypt(encrypted)
b1 = bytes.fromhex(encrypted[:len(encrypted) - 32])
b2 = bytes.fromhex(decrypted[32:])
flag = ""
for i in range(len(b1)):
    flag += chr(b1[i] ^ b2[i])
print(flag)
