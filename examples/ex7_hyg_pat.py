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
from fca.defs.patterns.hypergraphs import PartitionPattern
from fca.reader import List2IntervalsTransformer

from fca.reader import read_representations
from fca.algorithms.addIntent import AddIntent
from ex2_fc import dict_printer

class List2PartitionsTransformer(List2IntervalsTransformer):
    """
    Transforms a list of values to a partition containing equivalence classes of indices
    [0,1,0,1,1] -> [set([0,2]), set([1,3,4])]
    """
    def parse(self, lst):
        hashes = {}
        for i, j in enumerate(lst):
            hashes.setdefault(j, []).append(i)
        return [set(i) for i in hashes.values()]

def exec_ex7(filepath):
    """
    Execute CbO over pattern structures

    Notice that the algorithm is different and it also works differently
    PSCbO lists objects one by one, in a bottom-up way
    """
    # the formal context should be said how to read the input file

    dict_printer(
        AddIntent(
            read_representations(
                filepath,
                transformer=List2PartitionsTransformer(int),
                transposed=True,
                fmgr='tab'
            ),
            pattern=PartitionPattern,
            lazy=False,
            silent=False,
        ).lat
    )


if __name__ == "__main__":
    exec_ex7(sys.argv[1])
