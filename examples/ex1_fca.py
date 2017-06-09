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
from fca.algorithms.addIntent import AddIntent
from fca.reader import read_representations


def exec_ex1(filepath):
    """
    In this example we mine formal concepts in a single line
    """
    print (AddIntent(read_representations(filepath), lazy=False, silent=False).lat.as_dict())

if __name__ == "__main__":
    exec_ex1(sys.argv[1])
