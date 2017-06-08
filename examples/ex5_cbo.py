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
import re
from fca.reader import FormalContextManager
from fca.algorithms.cbo import CbO
from ex2_fc import dict_printer

def read_float_input(msg):
    """
    Returns a float from user interface
    """
    entry = ''
    while re.match(r'^\d+\.\d+$|^\d+$', entry) is None or float(entry > 1):
        entry = raw_input(msg)
    return float(entry)

def exec_ex5(filepath, min_sup=0):
    """
    Executes CbO in a single line
    """
    dict_printer(
        CbO(
            FormalContextManager(filepath=filepath),
            min_sup=min_sup,
            lazy=False
            ).poset
        )

if __name__ == "__main__":
    __msg__ = "Insert minimal support [0,1]:"
    exec_ex5(sys.argv[1], read_float_input(__msg__))
