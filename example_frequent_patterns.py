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
from fca.defs.patterns import IcebergSetPattern
#from libs.defs.Intervals import IntervalPattern
#from libs.defs.Sequences.SequencePattern import SequencePattern
from fca.reader import read_representations

#import os

if __name__ == "__main__":
    __path__ = sys.argv[1]
    __representations__ = read_representations(__path__)

    IcebergSetPattern.MIN_SUP = 3

    ConceptLattice.EXTENT_MARK = 'in'
    ConceptLattice.INTENT_MARK = 'ex'
    __lattice__ = add_intent(__representations__, pattern=IcebergSetPattern, silent=False)

    print (__lattice__.as_dict())


    #print g.nodes(data=True)
