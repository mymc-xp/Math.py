import random
import sys
#sys.path.append('C:\\Users\\catch\\Desktop\\Math.py')
from abstract_alg import *
from groups import *
'''
Theorem:
If you can solve DLog in cyclic groups of prime order p and you can factor N
then  you can solve Dlog in cyclic grsoups of order N
'''
def ph1(g, h, N):#given g^a = h mod N where g is a generator of cyclic group of order N so g is of order N
    p = N + 1
    ps = Integer(N).prime_factorization()
    #print(ps)
    args = []#for chinease remainder theorem
    if len(set(ps)) == 1:
        print("N is a prime power, use another algorithm")
        return False
    for x in set(ps):
        i = ps.count(x)
        e = int(N/(x**i))
        o = x**i
        gx = CongruInt(g, p) ** e #group of order o in zp since power e removes other elements from the order
        hx = CongruInt(h,p) ** e
        #search manually
        for f in range(0, o):#1 is a solution occasionally such that a' = 0 mod p in args
            if gx ** f == hx:
                args.append((f, o))
    #print(args)
    return chirt(*args)#solution may need to be ajusted mod p*q and mod N
#print(ph1(2, 7, 12))
p = random.choice([Integer(x) for x in range(13,250) if Integer(x).is_prime()])
print(p)
Zn = Group.zmod(p)
g = random.choice(Zn.gens())
h = random.choice(list(Zn.elements))
print(f"{g}^a = {h} mod {p}")
s = ph1(g, h, p - 1)
print(s)
'''

'''
def ph2(g, h, p):#given integer q^e, g of order q^e and h = g^a find a
    pass# a bit complicated will do later
Zn = Group.zmod(p)

