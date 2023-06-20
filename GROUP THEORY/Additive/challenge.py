from pwn import *
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from my_library import inverse_modulo


def is_pkcs7_padded(message):
    padding = message[-message[-1]:]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode('ascii')
    else:
        return plaintext.decode('ascii')


r = remote("socket.cryptohack.org", 13380)

data = json.loads(r.recvline().decode().split("Intercepted from Alice: ")[1][:-1])
p = int(data["p"][2:], 16)
g = int(data["g"][2:], 16)
A = int(data["A"][2:], 16)
data = json.loads(r.recvline().decode().split("Intercepted from Bob: ")[1][:-1])
B = int(data["B"][2:], 16)
data = json.loads(r.recvline().decode().split("Intercepted from Alice: ")[1][:-1])
iv = data["iv"]
ciphertext = data["encrypted"]

share_secret = A * B * inverse_modulo(2, p) % p
print(decrypt_flag(share_secret, iv, ciphertext))
