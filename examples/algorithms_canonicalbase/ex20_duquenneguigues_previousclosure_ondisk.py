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
from fca.algorithms import lst2str
from fca.algorithms.canonical_base import CanonicalBase
from fca.reader import FormalContextManager

def exec_ex20(filepath, min_sup=0, output_fname=None):
    """
    Example 20: Obtains the Duquenne-Guigues Canonical Base OnDisk - Streaming pattern to disk
    """

    canonical_base = CanonicalBase(
        FormalContextManager(filepath=filepath),
        min_sup=min_sup,
        lazy=False,
        silent=True,
        ondisk=True,
        ondisk_kwargs={
            'output_path':'/tmp',
            'output_fname': output_fname,
            'write_support':True,
            'write_extent':False
            }
    )

    output_path = canonical_base.poset.close()

    for rule, support in canonical_base.get_implications():
        ant, con = rule
        print('{:10s} => {:10s}'.format(lst2str(ant), lst2str(con)), support)

    print ("\t=> Pseudo closures stored in {}".format(output_path))

if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(
        description='Example 20: Obtains the Duquenne-Guigues Canonical Base OnDisk - Streaming pattern to disk'
    )
    __parser__.add_argument(
        'context_path',
        metavar='context_path',
        type=str,
        help='path to the formal context'
    )

    __parser__.add_argument(
        '-m',
        '--min_sup',
        metavar='min_sup',
        type=float,
        help='Relative minimum support [0,1]',
        default=0.0
    )

    __parser__.add_argument(
        '-o',
        '--output_fname',
        metavar='output_fname',
        type=str,
        help='Output file to save formal concepts',
        default=None
    )

    __args__ = __parser__.parse_args()
    exec_ex20(__args__.context_path, __args__.min_sup, __args__.output_fname)
