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
from __future__ import print_function
import sys
from fca.defs.patterns import DistanceIntervalPattern
from fca.reader import List2IntervalsTransformer

from fca.reader import FormalContextManager
from fca.algorithms.cbo import PSCbO
from ex2_fc import dict_printer, read_int_input

def exec_ex6(filepath, theta):
    """
    Execute CbO over pattern structures

    Notice that the algorithm is different and it also works differently
    PSCbO lists objects one by one, in a bottom-up way
    """
    # the formal context should be said how to read the input file
    fctx = FormalContextManager(filepath=filepath, transformer=List2IntervalsTransformer(int))

    # Configure the pattern structure
    DistanceIntervalPattern.THETA = theta

    # Execute the pattern structure and print
    dict_printer(PSCbO(fctx, pattern=DistanceIntervalPattern, lazy=False).poset)

if __name__ == "__main__":
    __msg__ = "Insert maximal length for intervals [0,inf]: "
    exec_ex6(sys.argv[1], read_int_input(__msg__))
