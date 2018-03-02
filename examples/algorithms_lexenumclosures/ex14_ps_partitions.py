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
import argparse
from fca.algorithms import dict_printer
from fca.algorithms.lexenum_closures import PSLexEnumClosures
from fca.defs.patterns.hypergraphs import PartitionPattern
from fca.io.transformers import List2PartitionsTransformer
from fca.io.input_models import PatternStructureModel


def exec_ex14(filepath, max_parts):
    """
    Example 14 - Partition Pattern Structure Mining with NextClosure

    Calculates the partition pattern structures based on equivalence classes
    using NextClosure algorithm

    We include a maximum parts threshold for mining partitions with at most
    max_parts elements in the partition
    """
    # PATTERNS HAVE SINGLETONS THAT NEED TO BE RESETED
    # WHEN REUSING THEM, WHENEVER YOU CALCULATE PATTERN STRUCTURES
    # MULTIPLE TIMES, YOU NEED TO RESET THEM BEFORE RE-USING
    # THEM, NOT DOING THIS MAY LEAD TO INCONSISTENCIES

    transposed = True
    PartitionPattern.reset()

    conditions = [
        lambda pattern: len(pattern) <= max_parts
    ]
    fctx = PatternStructureModel(
        filepath=filepath,
        transformer=List2PartitionsTransformer(transposed=transposed),
        transposed=transposed,
        file_manager_params={
            'style': 'tab'
        }
    )
    poset = PSLexEnumClosures(
        fctx,
        conditions=conditions,
        pattern=PartitionPattern,
        lazy=False
    ).poset
    dict_printer(
        poset,
        transposed=transposed
    )

if __name__ == "__main__":
    __parser__ = argparse.ArgumentParser(
        description='Example 14 - Partition Pattern Structure Mining with NexClosure'
    )
    __parser__.add_argument(
        'context_path',
        metavar='context_path',
        type=str,
        help='path to the formal context'
    )
    __parser__.add_argument(
        '-m',
        '--max_parts',
        metavar='max_parts',
        type=int,
        help='Maximum number of parts in a partition, between 0 and the number of rows',
        default=sys.maxint
    )
    __args__ = __parser__.parse_args()
    exec_ex14(__args__.context_path, __args__.max_parts)
