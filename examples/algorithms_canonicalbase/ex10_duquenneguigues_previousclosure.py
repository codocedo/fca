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
import argparse
from fca.reader import FormalContextManager
from fca.algorithms import lst2str
from fca.algorithms.canonical_base import CanonicalBase

def exec_ex10(filepath, min_sup=0):
    """
    Example 10 - Obtains the Duquenne-Guigues Canonical Base
    of Implications Rules with NextClosure
    """
    
    canonical_base = CanonicalBase(FormalContextManager(filepath=filepath), min_sup=min_sup, lazy=False, silent=False)
    for rule, support in canonical_base.get_implications():
        ant, con = rule
        print('{:>10s} => {:10s}'.format(lst2str(ant),lst2str(con)), support)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 10 - Obtains the Duquenne-Guigues Canonical Base\n                       of Implications Rules with NextClosure\n                    ')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context in txt, space separated values, one object representation per line')
    __parser__.add_argument('-m', '--min_sup', metavar='min_sup', type=float, help='Relative minimum support [0,1]', default=0.0)
    __args__ = __parser__.parse_args()
    exec_ex10(__args__.context_path, __args__.min_sup)
# okay decompiling ex10_dg_imp_base_nc.pyc
