import gmpy2
from Crypto.Util.number import long_to_bytes, bytes_to_long
from my_library import inverse_modulo
n = 95341235345618011251857577682324351171197688101180707030749869409235726634345899397258784261937590128088284421816891826202978052640992678267974129629670862991769812330793126662251062120518795878693122854189330426777286315442926939843468730196970939951374889986320771714519309125434348512571864406646232154103
e = 3
c = 63476139027102349822147098087901756023488558030079225358836870725611623045683759473454129221778690683914555720975250395929721681009556415292257804239149809875424000027362678341633901036035522299395660255954384685936351041718040558055860508481512479599089561391846007771856837130233678763953257086620228436828
FLAG = b"crypto{???????????????????????????????????}"
pad = (100 - len(FLAG)) * 3
m2 = 256 ** pad
n1_inv = inverse_modulo(m2, n)
x = m2 * n1_inv * c
x = x % (n * m2)
while True:
    y = int(gmpy2.iroot(x // m2, 3)[0])
    if b'crypto' in long_to_bytes(y):
        print(long_to_bytes(y))
        break
    x += n * m2
    if len(long_to_bytes(x)) > 300:
        break