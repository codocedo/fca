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
from fca.defs import POSET
from fca.algorithms import lexo
from fca.algorithms.previous_closure import PreviousClosure, PSPreviousClosure
from fca.algorithms.pre_closure import PreClosure

class CanonicalBase(PreviousClosure):
    """
    Calculates the Canonical Base using NextClosure
    as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    """

    def __init__(self, ctx, **kwargs):
        self.preclos = PreClosure()
        super(CanonicalBase, self).__init__(ctx, **kwargs)

    def meet_concepts(self, *args):
        m_prime, new_attribute, old_extent, old_intent = args
        self.pattern.join(new_attribute, old_intent)
        closed_pattern = self.preclos.preclose_pattern(new_attribute)

        if closed_pattern is None:
            del closed_pattern
            return None, self.pattern.bottom()

        extent = self.derive_extent([m_prime, old_extent])

        if self.evaluate_conditions(extent):
            return extent, closed_pattern
        del closed_pattern, extent
        return None, self.pattern.bottom()


    def run(self, *args, **kwargs):
        pattern = self.pattern.bottom()
        while pattern is not None:
            extent = self.stack_extents[-1]
            c_pattern = self.derive_intent(extent, pattern)

            if len(pattern) != len(c_pattern):
                self.preclos.register_implication(pattern, c_pattern, len(extent))
                # ENHANCEMENT: Applying proposition 22 in Conceptual Exploration Chapter 3
                try:
                    if self.pattern.is_empty(pattern) or min(c_pattern - pattern) > max(pattern):
                        self.stack[-1] = c_pattern
                        self.stack_enum[-1] = self.ctx.n_attributes - 1
                    else:
                        self.stack_enum[-1] = self.stack_enum[-2]
                # THIS ERROR HAPPENED BECAUSE OF SOMETHING, I DON'T REMEMBER :P
                except ValueError as err:
                    print ""
                    print "VALUE ERROR"
                    print "EXTENT:", extent
                    print "PATTERN:",pattern
                    print "CLOSED_PATTERN:", c_pattern
                    print "DIFFERENCE:", c_pattern - pattern
                    print err
                    exit()
            pattern = self.next_closure()
        print ''

    def get_implications(self):
        """
        Returns the stored list of implications calculated
        """
        m_map = self.ctx.transformer.m_map()

        def translate(lst): return [m_map.get(m, m) for m in lst]
        base = [
            (
                (sorted(translate(ant)), sorted(translate(con-ant))),
                support
            )
            for (ant, con), support in self.preclos.get_implication_base()
        ]
        return sorted(base, key=lambda s: (len(s[0][0]), tuple(sorted(s[0][0]))))

class PSCanonicalBase(PSPreviousClosure, CanonicalBase):
    """
    Do not really need an implementation, just the
    definition of the mixture of classes:
        Using next_closure from PSPreviousClosure and everything else from CanonicalBase
    """
    pass


class EnhancedDG(CanonicalBase):
    """
    Calculates the Canonical Base using NextClosure
    as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    Algorithm 17
    """
    def derive_extent(self, descriptions):
        return super(EnhancedDG, self).derive_extent([self.ctx.m_prime[m] for m in descriptions])

    def run(self, *args, **kwargs):
        """
        This enumeration works with a sort of relay of attributes
        """
        pattern = set([])  # START WITH EMPTY SET (A IN ALGORITHM DESCRIPTION)
        extent = self.all_objects
        c_pattern = self.derive_intent(extent)
        self.calls += 1

        if len(pattern) < len(c_pattern):# CHECK THAT EMPTY SET IS NOT CLOSED
            self.preclos.register_implication(pattern, c_pattern, extent)

        # BACKWARDS ENUMERATION
        i = max(self.ctx.m_prime.keys())
        
        # ENUMERATE UNTIL WE GET THE TOP INTENT
        while len(pattern) < len(self.ctx.m_prime.keys()):
            # BACKWARDS ENUMERATION
            for j in range(i, -1, -1):
                if j in pattern:
                    pattern = pattern - set([j])
                else:
                    self.calls += 1
                    B = self.preclos.preclose_pattern(
                        pattern.union(
                            set([j])
                            )
                        )
                    
                    C = B - pattern
                    # THE FOLLOWING IS A SORT OF CANONICAL TEST
                    if not bool(self.pattern.intersection(C, set(range(j)))):
                        pattern = B
                        i = j
                        break
            extent = self.derive_extent(pattern)
            c_pattern = self.derive_intent(extent)

            if len(pattern) != len(c_pattern):
                self.preclos.register_implication(
                    pattern,
                    c_pattern,
                    extent
                )

            C = c_pattern - pattern

            # CANONICAL TEST FOR THE CONSEQUENCE OF THE IMPLICATION
            if not bool(C.intersection(set(range(i)))):
                pattern = c_pattern
                i = max(self.ctx.m_prime.keys())
            else:
                pattern = set([m for m in range(i + 1) if m in pattern])
