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
from ex11_fca import exec_ex11
from ex12_ps_trimmed_partitions import exec_ex12
from ex18_ondisk import exec_ex18
from ex19_ps_ondisk import exec_ex19

__fctx_path__ = 'data/example.txt'
__ps_path__ = 'data/numerical_data.txt'
__part_ps_path__ = 'data/xyzw.csv'

__a_min_sup__ = 2
__r_min_sup__ = 0.25
__nasterisks__ = 100
__max_parts__ = 3

if __name__ == "__main__":

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
    print("Example 18: LecEnumClosures OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__fctx_path__))
    # print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex18(__fctx_path__, 0, None)

    print("*"*__nasterisks__)
    print("Example 19: StrippedPartitions with LecEnumClosures OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__part_ps_path__))
    print("*"*__nasterisks__)
    exec_ex19(__part_ps_path__, None)