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
from fca.defs import POSET, SetPattern
from fca.reader import FormalContextManager
from fca.algorithms import Algorithm, lexo

class CbO(Algorithm):
    """
    Implementation of Close-by-One
    """
    def __init__(self, ctx, pattern=SetPattern, **params):
        self.ctx = ctx
        self.poset = None
        self.pattern = pattern
        self.cache = params.get('cache', [])
        self.min_sup = params.get('min_sup', 0)
        self.printer = params.get('printer', lambda a, b, c: None)
        self.conditions = params.get('conditions', [])
        self.calls = 0

        self.config()

        super(CbO, self).__init__(**params)

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
        self.conditions.append(
            lambda new_extent: len(new_extent) > self.min_sup * self.ctx.n_objects
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

    def canonical_test(self, current_element, pointer, description):
        """
        Applies canonical test to a description
        """
        mask = self.pattern(set(range(pointer+1)))
        #return lexo(mask.desc, description.intersection(mask).desc)
        return lexo(current_element.intersection(mask).desc, description.intersection(mask).desc)

    def meet_concepts(self, extent1, intent1, extent2, intent2):
        """
        Meet Concepts 
        """
        new_extent = extent1.intersection(extent2)
        if self.evaluate_conditions(new_extent):
            new_intent = reduce(
                lambda x, y: x.intersection(y),
                [self.pattern(self.ctx.g_prime[i]) for i in new_extent]
            )
            return new_extent, new_intent
        return False, self.pattern.bottom()

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

        if len(intent) == self.ctx.n_attributes or current_element >= self.ctx.n_attributes:
            return

        self.printer(extent, intent, depth)

        for j in range(current_element, self.ctx.n_attributes):
            if j not in intent.desc:
                new_extent, new_intent = self.meet_concepts(
                    extent, #EXTENT1
                    intent, #INTENT1
                    self.ctx.m_prime[j], #EXTENT2
                    None, #INTENT2
                    )

                # CANONICAL TEST
                if bool(new_extent) and self.canonical_test(intent, j, new_intent) and \
                    new_intent.hash() not in self.cache:
                    self.cache.append(new_intent.hash())
                    new_concept = self.poset.new_formal_concept(new_extent, new_intent)
                    self.poset.add_edge(concept_id, new_concept)
                    self.run(new_concept, j+1, depth+1)

class PSCbO(CbO):
    """
    Implementation of Close-by-One for pattern structures,
    It is just a bottom-up enumeration
    """
    def __init__(self, ctx, pattern=SetPattern, **params):
        self.e_pattern = SetPattern
        super(PSCbO, self).__init__(ctx, pattern, **params)

    def config(self):
        self.poset = POSET(transformer=self.ctx.transformer)
        self.poset.new_formal_concept(
            self.e_pattern.bottom(),
            self.pattern.top(self.ctx.g_prime.values()),
            self.poset.infimum
            )
        self.ctx.g_prime = {g: self.pattern(desc) for g, desc in self.ctx.g_prime.items()}

    def canonical_test(self, pointer, description):
        """
        Applies canonical test to a new_intent
        """
        mask = self.e_pattern(set(range(pointer+1)))
        if lexo(mask.desc, description.intersection(mask).desc):
            if description.hash() not in self.cache:
                self.cache.append(description.hash())
                return True
        return False

    def run(self, concept_id=None, current_element=0, depth=0):
        """
        extent: SET OF INTEGERS
        intent: SET OF INTEGERS
        current_attribute: indicates the new attribute to add to the intent
        ctx: context manager

        BASIC CLOSE BY ONE ITERATION
        """
        if concept_id is None:
            concept_id = self.poset.infimum

        intent = self.poset.concept[concept_id][POSET.INTENT_MARK]
        extent = self.poset.concept[concept_id][POSET.EXTENT_MARK]

        if len(extent) == self.ctx.n_objects or current_element >= self.ctx.n_objects:
            return

        for j in range(current_element, self.ctx.n_objects):
            if j not in extent.desc:
                new_intent = intent.intersection(self.ctx.g_prime[j])
                if self.evaluate_conditions(new_intent):
                    # OBTAIN THE EXTENT OF THE NEW INTENT
                    # notice that this comparison is with respect to every representation
                    new_extent = self.e_pattern(
                        set([g for g, desc in self.ctx.g_prime.items() if new_intent <= desc])
                    )
                    # CANONICAL TEST
                    if self.canonical_test(j, new_extent):
                        new_concept = self.poset.new_formal_concept(new_extent, new_intent)
                        self.poset.add_edge(new_concept, concept_id)
                        self.run(new_concept, j+1, depth+1)
