from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib


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


p = 16007670376277647657
A = 8890314426632481334
a = 590089731416500801
arr = {'iv': 'c392a5e7cd7d3779b3db5078cc0a4d60', 'encrypted_flag': 'cba7a9fd10305ab482d400d465642060f36659f3447771ed47e419c97795eb51'}
B = 11619056636947148487
shared_secret = pow(B, a, p)
print(decrypt_flag(shared_secret, arr['iv'], arr['encrypted_flag']))
