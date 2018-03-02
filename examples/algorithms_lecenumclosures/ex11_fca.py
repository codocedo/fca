# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, Dec 20 2016, 23:05:08) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/victorcodocedo/Work/kyori_lab/github/fca/examples/ex9_next_closure.py
# Compiled at: 2017-09-27 11:43:36
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
from __future__ import print_function
import argparse
from fca.algorithms import dict_printer
from fca.algorithms.lecenum_closures import LecEnumClosures
from fca.io.input_models import FormalContextModel


def exec_ex11(filepath, min_sup=0):
    """
    Executes LecEnumClosures in a single line
    """
    dict_printer(LecEnumClosures(FormalContextModel(filepath=filepath), min_sup=min_sup, lazy=False).poset)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 11 - FCA with LecEnumClosures')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context in txt, space separated values, one object representation per line', action='store')
    __parser__.add_argument('-m', '--min_sup', metavar='min_sup', type=float, help='Relative minimum support [0,1]', default=0.0)
    __args__ = __parser__.parse_args()
    exec_ex11(__args__.context_path, __args__.min_sup)

