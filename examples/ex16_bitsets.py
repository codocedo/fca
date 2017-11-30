import argparse
from fca.defs import SSetPattern
from fca.algorithms.previous_closure import PSPreviousClosure
from fca.algorithms.addIntent import AddIntent
from fca.reader import read_representations, List2SetTransformer, FormalContextManager, PatternStructureManager
from ex2_fc import dict_printer

class List2BitSetTransformer(List2SetTransformer):
    def __init__(self, transposed=False):
        """
        Configures a data type to cast interval values
        """
        super(List2BitSetTransformer, self).__init__()
        if transposed:
            self.real_objects = self.real_elements
        else:
            self.real_attributes = self.real_elements
    
    def real_elements(self, args):
        """
        Returns the real attributes behind the indexed representation
        args: list of attribute indices
        return list of attributes
        """
        oneszeros = bin(args)[2:]
        args = [i for i in range(len(oneszeros)) if oneszeros[len(oneszeros)-i-1]=='1']
        return super(List2BitSetTransformer, self).real_attributes(args)

    def parse(self, lst):
        out = 0
        for att in lst:
            # out += 1<<self.attributes.setdefault(att, len(self.attributes))
            out += 1<<self.register_attribute(att)# .attributes.setdefault(att, len(self.attributes))
        return out

class BitSet(SSetPattern):
    _bottom = None
    _top = None

    @classmethod
    def bottom(cls, bot_rep=None):
        if cls._bottom is None:
            cls._bottom = 0
        return cls._bottom

    @classmethod
    def top(cls, top_rep=None):
        if cls._top is None:
            cls._top = 0
        if top_rep is not None:
            cls._top |= top_rep
        return cls._top
    @classmethod
    def length(cls, desc):
        return len([j for j in bin(desc)[2:] if j == '1'])
        # return len(desc)
    @classmethod
    def intersection(cls, desc1, desc2):
        return desc1 & desc2
    @classmethod
    def union(cls, desc1, desc2):
        return desc1 | desc2
    @classmethod
    def join(cls, desc1, desc2):
        desc1 |= desc2
    @classmethod
    def meet(cls, desc1, desc2):
        desc1 &= desc2
    @classmethod
    def leq(cls, desc1, desc2):
        return desc1 & desc2 == desc1
    @classmethod
    def is_empty(cls, desc):
        return desc == 0

def exec_ex9(filepath, min_sup=0):
    dict_printer(
        PSPreviousClosure(
            PatternStructureManager(
            # FormalContextManager(
                filepath=filepath,
                transformer=List2BitSetTransformer(transposed=True)
            ),
            pattern=BitSet,
            min_sup=min_sup,
            lazy=False
        ).poset,
        transposed=True
    )

    # lattice = AddIntent(
    #     read_representations(filepath,
    #                          transformer=List2BitSetTransformer(),
    #                         ),
    #     pattern=BitSet,
    #     silent=False,
    #     lazy=False,
    # ).lat
    # dict_printer(lattice)

if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 11 - FCA with PreviousClosure')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context in txt, space separated values, one object representation per line', action='store')
    __parser__.add_argument('-m', '--min_sup', metavar='min_sup', type=float, help='Relative minimum support [0,1]', default=0.0)
    __args__ = __parser__.parse_args()
    exec_ex9(__args__.context_path, __args__.min_sup)
    # exec_ex9(sys.argv[1])
