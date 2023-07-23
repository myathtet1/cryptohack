import string

from Crypto.Random.random import getrandbits
import random
from pwn import *
import json
from my_library import inverse_modulo
SEED = getrandbits(32)
FLAG = b'crypto{????????????????????}'
q = 127
# r = remote("socket.cryptohack.org", 13390)
#
# print(r.recvline())
# send = {"option": "reset"}
# send = json.dumps(send).encode()
# r.sendline(send)
# print(r.recvline())
a_arr = []
b_arr = []
for _ in range(73):
    r = remote("socket.cryptohack.org", 13390)
    print(r.recvline())
    send = {"option": "get_sample"}
    send = json.dumps(send).encode()
    r.sendline(send)
    data = json.loads(r.recvline().decode())
    print(data)
    a_arr.append(data["a"])
    b_arr.append(data["b"])


def compare(a1, b1, a2, b2):
    index = -1
    for i in range(len(FLAG)):
        if a1[i] != a2[i]:
            index = i
            break
    if index == -1:
        return None
    a = (a1[index] - a2[index]) % q
    a_inv = inverse_modulo(a, q)
    b = (b1 - b2) % q
    # print("index =", index, end=": ")
    arr = []
    for i in range(-2, 3, 1):
        arr.append(chr(((b + i) % q) * a_inv % q))
    return (index, arr)


dic = {}
alphabet = string.ascii_letters + string.digits + "_" + "@" + "!" + "$" + "{" + "}"
for i in range(len(FLAG)):
    dic[i] = {}
for i in range(len(a_arr) - 1):
    for j in range(i + 1, len(a_arr)):
        mat = compare(a_arr[i], b_arr[i], a_arr[j], b_arr[j])
        if mat != None:
            for c in mat[1]:
                if not c in alphabet:
                    continue
                if not c in dic[mat[0]]:
                    dic[mat[0]][c] = 1
                else:
                    dic[mat[0]][c] += 1
flag = ""
for i in range(len(FLAG)):
    m = 0
    c = '.'
    for j in dic[i]:
        if dic[i][j] > m:
            m = dic[i][j]
            c = j
    flag += c
    print(flag)
# flag = "crypto{f4ult_4ttack5_0n_LW3}"
