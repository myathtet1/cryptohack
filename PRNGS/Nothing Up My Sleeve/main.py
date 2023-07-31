from pwn import *
import json
from ecdsa import ellipticcurve
from ecdsa.ecdsa import curve_256, generator_256
casino_x = "0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296"
casino_y = "0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5"
reds = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
blacks = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}
odds = {1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35}
evens = {2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36}

Q = ellipticcurve.Point(curve_256, int(casino_x, 16), int(casino_y, 16))
P = ellipticcurve.Point(curve_256, int(casino_x, 16), int(casino_y, 16))

r = remote("socket.cryptohack.org", 13387)
print(r.recvline())
send = {"x": hex(Q.x()), "y": hex(Q.y())}
send = json.dumps(send).encode()
r.sendline(send)
print(r.recvline())


def next_s(seed):
    t = seed
    s = (t * P).x()
    seed = s
    z = (s * Q).x()
    return z & (2 ** (8 * 30) - 1), seed


def rebase(n, b=37):
    if n < b:
        return [n]
    else:
        return [n % b] + rebase(n // b, b)


spins = []
while True:
    send = {"choice": "EVEN"}
    send = json.dumps(send).encode()
    r.sendline(send)
    data = json.loads(r.recvline().decode())
    print(data)
    spin = data['spin']
    spins.append(spin)
    if "Good evening, I will be your new croupier for the time being. " in data["msg"]:
        break


seed = 0
print(spins)
for i in spins:
    seed *= 37
    seed += i
check = []
for i in range(5):
    send = {"choice": "EVEN"}
    send = json.dumps(send).encode()
    r.sendline(send)
    data = json.loads(r.recvline().decode())
    print(data)
    spin = data['spin']
    check.append(spin)
print(check)
for i in range(2 ** 16, -1, -1):
    if i % 1000 == 0:
        print(i)
    n_se = int(bin(i)[2:] + bin(seed)[2:], 2)
    ne = (n_se * Q).x() & (2 ** (8 * 30) - 1)
    spins = rebase(ne)
    check2 = []
    for j in range(len(check) - 1, -1, -1):
        check2.append(check[j])
    while check2.pop() == int(spins.pop()):
        if len(check2) == 0:
            break
    if len(check2) == 0:
        seed = n_se
        print("oke")
        break
ne = (seed * Q).x() & (2 ** (8 * 30) - 1)
spins = rebase(ne)
print(spins)
for i in range(5):
    spins.pop()
while True:
    spin = spins.pop()
    if len(spins) == 0:
        ne, seed = next_s(seed)
        spins = rebase(ne)
    send = {"choice": int(spin)}
    send = json.dumps(send).encode()
    r.sendline(send)
    data = json.loads(r.recvline().decode())
    print(data)
    if "Congratulations Mr Jarecki! Here's a flag: " in data["msg"]:
        break
