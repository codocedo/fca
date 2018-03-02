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
sys.path.append('./algorithms_addIntent')
sys.path.append('./algorithms_cbo')
sys.path.append('./algorithms_lecenumclosures')
sys.path.append('./algorithms_lexenumclosures')
sys.path.append('./algorithms_canonicalbase')

from ex1_fca import exec_ex1
from ex2_iceberg_lattice import exec_ex2
from ex3_ps_intervals import exec_ex3
from ex4_ps_custom_pattern import exec_ex4
from ex7_ps_partitions import exec_ex7
from ex16_ondisk import exec_ex16

from ex5_fca import exec_ex5
from ex6_ps_intervals import exec_ex6
from ex8_ps_partitions import exec_ex8

from ex9_fca import exec_ex9
from ex14_ps_partitions import exec_ex14
from ex17_ondisk import exec_ex17

from ex10_duquenneguigues_lecenumclosures import exec_ex10
from ex13_ps_duquenneguigues_lecenumclosures_trimmedpartitions import exec_ex13
from ex15_duquenneguigues_enhanced import exec_ex15
from ex20_duquenneguigues_lecenumclosures_ondisk import exec_ex20
from ex21_ps_duquenneguigues_lecenumclosures_strippedpartitions_ondisk import exec_ex21

from ex11_fca import exec_ex11
from ex12_ps_trimmed_partitions import exec_ex12
from ex18_ondisk import exec_ex18
from ex19_ps_ondisk import exec_ex19


__fctx_path__ = '../data/example.txt'
__ps_path__ = '../data/numerical_data.txt'
__part_ps_path__ = '../data/xyzw.csv'
__output_path__ = '../data/results.csv'
__a_min_sup__ = 2
__r_min_sup__ = 0.25
__nasterisks__ = 100
__max_parts__ = 3

if __name__ == "__main__":
    print("*"*__nasterisks__)
    print("Example 1: Formal Concept Analysis, AddIntent in a single line")
    print("Input File: {}".format(__fctx_path__))
    print("*"*__nasterisks__)
    exec_ex1(__fctx_path__)

    print("*"*__nasterisks__)
    print("Example 2: Frequent patterns by means of AddIntent")
    print("Input File: {}".format(__fctx_path__))
    print("Min. Sup.: {}".format(__a_min_sup__))
    print("*"*__nasterisks__)
    exec_ex2(__fctx_path__, __a_min_sup__)

    print("*"*__nasterisks__)
    print("Example 3: Pattern Structures, mining interval patterns")
    print("Input File: {}".format(__ps_path__))
    print("*"*__nasterisks__)
    exec_ex3(__ps_path__)

    print("*"*__nasterisks__)
    print("Example 4: Custom Pattern Structures, setting a threshold for mining interval patterns")
    print("Input File: {}".format(__ps_path__))
    print("THETA: {}".format(__a_min_sup__))
    print("*"*__nasterisks__)
    exec_ex4(__ps_path__, __a_min_sup__)

    print("*"*__nasterisks__)
    print("Example 5: FCA with Close-by-One (CbO)")
    print("Input File: {}".format(__ps_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex5(__fctx_path__, __r_min_sup__)

    print("*"*__nasterisks__)
    print("Example 6: Interval Pattern Structures with CbO")
    print("Input File: {}".format(__ps_path__))
    print("THETA: {}".format(__a_min_sup__))
    print("*"*__nasterisks__)
    exec_ex6(__ps_path__, __a_min_sup__)

    print("*"*__nasterisks__)
    print("Example 7: Partiton Pattern Structures with AddIntent")
    print("Input File: {}".format(__ps_path__))
    print("*"*__nasterisks__)
    exec_ex7(__ps_path__)

    print("*"*__nasterisks__)
    print("Example 8: Partiton Pattern Structures with CbO")
    print("Input File: {}".format(__ps_path__))
    print("*"*__nasterisks__)
    print (__ps_path__)
    exec_ex8(__ps_path__)
    

    print("*"*__nasterisks__)
    print("Example 9: FCA with LexEnumClosures")
    print("Input File: {}".format(__fctx_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex9(__fctx_path__, __r_min_sup__)

    print("*"*__nasterisks__)
    print("Example 10: Duquenne-Guigues Canonical Basis of Implication Rules with LexEnumClosures")
    print("Input File: {}".format(__fctx_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex10(__fctx_path__, __r_min_sup__)

    print("*"*__nasterisks__)
    print("Example 11: FCA with LecEnumClosures")
    print("Input File: {}".format(__fctx_path__))
    # print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex11(__fctx_path__, 0)

    print("*"*__nasterisks__)
    print("Example 12 - Partition Pattern Structure Mining with LecEnumClosures")
    print("Input File: {}".format(__part_ps_path__))
    print("Maximum Parts: INF")
    print("*"*__nasterisks__)
    exec_ex12(__part_ps_path__)

    print("*"*__nasterisks__)
    print("Example 13 - Canonical Base when extents are Partition Pattern Structures")
    print("Input File: {}".format(__part_ps_path__))
    print("Maximum Parts: INF")
    print("*"*__nasterisks__)
    exec_ex13(__part_ps_path__, sys.maxint)

    print("*"*__nasterisks__)
    print("Example 14 - Partition Pattern Structures with NexClosure")
    print("Input File: {}".format(__part_ps_path__))
    print("Maximum Parts: {}".format(__max_parts__))
    print("*"*__nasterisks__)
    exec_ex14(__part_ps_path__, __max_parts__)

    print("*"*__nasterisks__)
    print("Example 15 - Duquenne Guiges base with EnhanceDG")
    print("Input File: {}".format(__fctx_path__))
    print("*"*__nasterisks__)
    exec_ex15(__fctx_path__)

    print("*"*__nasterisks__)
    print("Example 16: CbO OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__ps_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    print (__ps_path__)
    exec_ex16(__ps_path__, __r_min_sup__, None)

    print("*"*__nasterisks__)
    print("Example 17: LexEnumClosures OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__fctx_path__))
    # print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex17(__fctx_path__, 0)

    print("*"*__nasterisks__)
    print("Example 18: LecEnumClosures OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__fctx_path__))
    # print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex18(__fctx_path__, 0, None)

    print("*"*__nasterisks__)
    print("Example 19: StrippedPartitions with LecEnumClosures OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__part_ps_path__))
    # print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex19(__part_ps_path__, None)

    print("*"*__nasterisks__)
    print("Example 20: Obtains the Duquenne-Guigues Canonical Base OnDisk - Streaming pattern to disk")
    print("Input File: {}".format(__fctx_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex20(__fctx_path__, __r_min_sup__, None)

    print("*"*__nasterisks__)
    print("Example 21: Duquenne Guigues Base using StrippedPartitions with LecEnumClosures OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__part_ps_path__))
    print("*"*__nasterisks__)
    exec_ex21(__part_ps_path__, None)
