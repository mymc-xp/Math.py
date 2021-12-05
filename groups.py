from abstract_alg import *#utilizes set wrapper class and zmodn
#generalized associativity applies as well as generalized commutativity if abelian
#if a is an element of a semigroup, then a^n is the standard product of the binary function applied n times
#note to self: create permutation elements
class Semigroup(Set):#while inherits from sets, should overide adding elements as Semigroups are immutable
    def __init__(self, bfun, elements):
        super().__init__(elements)
        if not self.issemigroup(bfun, elements):
            print("error: not a semigroup")
        self.bfun = bfun #binary function that operates on elements
        self.order = len(elements)
    @staticmethod
    def issemigroup(bfun, elements):
        #to check associativity, it is necessary to brute force a(bc) = (ab)c given a,b,c are in elements
        e = list(elements)
        mod = len(elements)
        for a in elements:
            for b in elements:
                for c in elements:
                    if a == b and b == c:#assuming equality (__eq__) is defined
                        continue
                    #print(a,b,c, bfun(a, bfun(b, c)), bfun(bfun(a, b), c), bfun(a, bfun(b, c)) == bfun(bfun(a, b), c))
                    if bfun(a, bfun(b, c)) != bfun(bfun(a, b), c):
                        return False
        return True
    @staticmethod
    def isabelian(bfun, elements):#checks for commutative property ab = ba for all a,b in elements
        for a in elements:
            for b in elements:
                if bfun(a,b) != bfun(b,a):
                    return False
        return True
    def ishomomorphicto(self, ufun, H):#checks unary homomorphism f:G -> such that f(a)fa(b) = f(ab) for all a,b in G(self)
        #need to check that f:G->H will implement soon: injective -> monomorphism, surjective ->epimorphism
        #bijetive -> isomorphism, homomorphic f: G -> G is endomorpism, isomorphism f:G -> G is automorphism
        for a in self:
            for b in self:#H.bfun since the group being mapped to may have a different binary function
                if not H.bfun(ufun(a), ufun(b)) == ufun(self.bfun(a, b)):#can optimize if abelian
                    return False
        return True
    def isinjectiveto(self, ufun, H):#one to one, easy to show false if order, cardinality,size of self > order of other group
        ones = []#elements mapped to H
        for one in self:
            num = ufun(one)
            if num in ones:#checks for instance of mapping elements to the same output
                return False
            else:
                ones.append(num)
        return True
    def ismonomorphicto(self, ufun, H):# -> ker f = {e_H}
        return self.ishomomorphicto(ufun,H) and self.isinjectiveto(ufun, H)
    def issurjectiveto(self, ufun, H):#onto, for h in H, there exists g in G(self) such that f(g) = h
        #G is domain f: G -> H, the image of G == Im f surjective -> H is subset F(G)
        #easy to show false if there are not enough elements in G to cover H during the check
        s = set()
        for g in self:
            num = ufun(g)
            if num in H:
                s.add(ufun(g))
        if len(s) == H.order:
            return True
        else:
            False
    def isepimorphicto(self, ufun, H):
        return self.ishomomorphicto(ufun,H) and self.issurjectiveto(ufun, H)
    def isbijectiveto(self, ufun, H):
        return isinjectiveto(ufun, H) and Issurjectiveto(ufun, H)
    def isisomorphicto(self, ufun, H):#iff there exists an inverse function and the compositions ff^-1 = 1_G, f^-1f = 1_H
        #automorphism if f:G -> G
        return ishomomorphicto(ufun, H) and isbijectiveto(ufun, H)
    def power(self, a, exp):
        if exp == 0:
            return self.e#monoid property, moght have to modify later
        elif exp == 1:
            return a
        else:
            ax = a
            for x in range(exp - 1):
                ax = self.bfun(ax, a)
            return ax
#
class Monoid(Semigroup):
    def __init__(self, bfun, elements):#check if set is a semigroup with 2 sided identity
        super().__init__(bfun, elements)
        self.e = self.identity = self.find_identity()
        if self.identity == None:
            print("error: not a monoid")
    def find_identity(self):#checks for 2 sided identity
        for e in self.elements:
            if len([a for a in self.elements if self.bfun(a,e) == a and self.bfun(e,a) == a]) == len(self.elements):
                return e
        return None
 #
class Group(Monoid):
    def __init__(self, bfun, elements):
        super().__init__(bfun, elements)
        self.inverses = self.find_inverses()
        #print(self.inverses)
        self.generators = set()#lazy implementation, if find_generators is called this will be set
        if len(self.inverses) != len(elements):
            #print(len(self.inverses), len(elements))
            print("error:not a group")
    @staticmethod
    def zmod(p):#returns multiplicative group, congruence set mod n units
        return Group(lambda a, b: a * b ,Zmodn(p).classes.difference({CongruInt(0, p)}))
    def find_inverses(self):#checks a^-1a = aa^1 = e for all a in elements, 2 sided inverse
        container = self.elements.copy()
        container.remove(self.e)
        inverses = {self.e:self.e}#dictionary starting with e
        for a in container:
            for b in container:
                if b in inverses:
                    continue
                #print(self.bfun(a,b),self.bfun(b,a))
                if self.bfun(a,b) == self.e and  self.bfun(b,a) == self.e:
                    #print(self.bfun(a,b),self.bfun(b,a))
                    inverses[a] = b
                    if a != b:
                        inverses[b] = a
        return inverses
    def kernel(self, ufun, H): #unary f:G->H
        return self.buildsubset(lambda g: ufun(g) == H.e)#returns subset filtered by f(g) == e
    def idealof(self, other):
        '''ideal if any element in ideal in a binary function with an element in the group 
        results in an element in the ideal'''
        #work on later for rings
        pass
    def isSubgroupof(self):#under the same binary function, instantiating an instance comfirms a subset traditionally
        #closure also suffics, not necessary rn
        pass
    def isCyclic(self):
        #need to find an element such that its order is equivalent to the order of the group
        for a in self.elements:#assuming not infinite, otherwise need induction
            gens = set([a])
            count = 1
            ax = self.bfun(a, a)
            for x in range(self.order):
                gens.add(ax)
                count += 1
                if len(gens) < count:
                    break
                if len(gens) == self.order:
                    return True
                ax = self.bfun(ax, a)
                #print(a,ax)
                #print(count, len(gens), self.order)
        return False
    def gens(self):#returns list of generators
        if self.generators != set():#lazy evaluation
            return self.generators
        for a in self.elements:
            gens = set([a])#generated numbers from a
            count = 1
            ax = self.bfun(a, a)
            for x in range(self.order):
                gens.add(ax)
                count += 1
                if len(gens) < count:
                    break
                if len(gens) == self.order:
                    self.generators.add(a)
                ax = self.bfun(ax, a)
        return list(self.generators)
#