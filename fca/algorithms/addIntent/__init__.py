
import copy
import sys
import os
from fca.defs import ConceptLattice, Intent

# These marks are used to represent extent and intent in dicts
__extent_mark__ = 'ex'
__intent_mark__ = 'in'

def to_bottom(lattice, atts):
    """
    Adds a set of attributes to the infimum of the lattice
    lattice: ConceptLattice(DiGraph)
    atts: list of attributes
    """
    lattice.concept[lattice.infimum][__intent_mark__].update(atts)


def read_lattice_as_dict(lattice, g_map=False, m_map=False):
    """
    Returns a dict serializable version of the lattice
    latice: Lattice to serialize
    g_map: Maps objects' indices to labels
    m_map: Maps attributes' indices to labels
    """
    g_map = g_map if g_map else {}
    m_map = m_map if m_map else {}
    concepts = {}
    for concept in lattice.concepts():
        concept_data = {}
        #c['id']=n[0]
        concept_data[__extent_mark__] = [g_map.get(i, i) for i in concept[1][__extent_mark__]]
        concept_data[__intent_mark__] = [m_map.get(i, i) for i in concept[1][__intent_mark__].repr()]
        concept_data['sup'] = lattice.successors(concept[0])
        concept_data['sub'] = lattice.predecessors(concept[0])
        concepts[concept[0]] = concept_data
    return concepts

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
    lattice.concept[concept][__extent_mark__].append(obj)

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
        if lattice.concept[super_concept][__intent_mark__] == intent:
            return super_concept
        # THE MOST COMMON CASE
        elif intent <= lattice.concept[super_concept][__intent_mark__]:
            return get_maximal_concept(lattice, intent, super_concept)
    return current_concept

def add_intent_iteration(lattice, intent, generator, depth=1):
    """
    A single add_intent iteration
    lattice: ConceptLattice(DiGraph)
    intent: intent to add
    generator: current concept
    depth: internal
    """

    generator = get_maximal_concept(lattice, intent, lattice.infimum)

    if generator != lattice.infimum and lattice.concept[generator][__intent_mark__] == intent:
        return generator

    new_parents = []
    for candidate in lattice.upper_neighbors(generator):
        if not lattice.concept[candidate][__intent_mark__] <= intent:
            cand_inter = lattice.concept[candidate][__intent_mark__].intersection(intent)
            candidate = add_intent_iteration(lattice, cand_inter, candidate, depth+1)

        add_parent = True
        for parent in new_parents:
            if lattice.concept[candidate][__intent_mark__] <= lattice.concept[parent][__intent_mark__]:
                add_parent = False
                break
            elif lattice.concept[parent][__intent_mark__] <= lattice.concept[candidate][__intent_mark__]:
                del new_parents[new_parents.index(parent)]
        if add_parent:
            new_parents.append(candidate)

    new_id = len(lattice.concepts()) - 2

    concept_data = {__extent_mark__:copy.copy(lattice.concept[generator][__extent_mark__]),
                    __intent_mark__:intent
                   }

    lattice.new_concept(new_id, concept_data)

    for parent in new_parents:
        if parent in lattice[generator]:
            lattice.remove_edge(generator, parent)

        lattice.add_edge(new_id, parent)

    lattice.add_edge(generator, new_id)
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

def add_intent(representations, pattern=Intent, silent=True):
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
    lattice.new_concept(lattice.infimum, {__intent_mark__:pattern.top(), __extent_mark__:[]})
    # Supremum
    lattice.new_concept(lattice.supremum, {__intent_mark__:pattern.bottom(), __extent_mark__:[]})

    # Create the simplest lattice
    lattice.add_edge(lattice.infimum, lattice.supremum)



    for obj, intent in enumerate(representations):
        if not silent:
            print('\r -> EXECUTING OBJECT:{}'.format(obj)),

        sys.stdout.flush()
        intent = pattern(intent, dirty=True)
        lattice.node[lattice.infimum][__intent_mark__].join(intent)

        #to_bottom(g,intent)
        aid = add_intent_iteration(lattice, intent, lattice.infimum)
        add_object(lattice, aid, obj)
        lattice.reset_parcour()
        
    print ('')
    print('{} concepts found'.format(len(lattice.nodes())))
    if silent:
        talk(oloss)
    return lattice
