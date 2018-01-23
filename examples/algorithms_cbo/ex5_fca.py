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
import re
import argparse
from fca.algorithms import dict_printer
from fca.algorithms.cbo import CbO
from fca.io.input_models import FormalContextModel

def read_float_input(msg):
    """
    Returns a float from user interface
    """
    entry = ''
    while re.match('^\\d+\\.\\d+$|^\\d+$', entry) is None or float(entry) > 1:
        entry = raw_input(msg)

    return float(entry)


def exec_ex5(filepath, min_sup=0):
    """
    Executes CbO in a single line
    """
    dict_printer(
        CbO(
            FormalContextModel(
                filepath=filepath
            ),
            min_sup=min_sup,
            lazy=False
        ).poset
    )


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 5 - FCA with Close-by-One (CbO)')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-m', '--min_sup', metavar='min_sup', type=float, help='Relative minimum support [0,1]', default=0.0)
    __args__ = __parser__.parse_args()
    exec_ex5(__args__.context_path, __args__.min_sup)
# okay decompiling ex5_cbo.pyc
