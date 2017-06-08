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
import copy
import sys
import os
from fca.defs import ConceptLattice, SetPattern
from fca.reader import PARSERS
from fca.algorithms import Algorithm

def silence():
    """
    Makes printing unavailable
    """
    old_stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    return old_stdout

def talk(old_stdout):
    """
    Makes printing available
    """
    sys.stdout = old_stdout

class AddIntent(Algorithm):
    """
    AddIntent algorithm executer
    """
    def __init__(self, input_manager, pattern=SetPattern, **params):
        self.ctx = input_manager
        self.lat = ConceptLattice(transformer=self.ctx.transformer)
        self.pattern = pattern
        self.silent = params.get('silent', True)

        self.config()

        super(AddIntent, self).__init__(**params)

    def config(self):
        """
        Configure the algorithm parameters
        """
        # Infimum
        self.lat.new_concept(
            self.lat.infimum,
            {self.lat.INTENT_MARK:self.pattern.top(), self.lat.EXTENT_MARK:[]}
            )
        # Supremum
        self.lat.new_concept(
            self.lat.supremum,
            {self.lat.INTENT_MARK:self.pattern.bottom(), self.lat.EXTENT_MARK:[]}
            )
        # Create the simplest lattice
        self.lat.add_edge(self.lat.infimum, self.lat.supremum)

    def run(self):
        """
        Executes Add Intent algorithm over a set of representations.
        Representations should be presented in a suitable format to the provided type of pattern.
        For example, Patter=SetIntent receives a string of space separated attributes per object.
        representations: iterable of representations
        Pattern: type of pattern to use (SetIntent, IntervalPattern, etc.)
        """
        if self.silent:
            oloss = silence()
        print('*' * 100)
        print('SePyrot - AddIntent for Python - KY')
        print('*' * 100)


        for obj, intent in enumerate(self.ctx.representations):
            print('\r -> EXECUTING OBJECT:{}'.format(obj), end='')
            sys.stdout.flush()
            intent = self.pattern(intent)
            self.lat[self.lat.infimum].intent.join(intent)

            #to_bottom(g,intent)
            aid = self.add_intent_iteration(intent, self.lat.infimum)
            self.add_object(aid, obj)
            self.lat.reset_parcour()

        print ('')
        print('{} concepts found'.format(len(self.lat.nodes())))
        if self.silent:
            talk(oloss)


    # These marks are used to represent extent and intent in dicts
    def to_bottom(self, atts):
        """
        Adds a set of attributes to the infimum of the lattice
        lattice: ConceptLattice(DiGraph)
        atts: list of attributes
        """
        self.lat[self.lat.infimum].intent.update(atts)


    def add_object(self, concept, obj, depth=1):
        """
        Adds an object to the extent of a formal concept in the lattice and to
        the concepts of its entire super-lattice.
        lattice: ConceptLattice(DiGraph)
        concept: concept to add the object to
        object: object to add - integer
        depth: internal
        """
        if self.lat.is_visited(concept):
            return 0

        self.lat.visit(concept)
        self.lat[concept].extent.append(obj)

        for j in self.lat.upper_neighbors(concept):
            self.add_object(j, obj, depth+1)



    def get_maximal_concept(self, intent, current_concept):
        """
        Given an intent, we explore the lattice and obtain the unique formal concept
        the intent of which subsumes the intent. We call this the maximal concept.

        """
        # If the given intent is empty (or is the bottom intent),
        # the maximal concept in the lattice is the supremum
        if intent.is_empty():
            return self.lat.supremum
        for super_concept in self.lat.upper_neighbors(current_concept):
            # THE CONCEPT ALREADY EXISTS. RETURN THE NODE ID OF THAT CONCEPT
            if self.lat[super_concept].intent == intent:
                return super_concept
            # THE MOST COMMON CASE
            elif intent <= self.lat[super_concept].intent:
                return self.get_maximal_concept(intent, super_concept)
        return current_concept

    def add_intent_iteration(self, intent, generator, depth=1):
        """
        A single add_intent iteration
        lat: ConceptLattice(DiGraph)
        intent: intent to add
        generator: current concept
        depth: internal
        """

        generator = self.get_maximal_concept(intent, self.lat.infimum)

        if generator != self.lat.infimum and self.lat[generator].intent == intent:
            return generator

        new_parents = []
        for candidate in self.lat.upper_neighbors(generator):
            if not self.lat[candidate].intent <= intent:
                cand_inter = self.lat[candidate].intent.intersection(intent)
                candidate = self.add_intent_iteration(cand_inter, candidate, depth+1)

            add_parent = True
            for parent in new_parents:
                if self.lat[candidate].intent <= self.lat[parent].intent:
                    add_parent = False
                    break
                elif self.lat[parent].intent <= self.lat[candidate].intent:
                    del new_parents[new_parents.index(parent)]
            if add_parent:
                new_parents.append(candidate)


        new_id = self.lat.new_formal_concept(copy.copy(self.lat[generator].extent), intent)

        for parent in new_parents:
            if parent in self.lat[generator]:
                self.lat.remove_edge(generator, parent)

            self.lat.add_edge(new_id, parent)

        self.lat.add_edge(generator, new_id)
        return new_id



