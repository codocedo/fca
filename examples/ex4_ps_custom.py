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
In this example we make a custom pattern structure by modifying
an existing one
Particularly, we modify the IntervalPattern intersection
to allow for a similarity thresholding of each individual interval
"""

class DistanceIntervalPattern(IntervalPattern):
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


if __name__ == "__main__":
    # Notice that we have imported a different kind of pattern
    # IcebergSetPattern allows setting a min sup value
    DistanceIntervalPattern.THETA = 2

    __lattice__ = add_intent(
        read_representations(sys.argv[1]),
        pattern=DistanceIntervalPattern,
        repr_parser=DistanceIntervalPattern.PARSERS['SSV.F'], # Float values
        silent=False
    )


    for concept_id, concept in __lattice__.as_dict().items():
        print ('{} - ({}, {})'.format(
            concept_id,
            concept[ConceptLattice.EXTENT_MARK],
            concept[ConceptLattice.INTENT_MARK])
              )
