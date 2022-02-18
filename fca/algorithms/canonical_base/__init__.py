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
from fca.algorithms import Algorithm, lexo
from fca.algorithms.lecenum_closures import LecEnumClosures, PSLecEnumClosures
from fca.algorithms.pre_closure import PreClosure
from fca.defs import SetPattern

class CanonicalBase(LecEnumClosures):
    """
    Calculates the Canonical Base using NextClosure
    as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    """

    def config(self):
        self.preclos = PreClosure()
    # def __init__(self, ctx, **kwargs):
        
    #     # super(CanonicalBase, self).__init__(ctx, **kwargs)
    #     super(CanonicalBase, self).__init__(ctx, **kwargs)

    def next_closure(self, X):
        """
        Original Next Closure algorithm as found in the book "Conceptual Exploration" by Ganter and Obiedkov
        Receives a closed pattern set X and returns the lectically next closed pattern set.
        If X contains all attributes, the algorithms will return None so AllClosures can end
        """
        for m in range(self.ctx.n_attributes-1, -1, -1):
            if m in X:
                X.remove(m)
            else:
                Xc = self.preclos.preclose_pattern(X.union([m]))
                if m <= min(Xc - X): # CANONICAL TEST
                    return Xc
        return None

    def run(self, *args, **kwargs):
        """
        LecEnumClosures takes a pre_closure, adds an attribute to it and then calculate this
        new set pre_closure. Let us call the first pre_closure X, the attribute m, such that
        A = (X + {m})
        L(A) = pre_closure(A)
        In here we receive L(A) and store it in the variable pattern.
        Then, we calculate L(A)'' and store it in c_pattern.
        When A'' != L(A), then L(A) is a pre_closure and also a pseudo-closure.
        """
        X = self.pattern.bottom()

        while X is not None:
            Y = self.derive_intent(X)
            Xc = self.derive_extent(Y)

            if len(X) != len(Xc):
                self.preclos.register_implication(set(X), set(Xc), len(Y))
                # ENHANCEMENT: Applying proposition 22 in Conceptual Exploration Chapter 3
                i = max(X)
                j = min(Xc - X)
                if i < j:
                    X = Xc
            X = self.next_closure(X)

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

class PSCanonicalBase(PSLecEnumClosures, CanonicalBase): # pylint: disable=too-many-ancestors
    """
    Do not really need an implementation, just the
    definition of the mixture of classes:
        Using next_closure from PSLecEnumClosures and everything else from CanonicalBase
    """
    def config(self):
        
        # self.e_pattern = self.pattern
        # self.pattern = SetPattern

        list(map(self.e_pattern.top, self.ctx.g_prime.values()))
        self.all_objects = self.e_pattern.top()
        self.ctx.m_prime = {g: self.e_pattern.fix_desc(desc) for g, desc in self.ctx.g_prime.items()}
        self.ctx.n_attributes = len(self.ctx.g_prime)
        self.preclos = PreClosure()


class EnhancedDG(CanonicalBase):
    """
    Calculates the Canonical Base using NextClosure
    as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    Algorithm 17
    """
    # def derive_extent(self, descriptions):
    #     return super(EnhancedDG, self).derive_extent([self.ctx.m_prime[m] for m in descriptions])

    def run(self, *args, **kwargs):
        """
        This enumeration works with a sort of relay of attributes
        """
        X = set([])  # START WITH EMPTY SET (A IN ALGORITHM DESCRIPTION)
        extent = self.derive_intent(X)
        Xc = self.derive_intent(extent)
        self.calls += 1

        if len(X) < len(Xc):# CHECK THAT EMPTY SET IS NOT CLOSED
            self.preclos.register_implication(X, Xc, len(extent))

        # BACKWARDS ENUMERATION
        i = max(self.ctx.m_prime.keys())

        # ENUMERATE UNTIL WE GET THE TOP INTENT
        while len(X) < len(self.ctx.m_prime.keys()):
            # BACKWARDS ENUMERATION
            for j in range(i, -1, -1):
                if j in X:
                    X = X - set([j])
                else:
                    self.calls += 1
                    B = self.preclos.preclose_pattern(
                        X.union(
                            set([j])
                            )
                        )
                    C = B - X
                    # THE FOLLOWING IS A SORT OF CANONICAL TEST
                    if not bool(self.pattern.intersection(C, set(range(j)))):
                        X = B
                        i = j
                        break
            extent = self.derive_intent(X)
            Xc = self.derive_extent(extent)
            if len(X) != len(Xc):
                self.preclos.register_implication(
                    X,
                    Xc,
                    len(extent)
                )

            C = Xc - X

            # CANONICAL TEST FOR THE CONSEQUENCE OF THE IMPLICATION
            if not bool(C.intersection(set(range(i)))):
                X = Xc
                i = max(self.ctx.m_prime.keys())
            else:
                X = set([m for m in range(i + 1) if m in X])
