#defines sets, Integers, and zmodn
class IntegerDivision:
    def __init__(self, num, den):#dividend and divisor
        self.num = Integer(num) #numerator
        self.den = Integer(den) #denominator
        self.remainder = Integer(num % den)
        self.quotient = Integer((self.num - self.remainder) / self.den if self.remainder > 0
                        else (self.num / self.den))
#
class Integer(int):#int wrapper class
    def __or__(self, other):# overiding the pipe operator for divides
        return self.divides(other)
    def divides(self, other):
        return other % self == 0
    def divisors(self, only_positve = False):#returnss a list of numbers that divide this
        divisors = []
        d = 1
        q = self
        limit = self ** (1/2)#not useful here unless using a predetermined list like primes, to check if prime
        while d < limit:
            if self % d == 0:
                q = self / d
                divisors.extend([Integer(d), Integer(q)])
                limit = q
            d += 1
        divisors.sort()
        if not only_positve:
            divisors.extend([-x for x in divisors])
        return divisors
    def is_prime(self):#to be faster without calling divisors, n is prime p not in set(range(<=sqrt(n))), requires knowing primes before tho, thus just cal divisors better similarly
        if self < 1:
            return False
        else:
            return len(self.divisors()) == 4
    def is_composite(self):
         return not self.is_prime()
    def prime_factorization(self):
        x = Integer(self)
        composition = []
        factors = x.divisors(True)
        factors.remove(1)
        p_factors = [j for j in factors if j.is_prime()]
        while len(p_factors) > 0:
            p = min(p_factors)
            x = Integer(x / p)
            composition.append(p)
            factors = x.divisors(True)
            p_factors = [j for j in factors if j.is_prime()]
        return composition
    @staticmethod
    def division(num, den):
        return IntegerDivision(num, den)
    @staticmethod
    def gcd(a, *args):#has errors
        if len(args) > 1:
            return Integer(Integer.gcd(Integer.gcd(a,args[0]), *args[1:]))
        else:
            return max(Set(Integer(a).divisors()).build_subset(lambda x : x in Integer(args[0]).divisors()))
    @staticmethod
    def euclidian_gcd(a, *args):#just optimized version of primitive gcd function via the algorithm
        if len(args) > 1:
            return Integer(Integer.euclidian_gcd(Integer.euclidian_gcd(a,args[0]), *args[1:]))
        else:
            state = Integer.division(a, args[0])
            r = state.remainder
            d = state.den
            while r > 0:
                state = Integer.division(state.den, r)
                r = state.remainder
                d = state.den
            return state.den
#
def eea(a, p):#extended euclidian algorithm
    if Integer.gcd(a, p) != 1:
        print("extended euclidian gcd error: inputs are not relatively prime")
        return None
    x0 = []
    state = Integer.division(a, p)
    r = state.remainder
    d = state.den
    x0.append(-state.quotient)
    while r > 0:
        #print(r,d)
        state = Integer.division(d, r)
        r = state.remainder
        d = state.den
        x0.append(-state.quotient)
    x1 = [0, 1]
    x2 = [1, 0]
    for i in range(2,len(x0) + 2):
        x1.append(x0[i - 2]*x1[i - 1] + x1[i - 2])
        x2.append(x0[i - 2]*x2[i - 1] + x2[i - 2])
    #print(x0)
    #print(x1)
    #print(x2)
    return { a:x2[len(x2) - 2], p:x1[len(x1) - 2]}
