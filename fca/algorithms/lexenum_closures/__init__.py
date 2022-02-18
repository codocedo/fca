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

from fca.algorithms.lecenum_closures import LecEnumClosures
from functools import reduce

class LexEnumClosures(LecEnumClosures):
    """
    Applies LexEnumClosures algorithm
    Enumerates Closures in Lexical Order
    Extends configuration from Close By One Algorithm

    Let the lexical order be: 1 < 2 < 3 < 4
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
    def next_closure(self, X):
        # What's the preffix?
        j = max(X)+1 if bool(X) else 0
        while True:
            for m in range(j, self.ctx.n_attributes):
            # if m < self.ctx.n_attributes:
                Y = self.e_pattern.intersection( self.stack[-1][1], self.ctx.m_prime[m] )
                Xc = self.derive_extent(Y)
                if self.canonical_test(X, m, Xc):
                    self.stack.append( (m , Y) )
                    return Xc
                # else:
                #     X = X.union([m])
            end = True
            for i in range(self.ctx.n_attributes-1, -1, -1):
                if i in X:
                    X.remove(i)
                    if self.stack[-1][0] == i:
                        self.stack.pop()
                    j = i+1
                    end = False
                    if j < self.ctx.n_attributes:
                        break
            if end:
                return None

    def canonical_test(self, *args):
        """
        Applies canonical test to a description
        """
        current_element, pointer, description = args
        mask = set(range(pointer))

        desc1 = self.pattern.intersection(current_element, mask)
        desc2 = self.pattern.intersection(description, mask)
        return desc1 == desc2


class PSLexEnumClosures(LexEnumClosures):
    """
    LexEnumClosures with support for pattern structure at extent level
    """
    def __init__(self, ctx, **kwargs):
        super(PSLexEnumClosures, self).__init__(ctx, **kwargs)

    def config(self):
        self.ctx.m_prime = {g: self.e_pattern.fix_desc(desc) for g, desc in self.ctx.g_prime.items()}
        list(map(self.e_pattern.top, self.ctx.m_prime.values()))
        
        self.ctx.n_attributes = len(self.ctx.g_prime)


    def derive_intent(self, P):
        """
        Derive an intent and obtain the associated pattern
        """
        if not bool(P):
            return self.e_pattern.top()
        return reduce(self.e_pattern.intersection, (self.ctx.m_prime[m] for m in P))
    
    def derive_extent(self, P):
        """
        Derive an extent to obtain its intent
        """
        return set([ei for ei, e in self.ctx.m_prime.items() if self.e_pattern.leq(P, e)])
