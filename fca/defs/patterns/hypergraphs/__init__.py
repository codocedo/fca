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
from itertools import product, chain
from fca.defs import Intent

class PartitionPattern(Intent):
    """
    Description is a list of sets
    """
    # the bottom will be a singleton
    __bottom = None

    def __init__(self, desc):
        super(PartitionPattern, self).__init__(PartitionPattern.sort_desc(desc))

    def intersection(self, other):
        new_desc = []
        counter = 0
        for i, j in product(self.desc, other.desc):
            intx = i.intersection(j)
            if bool(intx): # instead of len(x) > 0
                new_desc.append(intx)
                counter += len(intx)
        if len(new_desc) == counter:
            return PartitionPattern.bottom(new_desc)
        return PartitionPattern(new_desc)

    def __i_le__(self, other):
        if len(other) > len(self):
            return False
        for i in self.desc:
            check = False
            for j in other.desc:
                if i.issubset(j):
                    check = True
                    break
            if not check:
                return False
        return True

    def __i_eq__(self, other):
        if len(self) != len(other):
            return False
        for i, j in zip(self.desc, other.desc):
            if i != j:
                return False
        return True

    def __i_contains__(self, key):
        return key in self.desc

    def join(self, other):
        self.desc = [self.desc[0].union(chain(*other.desc))]

    def __i_len__(self):
        return len([i for i in self.desc if len(i) > 0])

    def repr(self):
        return [tuple(sorted(i)) for i in self.desc]

    def is_empty(self):
        return len(self) == 0

    def __i_iter__(self):
        for i in self.desc:
            yield i

    @classmethod
    def top(cls, top_rep=None):
        if top_rep is None:
            top = cls([set([])])
        else:
            top = cls([set(chain(*top_rep[0]))])

        top.__i_le__ = lambda s: False
        top.__type__ = 1
        top.__i_eq__ = lambda s: s.__type__ == 1
        return top

    @classmethod
    def bottom(cls, bot_rep=None):
        """
        The bottom is a singleton
        """
        if cls.__bottom is None:
            if bot_rep is None:
                bot_rep = [set([])]
            cls.__bottom = cls(bot_rep)
            cls.__bottom.__i_le__ = lambda s: True
            cls.__bottom.is_empty = lambda: True
            cls.__bottom.__type__ = -1
            cls.__bottom.__i_eq__ = lambda s: s.__type__ == -1 or s.desc == cls.__bottom.desc
            cls.__bottom.intersection = lambda s: cls.__bottom
            return cls.__bottom
        else:
            cls.__bottom.desc = bot_rep
            return cls.__bottom


    @staticmethod
    def sort_desc(desc):
        """
        Sort desc, necessary to ensure optimized comparisons
        """
        return sorted(desc, key=lambda x: sorted(x))

