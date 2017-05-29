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

class DiGraph(object):
    """
    Reimplementation of Networkx DiGraph's
    We only use the DiGraph structure which is very light.
    We do not need the rest of the library.
    This is done for the sake of performance and self containment.
    """
    EXTENT_MARK = 'ex'
    INTENT_MARK = 'in'
    def __init__(self):
        """
        Reimplementation of Networkx DiGraph's
        """
        self.__nodes__ = []
        self.node = {}
        #self.__edges__ = []
        self.__edges_data__ = {}
        self.__successors__ = {}
        self.__predecessors__ = {}


    def __getitem__(self, source):
        """
        Overwrites the [] operator. Returns a dict of successors' data given a source
        """
        return {target:self.node[target] for target in self.__successors__[source]}

    def add_node(self, node, params=False):
        """
        Adds a node to the graph
        node: id of the node to add, consider that it should be unique
        params = dict of node data

        ex.
        graph = DiGraph()
        graph.add_node(1, {'name': 'Victor'})
        """
        if node not in self.__nodes__:
            self.__nodes__.append(node)
        if isinstance(params, dict):
            self.node[node] = params

    def nodes(self, data=False):
        """
        Access the set of nodes, returns a list of node ids. if data==True then
        returns a list of pairs where the second element is the dictionary of data
        associated to the node.
        data: Boolean

        ex.abs
        graph.nodes(1, data=True)
        (1, {'name': Victor})
        """
        if data:
            return self.node.items()
        else:
            return self.__nodes__

    def add_edge(self, source, target, params=False):
        """
        Adds an edge to the graph.
        Params is the data to associate with the edge.abs
        ex.
        graph = DiGraph()
        graph.add_edge(1, 2, {'weight': 100})
        """
        self.add_node(source)
        self.add_node(target)
        #if (source, target) not in self.__edges__:
            #self.__edges__.append((source, target))
        self.__successors__.setdefault(source, set([])).add(target)
        self.__predecessors__.setdefault(target, set([])).add(source)
        if isinstance(params, dict):
            self.__edges_data__[(source, target)] = params

    def remove_edge(self, source, target):
        """
        Removes an edge from the graph.

        """

        edge = (source, target)
        if edge in self.__edges_data__:
            del self.__edges_data__[edge]
        #self.__edges__.remove(edge)
        self.__successors__[source].remove(target)
        self.__predecessors__[target].remove(source)

    def edges(self, data=False):
        """
        Access the list of edges.
        If data==True then returns a list of pairs.

        ex.
        graph.edges(data=True)
        [((1, 2), {'weight': 100}))]
        """
        if data:
            return self.__edges_data__.items()
        else:
            return self.__edges_data__.keys()

    def successors(self, node):
        """
        Returns the set of successors nodes given a node
        """
        return self.__successors__.get(node, set([]))
    def predecessors(self, node):
        """
        Returns the set of predecessors nodes given a node
        """
        return self.__predecessors__.get(node, set([]))

    def neighbors(self, node):
        """
        Returns the set of successors nodes given a node
        """
        return self.successors(node)


class ConceptLattice(DiGraph):
    """
    Wrapper for the DiGraph
    Adds some semantically sensitive methdos that wraps graph methods.
    Also adds functionality that belongs to a concept lattice rather than
    to a generic direcgted graph.
    """
    def __init__(self):
        super(ConceptLattice, self).__init__()
        self.infimum = -1
        self.supremum = -2
        self.concept = self.node

    def new_concept(self, concept_id, concept_data):
        """
        Adds a new concept to the lattice
        Wraps add_node
        """
        concept_data['not_visited'] = True
        self.add_node(concept_id, concept_data)

    def upper_neighbors(self, concept_id):
        """
        Obtain a list of upper neighbors indices
        Wraps self.successors
        concept_id: concept to obtain upper neighbors from
        """
        return self.successors(concept_id)

    def lower_neighbors(self, concept_id):
        """
        Obtain a list of upper neighbors indices
        Wraps self.predecessors
        concept_id: concept to obtain upepr neighbors from
        """
        return self.predecessors(concept_id)

    def concepts(self):
        """
        Obtains a list of pairs with the concept index and the concept data
        Wraps nodes(data=True)
        """
        return self.nodes(data=True)

    def reset_parcour(self):
        """
        Resets the visited flags from the graph
        """
        for concept in self.concept:
            self.concept[concept]['not_visited'] = True

    def visit(self, concept_id):
        """
        Mark the concept as visited for future references
        concept_id: index of the concept to mark as visited
        """
        self.concept[concept_id]['not_visited'] = False

    def is_visited(self, concept_id):
        """
        Check if the concept has been already visited in the current parcour
        concept_id: index of the concept to check
        """
        return not self.concept[concept_id]['not_visited']

    def as_dict(self, g_map=False, m_map=False):
        """
        Returns a dict serializable version of the lattice
        latice: Lattice to serialize
        g_map: Maps objects' indices to labels
        m_map: Maps attributes' indices to labels
        """
        g_map = g_map if g_map else {}
        m_map = m_map if m_map else {}
        concepts = {}
        for concept in self.concepts():
            concept_data = {
                self.EXTENT_MARK: [g_map.get(i, i) for i in concept[1][self.EXTENT_MARK]],
                self.INTENT_MARK: [m_map.get(i, i) for i in concept[1][self.INTENT_MARK].repr()],
                'sup': self.successors(concept[0]),
                'sub': self.predecessors(concept[0])
                }
            concepts[concept[0]] = concept_data
        return concepts