#
#chinese remainder theorem
'''
the solution is similar to that of polynomial interpolation,
where you construct and equation that is true at a certain point.
in this case, we are satisfying equivalence under a modulus for x
ex: x = 3 mod 19 and  x = 5 mod 37
-> x = (3 * -1 * 37) + (5*2*19)
       -1 is the inverse of 37 mod 19 and 37 is 0 mod 37,
       so it suffices as a solution to the system mod 19
       similar is true for the other addend
       the sum sasisfies both equations while being true mod 19*37
       additional equivalences can be found by extending the equation to
       satisfy all equations or by recusively using the solution between a pair of equations on another
'''
def chirt(a, *args):#pass in any number of tuples (a, b) a is the number b the modulus and we solve for x, moduli must be relatively prime
    if len(args) > 1:
            return chirt(chirt(a,args[0]), *args[1:])
    else:
        b = args[0]
        if Integer.gcd(a[1], b[1]) != 1:
            print("chinease remainder theorem error: inputs are not relatively prime")
            return None
        ime = eea(a[1], b[1]) #inverse mod other modulus
        return (a[0] *ime[b[1]] *b[1] + b[0] *ime[a[1]] * a[1], a[1]*b[1])
#
class Set(set):
    def __init__(self, elements):
        if type(elements) != set and isinstance(elements, set):
            elements = elements.elements
        self.set_elements(elements)
        self.universe = self.elements.copy()
    def __str__(self):
        return(self.elements.__str__())
    def __iter__(self):
        return self.elements.__iter__()
    def __len__(self):
        return self.elements.__len__()
    def __eq__(self, other):
        if type(other) == list:
            other = set(other)
        if type(other) == set:
            return self.elements == other
        elif type(other) == type(self):
            print(type(self))
            return self.elements == other.elements
        else:
            print("= error")
    def __contains__(self, e):
        return e in self.elements
    def set_elements(self, elements):#
        self.elements = set(elements.copy())
    def share_universe(self, other):#adds elements from another and syncs universe
        self.universe.update(other.elements)
        other.__set_universe(self.universe)
    def __set_universe(self, u):#assigns the same set, not a copy
        self.universe = u
    def same_universe(self, other):
        return self.universe == other.universe
    def add(self, *args):#eqivalent to .add() set method, but optimized for the class
        for a in args:
            if type(a) == type(self):
                self.elements.update(a.elements)
            elif type(a) == set:
                self.elements.update(a)
            else:
                self.elements.add(a)
    def remove(self, e):
        self.elements.remove(e)
    def build_subset(self, predicate):#returns a filtered set, which is a subset 
        #should add a map function later
        #may add functionality where a subset is created with its universe set to the one that generates it
        return Set([x for x in self.elements if predicate(x)])
    def subset_of(self, other):#.issubset() 
        return len([x for x in self if x in other]) == len(self)
    def union(self, *args):#.union() python | operate or .update() with modification
        combination = self.elements.copy()
        for a in args:
            combination.update(a)
        return Set(combination)
    def __or__(self, other):
        return self.union(other)
    def intersect(self, *args):#.intersection() in python
        sect = None
        for a in args:
            sect = self.build_subset(lambda e : e in a)
        return sect
    def __and__(self, other):
        return self.intersect(other)
    def disjoint(self, other):#.isdisjoint() in python
        return self.intersect(other) == set()#empty set
    def subtract(self, other):#difference
        return self.build_subset(lambda e: e not in other)
    def complement(self):
        return Set(self.universe).subtract(self)
    def __p(self, s):#got from some wiki don't remember where
        s = list(s)
        if s==[]: # base case
            return [s] # if s is empty, then the only sublist of s is s itself
        else:
            e = s[0] # any e from s (in this implementation, we choose the first e)
            t = s[1:] # s with e removed
            pt = self.__p(t) # the list of all sublists of t (note that this is a recursive call)
            fept = [x + [e] for x in pt] # pt with e appended to each sublist
            return pt + fept # the concatenation of all constructed sublists
    def power_set(self):#returns a list of sets otherwise have to deal with frozensets witch can't be check directly with in frozenset
        return [x for x in self.__p(self.elements)]
    def set_product(self, other):
        product = set()
        for x in self.elements():
            for y in self.elements():
                product.add((x, y))
        return product
