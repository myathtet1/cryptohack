from pwn import *
import json
from Crypto.Util.number import bytes_to_long, long_to_bytes
from my_library import inverse_modulo, pow_2

HOST = "socket.cryptohack.org"
PORT = 13376
ADMIN_TOKEN = b"admin=True"

r = remote(HOST, PORT)

data = r.recvline()
send = {'option': 'get_pubkey'}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
data = json.loads(data.decode())
n = int(data["N"][2:], 16)
e = int(data["e"][2:], 16)
inv_msg = inverse_modulo(bytes_to_long(ADMIN_TOKEN), n)
send = {'option': 'sign', 'msg': hex(inv_msg)[2:]}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
data = json.loads(data.decode())
signature = int(data["signature"][2:], 16)
signature = inverse_modulo(signature, n)
send = {'option': 'verify', 'msg': ADMIN_TOKEN.hex(), 'signature': hex(signature)[2:]}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
print(data)
