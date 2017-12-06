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
import sys
import argparse
# from fca.algorithms.previous_closure import PSPreviousClosure
from fca.algorithms import lst2str
from fca.algorithms.canonical_base import PSCanonicalBase
from fca.defs.patterns.hypergraphs import TrimmedPartitionPattern
from fca.reader import List2PartitionsTransformer
from fca.reader import PatternStructureManager

def exec_ex21(filepath, output_path=None):
    """
    Example 21: Duquenne Guigues Base using TrimmedPartitions with PreviousClosure OnDisk - Streaming patterns to disk
    """
    transposed = True
    TrimmedPartitionPattern.reset()

    fctx = PatternStructureManager(
        filepath=filepath,
        transformer=List2PartitionsTransformer(transposed),
        transposed=transposed,
        file_manager_params={
            'style': 'tab'
        }
    )
    canonical_base = PSCanonicalBase(
        # PSPreviousClosure(
        fctx,
        pattern=TrimmedPartitionPattern,
        lazy=False,
        silent=False,
        ondisk=True,
        ondisk_kwargs={
            'output_path': output_path,
            'write_support':True,
            'write_extent':False
            }
    )
    output_path = canonical_base.poset.close()

    for rule, support in canonical_base.get_implications():
        ant, con = rule
        print('{:>10s} => {:10s}'.format(lst2str(ant),lst2str(con)), support)

    print ("\t=> Results stored in {}".format(output_path))

if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(
        description='Example 21: Duquenne Guigues Base using TrimmedPartitions with PreviousClosure OnDisk - Streaming patterns to disk'
    )
    __parser__.add_argument(
        'context_path',
        metavar='context_path',
        type=str,
        help='path to the formal context'
    )
    __parser__.add_argument(
        '-o',
        '--output_path',
        metavar='output_path',
        type=str,
        help='Output file to save formal concepts',
        default=None
    )

    __args__ = __parser__.parse_args()
    exec_ex21(__args__.context_path, __args__.output_path)
# okay decompiling ex5_cbo.pyc
