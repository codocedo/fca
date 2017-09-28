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
from fca.algorithms.next_closure import NextClosure

class PreClosure(object):
    """
    Calculates Pre-closure as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    """
    def __init__(self):
        """
        Starts with an empty implication base
        Implications are to be stored as pairs of sets
        """
        self.imp_base = []
        self.supports = []

    def register_implication(self, ant, con, support):
        self.imp_base.append((ant, con))
        self.supports.append(support)
    
    def get_implication_base(self):
        for implication, extent in zip(self.imp_base, self.supports):
            yield implication, extent

    def preclose_pattern(self, pattern):
        """
        Calculates pre-closure of pattern
        """
        old_len = -1
        while old_len != len(pattern):
            old_len = len(pattern)
            for ant, con in self.imp_base:
                if ant <= pattern and len(ant) != len(pattern):
                    pattern.join(con)
        return pattern

class CanonicalBaseNC(NextClosure):
    """
    Calculates the Canonical Base using NextClosure
    as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    """
    def __init__(self, ctx, pattern=SetPattern, **params):
        self.preclos = PreClosure()
        super(CanonicalBaseNC, self).__init__(ctx, pattern, **params)

    def meet_concepts(self, extent1, intent1, extent2, intent2):
        pattern = intent1.copy()
        pattern.join(intent2)
        closed_pattern = self.preclos.preclose_pattern(pattern)
        extent = self.ctx.intent_prime(closed_pattern)
        if self.evaluate_conditions(extent):
            return extent, closed_pattern
        return False, self.pattern.bottom()

    def run(self):
        pattern = self.next_closure()
        while pattern is not None:
            extent = self.ctx.intent_prime(pattern)
            c_pattern = self.pattern(self.ctx.extent_prime(extent))
            if len(pattern) != len(c_pattern):
                self.preclos.register_implication(pattern, c_pattern, extent)

            pattern = self.next_closure()

    def get_implications(self):
        m_map = self.ctx.transformer.m_map()
        for implication, objects in self.preclos.get_implication_base():
            ant, con = implication
            support = len(objects)
            yield (
                (
                    sorted([m_map[m] for m in ant]),
                    sorted([m_map[m] for m in con.desc - ant.desc])
                ),
                support
            )
