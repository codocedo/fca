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
from __future__ import print_function
from functools import reduce
from fca.defs import POSET, SSetPattern
from fca.reader import FormalContextManager
from fca.algorithms import Algorithm, lexo


class CbO(Algorithm):
    """
    Implementation of Close-by-One
    """

    def __init__(self, ctx, **kwargs):
        self.ctx = ctx
        self.poset = None
        self.pattern = kwargs.get('pattern', SSetPattern)
        self.cache = kwargs.get('cache', [])
        self.min_sup = kwargs.get('min_sup', 0)
        self.printer = kwargs.get('printer', lambda a, b, c: None)
        self.conditions = kwargs.get('conditions', [])
        self.calls = 0

        self.config()

        super(CbO, self).__init__(**kwargs)
        print (self.calls)

    def config(self):
        """
        Configure the internal parameters of the class
        """
        self.poset = POSET(transformer=self.ctx.transformer)
        self.poset.new_formal_concept(
            set(self.ctx.g_prime.keys()),
            self.pattern.bottom(),
            self.poset.supremum
        )
        self.pattern.top(set(self.ctx.m_prime.keys()))
        self.conditions.append(
            lambda new_extent: len(
                new_extent) >= self.min_sup * self.ctx.n_objects
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
        mask = set(range(pointer + 1))
        # return lexo(mask.desc, description.intersection(mask).desc)
        desc1 = self.pattern.intersection(current_element, mask)
        desc2 = self.pattern.intersection(description, mask)
        return lexo(desc1, desc2)

    def derive_extent(self, *args):
        """
        Obtain next iteration extent
        """
        # extent1, extent2 = args
        # return extent1.intersection(extent2)
        return reduce(
            lambda x, y: x.intersection(y),
            args
        )

    def derive_intent(self, *args):
        """
        Obtain next iteration intent
        """
        new_extent = args[0]
        if not bool(new_extent):
            return self.pattern.top()
        return reduce(
            self.pattern.intersection,
            [self.ctx.g_prime[g] for g in new_extent]
        )

    def cbo(self, concept_id=None, current_element=0, depth=0):
        """
        concept_id: int current concept id
        current_element: int current element in the intent enumeration
        depth: int depth in the recursion
        BASIC CLOSE BY ONE ITERATION
        """
        self.calls += 1
        if concept_id is None:
            concept_id = self.poset.supremum

        intent = self.poset.concept[concept_id][POSET.INTENT_MARK]
        extent = self.poset.concept[concept_id][POSET.EXTENT_MARK]

        if self.pattern.length(intent) == self.ctx.n_attributes or current_element >= self.ctx.n_attributes:
            return

        self.printer(extent, intent, depth)

        for j in range(current_element, self.ctx.n_attributes):
            if not self.pattern.contains(intent, j):
                new_extent = self.derive_extent(extent, self.ctx.m_prime[j])
                if self.evaluate_conditions(new_extent):
                    new_intent = self.derive_intent(new_extent)
                    # CANONICAL TEST
                    if not self.canonical_test(intent, j, new_intent) or \
                            self.pattern.hash(new_intent) in self.cache:
                        pass
                    else:
                        self.cache.append(self.pattern.hash(new_intent))
                        new_concept = self.poset.new_formal_concept(
                            new_extent, new_intent)
                        self.poset.add_edge(concept_id, new_concept)
                        self.cbo(new_concept, j + 1, depth + 1)

    def run(self, *args, **kwargs):
        self.cbo()


class PSCbO(CbO):
    """
    Implementation of Close-by-One for pattern structures,
    It is just a bottom-up enumeration and pattern structures
    are contained by extents, not intents
    """

    def __init__(self, ctx, **kwargs):
        self.e_pattern = kwargs.get('pattern', SSetPattern)  # extent pattern
        kwargs['pattern'] = SSetPattern
        super(PSCbO, self).__init__(ctx, **kwargs)

    def derive_extent(self, *args):
        """
        Obtain next iteration extent
        """
        # extent1, extent2 = args
        # return extent1.intersection(extent2)
        return reduce(
            lambda x, y: self.e_pattern.intersection(x, y),
            args
        )

    def derive_intent(self, *args):
        new_extent = args[0]
        result = set([m for m, desc in self.ctx.m_prime.items() if self.e_pattern.leq(new_extent, desc)])
        return result

    def config(self):
        self.poset = POSET(transformer=self.ctx.transformer)
        # self.evaluate_conditions = lambda s: True
        map(self.e_pattern.top, self.ctx.g_prime.values())
        self.poset.new_formal_concept(
            self.e_pattern.top(),
            self.pattern.bottom(),
            self.poset.supremum
        )
        self.ctx.m_prime = {g: self.e_pattern.fix_desc(desc) for g, desc in self.ctx.g_prime.items()}
        self.ctx.n_attributes = len(self.ctx.g_prime)
        # THE NOTION OF MINIMUM SUPPORT SHOULD NOT BE APPLIED
        # DIRECTLY TO PATTERN STRUCTURE EXTENTS, SINCE THEY APPLY
        # ONLY TO SetPattern PATTERN STRUCTURES
        # IF YOU WANT TO FORCE THEM, UNCOMMENT NEXT LINES
        '''
        self.conditions.append(
            lambda new_extent: len(new_extent) >= self.min_sup * self.ctx.n_objects
        )
        '''


# from fca.defs import POSET, SetPattern
# from fca.reader import FormalContextManager
# from fca.algorithms import Algorithm, lexo


# class CbO(Algorithm):
#     """
#     Implementation of Close-by-One
#     """

#     def __init__(self, ctx, **kwargs):
#         self.ctx = ctx
#         self.poset = None
#         self.pattern = SetPattern
#         self.cache = kwargs.get('cache', [])
#         self.min_sup = kwargs.get('min_sup', 0)
#         self.printer = kwargs.get('printer', lambda a, b, c: None)
#         self.conditions = kwargs.get('conditions', [])
#         self.calls = 0

#         self.config()

#         super(CbO, self).__init__(**kwargs)
#         print (self.calls)

#     def config(self):
#         """
#         Configure the internal parameters of the class
#         """
#         self.poset = POSET(transformer=self.ctx.transformer)
#         self.poset.new_formal_concept(
#             set(self.ctx.g_prime.keys()),
#             self.pattern.bottom(),
#             self.poset.supremum
#         )
#         self.pattern.top(frozenset(self.ctx.m_prime.keys()))
#         self.conditions.append(
#             lambda new_extent: len(
#                 new_extent) >= self.min_sup * self.ctx.n_objects
#         )

#     def evaluate_conditions(self, new_extent):
#         """
#         Evaluates if a new_extent holds arbitrary conditions
#         such as minimal support. These conditions have been
#         predefined in a list of conditions that by default
#         test minimal conditions. More can be included.
#         """
#         for res in self.conditions:
#             if not res(new_extent):
#                 return False
#         return True

#     def canonical_test(self, *args):
#         """
#         Applies canonical test to a description
#         """

#         current_element, pointer, description = args
#         mask = self.pattern(frozenset(range(pointer + 1)))
#         # return lexo(mask.desc, description.intersection(mask).desc)
#         return lexo(current_element.intersection(mask).desc, description.intersection(mask).desc)

#     def derive_extent(self, *args):
#         """
#         Obtain next iteration extent
#         """
#         # extent1, extent2 = args
#         # return extent1.intersection(extent2)
#         return reduce(
#             lambda x, y: x.intersection(y),
#             args
#         )

#     def derive_intent(self, *args):
#         """
#         Obtain next iteration intent
#         """
#         new_extent = args[0]
#         if not bool(new_extent):
#             return self.pattern.top()
#         return reduce(
#             lambda x, y: x.intersection(y),
#             [self.pattern(self.ctx.g_prime[g]) for g in new_extent]
#         )

#     def cbo(self, concept_id=None, current_element=0, depth=0):
#         """
#         concept_id: int current concept id
#         current_element: int current element in the intent enumeration
#         depth: int depth in the recursion
#         BASIC CLOSE BY ONE ITERATION
#         """
#         self.calls += 1
#         if concept_id is None:
#             concept_id = self.poset.supremum

#         intent = self.poset.concept[concept_id][POSET.INTENT_MARK]
#         extent = self.poset.concept[concept_id][POSET.EXTENT_MARK]

#         if len(intent) == self.ctx.n_attributes or current_element >= self.ctx.n_attributes:
#             return

#         self.printer(extent, intent, depth)

#         for j in range(current_element, self.ctx.n_attributes):
#             if j not in intent.desc:
#                 new_extent = self.derive_extent(extent, self.ctx.m_prime[j])
#                 if self.evaluate_conditions(new_extent):
#                     new_intent = self.derive_intent(new_extent)
#                     # CANONICAL TEST
#                     if not self.canonical_test(intent, j, new_intent) or \
#                             new_intent.hash() in self.cache:
#                         pass
#                     else:
#                         self.cache.append(new_intent.hash())
#                         new_concept = self.poset.new_formal_concept(
#                             new_extent, new_intent)
#                         self.poset.add_edge(concept_id, new_concept)
#                         self.cbo(new_concept, j + 1, depth + 1)

#     def run(self, *args, **kwargs):
#         self.cbo()


# class PSCbO(CbO):
#     """
#     Implementation of Close-by-One for pattern structures,
#     It is just a bottom-up enumeration and pattern structures
#     are contained by extents, not intents
#     """

#     def __init__(self, ctx, **kwargs):
#         self.e_pattern = kwargs.get('pattern', SetPattern)  # extent pattern
#         super(PSCbO, self).__init__(ctx, **kwargs)

#     def derive_intent(self, *args):
#         new_extent = args[0]
#         result = self.pattern(
#             set([m for m, desc in self.ctx.m_prime.items() if new_extent <= desc])
#         )
#         return result

#     def config(self):
#         self.poset = POSET(transformer=self.ctx.transformer)
#         # self.evaluate_conditions = lambda s: True
#         self.poset.new_formal_concept(
#             self.e_pattern.top(self.ctx.g_prime.values()),
#             self.pattern.bottom(),
#             self.poset.supremum
#         )

#         self.ctx.m_prime = {g: self.e_pattern(
#             desc) for g, desc in self.ctx.g_prime.items()}
#         self.ctx.n_attributes = len(self.ctx.g_prime)
#         # THE NOTION OF MINIMUM SUPPORT SHOULD NOT BE APPLIED
#         # DIRECTLY TO PATTERN STRUCTURE EXTENTS, SINCE THEY APPLY
#         # ONLY TO SetPattern PATTERN STRUCTURES
#         # IF YOU WANT TO FORCE THEM, UNCOMMENT NEXT LINES
#         '''
#         self.conditions.append(
#             lambda new_extent: len(new_extent) >= self.min_sup * self.ctx.n_objects
#         )
#         '''
