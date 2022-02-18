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
from fca.algorithms import lst2str
from fca.algorithms.canonical_base import PSCanonicalBase
from fca.defs.patterns.hypergraphs import StrippedPartitionPattern
from fca.io.transformers import List2PartitionsTransformer
from fca.io.sorters import PartitionSorter
from fca.io.input_models import PatternStructureModel

def exec_ex21(filepath, output_fname=None):
    """
    Example 21: Duquenne Guigues Base using StrippedPartitionPattern with LecEnumClosures OnDisk - Streaming patterns to disk
    """
    transposed = True
    StrippedPartitionPattern.reset()

    fctx = PatternStructureModel(
        filepath=filepath,
        transformer=List2PartitionsTransformer(transposed),
        sorter=PartitionSorter(),
        transposed=transposed,
        file_manager_params={
            'style': 'tab'
        }
    )
    canonical_base = PSCanonicalBase(
        # PSPreviousClosure(
        fctx,
        e_pattern=StrippedPartitionPattern,
        lazy=False,
        silent=True,
        ondisk=True,
        ondisk_kwargs={
            'output_path':'/tmp',
            'output_fname': output_fname,
            'write_support':True,
            'write_extent':False
            }
    )
    output_path = canonical_base.poset.close()

    fctx.transformer.attribute_index = {i:j for i, j in enumerate(fctx.sorter.processing_order)}

    for i, (rule, support) in enumerate(canonical_base.get_implications()):
        ant, con = rule
        print('{}: {:10s} => {:10s}'.format(i+1, lst2str(ant), lst2str(con)), support)

    print ("\t=> Pseudo closures stored in {}".format(output_path))

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
        '--output_fname',
        metavar='output_fname',
        type=str,
        help='Output file to save formal concepts',
        default=None
    )

    __args__ = __parser__.parse_args()
    exec_ex21(__args__.context_path, __args__.output_fname)
