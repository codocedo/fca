# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, Dec 20 2016, 23:05:08) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/victorcodocedo/Work/kyori_lab/github/fca/examples/ex8_hyg_pat_cbo.py
# Compiled at: 2017-09-28 11:13:47
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
from __future__ import print_function
import argparse
from fca.defs.patterns.hypergraphs import PartitionPattern
from fca.reader import PatternStructureManager, List2PartitionsTransformer
from fca.algorithms.cbo import PSCbO
from ex2_fc import dict_printer

def exec_ex8(filepath):
    """
    Example 8 - Partition Pattern Structures with CbO:
    
    Generates partitions based on equivalence classes,
    using a custom Transformer (List2PartitionsTransformer)
    """
    fctx = PatternStructureManager(filepath=filepath, transformer=List2PartitionsTransformer(int), transposed=True, file_manager_params={'style': 'tab'
       })
    dict_printer(PSCbO(fctx, pattern=PartitionPattern, lazy=False).poset)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 8 - Partition Pattern Structures with CbO:\n                       Generates partitions based on equivalence classes,\n                       using a custom Transformer (List2PartitionsTransformer)\n                    ')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __args__ = __parser__.parse_args()
    exec_ex8(__args__.context_path)
# okay decompiling ex8_hyg_pat_cbo.pyc
