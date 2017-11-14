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
from fca.algorithms.previous_closure import PSPreviousClosure
from fca.reader import PatternStructureManager, List2PartitionsTransformer
from fca.defs.patterns.hypergraphs import PartitionPattern

def dict_printer(poset):
    """
    Nicely print the concepts in the poset
    """
    order = lambda s: (
        len(s[1][poset.EXTENT_MARK]), s[1][poset.EXTENT_MARK]
    )
    for concept_id, concept in sorted(poset.as_dict().items(), key=order):
        if concept_id >= -2:
            print '{} {} || {}'.format(
                '',
                [sorted(set(sorted(i)[:2]+sorted(i)[-3:])) for i in concept[poset.EXTENT_MARK]],
                concept[poset.INTENT_MARK]
            )



def exec_ex12(filepath, max_parts):
    """
    Example 12 - Partition Pattern Structure Mining with PreviousClosure

    Calculates the partition pattern structures based on equivalence classes
    using PreviousClosure algorithm

    We include a maximum parts threshold for mining partitions with at most
    max_parts elements in the partition
    """
    # PATTERNS HAVE SINGLETONS THAT NEED TO BE RESETED
    # WHEN REUSING THEM, WHENEVER YOU CALCULATE PATTERN STRUCTURES
    # MULTIPLE TIMES, YOU NEED TO RESET THEM BEFORE RE-USING
    # THEM, NOT DOING THIS MAY LEAD TO INCONSISTENCIES
    PartitionPattern.reset()

    conditions = [
        lambda pattern: len(pattern) <= max_parts
    ]
    fctx = PatternStructureManager(
        filepath=filepath,
        transformer=List2PartitionsTransformer(int),
        transposed=True,
        file_manager_params={
            'style': 'tab'
        }
    )

    dict_printer(
        PSPreviousClosure(
            fctx,
            conditions=conditions,
            pattern=PartitionPattern,
            lazy=False
        ).poset
    )


if __name__ == "__main__":
    __parser__ = argparse.ArgumentParser(
        description='Example 12 - Partition Pattern Structure Mining with PreviousClosure'
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
    exec_ex12(__args__.context_path, __args__.max_parts)