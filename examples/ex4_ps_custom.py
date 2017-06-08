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
from fca.algorithms.addIntent import AddIntent
from fca.defs.patterns import IntervalPattern
from fca.reader import read_representations, List2IntervalsTransformer
from ex2_fc import dict_printer, read_int_input

class DistanceIntervalPattern(IntervalPattern):
    """
    In this example we make a custom pattern structure by modifying
    an existing one
    Particularly, we modify the IntervalPattern intersection
    to allow for a similarity thresholding of each individual interval
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

def exec_ex4(filepath, theta_value):
    """
    Execute this example
    """
    DistanceIntervalPattern.THETA = int(theta_value)

    '''
    The rest is the same as the previous example, but we are going to assign the
    pattern structure just created
    '''
    dict_printer(
        AddIntent(
            read_representations(filepath,
                                 transformer=List2IntervalsTransformer(int)
                                ),
            pattern=DistanceIntervalPattern,
            lazy=False
        ).lat
    )

if __name__ == "__main__":
    __msg__ = "Insert maximal length for intervals [0,inf]:"
    exec_ex4(sys.argv[1], read_int_input(__msg__))




