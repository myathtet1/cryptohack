# Python3 program to implement Shanks Tonelli
# algorithm for finding Modular Square Roots

# utility function to find pow(base,
# exponent) % modulus
def pow1(base, exponent, modulus):
    result = 1
    base = base % modulus
    while (exponent > 0):
        if (exponent % 2 == 1):
            result = result * base
            result = result % modulus
        exponent = int(exponent) >> 1
        base = base * base
        base = base % modulus

    return result;


# utility function to find gcd
def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a


# Returns k such that b^k = 1 (mod p)
def order(p, b):
    if (gcd(p, b) != 1):
        print("p and b are not co-prime.\n");
        return -1;

    # Initializing k with first
    # odd prime number
    k = 3;
    while (True):
        if (pow1(b, k, p) == 1):
            return k;
        k += 1;


# function return p - 1 (= x argument) as
# x * 2^e, where x will be odd sending e
# as reference because updation is needed
# in actual e
def convertx2e(x):
    z = 0
    while x % 2 == 0:
        x = x >> 1
        z += 1

    return [x, z]


# Main function for finding the
# modular square root
def STonelli(n, p):
    # a and p should be coprime for
    # finding the modular square root
    if (gcd(n, p) != 1):
        print("a and p are not coprime\n");
        return -1;

    # # If below expression return (p - 1) then
    # # modular square root is not possible
    # if pow1(n, int((p - 1) / 2), p) == (p - 1):
    #     print("no sqrt possible\n");
    #     return -1;

    # expressing p - 1, in terms of s * 2^e,
    # where s is odd number
    ar = convertx2e(p - 1);
    s = ar[0];
    e = ar[1];

    # finding smallest q such that
    # q ^ ((p - 1) / 2) (mod p) = p - 1
    q = 2;
    while (True):

        # q - 1 is in place of (-1 % p)
        k = (p - 1) >> 1
        if pow1(q, k, p) == (p - 1):
            break
        q += 1

    # Initializing variable x, b and g
    s_1 = (s + 1) >> 1
    x = pow1(n, s_1, p)
    b = pow1(n, s, p)
    g = pow1(q, s, p)

    r = e;

    # keep looping until b become
    # 1 or m becomes 0
    while (True):
        m = 0;
        while (m < r):
            if (order(p, b) == -1):
                return -1;

            # finding m such that b^ (2^m) = 1
            if (order(p, b) == pow(2, m)):
                break;
            m += 1;

        if (m == 0):
            return x;

        # updating value of x, g and b
        # according to algorithm
        x = (x * pow1(g, pow(2, r - m - 1), p)) % p;
        g = pow1(g, pow(2, r - m), p);
        b = (b * g) % p;

        if (b == 1):
            return x;
        r = m;

