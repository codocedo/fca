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
from fca.algorithms.next_closure import NextClosure
<<<<<<< HEAD
from fca.io.input_models import FormalContextModel

def exec_ex17(filepath, min_sup=0, output_fname=None):
=======
from fca.reader import FormalContextManager

def exec_ex17(filepath, min_sup=0, output_path=None):
>>>>>>> Fixed problems with previous closure canonical test
    """
    Example 17: NextClosure OnDisk - Streaming patterns to disk
    """
    ondisk_poset = NextClosure(
<<<<<<< HEAD
        FormalContextModel(
            filepath=filepath
        ),
        min_sup=min_sup,
        ondisk=True,
        ondisk_kwargs={
            'output_path':'/tmp',
            'output_fname':output_fname
=======
        FormalContextManager(
            filepath=filepath
        ),
        min_sup=min_sup,
        ondisk = True,
        ondisk_kwargs = {
            'output_path':output_path
>>>>>>> Fixed problems with previous closure canonical test
        },
        silent=False
    ).poset
    output_path = ondisk_poset.close()
    print ("\t=> Results stored in {}".format(output_path))


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(
        description='Example 17: NextClosure OnDisk - Streaming patterns to disk'
    )
    __parser__.add_argument(
        'context_path',
        metavar='context_path',
        type=str,
        help='path to the formal context'
    )
    __parser__.add_argument(
        '-o',
<<<<<<< HEAD
        '--output_fname',
        metavar='output_fname',
=======
        '--output_path',
        metavar='output_path',
>>>>>>> Fixed problems with previous closure canonical test
        type=str,
        help='Output file to save formal concepts',
        default=None
    )
    __parser__.add_argument(
        '-m',
        '--min_sup',
        metavar='min_sup',
        type=float,
        help='Relative minimum support [0,1]',
        default=0.0
    )

    __args__ = __parser__.parse_args()
<<<<<<< HEAD
    exec_ex17(__args__.context_path, __args__.min_sup, __args__.output_fname)
=======
    exec_ex17(__args__.context_path, __args__.min_sup, __args__.output_path)
# okay decompiling ex5_cbo.pyc
>>>>>>> Fixed problems with previous closure canonical test
