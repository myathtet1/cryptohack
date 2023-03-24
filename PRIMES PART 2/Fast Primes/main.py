import math
from Crypto.PublicKey import RSA
from my_library import pow_2, inverse_modulo
from Crypto.Cipher import PKCS1_OAEP
primes = []


def sieve(maximum=10000):
    # In general Sieve of Sundaram, produces primes smaller
    # than (2*x + 2) for a number given number x. Since
    # we want primes smaller than maximum, we reduce maximum to half
    # This array is used to separate numbers of the form
    # i+j+2ij from others where 1 <= i <= j
    marked = [False]*(int(maximum/2)+1)

    # Main logic of Sundaram. Mark all numbers which
    # do not generate prime number by doing 2*i+1
    for i in range(1, int((math.sqrt(maximum)-1)/2)+1):
        for j in range(((i*(i+1)) << 1), (int(maximum/2)+1), (2*i+1)):
            marked[j] = True

    # Since 2 is a prime number
    primes.append(2)

    # Print other primes. Remaining primes are of the
    # form 2*i + 1 such that marked[i] is false.
    for i in range(1, int(maximum/2)):
        if (marked[i] == False):
            primes.append(2*i + 1)


def get_primorial(n):
    result = 1
    for i in range(n):
        result = result * primes[i]
    return result


sieve()
M = get_primorial(40)
print("M =", M)
ciphertext = "249d72cd1d287b1a15a3881f2bff5788bc4bf62c789f2df44d88aae805b54c9a94b8944c0ba798f70062b66160fee312b98879f1dd5d17b33095feb3c5830d28"
file = open("key.pem", 'rb')
data = file.read().decode()
key = RSA.import_key(data)
n = key.n
e = key.e
file.close()
print("n =", n)     # use http://factordb.com/index.php?query=
x = 6496671072123871038     # e ^ x = c [M]
p = 51894141255108267693828471848483688186015845988173648228318286999011443419469
q = 77342270837753916396402614215980760127245056504361515489809293852222206596161
phi = (p - 1) * (q - 1)
d = inverse_modulo(e, phi)
key = RSA.construct((n, e, d))
cipher = PKCS1_OAEP.new(key)
print(cipher.decrypt(bytes.fromhex(ciphertext)))
