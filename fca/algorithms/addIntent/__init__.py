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

import copy
import sys
import os
from fca.defs import ConceptLattice, SetPattern
from fca.reader import PARSERS

# These marks are used to represent extent and intent in dicts
def to_bottom(lattice, atts):
    """
    Adds a set of attributes to the infimum of the lattice
    lattice: ConceptLattice(DiGraph)
    atts: list of attributes
    """
    lattice.concept[lattice.infimum][lattice.INTENT_MARK].update(atts)


def add_object(lattice, concept, obj, depth=1):
    """
    Adds an object to the extent of a formal concept in the lattice and to
    the concepts of its entire super-lattice.
    lattice: ConceptLattice(DiGraph)
    concept: concept to add the object to
    object: object to add - integer
    depth: internal
    """
    if lattice.is_visited(concept):
        return 0

    lattice.visit(concept)
    lattice.concept[concept][lattice.EXTENT_MARK].append(obj)

    for j in lattice.upper_neighbors(concept):
        add_object(lattice, j, obj, depth+1)



def get_maximal_concept(lattice, intent, current_concept):
    """
    Given an intent, we explore the lattice and obtain the unique formal concept
    the intent of which subsumes the intent. We call this the maximal concept.

    """
    # If the given intent is empty (or is the bottom intent),
    # the maximal concept in the lattice is the supremum
    if intent.is_empty():
        return lattice.supremum
    for super_concept in lattice.upper_neighbors(current_concept):
        # THE CONCEPT ALREADY EXISTS. RETURN THE NODE ID OF THAT CONCEPT
        if lattice.concept[super_concept][lattice.INTENT_MARK] == intent:
            return super_concept
        # THE MOST COMMON CASE
        elif intent <= lattice.concept[super_concept][lattice.INTENT_MARK]:
            return get_maximal_concept(lattice, intent, super_concept)
    return current_concept

def add_intent_iteration(lat, intent, generator, depth=1):
    """
    A single add_intent iteration
    lat: ConceptLattice(DiGraph)
    intent: intent to add
    generator: current concept
    depth: internal
    """

    generator = get_maximal_concept(lat, intent, lat.infimum)

    if generator != lat.infimum and lat.concept[generator][lat.INTENT_MARK] == intent:
        return generator

    new_parents = []
    for candidate in lat.upper_neighbors(generator):
        if not lat.concept[candidate][lat.INTENT_MARK] <= intent:
            cand_inter = lat.concept[candidate][lat.INTENT_MARK].intersection(intent)
            candidate = add_intent_iteration(lat, cand_inter, candidate, depth+1)

        add_parent = True
        for parent in new_parents:
            if lat.concept[candidate][lat.INTENT_MARK] <= lat.concept[parent][lat.INTENT_MARK]:
                add_parent = False
                break
            elif lat.concept[parent][lat.INTENT_MARK] <= lat.concept[candidate][lat.INTENT_MARK]:
                del new_parents[new_parents.index(parent)]
        if add_parent:
            new_parents.append(candidate)

    new_id = len(lat.concepts()) - 2

    concept_data = {lat.EXTENT_MARK:copy.copy(lat.concept[generator][lat.EXTENT_MARK]),
                    lat.INTENT_MARK:intent
                   }

    lat.new_concept(new_id, concept_data)

    for parent in new_parents:
        if parent in lat[generator]:
            lat.remove_edge(generator, parent)

        lat.add_edge(new_id, parent)

    lat.add_edge(generator, new_id)
    return new_id


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

def add_intent(representations, pattern=SetPattern, repr_parser=PARSERS['SSV'], silent=True):
    """
    Executes Add Intent algorithm over a set of representations.
    Representations should be presented in a suitable format to the provided type of pattern.
    For example, Patter=SetIntent receives a string of space separated attributes per object.
    representations: iterable of representations
    Pattern: type of pattern to use (SetIntent, IntervalPattern, etc.)
    """
    if silent:
        oloss=silence()
    print('*' * 100)
    print('SePyrot - AddIntent for Python - KY')
    print('*' * 100)
    
    lattice = ConceptLattice()
    # Infimum
    lattice.new_concept(lattice.infimum, {lattice.INTENT_MARK:pattern.top(), lattice.EXTENT_MARK:[]})
    # Supremum
    lattice.new_concept(lattice.supremum, {lattice.INTENT_MARK:pattern.bottom(), lattice.EXTENT_MARK:[]})

    # Create the simplest lattice
    lattice.add_edge(lattice.infimum, lattice.supremum)



    for obj, intent in enumerate(representations):
        if not silent:
            print('\r -> EXECUTING OBJECT:{}'.format(obj)),

        sys.stdout.flush()
        intent = pattern(repr_parser(intent))
        lattice.node[lattice.infimum][lattice.INTENT_MARK].join(intent)

        #to_bottom(g,intent)
        aid = add_intent_iteration(lattice, intent, lattice.infimum)
        add_object(lattice, aid, obj)
        lattice.reset_parcour()
        
    print ('')
    print('{} concepts found'.format(len(lattice.nodes())))
    if silent:
        talk(oloss)
    return lattice
