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
from fca.io.input_models import FormalContextModel
from fca.algorithms.canonical_base import EnhancedDG


def exec_ex15(filepath):
    """
    Example 15 - Obtains the Duquenne-Guigues Canonical Base
    of Implications Rules using the improved algorithm 17
    in chapter 3 of Conceptual Exploration
    """
    canonical_base = EnhancedDG(
<<<<<<< HEAD:examples/algorithms_canonicalbase/ex15_duquenneguigues_enhanced.py
        FormalContextModel(
            filepath=filepath
        ),
        lazy=False,
        silent=False
=======
        FormalContextManager(filepath=filepath), lazy=False, silent=False
>>>>>>> Fixed problems with previous closure canonical test:examples/algorithms_canonicalbase/ex15_duquenneguigues_enhanced.py
    )
    
    for rule, support in canonical_base.get_implications():
        ant, con = rule
        print('{:>10s} => {:10s}'.format(lst2str(ant),lst2str(con)), support)


if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(description="""
    Example 15 - Obtains the Duquenne-Guigues Canonical Base
    of Implications Rules using the improved algorithm 17
    in chapter 3 of Conceptual Exploration
    """)
    __parser__.add_argument('context_path', metavar='context_path', type=str,
                            help='path to the formal context in txt, space separated values, one object representation per line')
    __args__ = __parser__.parse_args()
    exec_ex15(__args__.context_path)
