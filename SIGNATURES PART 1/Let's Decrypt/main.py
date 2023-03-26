from pwn import *
import json
from Crypto.Util.number import long_to_bytes, bytes_to_long
import re
from pkcs1 import emsa_pkcs1_v15
from Crypto.Hash import SHA256
from my_library import pow_2

HOST = "socket.cryptohack.org"
PORT = 13391

r = remote(HOST, PORT)

msg = 'I am MalloryWe are hyperreality and Jack and we own CryptoHack.org'
digest = emsa_pkcs1_v15.encode(msg.encode(), 256)
digest = bytes_to_long(digest)
MSG = 'We are hyperreality and Jack and we own CryptoHack.org'
DIGEST = emsa_pkcs1_v15.encode(MSG.encode(), 256)
DIGEST = bytes_to_long(DIGEST)

data = r.recvline()
send = {'option': 'get_signature'}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
data = json.loads(data.decode())
n = int(data["N"][2:], 16)
e = int(data["e"][2:], 16)
signature = int(data["signature"][2:], 16)
send = {'option': 'verify', 'msg': msg, 'e': hex(1)[2:], 'N': hex(signature - digest)[2:]}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
print(data)
