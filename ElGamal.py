import random
import sys
#sys.path.append('C:\\Users\\catch\\Desktop\\Math.py')
from abstract_alg import *
from groups import *
#hard problem: given g, g^a, g^k, m*g^ak mod p compute m
def EG(bounds):
    pass
    p = random.choice([Integer(x) for x in range(bounds[0],bounds[1] + 1) if Integer(x).is_prime()])
    Zn = Group(lambda a, b: a * b ,Zmodn(p).classes.difference({CongruInt(0, p)}))
    print("p = prime:", p)
    print("is cylcic:", Zn.isCyclic())
    generators = Zn.gens()
    g = random.choice(generators)
    mspace = list(Zn.elements)
    a = random.choice(mspace).val #alice private
    A = g**a#alice public num
    b = random.choice(mspace).val #bob num
    k = random.choice(range(1, p)) #power
    m = random.choice(mspace) #bobs message
    c1 = g**k
    c2 = m * (A**k)
    #decryption
    cin1 = CongruInt(eea(c1.val, p)[c1.val], p)
    print((cin1 ** a)* c2)
    print("g, a, A, k, m, c1, c2")
    print(g,a,A,k,m,c1,c2 )
    
EG([2,500])