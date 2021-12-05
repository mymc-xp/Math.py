import random
import sys
#sys.path.append('C:\\Users\\catch\\Desktop\\Math.py')
from abstract_alg import *
from groups import *
#hard problem: govem g. g^a, g^b mod p compute g^ab mod p
def DHE(bounds):#bounds will be the range(inclusive) of numbers the prime will be selected from if it exists
    #randomly selects a generator and a prime then 2 random integers and generates a key
    #g = random.choice(cGroup)#needs to be a primitive root aka genrerator
    p = random.choice([Integer(x) for x in range(bounds[0],bounds[1] + 1) if Integer(x).is_prime()])
    Zn = Group(lambda a, b: a * b ,Zmodn(p).classes.difference({CongruInt(0, p)}))
    print("p = prime:", p)
    print("is cylcic:", Zn.isCyclic())
    generators = Zn.gens()
    g = random.choice(list(generators))
    a = random.choice(list(Zn.elements)).val #alice num
    b = random.choice(list(Zn.elements)).val #bob num
    alice_msg = Zn.power(g, a)
    bob_msg = Zn.power(alice_msg, b)
    print("shared secret:", bob_msg)
    print("g^b*a = g^a*b:", ((g**b)**a) == bob_msg)
    print("p, g, a, b:", p, g, a, b)
DHE([2,100])