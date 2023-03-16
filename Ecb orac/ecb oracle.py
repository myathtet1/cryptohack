import json
import requests


def encrypt(plaintext):
    enc = requests.get(f"https://aes.cryptohack.org/ecb_oracle/encrypt/{plaintext}/")
    encr_byte = json.loads(enc.text)
    return encr_byte["ciphertext"]


def last_new_char(encrypt_0, string_compare):
    for i in range(255):
        new_char = hex(i)
        if len(new_char) % 2 == 1:
            new_char = "0" + new_char[2:]
        else:
            new_char = new_char[2:]
        string_try = string_compare
        string_try += new_char
        print(string_try)
        encrypt_compare = encrypt(string_try)
        if encrypt_0[32:64] == encrypt_compare[32:64]:
            return new_char
    return "00"


string_use = ""
flagg = False
length = 10
while True:
    if length == 1:
        break
    count = 16
    for x in range(count, 0, -1):
        string =""
        for y in range(x):
            string += "00"
        encrypt_0 = encrypt(string)
        string_compare = string + "63727970746f7b70336e3675316e35" + string_use
        n_char = last_new_char(encrypt_0, string_compare)
        string_use += n_char
        length -= 1
        if length == 1:
            break
out_string = bytes.fromhex(string_compare + n_char).decode()
print(out_string)

