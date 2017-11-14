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

    def derive_extent(self, *args):
        if not bool(args):
            return frozenset(self.ctx.g_prime.keys())
        return super(CanonicalBase, self).derive_extent(*[self.ctx.m_prime[s] for s in args])

    def meet_concepts(self, *args):
        intent1 = args[1]
        intent2 = args[3]
        pattern = intent1.copy()
        pattern.join(intent2)
        closed_pattern = self.preclos.preclose_pattern(pattern)
        if closed_pattern is None:
            return None, self.pattern.bottom()
        extent = self.derive_extent(*closed_pattern)

        if self.evaluate_conditions(extent):
            return extent, closed_pattern
        return None, self.pattern.bottom()

    def run(self, *args, **kwargs):
        pattern = SetPattern([])

        while pattern is not None:

            extent = self.derive_extent(*pattern)
            c_pattern = self.derive_intent(extent)

            if len(pattern) != len(c_pattern):
                self.preclos.register_implication(pattern, c_pattern, extent)
                # ENHANCEMENT: Applying proposition 22 in Conceptual Exploration Chapter 3
                if min(c_pattern.desc - pattern.desc) > max(pattern.desc):
                    self.stack[-1] = c_pattern
                    self.stack_enum[-1] = self.ctx.n_attributes - 1
                else:
                    self.stack_enum[-1] = self.stack_enum[-2]

            pattern = self.next_closure()

    def get_implications(self):
        """
        Returns the stored list of implications calculated
        """
        m_map = self.ctx.transformer.m_map()

        def translate(lst): return [m_map.get(m, m) for m in lst]
        base = [
            (
                (sorted(translate(ant)), sorted(translate(con.desc-ant.desc))),
                len(objects)
            )
            for (ant, con), objects in self.preclos.get_implication_base()
        ]
        return sorted(base, key=lambda s: (len(s[0][0]), tuple(sorted(s[0][0]))))


class PSCanonicalBase(PSPreviousClosure, CanonicalBase):
    """
    Calculates the Canonical Base using NextClosure
    as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    """

    def derive_extent(self, *args):
        if not bool(args):
            return self.e_pattern.top()  # frozenset(self.ctx.g_prime.keys())
        return super(PSCanonicalBase, self).derive_extent(*args)


class EnhancedDG(CanonicalBase):
    """
    Calculates the Canonical Base using NextClosure
    as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    Algorithm 17
    """

    def run(self, *args, **kwargs):
        """
        This enumeration works with a sort of relay of attributes
        """
        pattern = frozenset(
            [])  # START WITH EMPTY SET (A IN ALGORITHM DESCRIPTION)
        extent = self.derive_extent(*pattern)
        c_pattern = self.derive_intent(extent).desc
        self.calls += 1

        if len(pattern) < len(c_pattern):  # CHECK THAT EMPTY SET IS NOT CLOSED
            self.preclos.register_implication(pattern, c_pattern, extent)

        # BACKWARDS ENUMERATION
        i = max(self.ctx.m_prime.keys())

        # ENUMERATE UNTIL WE GET THE TOP INTENT
        while len(pattern) < len(self.ctx.m_prime.keys()):
            # BACKWARDS ENUMERATION
            for j in range(i, -1, -1):

                if j in pattern:
                    pattern = pattern - frozenset([j])
                else:
                    self.calls += 1
                    B = self.preclos.preclose_pattern(
                        self.pattern(
                            pattern.union(
                                frozenset([j])
                            )
                        )
                    ).desc
                    C = B - pattern
                    # THE FOLLOWING IS A SORT OF CANONICAL TEST
                    if not bool(C.intersection(frozenset(range(j)))):
                        pattern = B
                        i = j
                        break

            extent = self.derive_extent(*pattern)
            c_pattern = self.derive_intent(extent).desc
            if len(pattern) != len(c_pattern):
                self.preclos.register_implication(
                    self.pattern(pattern),
                    self.pattern(c_pattern),
                    extent
                )
            C = c_pattern - pattern

            # CANONICAL TEST FOR THE CONSEQUENCE OF THE IMPLICATION
            if not bool(C.intersection(frozenset(range(i)))):
                pattern = c_pattern
                i = max(self.ctx.m_prime.keys())
            else:
                pattern = frozenset([m for m in range(i + 1) if m in pattern])
