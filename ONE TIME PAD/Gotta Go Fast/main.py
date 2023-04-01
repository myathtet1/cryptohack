import time
from Crypto.Util.number import long_to_bytes
import hashlib
from pwn import *
import json


HOST = "socket.cryptohack.org"
PORT = 13372

r = remote(HOST, PORT)

send1 = {'option': 'get_flag'}
send1 = json.dumps(send1).encode()
send2 = {'option': 'encrypt_data', 'input_data': '00' * 28}
send2 = json.dumps(send2).encode()
data = r.recvline()
print(data)
r.sendline(send1)

flag = r.recvline()
r.sendline(send2)
data = r.recvline()
print(flag)
print(data)

flag = json.loads(flag.decode())["encrypted_flag"]
data = json.loads(data.decode())["encrypted_data"]
flag = bytes.fromhex(flag)
data = bytes.fromhex(data)
ans = b''
print(len(flag))
print(len(data))
for i in range(28):
    print(chr(flag[i] ^ data[i]), end='')
