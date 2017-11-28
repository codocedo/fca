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

lst2str = lambda lst: reduce(lambda x, y: str(x)+', '+str(y), lst+['']) if len(lst) > 0 else "[]"

def lexo(set_a, set_b):
    """
    LEXICAL COMPARISON BETWEEN TWO SETS OF INTEGERS
    """
    return tuple(sorted(set_a)) <= tuple(sorted(set_b))


def dict_printer(poset, transposed=False, indices=False):
    """
    Nicely print the concepts in the poset
    """
    ema = poset.EXTENT_MARK
    ima = poset.INTENT_MARK
    if transposed:
        ema = poset.INTENT_MARK
        ima = poset.EXTENT_MARK

    order = lambda s: (
        len(s[1][ema]), s[1][ima]
    )

    for i, (concept_id, concept) in enumerate(sorted(poset.as_dict(indices).items(), key=order)):
        print '{}\t{}\t\t{}'.format(
            i+1,
            lst2str(concept[ema]),
            lst2str(concept[ima])
        )


class Algorithm(object):
    """
    Abstract class for algorithm.
    Implemented by AddIntent and PSCbO
    """
    def __init__(self, lazy=True, **params):
        """
        if not lazy it should run the algorithm as soon as this class
        is instantiated
        """
        if not lazy:
            self.run()

    def config(self):
        """
        Configs the main parameters of the algorithm
        """
        raise NotImplementedError

    def run(self, *args, **kwargs):
        """
        Executes the algorithm
        """
        raise NotImplementedError
