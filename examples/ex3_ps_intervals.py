# uncompyle6 version 2.12.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.13 |Continuum Analytics, Inc.| (default, Dec 20 2016, 23:05:08) 
# [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.57)]
# Embedded file name: /Users/victorcodocedo/Work/kyori_lab/github/fca/examples/ex3_ps_intervals.py
# Compiled at: 2017-09-27 10:37:07
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
import argparse
from fca.algorithms.addIntent import AddIntent
from fca.defs.patterns import IntervalPattern
from fca.reader import read_representations, List2IntervalsTransformer
from ex2_fc import dict_printer

def exec_ex3(filepath):
    """
    Executes example 3
    
    Notice that we have imported a different kind of pattern
    in this case, we import IntervalPattern that is able to mine
    interval patterns. Plus, we import a different file transformer.
    List2IntervalsTransformer knows how to convert data file to the format
    suitable for IntervalPatterns. It can be configured to use int or floats
    as a base for value
    """
    dict_printer(AddIntent(read_representations(filepath, transformer=List2IntervalsTransformer(int)), pattern=IntervalPattern, lazy=False).lat)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 3 - Interval Pattern Structures with AddIntent')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __args__ = __parser__.parse_args()
    exec_ex3(__args__.context_path)
# okay decompiling ex3_ps_intervals.pyc
