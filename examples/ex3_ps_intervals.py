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
from ex2_fc import dict_printer

"""
In this example we mine pattern structure
particularly interval pattern structures
"""

def exec_ex3(filepath):
    """
    Executes exercise 2

    Notice that we have imported a different kind of pattern
    in this case, we import IntervalPattern that is able to mine
    interval patterns. Plus, we import a different file transformer.
    List2IntervalsTransformer knows how to convert data file to the format
    suitable for IntervalPatterns. It can be configured to use int or floats
    as a base for value
    """
    dict_printer(
        AddIntent(
            read_representations(filepath,
                                 transformer=List2IntervalsTransformer(int)
                                ),
            pattern=IntervalPattern,
            lazy=False
        ).lat
    )

if __name__ == "__main__":
    exec_ex3(sys.argv[1])
