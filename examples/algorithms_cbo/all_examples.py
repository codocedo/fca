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
from ex5_fca import exec_ex5
from ex6_ps_intervals import exec_ex6
from ex8_ps_partitions import exec_ex8
from ex16_ondisk import exec_ex16

__fctx_path__ = 'data/example.txt'
__ps_path__ = 'data/numerical_data.txt'
__part_ps_path__ = 'data/xyzw.csv'

__a_min_sup__ = 2
__r_min_sup__ = 0.25
__nasterisks__ = 100
__max_parts__ = 3

if __name__ == "__main__":

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
    print("Example 8: Partiton Pattern Structures with CbO")
    print("Input File: {}".format(__ps_path__))
    print("*"*__nasterisks__)
    print (__ps_path__)
    exec_ex8(__ps_path__)

    print("*"*__nasterisks__)
    print("Example 16: CbO OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__ps_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    print (__ps_path__)
    exec_ex16(__ps_path__, __r_min_sup__, None)
