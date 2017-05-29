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
from fca.algorithms.addIntent import add_intent
from fca.defs import ConceptLattice
from fca.defs.patterns import IntervalPattern
from fca.reader import read_representations


"""
In this example we mine pattern structure
particularly interval pattern structures
"""

class IntervalPatternDistance(IntervalPattern):
    THETA = 0

    def intersection(self, other):
        new_interval = []
        for i, j in zip(self.desc, other.desc):
            if max(i[1], j[1]) - min(i[0], j[0]) <= IntervalPatternDistance.THETA:
                new_interval.append((min(i[0], j[0]), max(i[1], j[1])))
            else:
                return self.bottom()
        return IntervalPatternDistance(new_interval)


if __name__ == "__main__":
    # Notice that we have imported a different kind of pattern
    # IcebergSetPattern allows setting a min sup value
    IntervalPatternDistance.THETA = 2

    __lattice__ = add_intent(
        read_representations(sys.argv[1]),
        pattern=IntervalPatternDistance,
        repr_parser=IntervalPatternDistance.PARSERS['SSV.I'],
        silent=False
    )


    for concept_id, concept in __lattice__.as_dict().items():
        # Another option is to invert intent and extents when getting the lattice
        print ('{} - ({}, {})'.format(
            concept_id,
            concept[ConceptLattice.EXTENT_MARK],
            concept[ConceptLattice.INTENT_MARK])
              )
