# GNU LICENCE
# Kyori code.
import sys
from fca.algorithms.addIntent import add_intent
#from libs.defs.Intervals import IntervalPattern
#from libs.defs.Sequences.SequencePattern import SequencePattern
from fca.reader import read_representations

#import os

if __name__ == "__main__":
    __path__ = sys.argv[1]
    __representations__ = read_representations(__path__)
    __lattice__ = add_intent(__representations__)
    print __lattice__.as_dict()


    #print g.nodes(data=True)
