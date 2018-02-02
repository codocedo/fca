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

from ex10_duquenneguigues_previousclosure import exec_ex10
from ex13_ps_duquenneguigues_previousclosure_trimmedpartitions import exec_ex13
from ex15_duquenneguigues_enhanced import exec_ex15
from ex20_duquenneguigues_previousclosure_ondisk import exec_ex20
from ex21_ps_duquenneguigues_previousclosure_trimmedpartitions_ondisk import exec_ex21

__fctx_path__ = 'data/example.txt'
__ps_path__ = 'data/numerical_data.txt'
__part_ps_path__ = 'data/xyzw.csv'
__a_min_sup__ = 2
__r_min_sup__ = 0.25
__nasterisks__ = 100
__max_parts__ = 3

if __name__ == "__main__":

    print("*"*__nasterisks__)
    print("Example 10: Duquenne-Guigues Canonical Basis of Implication Rules with NextClosure")
    print("Input File: {}".format(__fctx_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex10(__fctx_path__, __r_min_sup__)

    print("*"*__nasterisks__)
    print("Example 13 - Canonical Base when extents are Partition Pattern Structures")
    print("Input File: {}".format(__part_ps_path__))
    print("Maximum Parts: INF")
    print("*"*__nasterisks__)
    exec_ex13(__part_ps_path__, sys.maxint)

    print("*"*__nasterisks__)
    print("Example 15 - Duquenne Guiges base with EnhanceDG")
    print("Input File: {}".format(__fctx_path__))
    print("*"*__nasterisks__)
    exec_ex15(__fctx_path__)

    print("*"*__nasterisks__)
    print("Example 20: Obtains the Duquenne-Guigues Canonical Base OnDisk - Streaming pattern to disk")
    print("Input File: {}".format(__fctx_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex20(__fctx_path__, __r_min_sup__, None)

    print("*"*__nasterisks__)
    print("Example 21: Duquenne Guigues Base using TrimmedPartitions with PreviousClosure OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__part_ps_path__))
    print("*"*__nasterisks__)
    exec_ex21(__part_ps_path__, None)
