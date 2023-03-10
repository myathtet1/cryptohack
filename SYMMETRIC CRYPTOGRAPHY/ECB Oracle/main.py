import requests
import json


def encrypt(plaintext):
    url = "http://aes.cryptohack.org/ecb_oracle/encrypt/"+plaintext
    r = requests.get(url)
    ct = (json.loads(r.text))['ciphertext']
    return ct


plaintext = ""
flag = ""
len_plaintext = 0
str_len = "00"
while True:
    if len(encrypt("00")) < len(encrypt(str_len)):
        len_plaintext = len(encrypt("00")) - len(str_len)
        break
    else:
        str_len += "00"
while len(plaintext) < len_plaintext:
    print(flag, end=", ")
    print(plaintext)
    current = len(plaintext) >> 5
    temp_string = ""
    for i in range((current + 1) * 32 - len(plaintext) - 2):
        temp_string += "0"
    if len(temp_string) == 0:
        current += 1
        temp_string = "00000000000000000000000000000000"
    data = encrypt(temp_string)
    for i in range(256):
        hex_str = hex(i)
        if len(hex_str) % 2 == 1:
            hex_str = "0" + hex_str[2:]
        else:
            hex_str = hex_str[2:]
        if data[current * 32: (current + 1) * 32] == encrypt(temp_string + plaintext + hex_str)[current * 32: (current + 1) * 32]:
            plaintext += hex_str
            flag += bytes.fromhex(hex_str).decode()
            break
print(flag)

# print(len_plaintext)
