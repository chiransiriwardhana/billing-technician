from random import randrange, getrandbits
from itertools import repeat
from functools import reduce

import sys, json, numpy as np

#Read data from stdin
def read_in():
    lines = sys.stdin.readlines()
    #Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def getPrime(n):

    def isProbablePrime(n, t = 7):

        def isComposite(a):

            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2 ** i * d, n) == n - 1:
                    return False
            return True

        assert n > 0
        if n < 3:
            return [False, False, True][n]
        elif not n & 1:
            return False
        else:
            s, d = 0, n - 1
            while not d & 1:
                s += 1
                d >>= 1
        for _ in repeat(None, t):
            if isComposite(randrange(2, n)):
                return False
        return True

    p = getrandbits(n)
    while not isProbablePrime(p):
        p = getrandbits(n)
    return p

def inv(p, q):

    def xgcd(x, y):

        s1, s0 = 0, 1
        t1, t0 = 1, 0
        while y:
            q = x // y
            x, y = y, x % y
            s1, s0 = s0 - q * s1, s1
            t1, t0 = t0 - q * t1, t1
        return x, s0, t0

    s, t = xgcd(p, q)[0:2]
    assert s == 1
    if t < 0:
        t += q
    return t

def genRSA(p, q):

    phi, mod = (p - 1) * (q - 1), p * q
    if mod < 65537:
        return (3, inv(3, phi), mod)
    else:
        return (65537, inv(65537, phi), mod)

def text2Int(text):

    return reduce(lambda x, y : (x << 8) + y, map(ord, text))

def int2Text(number, size):

    text = "".join([chr((number >> j) & 0xff)
                    for j in reversed(range(0, size << 3, 8))])
    return text.lstrip("\x00")

def int2List(number, size):

    return [(number >> j) & 0xff
            for j in reversed(range(0, size << 3, 8))]

def list2Int(listInt):

    return reduce(lambda x, y : (x << 8) + y, listInt)

def modSize(mod):

    modSize = len("{:02x}".format(mod)) // 2
    return modSize

def encrypt(ptext, pk, mod):

    size = modSize(mod)
    output = []
    while ptext:
        nbytes = min(len(ptext), size - 1)
        aux1 = text2Int(ptext[:nbytes])
        assert aux1 < mod
        aux2 = pow(aux1, pk, mod)
        output += int2List(aux2, size + 2)
        ptext = ptext[size:]
    return output

def decrypt(ctext, sk, p, q):

    mod = p * q
    size = modSize(mod)
    output = ""
    while ctext:
        aux3 = list2Int(ctext[:size + 2])
        assert aux3 < mod
        m1 = pow(aux3, sk % (p - 1), p)
        m2 = pow(aux3, sk % (q - 1), q)
        h = (inv(q, p) * (m1 - m2)) % p
        aux4 = m2 + h * q
        output += int2Text(aux4, size)
        ctext = ctext[size + 2:]
    return output

if __name__ == "__main__":

    from math import log10
    from time import time

    def printHexList(intList):
        total=""
        for index, elem in enumerate(intList):
            if index % 32 == 0:
                    pass
           
            total+="{:02x}".format(elem)
        
        return total

    def printLargeInteger(number):

        string = "{:02x}".format(number)
        for j in range(len(string)):
            if j % 64 == 0:
               print()
            print(string[j], end="")
        print()



    n=64
    p5=13477
    p6=52813
    pk, sk, mod = genRSA(p5, p6)
    lines = read_in()
    lines=np.array(lines)
    list_=[]
    #print(lines)
    symbol="/"
    final_str=""
    temp=""
    for elem in range(len(lines)):
        encrypted_each = encrypt(lines[elem], pk, mod)
        temp=printHexList(encrypted_each)+symbol
        final_str=final_str+temp
        
    print(final_str)
        
    
