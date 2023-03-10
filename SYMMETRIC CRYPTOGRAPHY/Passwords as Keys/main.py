import requests
from Crypto.Cipher import AES
import hashlib


def decrypt(ciphertext, password_hash):
    ciphertext = bytes.fromhex(ciphertext)
    key = bytes.fromhex(password_hash)

    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
    except ValueError as e:
        return {"error": str(e)}

    return {"plaintext": decrypted.hex()}


r = requests.get('https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words')
words = r.text

ct_json = {"ciphertext": "c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66"}
ct = ct_json["ciphertext"]

arr = words.strip().split("\n")
for keyword in arr:
    KEY = hashlib.md5(keyword.encode()).digest()
    password_hash = KEY.hex()
    plaintext = decrypt(ct, password_hash)
    byte = bytes.fromhex(plaintext["plaintext"])
    text = ""
    for i in range(len(byte)):
        text += chr(int(byte[i]))
    if text[:6] == "crypto":
        print(text)
        break
    # print(plaintext)
