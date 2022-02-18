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
import sys
import os
from functools import reduce
from fca.defs import OnDiskPOSET, POSET, SetPattern

lst2str = lambda lst: ','.join(map(str, lst[:8])) if len(lst) > 0 else "[]"

def lexo(set_a, set_b):
    """
    LEXICAL COMPARISON BETWEEN TWO SETS OF INTEGERS
    """
    return tuple(sorted(set_a)) <= tuple(sorted(set_b))


def dict_printer(poset, **kwargs): #print_support=False, transposed=False, indices=False):
    """
    Nicely print the concepts in the poset
    """
    template = kwargs.get('template', '{:4s}\t{:30s}\t{:30s}')
    transposed = kwargs.get('transposed', False)
    indices = kwargs.get('indices', False)
    extent_postproc = kwargs.get('extent_postproc', lst2str)
    intent_postproc = kwargs.get('intent_postproc', lst2str)

    ema = poset.EXTENT_MARK
    ima = poset.INTENT_MARK
    if transposed:
        ema = poset.INTENT_MARK
        ima = poset.EXTENT_MARK

    order = lambda s: (
        len(s[1][ema]), s[1][ima]
    )
    for i, (concept_id, concept) in enumerate(sorted(poset.as_dict(indices).items(), key=order)):
        print (template.format(
            str(i+1),
            str(extent_postproc(concept[ema])),
            str(intent_postproc(concept[ima]))
        ))


class Algorithm(object):
    """
    Abstract class for algorithm.
    Implemented by AddIntent and PSCbO
    """
    def __init__(self, ctx, **kwargs):
        """
        if not lazy it should run the algorithm as soon as this class
        is instantiated
        """
        self.ctx = ctx
        self.poset = None
        self.pattern = kwargs.get('pattern', SetPattern)
        self.e_pattern = kwargs.get('e_pattern', SetPattern)
        
        self.min_sup = kwargs.get('min_sup', 0)
        self.printer = kwargs.get('printer', lambda a, b, c: None)

        self.calls = 0
        self.stdout = sys.stdout
        self.lazy = kwargs.get('lazy', False)
        self.silent = kwargs.get('silent', True)

        self.ondisk = kwargs.get('ondisk', False)
        self.ondisk_kwargs = kwargs.get('ondisk_kwargs', {})

        self.config()
        
        if not self.ondisk:
            self.poset = POSET(transformer=self.ctx.transformer)
        else:
            self.poset = OnDiskPOSET(transformer=self.ctx.transformer, **self.ondisk_kwargs)
    
        if not self.lazy:
            if self.silent:
                self.silence()
            self.run()
            if self.silent:
                self.talk()

    def config(self):
        """
        Configs the main parameters of the algorithm
        """
        raise NotImplementedError

    def run(self, *args, **kwargs):
        """
        Executes the algorithm
        """
        raise NotImplementedError

    def silence(self):
        """
        Makes printing unavailable
        """
        sys.stdout = open(os.devnull, "w")

    def talk(self):
        """
        Makes printing available
        """
        sys.stdout = self.stdout
    
    def derive_intent(self, P):
        """
        Derive an intent to obtain its extent
        """
        return set([ ei for ei, e in self.ctx.g_prime.items() if P.issubset(e)] )

    def derive_extent(self, P):
        """
        Derive an extent to obtain its intent
        """
        return set([ei for ei, e in self.ctx.m_prime.items() if P.issubset(e)])
