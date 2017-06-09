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
from fca.defs import Intent
from fca.defs import SetPattern

class IcebergSetPattern(SetPattern):
    """
    Generalizes SetPattern to allow for a minimal cardinality representation
    """
    MIN_SUP = 0
    def __init__(self, desc):
        if len(desc) < self.MIN_SUP:
            desc = set([])
        super(IcebergSetPattern, self).__init__(desc)

    def intersection(self, other):
        assert IcebergSetPattern.MIN_SUP >= 0, 'MIN_SUP value should be a positive number'
        newdesc = self.desc.intersection(other.desc)
        if len(newdesc) < self.MIN_SUP:
            return self.bottom()
        else:
            return IcebergSetPattern(newdesc)

class IntervalPattern(Intent):
    """
    Interval pattern as defined by Kaytoue
    CONVEX HULL: [a,b] \\cap [x,y] = [min(a,x),max(b,y)]
    """
    @classmethod
    def top(cls, top_rep=None):
        top = cls([])
        top.__i_le__ = lambda s: False
        top.__i_eq__ = lambda s: False
        top.is_empty = lambda: False
        top.__i_str__ = lambda: "Top"
        top.intersection = lambda s: s
        return top

    @classmethod
    def bottom(cls, bot_rep=None):
        bottom = cls([])
        bottom.__i_le__ = lambda s: True
        bottom.is_empty = lambda: True
        bottom.__type__ = -1
        bottom.__i_eq__ = lambda s: s.__type__ == -1
        return bottom

    def intersection(self, other):
        interval = [(min(i[0], j[0]), max(i[1], j[1])) for i, j in zip(self.desc, other.desc)]
        return IntervalPattern(interval)

    def __i_str__(self):
        return str(self.desc)

    def __i_le__(self, other):
        if other.is_empty():
            return False
        for i, j in zip(self.desc, other.desc):
            if i[0] > j[0] or i[1] < j[1]:
                return False
        return True
    def __i_eq__(self, other):
        for i, j in zip(self.desc, other.desc):
            if i[0] != j[0] or i[1] != j[1]:
                return False
        return True
    def join(self, other):
        pass
    def is_empty(self):
        return False
    def __i_contains__(self, key):
        return key in self.desc
    def __i_len__(self):
        return len(self.desc)
    def __i_iter__(self):
        for interval in self.desc:
            yield interval


class DistanceIntervalPattern(IntervalPattern):
    """
    Generalizes IntervalPattern to allow for a length threshold
    for each interval
    """
    THETA = 0 # Distance between intervals

    def intersection(self, other):
        """
        Each interval should be at most of length THETA
        if not, the intersection is the bottom
        """
        new_interval = []
        for i, j in zip(self.desc, other.desc):
            if max(i[1], j[1]) - min(i[0], j[0]) <= DistanceIntervalPattern.THETA:
                new_interval.append((min(i[0], j[0]), max(i[1], j[1])))
            else:
                return self.bottom()

        return DistanceIntervalPattern(new_interval)


