from random import randint


def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


def pow1(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = result * base
            result = result % modulus
        exponent = int(exponent) >> 1
        base = base * base
        base = base % modulus

    return result


# utility function to find gcd
# Returns k such that b^k = 1 (mod p)
def order(p, b):
    if gcd(p, b) != 1:
        print("p and b are not co-prime.\n")
        return -1
        # Initializing k with first
        # odd prime number
    k = 3
    while True:
        print(k)
        if pow1(b, k, p) == 1:
            return k
        k += 1


a = 288260533169915
p = 1007621497415251 # a = x ^ 2 (mod p)

FLAG = b'crypto{????????????????????}'


def encrypt_flag(flag):
    print(bin(flag[9]))
    print(bin(flag[8]))
    print(bin(flag[0]))
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag]) # array to string
    # print(plaintext)
    for b in plaintext:
        e = randint(1, p)
        n = pow(a, e, p)
        if b == '1':
            ciphertext.append(n)
        else:
            n = -n % p
            ciphertext.append(n)
    return ciphertext


file = open("output.txt")
data = file.read()
arr = data[1:len(data) - 2].split(", ")
str_sol = ""
for i in range(len(arr)):
    number = int(arr[i])
    if pow(number, (p - 1) >> 1, p) == 1:
        str_sol += '1'
    else:
        str_sol += '0'
print(str_sol)
size = len(str_sol) >> 3
for i in range(size):
    temp = 0
    for j in range(8):
        if str_sol[i * 8 + j] == '1':
            temp += 2 ** (7 - j)
    print(chr(temp), end='')
