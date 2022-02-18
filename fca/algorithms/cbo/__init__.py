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
from functools import reduce
from fca.defs import OnDiskPOSET, POSET, SetPattern
from fca.algorithms import Algorithm, lexo

class CbO(Algorithm):
    """
    Implementation of Close-by-One
    """

    def __init__(self, ctx, **kwargs):
    #     self.ctx = ctx
    #     self.poset = None
    #     # self.e_pattern = SetPattern
    #     self.pattern = kwargs.get('pattern', SetPattern)
    #     self.cache = kwargs.get('cache', [])
    #     self.min_sup = kwargs.get('min_sup', 0)
    #     self.printer = kwargs.get('printer', lambda a, b, c: None)
        self.conditions = kwargs.get('conditions', [])
    #     self.ondisk = kwargs.get('ondisk', False)
    #     self.ondisk_kwargs = kwargs.get('ondisk_kwargs', {})
        
    #     self.calls = 0

    #     self.config()
        super(CbO, self).__init__(ctx, **kwargs)

    def config(self):
        """
        Configure the internal parameters of the class
        """
        # if not self.ondisk:
        #     self.poset = POSET(transformer=self.ctx.transformer)
        # else:
        #     self.poset = OnDiskPOSET(transformer=self.ctx.transformer, **self.ondisk_kwargs)
        self.e_pattern.top(set(self.ctx.g_prime.keys()))

        # self.all_objects = set(self.ctx.g_prime.keys())

        # self.poset.new_formal_concept(
        #     self.all_objects,
        #     self.pattern.bottom(),
        #     self.poset.supremum
        # )
        # self.pattern.top(set(self.ctx.m_prime.keys()))
        self.conditions.append(
            lambda new_extent: len(new_extent) >= self.min_sup * self.ctx.n_objects
        )

    def evaluate_conditions(self, new_extent):
        """
        Evaluates if a new_extent holds arbitrary conditions
        such as minimal support. These conditions have been
        predefined in a list of conditions that by default
        test minimal conditions. More can be included.
        """
        for res in self.conditions:
            if not res(new_extent):
                return False
        return True

    def canonical_test(self, *args):
        """
        Applies canonical test to a description
        """
        current_element, pointer, description = args
        mask = set(range(pointer))

        desc1 = self.pattern.intersection(current_element, mask)
        desc2 = self.pattern.intersection(description, mask)
        return desc1 == desc2

    def cbo(self, concept_id=None, extent=None, intent=None, current_element=0, depth=0):
        """
        concept_id: int current concept id
        current_element: int current element in the intent enumeration
        depth: int depth in the recursion
        BASIC CLOSE BY ONE ITERATION
        """
        if concept_id is None:
            concept_id = self.poset.supremum
            extent = set(self.ctx.g_prime.keys())# self.poset.concept[self.poset.supremum][POSET.EXTENT_MARK]
            intent = self.pattern.bottom()#self.poset.concept[self.poset.supremum][POSET.INTENT_MARK]
        # print (extent, intent)
        
        if self.pattern.length(intent) == self.ctx.n_attributes or current_element >= self.ctx.n_attributes:
            
            return

        self.printer(extent, intent, depth)
        
        for j in range(current_element, self.ctx.n_attributes):
            if not self.pattern.contains(intent, j):
                self.calls += 1
                
                new_extent = self.e_pattern.intersection( extent, self.ctx.m_prime[j])# self.derive_extent( (extent, self.ctx.m_prime[j]) )
                # print('ME',new_extent)
                # if self.evaluate_conditions(new_extent):
                new_intent = self.derive_extent(new_extent)
                if self.canonical_test(intent, j, new_intent):
                    new_concept = self.poset.new_formal_concept(
                        new_extent,
                        new_intent
                    )
                    # self.poset.add_edge(concept_id, new_concept)
                    self.cbo(new_concept, new_extent, new_intent, j + 1, depth + 1)

    def run(self, *args, **kwargs):
        # First Closure
        Y = self.e_pattern.top()
        X = self.derive_extent(Y)
        nid = self.poset.new_formal_concept(Y, set(X))
        self.cbo(nid, Y, X)

class PSCbO(CbO):
    """
    Implementation of Close-by-One for pattern structures,
    It is just a bottom-up enumeration and pattern structures
    are contained by extents, not intents
    """
    def intersect_descriptions(self, descriptions):
        """
        Obtain next iteration extent
        """
        return reduce(self.e_pattern.intersection, descriptions)

    def derive_extent(self, P):
        """
        Derive an extent to obtain its intent
        """
        X = set([ei for ei, e in self.ctx.m_prime.items() if self.e_pattern.leq(P, e)])
        return X

    # def derive_intent(self, P):
    #     return self.intersect_descriptions([self.m_prime[m] for m in P])

    def config(self):
        # self.e_pattern = self.pattern
        # self.pattern = SetPattern

        # if not self.ondisk:
        #     self.poset = POSET(transformer=self.ctx.transformer)
        # else:
        #     self.poset = OnDiskPOSET(transformer=self.ctx.transformer, **self.ondisk_kwargs)
        
        TOP = self.intersect_descriptions(self.ctx.g_prime.values())

        self.ctx.n_attributes = len(self.ctx.g_prime)

        self.ctx.m_prime = {g: self.e_pattern.fix_desc(desc) for g, desc in self.ctx.g_prime.items()}
        list(map(self.e_pattern.top, self.ctx.m_prime.values()))

        # THE NOTION OF MINIMUM SUPPORT SHOULD NOT BE APPLIED
        # DIRECTLY TO PATTERN STRUCTURE EXTENTS, SINCE THEY APPLY
        # ONLY TO SetPattern PATTERN STRUCTURES
        # IF YOU WANT TO FORCE THEM, UNCOMMENT NEXT LINES
        '''
        self.conditions.append(
            lambda new_extent: len(new_extent) >= self.min_sup * self.ctx.n_objects
        )
        '''

    # def run(self, *args, **kwargs):
    #     self.cbo(self.poset.supremum, self.e_pattern.top(), self.pattern.bottom())
