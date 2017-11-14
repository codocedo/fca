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
import argparse
import re
from fca.algorithms.addIntent import AddIntent
from fca.defs.patterns import IcebergSetPattern
from fca.reader import read_representations

def dict_printer(poset):
    """
    Nicely print the concepts in the poset
    """
    order = lambda s: (
     len(s[1][poset.EXTENT_MARK]), s[1][poset.EXTENT_MARK])
    for concept_id, concept in sorted(poset.as_dict().items(), key=order):
        if concept_id >= -2:
            print '{} {} {}'.format('', concept[poset.EXTENT_MARK], concept[poset.INTENT_MARK])


def read_int_input(msg):
    """
    Returns an int from user interface
    """
    entry = ''
    while re.match('\\d+', entry) is None or int(entry < 0):
        entry = raw_input(msg)

    return int(entry)


def exec_ex2(filepath, min_sup):
    """
    Notice that we have imported a different kind of pattern
    IcebergSetPattern allows setting a min sup value
    """
    IcebergSetPattern.MIN_SUP = min_sup
    lattice = AddIntent(read_representations(filepath, transposed=True), pattern=IcebergSetPattern, lazy=False, silent=False).lat
    dict_printer(lattice)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description='Example 2 - IcebergSetPattern with AddIntent')
    __parser__.add_argument('context_path', metavar='context_path', type=str, help='path to the formal context')
    __parser__.add_argument('-m', '--min_sup', metavar='min_sup', type=float, help='Absolute Minimum Support [0, inf]', default=0.0)
    __args__ = __parser__.parse_args()
    exec_ex2(__args__.context_path, __args__.min_sup)
# okay decompiling ex2_fc.pyc