#
class CongruInt:#"wrapper" for integers that acts as a congruence for all integers equivalent mod p
    #a == b mod p -> a - b = pd for some p
    def __init__(self, val = 0, modulus = None):
        self.modulus = modulus
        self.set_val(val)
    def __repr__(self):
        return str(self.val)
    def __int__(self):
        return self.val
    def set_val(self, val):#value is reduced to its class rep
        if self.modulus == None:
            self.val = int(val)
        else:
            self.original = int(val)
            self.val = int(val) % self.modulus
    def __hash__(self):
        return hash((self.val, self.modulus))
    def __eq__(self, other):
        if type(other) == int:
            return self.val == other % self.modulus
        elif type(other) == type(self):
            return self.val == other.val and self.modulus == other.modulus
        else:
            #print(self, other, type(self), type(other))
            return False
    def __mul__(self, other):
        if type(other) == int:
            return CongruInt(self.val * other, self.modulus)
        elif type(other) == type(self):
            if self.modulus == other.modulus:
                return CongruInt(self.val * other.val, self.modulus)
            else:
                print("error, classes not of the same set zmodn")
                return False
        else:
            return False
    def __pow__(self, other):
        #in some instances pow could indicate multiplication, so i may include a way to switch functionality
        #but as of now a**b -> repeated multiplication
        if type(other) == int:
            e = other
        elif type(other) == type(self):
            if self.modulus == other.modulus:
                e = other.val
            else:
                print("error: pow")
                return False
        else:
            return False
        #need to write optimized exponent formula for congruence
        exp = [int(x) for x in bin(e)[2:]]
        exp.reverse()
        p = 1
        b = self.val
        for x in range(len(exp)):
            if exp[x] == 1:
                p *= b
            if x != len(exp) - 1:
                b = (b**2) % self.modulus
        #return p
        return CongruInt(p, self.modulus)
    def __add__(self, other):
        if type(other) == int:
            return CongruInt(self.val + other, self.modulus)
        elif type(other) == type(self):
            if self.modulus == other.modulus:
                return CongruInt(self.val + other.val, self.modulus)
            else:
                print("error, classes not of the same set zmodn")
                return False
        else:
            return False
    def __neg__(self):#this return additive inverse
        return CongruInt(-self.val, self.modulus)
    def __sub__(self, other):
        return self.__add__(-other)
    def inverse(self):#multiplicative inverse
        #return eea
        return [CongruInt(x) for x in range(self.modulus) if self*x == 1][0]
    def order(self):#should implement abstraction for groups
        #can probably filter out numbers where gcd != 1
        c = 1
        while True:
            x = self**c
            #print(x)
            if x == 0:
                return None #infinite
            elif x == 1:
                return c
            c += 1
#
class Zmodn(Set):#set of congruence classes, z mod n, a - b = c * n meaning difference is a multiple of n
    def __init__(self, modulus):
        self.modulus = modulus#should be an int
        self.classes = {CongruInt(x, modulus) for x in range(modulus)}
        self.elements = []
        super().__init__(self)
    def class_of(self, value):
        return CongruInt(value, self.modulus)
    def units(self):# ax = 1 iff (a, n) = 1, n = modulus
        return [x for x in self.classes if 1 in [(x*j).val for j in range(self.modulus)]]
    def zero_divs(self):
        return [x for x in self.classes if 0 in [(x*j).val for j in range(1, self.modulus)]]
#
if __name__ == "__main__":
    print(Integer.gcd(133, 589))
    import time as t
    s = t.time()
    print(chirt((54,11), (525,1334)))
    print(t.time() - s)
    '''
    
    b = 522
    e = 5424244
    p = 63
    s = t.time()
    x = CongruInt(b, p)
    print(x**e)
    print(t.time() - s)
    s = t.time()
    print((b**e)%p)
    print(t.time() - s)
    s = t.time()
    print(pow(b, e, p))
    print(t.time() - s)'''
    
    #print(f"x = {x}")
    #print(2 + x)#error