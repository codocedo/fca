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
<<<<<<< HEAD
from ex9_fca import exec_ex9
from ex14_ps_partitions import exec_ex14
from ex17_ondisk import exec_ex17
=======
import sys
from ex9_fca import exec_ex9
from ex14_ps_partitions import exec_ex14
>>>>>>> Fixed problems with previous closure canonical test

__fctx_path__ = 'data/example.txt'
__ps_path__ = 'data/numerical_data.txt'
__part_ps_path__ = 'data/xyzw.csv'
__a_min_sup__ = 2
__r_min_sup__ = 0.25
__nasterisks__ = 100
__max_parts__ = 3

if __name__ == "__main__":

    print("*"*__nasterisks__)
    print("Example 9: FCA with NextClosure")
    print("Input File: {}".format(__fctx_path__))
    print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex9(__fctx_path__, __r_min_sup__)

    print("*"*__nasterisks__)
    print("Example 14 - Partition Pattern Structures with NexClosure")
    print("Input File: {}".format(__part_ps_path__))
    print("Maximum Parts: {}".format(__max_parts__))
    print("*"*__nasterisks__)
    exec_ex14(__part_ps_path__, __max_parts__)
<<<<<<< HEAD

    print("*"*__nasterisks__)
    print("Example 17: NextClosure OnDisk - Streaming patterns to disk")
    print("Input File: {}".format(__fctx_path__))
    # print("Min. Sup.: {}".format(__r_min_sup__))
    print("*"*__nasterisks__)
    exec_ex17(__fctx_path__, 0)
=======
>>>>>>> Fixed problems with previous closure canonical test
