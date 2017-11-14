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

from fca.defs import POSET, SetPattern
from fca.algorithms import lexo
from fca.algorithms.cbo import CbO, PSCbO

class NextClosure(CbO):
    """
    Applies NextClosure algorithm
    Extends configuration from Close By One Algorithm
    Let the lectical order be: 1 < 2 < 3 < 4
    Then the enumeration goes:
    1
    12
    123
    124
    1234
    2
    23
    234
    24
    3
    34
    4
    """
    def __init__(self, ctx, **kwargs):
        """
        Initialize stacks to maintain the trace of the execution
        Extends configurations from Close By One
        Particularly, minimal support and poset initialization

        This class uses a close_pattern that is a method to close an intent
        It can be changed externally to support other closures
        """
        self.stack = None # Stack of patterns
        self.stack_enum = None # Stack of enumerators
        self.stack_supports = None
        self.calls = 0

        super(NextClosure, self).__init__(ctx, **kwargs)
        
    
    def config(self):
        """
        Configure the stacks

        stack: stack with the patterns
        stack_enum: stack with the enumerators used for in the stack
        stack_cid: stack witht the mappings to the poset of formal concepts
        """
        super(NextClosure, self).config()

        self.stack = [self.pattern(set([]))] # Stack of patterns
        self.stack_enum = [0] # Stack of enumerators
        self.stack_supports = [self.ctx.n_objects]
        self.stack_cid = [self.poset.supremum] # Stack of concept ids mapping the stack to the poset

    def meet_concepts(self, *args):
        """
        Meet Concepts
        """
        extent1 = args[0]
        extent2 = args[2]
        new_extent = self.derive_extent(extent1, extent2)
        if self.evaluate_conditions(new_extent):
            new_intent = self.derive_intent(new_extent)
            return new_extent, new_intent
        return None, self.pattern.bottom()

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
                    j += 1
                if j == self.ctx.n_attributes:
                    self.stack.pop()
                    self.stack_enum.pop()
                    self.stack_cid.pop()
                else:
                    make_j = False
            self.calls += 1
            # CLOSURE
            new_extent, new_intent = self.meet_concepts(
                self.ctx.m_prime[j], #EXTENT1,
                self.stack[-1], #INTENT1
                self.poset.concept[self.stack_cid[-1]].extent, #EXTENT2
                self.pattern([j]) #INTENT2
            )
            # END CLOSURE

            if new_extent is None or \
            not self.canonical_test(self.stack[-1], j, new_intent) \
            or new_intent.hash() in self.cache:
                self.stack_enum[-1] = j+1
            else:
                found_closure = True


        self.stack_enum[-1] = j+1
        self.stack.append(new_intent)
        self.stack_enum.append(j+1)
        cid = self.poset.new_formal_concept(new_extent, new_intent)
        self.poset.add_edge(self.stack_cid[-1], cid)
        self.stack_cid.append(cid)
        self.stack_supports.append(len(new_extent))
        self.cache.append(new_intent.hash())
        return new_intent

    def run(self, *args, **kwargs):
        """
        Computes all the closures and store them in the poset
        """
        while self.next_closure() is not None:
            continue



class PSNextClosure(NextClosure, PSCbO):
    """
    NextClosure with support for pattern structure at extent level
    """
    def __init__(self, ctx, **kwargs):
        super(PSNextClosure, self).__init__(ctx, **kwargs)