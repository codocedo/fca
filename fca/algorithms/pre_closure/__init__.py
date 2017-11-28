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

class PreClosure(object):
    """
    Calculates Pre-closure as explained in "Conceptual Exploration"
    Chapter 3. The canonical basis
    """
    def __init__(self):
        """
        Starts with an empty implication base
        Implications are to be stored as pairs of sets
        """
        self.imp_base = []
        self.supports = []
        self.translate = lambda s: s

    def register_implication(self, ant, con, support):
        """
        Adds a new implication to the database
        ant => con
        """
        # print "\t\tRegistering {}=>{}".format(self.translate(ant), self.translate(con))
        self.imp_base.append((ant, con))
        self.supports.append(support)
    
    def get_implication_base(self):
        """
        Returns the base of implications
        (ant, con), support
        """
        for implication, support in zip(self.imp_base, self.supports):
            yield implication, support

    def preclose_pattern(self, pattern):
        """
        Calculates pre-closure of pattern
        """
        old_len = -1
        while old_len != len(pattern):
            old_len = len(pattern)
            for ant, con in self.imp_base:
                if ant <= pattern and len(ant) != len(pattern):
                    pattern.update(con)
        return pattern