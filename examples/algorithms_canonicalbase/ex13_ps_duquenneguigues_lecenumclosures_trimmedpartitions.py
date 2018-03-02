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
from fca.algorithms import lst2str
from fca.algorithms.canonical_base import PSCanonicalBase
from fca.defs.patterns.hypergraphs import TrimmedPartitionPattern, PartitionPattern
from fca.io.transformers import List2PartitionsTransformer
from fca.io.input_models import PatternStructureModel

def exec_ex13(filepath, max_parts):
    """
    Example 13 - Canonical Base when extents are Partition Pattern Structures

    Calculates the canonical base of implications using partition pattern structures
    as extents, this actually amounts to calculate functional dependencies

    We include a maximum parts threshold for mining partitions with at most
    max_parts elements in the partition
    """
    # PATTERNS HAVE SINGLETONS THAT NEED TO BE RESETED
    # WHEN REUSING THEM, WHENEVER YOU CALCULATE PATTERN STRUCTURES
    # MULTIPLE TIMES, YOU NEED TO RESET THEM BEFORE RE-USING
    # THEM, NOT DOING THIS MAY LEAD TO INCONSISTENCIES
    TrimmedPartitionPattern.reset()

    conditions = [
        lambda pattern: len(pattern) <= max_parts
    ]
    fctx = PatternStructureModel(
        filepath=filepath,
        transformer=List2PartitionsTransformer(int),
        transposed=True,
        file_manager_params={
            'style': 'tab'
        }
    )

    canonical_base = PSCanonicalBase(
        fctx,
        pattern=PartitionPattern,
        conditions=conditions,
        lazy=False,
        silent=True
    )

    for rule, support in canonical_base.get_implications():
        ant, con = rule
        print('{:>10s} => {:10s}'.format(lst2str(ant),lst2str(con)), support)


if __name__ == "__main__":
    __parser__ = argparse.ArgumentParser(
        description='Example 13 - Canonical Base when extents are Partition Pattern Structures'
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
    exec_ex13(__args__.context_path, __args__.max_parts)

