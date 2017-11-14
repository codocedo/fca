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
    # PATTERNS HAVE SINGLETONS THAT NEED TO BE RESETED 
    # WHEN REUSING THEM, WHENEVER YOU CALCULATE PATTERN STRUCTURES
    # MULTIPLE TIMES, YOU NEED TO RESET THEM BEFORE RE-USING
    # THEM, NOT DOING THIS MAY LEAD TO INCONSISTENCIES
    PartitionPattern.reset()

    fctx = PatternStructureManager(
        filepath=filepath,
        transformer=List2PartitionsTransformer(int),
        transposed=True,
        file_manager_params={
            'style': 'tab'
        }
    )
    dict_printer(PSCbO(fctx, pattern=PartitionPattern, lazy=False).poset)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 8 - Partition Pattern Structures with CbO:\n                       Generates partitions based on equivalence classes,\n                       using a custom Transformer (List2PartitionsTransformer)\n                    ')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __args__ = __parser__.parse_args()
    exec_ex8(__args__.context_path)
# okay decompiling ex8_hyg_pat_cbo.pyc
