# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, Dec 20 2016, 23:05:08) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/victorcodocedo/Work/kyori_lab/github/fca/examples/ex6_cbo_ps.py
# Compiled at: 2017-09-27 11:41:31
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
from fca.defs.patterns import DistanceIntervalPattern
from fca.reader import List2IntervalsTransformer
from fca.reader import FormalContextManager
from fca.algorithms.cbo import PSCbO
from ex2_fc import dict_printer

def exec_ex6(filepath, theta):
    """
    Execute CbO over pattern structures
    
    Notice that the algorithm is different and it also works differently
    PSCbO lists objects one by one, in a bottom-up way
    """
    fctx = FormalContextManager(filepath=filepath, transformer=List2IntervalsTransformer(int))
    DistanceIntervalPattern.THETA = theta
    dict_printer(PSCbO(fctx, pattern=DistanceIntervalPattern, lazy=False).poset)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 6 - Interval with theta value with CbO')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-t', '--theta', metavar='theta', type=int, help='Maximal length for intervals [0,inf]', default=0)
    __args__ = __parser__.parse_args()
    exec_ex6(__args__.context_path, __args__.theta)
# okay decompiling ex6_cbo_ps.pyc
