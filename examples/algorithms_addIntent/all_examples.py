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
from ex1_fca import exec_ex1
from ex2_iceberg_lattice import exec_ex2
from ex3_ps_intervals import exec_ex3
from ex4_ps_custom_pattern import exec_ex4
from ex7_ps_partitions import exec_ex7

__fctx_path__ = 'data/example.txt'
__ps_path__ = 'data/numerical_data.txt'
__part_ps_path__ = 'data/xyzw.csv'
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
    print("Example 7: Partiton Pattern Structures with AddIntent")
    print("Input File: {}".format(__ps_path__))
    print("*"*__nasterisks__)
    exec_ex7(__ps_path__)
