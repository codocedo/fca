# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, Dec 20 2016, 23:05:08) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/victorcodocedo/Work/kyori_lab/github/fca/examples/ex4_ps_custom.py
# Compiled at: 2017-09-27 10:37:50
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
import argparse
from fca.algorithms.addIntent import AddIntent
from fca.defs.patterns import IntervalPattern
from fca.reader import read_representations, List2IntervalsTransformer
from ex2_fc import dict_printer

class DistanceIntervalPattern(IntervalPattern):
    """
    In this example we make a custom pattern structure by modifying
    an existing one
    Particularly, we modify the IntervalPattern intersection
    to allow for a similarity thresholding of each individual interval
    """
    THETA = 0

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


def exec_ex4(filepath, theta_value):
    """
    Execute this example
    """
    DistanceIntervalPattern.THETA = int(theta_value)
    dict_printer(AddIntent(read_representations(filepath, transformer=List2IntervalsTransformer(int)), pattern=DistanceIntervalPattern, lazy=False).lat)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 4 - Custom Pattern Structure with AddIntent: Interval with theta value')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-t', '--theta', metavar='theta', type=int, help='Maximal length for intervals [0,inf]', default=0)
    __args__ = __parser__.parse_args()
    exec_ex4(__args__.context_path, __args__.theta)
# okay decompiling ex4_ps_custom.pyc
