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
from itertools import product, chain
from fca.defs import Intent

class PartitionPattern(Intent):
    """
    Description is a list of frozensets
    TOP: is a partition with a single element with all attributes
    BOTTOM: is a partition with one element per attribute
    """
    # the bottom will be a singleton
    _top = None
    _bottom = None

    @classmethod
    def fix_desc(cls, desc):
        return cls.sort_description(desc)

    @classmethod
    def intersection(cls, desc1, desc2):
        if desc2 == cls._top:
            return desc1
        new_desc = []
        counter = 0
        for i, j in product(desc1, desc2):
            x, y = (i, j) if len(i) < len(j) else (j, i)
            if x.issubset(y):
                new_desc.append(x)
                counter += len(x)
            else:
                intx = x.intersection(y)
                if bool(intx): # instead of len(x) > 0
                    new_desc.append(intx)
                    counter += len(intx)
        # print len(new_desc)
        if len(new_desc) == counter:
            return PartitionPattern.bottom(new_desc)
        return cls.fix_desc(new_desc)

    @classmethod
    def leq(cls, desc1, desc2):
        if desc1 == cls._bottom:
            return True
        if cls.length(desc1) < cls.length(desc2):
            return False
        for i in desc1:
            check = False
            for j in desc2:
                if len(i) > len(j):
                    break
                if i.issubset(j):
                    check = True
                    break
            if not check:
                return False
        return True

    @classmethod
    def is_equal(cls, desc1, desc2):
        if len(desc1) != len(desc2):
            return False
        for i, j in zip(desc1, desc2):
            if i != j:
                return False
        return True

    @classmethod
    def contains(cls, desc, key):
        return key in desc

    @classmethod
    def join(cls, desc1, desc2):
        desc1 = cls.fix_desc([desc1[0].union(chain(*desc2))])

    @classmethod
    def meet(cls, desc1, desc2):
        new_desc = []
        for i, j in product(desc1, desc2):
            intx = i.intersection(j)
            if bool(intx): # instead of len(x) > 0
                new_desc.append(intx)
        desc1 = cls.fix_desc(new_desc)

    @classmethod
    def length(cls, desc):
        return len([i for i in desc if len(i) > 0])

    @classmethod
    def is_empty(cls, desc):
        return len(desc) == 0

    @classmethod
    def get_iterator(cls, desc):
        for i in desc:
            yield i

    @classmethod
    def top(cls, top_rep=None):
        if cls._top is None:
            cls._top = [set([])]
        if top_rep is not None:
            cls._top[0].update(set(list(chain(*top_rep))))
        return cls._top

    @classmethod
    def bottom(cls, bot_rep=None):
        if cls._bottom is None:
            cls._bottom = []
        if bot_rep is not None:
            if bool(cls._bottom):
                cls.meet(cls._bottom, bot_rep)
            else:
                for i in bot_rep:
                    cls._bottom.append(i)
        return cls.fix_desc(cls._bottom)

    @classmethod
    def sort_description(cls, desc):
        desc.sort(key=lambda x: (len(x), sorted(x)), reverse=True)
        return desc

class TrimmedPartitionPattern(PartitionPattern):
    """
    Description is a list of frozensets
    Sets with 1 elements are deleted from the partition
    """
    # the bottom will be a singleton
    _top = None
    _bottom = None

    n_elements = 0

    @classmethod
    def leq(cls, desc1, desc2):
        if desc1 == cls._bottom:
            return True
        for i in desc1:
            check = False
            for j in desc2:
                if len(i) > len(j):
                    break
                if i.issubset(j):
                    check = True
                    break
            if not check:
                return False
        return True

    @classmethod
    def bottom(cls, bot_rep=None):
        if cls._bottom is None:
            cls._bottom = []
        if cls.n_elements != 0 and len(cls._bottom) != cls.n_elements:
            for i in range(cls.n_elements):
                cls._bottom.append(set([i]))
        return cls._bottom

    @classmethod
    def fix_desc(cls, desc):
        n_elements = sum([len(i) for i in desc])
        if cls.n_elements < n_elements:
            cls.n_elements = n_elements
        for i in range(len(desc)-1, -1, -1):
            if len(desc[i]) == 1:
                del desc[i]
        return cls.sort_description(desc)

    @classmethod
    def intersection(cls, desc1, desc2):
        new_desc = []
        counter = 0
        for i, j in product(desc1, desc2):
            x, y = (i, j) if len(i) < len(j) else (j, i)
            if x.issubset(y):
                new_desc.append(x)
                counter += len(x)
            else:
                intx = i.intersection(j)
                if len(intx) > 1: # instead of len(x) > 0
                    new_desc.append(intx)
                    counter += len(intx)

        if len(new_desc) == counter:
            return cls.bottom()
        return cls.fix_desc(new_desc)
