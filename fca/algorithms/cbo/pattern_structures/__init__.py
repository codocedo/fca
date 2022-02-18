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
from fca.algorithms import Algorithm, lexo
from fca.algorithms.cbo import CbO
from fca.defs import POSET, SSetPattern
from fca.defs.patterns.enumerators import SetObjectEnumerator
from functools import reduce


#####################################################################################
#### ALGORITHM - DEPRECATED
#####################################################################################

class CbOPS(CbO):
    """
    Implementation of Close-by-One
    """
    def __init__(self, ctx, enumerator=SetObjectEnumerator, **params):
        self.enumerator = enumerator(ctx)
        super(CbOPS, self).__init__(ctx, **params)

    def config(self):
        """ 
        Configure the internal parameters of the class
        """
        self.poset = POSET(transformer=self.ctx.transformer)
        self.poset.new_formal_concept(
            set(self.ctx.g_prime.keys()),
            #self.pattern.bottom(),
            self.enumerator.bottom(self.pattern),
            self.poset.supremum
            )
        self.conditions.append(
            lambda new_extent: len(new_extent) > self.min_sup * self.ctx.n_objects
        )


    def run(self, concept_id=None, current_element=0, depth=0):
        """
        extent: SET OF INTEGERS
        intent: SET OF INTEGERS
        current_attribute: indicates the new attribute to add to the intent
        ctx: context manager

        BASIC CLOSE BY ONE ITERATION
        """

        self.calls += 1
        if concept_id is None:
            concept_id = self.poset.supremum

        intent = self.poset.concept[concept_id][POSET.INTENT_MARK]
        extent = self.poset.concept[concept_id][POSET.EXTENT_MARK]
        
        self.printer(extent, intent, depth)

        ticket = self.enumerator.new_ticket(current_element, depth)
        
        j = self.enumerator.next(ticket, intent, depth, extent=extent)

        while j is not None:
            new_extent = self.enumerator.next_objects(ticket, j, extent, depth)
            if self.evaluate_conditions(new_extent):
                new_intent = reduce(
                    self.pattern.intersection,
                    [self.pattern.fix_desc(self.ctx.g_prime[i]) for i in new_extent]
                )
                if not self.enumerator.canonical_test(ticket, intent, new_intent) or \
                    self.pattern.hash(new_intent) in self.cache:
                    pass
                else:
                    self.cache.append(self.pattern.hash(new_intent))
                    new_concept = self.poset.new_formal_concept(new_extent, new_intent)
                    # print '\n',new_extent
                    self.poset.add_edge(concept_id, new_concept)
                    self.run(new_concept, ticket, depth+1)
                
            j = self.enumerator.next(ticket, intent, depth, extent=extent)
