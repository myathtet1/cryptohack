from pwn import *
import json
import my_library
import decrypt

HOST = "socket.cryptohack.org"
PORT = 13379

r = remote(HOST, PORT)

alice = r.recvline().decode().split('Intercepted from Alice: ')[1]
alice = json.loads(alice)
alice['supported'] = ["DH64"]
alice = json.dumps(alice).encode()
print(alice)
r.sendline(alice)
#
bob = r.recvline().decode().split('Intercepted from Bob: ')[1]
bob = json.loads(bob)
print(bob)
# bob['chosen'] = "DH64"
bob = json.dumps(bob).encode()
r.sendline(bob)

alice = r.recvline().decode().split('Intercepted from Alice: ')[1]
alice = json.loads(alice)
p = int(alice['p'][2:], 16)
g = 2
A = int(alice['A'][2:], 16)
print(p)
print(A)
alice = json.dumps(alice).encode()
r.sendline(alice)
print(alice)

bob = r.recvline().decode().split('Intercepted from Bob: ')[1]
bob = json.loads(bob)
print(bob)
B = int(bob['B'][2:], 16)
print(B)
bob = json.dumps(bob).encode()
r.sendline(bob)
shared_secret = my_library.pow_2(B, a, p)
print(shared_secret)

alice = r.recvline().decode().split('Intercepted from Alice: ')[1]
alice = json.loads(alice)
print(alice)
# print(decrypt.decrypt_flag(shared_secret, alice['iv'], alice['encrypted_flag']))
