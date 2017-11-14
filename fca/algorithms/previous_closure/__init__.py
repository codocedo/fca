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
from fca.algorithms.next_closure import NextClosure
from fca.algorithms.cbo import PSCbO
from fca.algorithms import lexo

class PreviousClosure(NextClosure):
    """
    Same as NextClosure
    but enumerates backwards
    Let the lectical order be: 1 < 2 < 3 < 4
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

    def config(self):
        """
        Configure the stacks

        stack: stack with the patterns
        stack_enum: stack with the enumerators used for in the stack
        stack_cid: stack witht the mappings to the poset of formal concepts
        """
        super(PreviousClosure, self).config()

        self.stack = [self.pattern(set([]))] # Stack of patterns
        self.stack_enum = [-2, self.ctx.n_attributes-1] # Stack of enumerators
        self.stack_supports = [self.ctx.n_objects]
        self.stack_cid = [self.poset.supremum] # Stack of concept ids mapping the stack to the poset


    def canonical_test(self, *args):
        """
        Applies canonical test to a description
        """
        current_element, pointer, description = args
        mask = self.pattern(frozenset([pointer]))
        return lexo(current_element.union(mask).desc, description)

    def next_closure(self):
        """
        Computes the next closure in the stack
        Can be used externally or in a batch with self.run()
        """
        found_closure = False
        while not found_closure:

            make_j = True
            while make_j:
                if not bool(self.stack):
                    return None
                j = self.stack_enum[-1]
                while j in self.stack[-1]:
                    j -= 1
                if j <= self.stack_enum[-2]+1:
                    self.stack.pop()
                    self.stack_enum.pop()
                    self.stack_cid.pop()
                else:
                    make_j = False

            # CLOSURE
            self.calls += 1

            # print self.translate(self.pattern(frozenset([j])).union(self.stack[-1]))
            new_extent, new_intent = self.meet_concepts(
                self.ctx.m_prime[j], #EXTENT1,
                self.pattern(frozenset([j])), #INTENT2
                self.poset.concept[self.stack_cid[-1]].extent, #EXTENT2
                self.stack[-1], #INTENT2
            )

            if new_extent is None or \
            not self.canonical_test(self.stack[-1], j, new_intent) \
            or new_intent.hash() in self.cache:
                self.stack_enum[-1] = j-1
            else:
                found_closure = True

        self.stack_enum[-1] = j-1
        
        self.stack.append(new_intent)
        self.stack_enum.append(self.ctx.n_attributes-1)
        cid = self.poset.new_formal_concept(new_extent, new_intent)
        self.poset.add_edge(self.stack_cid[-1], cid)
        self.stack_cid.append(cid)
        self.stack_supports.append(len(new_extent))
        self.cache.append(new_intent.hash())
        return new_intent


class PSPreviousClosure(PreviousClosure, PSCbO):
    """
    NextClosure with support for pattern structure at extent level
    """
    def __init__(self, ctx, **kwargs):
        super(PSPreviousClosure, self).__init__(ctx, **kwargs)
