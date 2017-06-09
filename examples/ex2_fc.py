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
import re
from fca.algorithms.addIntent import AddIntent
from fca.defs.patterns import IcebergSetPattern
from fca.reader import read_representations

"""
In this example we mine frequent formal concepts
Frequent Formal Concepts cannot be directly mined with addIntent
which is a bottom up concept builder

Luckily, we can just invert the notions of extents and intents
and go on exactly as with a normal setting
"""

def dict_printer(poset):
    """
    Nicely print the concepts in the poset
    """
    order = lambda s: (len(s[1][poset.EXTENT_MARK]), s[1][poset.EXTENT_MARK])
    for concept_id, concept in sorted(poset.as_dict().items(), key=order):
        # Another option is to invert intent and extents when getting the lattice
        if concept_id >= -2:
            print ('{} {} {}'.format(
                concept_id,
                concept[poset.EXTENT_MARK],
                concept[poset.INTENT_MARK]
                )
                  )

def read_int_input(msg):
    """
    Returns an int from user interface
    """
    entry = ''
    while re.match(r'\d+', entry) is None or int(entry < 0):
        entry = raw_input(msg)
    return int(entry)

def exec_ex2(filepath, min_sup):
    """
    Notice that we have imported a different kind of pattern
    IcebergSetPattern allows setting a min sup value
    """

    IcebergSetPattern.MIN_SUP = min_sup

    lattice = AddIntent(
        read_representations(filepath,
                             transposed=True
                            ),
        pattern=IcebergSetPattern,
        lazy=False
    ).lat

    dict_printer(lattice)


if __name__ == "__main__":
    __msg__ = "Insert absolute minimal support [0,inf]:"
    exec_ex2(sys.argv[1], read_int_input(__msg__))
