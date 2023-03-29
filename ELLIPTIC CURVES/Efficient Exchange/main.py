from my_library import compute_sum, compute_2p, inverse_modulo, compute_kp, pow_2
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


arr = {'iv': 'cd9da9f1c60925922377ea952afc212c', 'encrypted_flag': 'febcbe3a3414a730b125931dccf912d2239f3e969c4334d95ed0ec86f6449ad8'}
iv = arr['iv']
encrypted_flag = arr['encrypted_flag']
q_x = 4726
p = 9739
nB = 6534
y2 = q_x ** 3 + 497 * q_x + 1768
y = pow_2(y2, (p + 1) >> 2, p)
ans = compute_kp(nB, [q_x, y], p, 497)
print(decrypt_flag(ans[0], iv, encrypted_flag))
