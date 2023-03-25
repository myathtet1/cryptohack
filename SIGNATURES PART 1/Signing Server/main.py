from pwn import *
import json
from Crypto.Util.number import long_to_bytes

HOST = "socket.cryptohack.org"
PORT = 13374

r = remote(HOST, PORT)
data = r.recvline()
print(data)

send = {'option': 'get_pubkey'}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
data = json.loads(data.decode())
n = int(data["N"][2:], 16)
e = int(data["e"][2:], 16)
send = {'option': 'get_secret'}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
data = json.loads(data.decode())
s_hex = data['secret'][2:]
s = int(data["secret"][2:], 16)
send = {'option': 'sign', 'msg': s_hex}
send = json.dumps(send).encode()
r.sendline(send)

data = r.recvline()
data = json.loads(data.decode())
flag = int(data["signature"][2:], 16)
print(long_to_bytes(flag))