"""
    Abstract class
"""
class Intent(object):
    """
    Abstract class for a formal concept intent
    """
    def __init__(self, desc):
        self.__map__ = {}
        self.desc = desc
        self.__type__ = 0 # 1: top, -1: bottom, 0: non-top-bottom concepts

    def repr(self):
        """
        Returns a suitable representation
        If not, returns the actual representation
        """
        return self.desc
    @classmethod
    def bottom(cls):
        """
        returns the bottom of the intent representation.
        It may not exists in certain spaces.
        Returns Intent type
        """
        raise NotImplementedError
    @classmethod
    def top(cls):
        """
        returns the top of the intent representation.
        It may not exists in certain spaces.
        Returns Intent type
        """
        raise NotImplementedError

    def set_map(self, representation_map):
        """
        Sets a dictionary map to output the description
        TODO: Maybe this should not be here
        """
        self.__map__ = representation_map
    def __str__(self):
        """
        Returns a string representation of the intent
        """
        return self.__i_str__()
    def __le__(self, other):
        """
        overrides the < operator
        Tests if this intent is subsumed by another
        In the case of sets, tests if this intent is a subset of the other
        """
        return self.__i_le__(other)

    def __eq__(self, other):
        """
        overrrides the == operator
        Tests if this intent is the same as another
        """
        return self.__i_eq__(other)

    # IMPLEMENTATIONS: THESE NEXT METHODS SHOULD BE IMPLEMENTED BY ANY NEW REPRESENTATION
    def intersection(self, other):
        """
        Intersects two intent representations
        For the case of sets, this is actually set intersection
        Returns a new intersected intent
        """
        raise NotImplementedError
    def join(self, other):
        """
        Joins two representations from the perspective of the lattice
        For the case of sets, this is actually set union
        Instead of returning a new intent, this modifies this intent
        by joining it with the other
        The other should remain unchanged
        """
        raise NotImplementedError
    def is_empty(self):
        """
        Tests the notion of empty representation
        In the case of sets, this is if the cardinality is zero
        """
        raise NotImplementedError
    def __i_str__(self):
        """
        Implements the string representation
        """
        raise NotImplementedError
    def __i_eq__(self, other):
        """
        Implements the == operator
        """
        raise NotImplementedError
    def __i_le__(self, other):
        """
        Implements the < operator
        """
        raise NotImplementedError



"""
    Set pattern, classic FCA
"""
class SetPattern(Intent):
    """
    Implements the set intent representation
    This is, standard FCA
    """
    @classmethod
    def bottom(cls):
        return cls(set([]))
    @classmethod
    def top(cls):
        return cls(set([]))
    def repr(self):
        return [self.__map__.get(i, i) for i in self.desc]
    # IMPLEMENTATIONS
    def intersection(self, other):
        return SetPattern(self.desc.intersection(other.desc))
    def join(self, other):
        self.desc = self.desc.union(other.desc)
    def is_empty(self):
        return len(self.desc) == 0
    def __i_str__(self):
        return str(self.repr())
    def __i_eq__(self, other):
        return self.desc == other.desc
    def __i_le__(self, other):
        return self.desc.issubset(other.desc)
