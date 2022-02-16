"""
FCA - Python libraries to support FCA tasks
Copyright (C) 2017  Victor Codocedo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Kyori code.
from inspect import stack
from functools import reduce
from fca.defs import OnDiskPOSET, POSET, SetPattern
from fca.algorithms.cbo import PSCbO
from fca.algorithms import Algorithm, lexo
# import objgraph

class LecEnumClosures(Algorithm):
    """
    Applies LexEnumClosures algorithm
    Enumeraes Closures in Lectical Order
    Enumerates in lectical order:
    A < B \iff \exists_i (i \in B, i \not \in A, \forall_{j<i} (j \in A \iff j \in B))

    Let the lexical order be: 1 < 2 < 3 < 4
    Then the enumeration goes:
    4
    3
    34
    2
    24
    23
    234
    1
    14
    13
    134
    12
    124
    123
    1234

    The main benefit is that when an element appears in the enumeration, all its proper subsets
    have already been enumerated
    This is particularly needed for calculating pre-closure and implications
    """
    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.poset = None
        self.e_pattern = SetPattern
        self.pattern = kwargs.get('pattern', SetPattern)
        self.cache = kwargs.get('cache', [])
        self.min_sup = kwargs.get('min_sup', 0)
        self.printer = kwargs.get('printer', lambda a, b, c: None)
        self.conditions = kwargs.get('conditions', [])
        self.ondisk = kwargs.get('ondisk', False)
        self.ondisk_kwargs = kwargs.get('ondisk_kwargs', {})
        
        self.calls = 0

        self.config()
        super(LecEnumClosures, self).__init__(**kwargs)

    def config(self):
        """
        Configure the stacks

        stack: stack with the patterns
        stack_enum: stack with the enumerators used for in the stack
        stack_cid: stack witht the mappings to the poset of formal concepts
        """
        if not self.ondisk:
            self.poset = POSET(transformer=self.ctx.transformer)
        else:
            self.poset = OnDiskPOSET(transformer=self.ctx.transformer, **self.ondisk_kwargs)

    def next_closure(self, X):
        """
        Original Next Closure algorithm as found in the book "Conceptual Exploration" by Ganter and Obiedkov
        Receives a closed pattern set X and returns the lectically next closed pattern set.
        If X contains all attributes, the algorithms will return None so AllClosures can end
        """
        for m in range(self.ctx.n_attributes-1, -1, -1):
            if m in X:
                X.remove(m)
                if self.stack[-1][0] == m:
                    self.stack.pop()
            else:
                Y = self.e_pattern.intersection( self.stack[-1][1], self.ctx.m_prime[m] )
                Xc = self.derive_extent(Y)
                if m <= min(Xc - X): # CANONICAL TEST
                    self.stack.append( (m , Y) )
                    return Xc
        return None

    def run(self, *args, **kwargs):
        """
        Computes all the closures and store them in the poset
        Implements all_closures algorithm
        """
        # FIRST CLOSURE
        X = self.pattern.bottom()
        Y = self.derive_intent(X)
        X = self.derive_extent(Y)
        
        self.stack = [ (None, Y) ]

        while X is not None:
            self.poset.new_formal_concept(self.stack[-1][1], self.pattern.copy(X) )
            X = self.next_closure(X)

    def derive_intent(self, P):
        """
        Derive an intent to obtain its extent
        """
        return set([ei for ei, e in self.ctx.g_prime.items() if P.issubset(e)])

    def derive_extent(self, P):
        """
        Derive an extent to obtain its intent
        """
        return set([ei for ei, e in self.ctx.m_prime.items() if P.issubset(e)])

class PSLecEnumClosures(LecEnumClosures):
    """
    LexEnumClosures with support for pattern structure at extent level
    """
    def config(self):
        
        self.e_pattern = self.pattern
        self.pattern = SetPattern

        if not self.ondisk:
            self.poset = POSET(transformer=self.ctx.transformer)
        else:
            self.poset = OnDiskPOSET(transformer=self.ctx.transformer, **self.ondisk_kwargs)

        list(map(self.e_pattern.top, self.ctx.g_prime.values()))

        self.all_objects = self.e_pattern.top()

        self.ctx.m_prime = {g: self.e_pattern.fix_desc(desc) for g, desc in self.ctx.g_prime.items()}
        
        self.ctx.n_attributes = len(self.ctx.g_prime)

    def derive_intent(self, P):
        """
        Derive an intent and obtain the associated pattern
        """
        if not bool(P):
            return self.e_pattern.top()
        return reduce(self.e_pattern.intersection, (self.ctx.m_prime[m] for m in P))
    
    def derive_extent(self, P):
        """
        Derive an extent to obtain its intent
        """
        return set([ei for ei, e in self.ctx.m_prime.items() if self.e_pattern.leq(P, e)])
