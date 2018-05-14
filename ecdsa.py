from random import SystemRandom
from hashlib import sha256 #ganti dengan keccak
import math


def divisors(n):
    d = [0]
    for i in range(1, abs(n)+1):
        if n % i == 0:
            d.append(i)
            d.append(-i)
    return d


def euclid(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g,y,x = euclid(b%a,a)
        return (g,x-(b//a)*y, y)


def invmod(a, n):
    g,x,y = euclid(a, n)
    if g != 1:
        raise ValueError('multiplicative inverse does not exist')
    else:
        return x%n


class Point(object):
    def __init__(self, x, y):
        self.x,self.y = x,y
        self.infstat = False

    def infinity_point(self):
        P = Point(0, 0)
        P.infstat = True
        return P

    def __repr__(self):
        if self.infstat:
            return 'O'
        else:
            return '(' + repr(self.x) + ',' + repr(self.y) + ')'

    def __eq__(self,other):
        if self.infstat:
            return other.inf
        elif other.inf:
            return self.infstat
        else:
            return self.x == other.x and self.y == other.y

    def is_infinite(self):
        return self.infstat


class Curve(object):
    def __init__(self, a, b, c, char):
        self.a, self.b, self.c = a, b, c
        self.char = char

    def __str__(self):
        if self.a == 0:
            astr = ''
        elif self.a == 1:
            astr = ' + x^2'
        elif self.a == -1:
            astr = ' - x^2'
        elif self.a < 0:
            astr = " - " + str(-self.a) + 'x^2'
        else:
            astr = " + " + str(self.a) + 'x^2'

        if self.b == 0:
            bstr = ''
        elif self.b == 1:
            bstr = ' + x'
        elif self.b == -1:
            bstr = ' - x'
        elif self.b < 0:
            bstr = " - " + str(-self.b) + 'x'
        else:
            bstr = " + " + str(self.b) + 'x'

        if self.c == 0:
            cstr = ''
        elif self.c < 0:
            cstr = " - " + str(-self.c)
        else:
            cstr = " + " + str(self.c)

        self.eq = 'y^2 = x^3' + astr + bstr + cstr
        return self.eq + ' mod ' + str(self.char)

    def nth_order(self, P):
        Q = P
        orderP = 1
        while not Q.is_infinite():
            Q = self.add(P,Q)
            orderP += 1
        return orderP

    def get_y(self, x):
        return math.sqrt(x*x*x + self.a*x*x + self.b*x + self.c)

    def double(self, P):
        return self.add(P,P)

    def multiply(self, P, k):
        p = Point(0,0)
        if P.is_infinite():
            return P
        elif k == 0:
            return p.infinity_point()
        elif k < 0:
            return self.multiply(self.invert(P), -k)
        else:
            b = bin(k)[2:]
            return self.repeat_additions(P, b, 1)

    def repeat_additions(self, P, b, n):
        p = Point(0, 0)
        if b == '0':
            return p.infinity_point()
        elif b == '1':
            return P
        elif b[-1] == '0':
            return self.repeat_additions(self.double(P), b[:-1], n+1)
        elif b[-1] == '1':
            return self.add(P, self.repeat_additions(self.double(P), b[:-1], n+1))

    def show_points(self):
        return [repr(P) for P in self.get_points()]

    #List all multiples of a point on the curve.
    def generate(self, P):
        p = Point(0, 0)
        Q = P
        orbit = [repr(p.infinity_point())]
        while not Q.is_infinite():
            orbit.append(repr(Q))
            Q = self.add(P,Q)
        return orbit


class CurveModP(Curve):
    def __init__(self, a, b, c, p):
        Curve.__init__(self, a, b, c, p)

    def contains(self, P):
        if P.is_infinite():
            return True
        else:
            return (P.y*P.y) % self.char == (P.x*P.x*P.x + self.a*P.x*P.x + self.b*P.x + self.c) % self.char

    def get_points(self):
        p = Point(0, 0)
        points = [p.infinity_point()]
        for x in range(self.char):
                for y in range(self.char):
                    P = Point(x,y)
                    if (y*y) % self.char == (x*x*x + self.a*x*x + self.b*x + self.c) % self.char:
                        points.append(P)
        return points

    def invert(self, P):
        if P.is_infinite():
            return P
        else:
            return Point(P.x, -P.y % self.char)

    def add(self, p1, p2):
        yd = (p2.y - p1.y) % self.char
        xd = (p2.x - p1.x) % self.char
        p = Point(0,0)
        if p1.is_infinite():
            return p2
        elif p2.is_infinite():
            return p1
        elif xd == 0 and yd != 0:
            return p.infinity_point()
        elif xd == 0 and yd == 0:
            if p1.y == 0:
                return p.infinity_point()
            else:
                ld = ((3 * p1.x * p1.x + 2 * self.a * p1.x + self.b) * invmod(2 * p1.y, self.char)) % self.char
        else:
            ld = (yd * invmod(xd, self.char)) % self.char
        nu = (p1.y - ld * p1.x) % self.char
        x = (ld * ld - self.a - p1.x - p2.x) % self.char
        y = (-ld*x - nu) % self.char
        return Point(x,y)

#ECDSA section INI NANTI GANTI2 AJA

#Use sha256 to hash a message, and return the hash value as an integer. nanti ganti keccak
def hash(message):
    return int(sha256(message).hexdigest(), 16)

#Hash the message and return integer whose binary representation is the the L leftmost bits
#of the hash value, where L is the bit length of n.
def hash_and_truncate(message, n):
    h = hash(message)
    b = bin(h)[2:len(bin(n))]
    return int(b, 2)

#Generate a keypair using the point P of order n on the given curve. The private key is a
#positive integer d smaller than n, and the public key is Q = dP.
def generate_keypair(curve, P, n):
    r = SystemRandom()
    d = r.randrange(1, n)
    Q = curve.multiply(P, d)
    writefile("eccpublic", repr(Q))
    writefile("eccprivate", d)
    return (d, Q)

#Create a digital signature for the string message using a given curve with a distinguished
#point P which generates a prime order subgroup of size n.
def sign(message, curve, P, n, keypair):
    #Extract the private and public keys, and compute z by hashing the message.
    d, Q = keypair
    z = hash_and_truncate(message, n)
    #Choose a randomly selected secret point kP then compute r and s.
    r, s = 0, 0
    while r == 0 or s == 0:
        k = 4
        R = curve.multiply(P, k)
        r = R.x % n
        s = (invmod(k, n) * (z + r * d)) % n
    return (Q,r,s)

def calculate_r_and_s(message, curve, P, n, d):
    z = hash_and_truncate(message, n)
    r, s = 0, 0
    while r == 0 or s == 0:
        k = 4
        R = curve.multiply(P, k)
        r = R.x % n
        s = (invmod(k, n) * (z + r * d)) % n
    return (r, s)

def parse_sign(Q, r, s):
    p = repr(Q) + repr(r) + repr(s)
    return p

#Verify the string message is authentic, given an ECDSA signature generated using a curve with
#a distinguished point P that generates a prime order subgroup of size n.
def verify(message, curve, P, n, signature):
    Q, r, s = signature
    #Confirm that Q is on the curve.
    if Q.is_infinite() or not curve.contains(Q):
        return False
    #Confirm that Q has order that divides n.
    if not curve.multiply(Q, n).is_infinite():
        return False
    #Confirm that r and s are at least in the acceptable range.
    if r > n or s > n:
        return False
    #Compute z in the same manner used in the signing procedure,
    #and verify the message is authentic.
    z = hash_and_truncate(message, n)
    w = invmod(s, n) % n
    u_1, u_2 = z * w % n, r * w % n
    C_1, C_2 = curve.multiply(P, u_1), curve.multiply(Q, u_2)
    C = curve.add(C_1, C_2)
    return r % n == C.x % n

def writefile(fl, w):
    f = open(fl, "w")
    f.write(repr(w))
    f.close()

def readfile(fl):
    with open (fl, "r") as myfile:
        x = myfile.read()
    return x

def parse_publickey(p):
    tx = p[p.find("(") + 1:p.find(")")]
    tx1 = tx.split(",")
    x,y = 0,0
    try:
        x = int(tx1[0])
    except ValueError:
        x = int(float(tx1[0]))

    try:
        y = int(tx1[1])
    except ValueError:
        y = int(float(tx1[1]))
    Q = Point(x,y)
    return Q

def parse_privatekey(p):
    try:
        return int(p)
    except ValueError:
        return int(float(p))



c = CurveModP(1,0,3,7)
print(c.show_points())

#pilih point yang ada di show_points
p = Point(3,5)
print(str(p))
k = generate_keypair(c,p,c.nth_order(p))
str = "apa sih ini"
str = str.encode('utf-8')
s = sign(str,c,p,c.nth_order(p),k)

z = parse_sign(s[0],s[1],s[2])

print(s)

#cek signature
pri = readfile("eccprivate")
pub = readfile("eccpublic")

d = parse_privatekey(pri)
Q = parse_publickey(pub)

w = calculate_r_and_s(str,c,p,c.nth_order(p),d)

signat = (Q,w[0],w[1])

print(verify(str,c,p,c.nth_order(p),signat))
