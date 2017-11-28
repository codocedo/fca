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
import sys
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

    def derive_extent(self, *args):
        if not bool(args):
            return set(self.ctx.g_prime.keys())
        return super(CanonicalBase, self).derive_extent(*[self.ctx.m_prime[s] for s in args])

    
    def meet_concepts(self, *args):
        self.pattern.join(args[1], args[3])
        closed_pattern = self.preclos.preclose_pattern(args[1])
        if closed_pattern is None:
            del closed_pattern
            return None, self.pattern.bottom()

        extent = self.derive_extent(*closed_pattern)

        if self.evaluate_conditions(extent):
            return extent, closed_pattern
        del closed_pattern, extent
        return None, self.pattern.bottom()


    def run(self, *args, **kwargs):
        cid = self.poset.supremum #self.pattern.bottom()
        # counter=0
        # tr = tracker.SummaryTracker()
        while cid is not None:
            print '\r',self.stack_enum,'%1s' % str(' '),
            # print len(self.poset.concepts()),
            # print float(sum([sys.getsizeof(self.poset.concept[cid].extent) for cid in self.poset.concept.keys()]))/1024,
            # print '%10s' % str(' ')

            sys.stdout.flush()
            # tr.print_diff()
            extent = self.poset.concept[cid].extent #self.derive_extent(*pattern)
            pattern = self.poset.concept[cid].intent
            # print extent, pattern
            # tr.print_diff()
            # print '::Extent:', id(extent), extent
            # print '::Intent:', id(pattern), pattern
            # raw_input()
            c_pattern = self.derive_intent(extent)

            if len(pattern) != len(c_pattern):
                self.preclos.register_implication(pattern, c_pattern, extent)
                # ENHANCEMENT: Applying proposition 22 in Conceptual Exploration Chapter 3
                try:
                    if min(c_pattern - pattern) > max(pattern):
                        self.stack[-1] = c_pattern
                        self.stack_enum[-1] = self.ctx.n_attributes - 1
                    else:
                        self.stack_enum[-1] = self.stack_enum[-2]

                except ValueError as e:
                    print ""
                    print "VALUE ERROR"
                    print "EXTENT:", extent
                    print "PATTERN:",pattern
                    print "CLOSED_PATTERN:",c_pattern
                    print "DIFFERENCE:",c_pattern.desc - pattern.desc
                    exit()
            
            cid = self.next_closure()
            
            # gc.collect()

    def get_implications(self):
        """
        Returns the stored list of implications calculated
        """
        m_map = self.ctx.transformer.m_map()

        def translate(lst): return [m_map.get(m, m) for m in lst]
        base = [
            (
                (sorted(translate(ant)), sorted(translate(con-ant))),
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
        pattern = set([])  # START WITH EMPTY SET (A IN ALGORITHM DESCRIPTION)
        extent = self.derive_extent(*pattern)
        c_pattern = self.derive_intent(extent)
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
            extent = self.derive_extent(*pattern)
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
