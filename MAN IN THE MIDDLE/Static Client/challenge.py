from pwn import *
import json
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


send = {"p": "0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff", "g": "0x5a9e107b9717b719c6376d43bb0254d092d7d39f820f8a3c4564422d40e20f992a41ea22b9a6c64a2a7f68e9374b9f1500fa2d33d293f6e3d6c7f3a08641dae0f04114c65762b77345744a8615d4cb8164a1bb829d25399b691c7884ba1a78208915290be41f16ca36b1b9c778f18fe3068e529eed2dc6eea29d214c54467ec1fc5f650995507f7d8781ed0bbc861bc0600641f2f6f8e044b6c4c5865f0885c8f0d9fbdbe94a0d35c173831a0c0e7acc7658fda2e58ed02a218d8576c05a60a4", "A": "0x01"}
share_secret = int("a98ae627c64b128d28f1669bf5f9465ca023b0ac55bff104f866696f290e6fdff193548e191bcf0e69b3c23bc5fe6d14f3253868d43dc274740b44e00c57d2467d646cfeeea840ba9c4d02ef87d0167eec02167a9a9dd2c2abfd54211ed898f79d8428911712dc16cf8b66dfa30de7fb235b176ae8935f4514f4b1abc5b23553798f1b0ea663c110579508f02da7b213dc9a7f1dc53a8616450d1e92fc277938c9822121cdffd5d7bbed51c4e2fc0e5a08f606f17a3b62c95ed3ee71159c3cfe", 16)
ct = {"iv": "242c03002b0ae3241878769c22ce9042", "encrypted": "e18383f7b73ce60503f4f7419198b214b72f4f107efb2afea24965e0b6999834"}
print(decrypt_flag(share_secret, ct["iv"], ct["encrypted"]))
