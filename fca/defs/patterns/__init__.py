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
from fca.defs import Intent
from fca.defs import SetPattern

class IcebergSetPattern(SetPattern):
    """
    Generalizes SetPattern to allow for a minimal cardinality representation
    """
    MIN_SUP = 0
    @classmethod
    def fix_desc(cls, desc):
        if len(desc) < cls.MIN_SUP:
            return cls.bottom()
        return desc

    @classmethod
    def intersection(cls, desc1, desc2):
        assert cls.MIN_SUP >= 0, 'MIN_SUP value should be a positive number'
        new_desc = cls.fix_desc(desc1.intersection(desc2))
        return new_desc

class IntervalPattern(Intent):
    """
    Interval pattern as defined by Kaytoue
    CONVEX HULL: [a,b] \\cap [x,y] = [min(a,x),max(b,y)]
    """

    @classmethod
    def top(cls, top_rep=None):
        if cls._top is None:
            cls._top = []
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
        return cls._bottom

    @classmethod
    def meet(cls, desc1, desc2):
        for i, (j, k) in enumerate(zip(desc1, desc2)):
            desc1[i] = (min(j[0], k[0]), max(j[1], k[1]))

    @classmethod
    def intersection(cls, desc1, desc2):
        if desc2 == cls._top:
            return desc1
        interval = [(min(i[0], j[0]), max(i[1], j[1])) for i, j in zip(desc1, desc2)]
        return interval

    @classmethod
    def leq(cls, desc1, desc2):
        # print desc1, desc2,
        if desc1==cls._bottom:
            return True
        for i, j in zip(desc1, desc2):
            if i[0] > j[0] or i[1] < j[1]:
                return False
        return True

    @classmethod
    def is_equal(cls, desc1, desc2):
        if len(desc1) != len(desc2):
            return False
        for i, j in zip(desc1, desc2):
            if i[0] != j[0] or i[1] != j[1]:
                return False
        return True

    @classmethod
    def join(cls, desc1, desc2):
        if desc1 == cls._top:
            return True
        raise NotImplementedError

    @classmethod
    def union(cls, desc1, desc2):
        raise NotImplementedError

    @classmethod
    def is_empty(cls, desc):
        return False

    @classmethod
    def contains(cls, desc, key):
        return key in desc

    @classmethod
    def length(cls, desc):
        return len(desc)

    @classmethod
    def get_iterator(cls, desc):
        for interval in desc:
            yield interval

class MaxLengthIntervalPattern(IntervalPattern):
    """
    In this example we make a custom pattern structure by modifying
    an existing one
    Particularly, we modify the IntervalPattern intersection
    to allow for a similarity thresholding of each individual interval
    """
    THETA = 0

    @classmethod
    def intersection(cls, desc1, desc2):
        """
        Each interval should be at most of length THETA
        if not, the intersection is the bottom
        """
        # print desc1, desc2,'::',
        if desc1 == cls._top:
            return desc2
        new_interval = []
        bottom = False
        for i, j in zip(desc1, desc2):
            new_interval.append((min(i[0], j[0]), max(i[1], j[1])))
            if max(i[1], j[1]) - min(i[0], j[0]) > MaxLengthIntervalPattern.THETA:
                bottom = True
        if bottom:
            bot = MaxLengthIntervalPattern.bottom(new_interval)
            # print bot,'<-', id(bot)
            return bot
        # print new_interval
        return new_interval

# class TolerantIntervalPattern(IntervalPattern):
#     """
#     In this example we make a custom pattern structure by modifying
#     an existing one
#     Particularly, we modify the IntervalPattern intersection
#     to allow for a similarity thresholding of each individual interval
#     """
#     THETA = 0
#     NINTERVAL = (-sys.maxint, sys.maxint)

#     def intersection(self, other):
#         """
#         Each interval should be at most of length THETA
#         if not, the intersection is the bottom
#         """
#         if other == self._top:
#             return self
#         new_interval = []
#         bot = True
#         for i, j in zip(self.desc, other.desc):
#             if max(i[1], j[1]) - min(i[0], j[0]) <= TolerantIntervalPattern.THETA:
#                 new_interval.append((min(i[0], j[0]), max(i[1], j[1])))
#                 bot = False
#             else:
#                 new_interval.append(TolerantIntervalPattern.NINTERVAL)
#         if bot:
#             return self.bottom(new_interval)

#         return TolerantIntervalPattern(new_interval)

#     def repr(self):
#         out = []
#         for i in self.desc:
#             if i == TolerantIntervalPattern.NINTERVAL:
#                 out.append('*')
#             else:
#                 out.append(i)
#         return out
