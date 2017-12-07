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
import hashlib
import copy
from enum import Enum
import csv
import uuid


class DiGraph(object):
    """
    Reimplementation of Networkx DiGraph's
    We only use the DiGraph structure which is very light.
    We do not need the rest of the library.
    This is done for the sake of performance and self containment.
    """

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
        return {target: self.node[target] for target in self.__successors__[source]}

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
        # if (source, target) not in self.__edges__:
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
        # self.__edges__.remove(edge)
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


class Concept(dict):
    """
    extends dictionary to add two properties
    this is easier when accesing intent and extent
    """
    EMARK = '0'
    IMARK = '1'

    @property
    def extent(self):
        """
        access extent
        """
        return self[self.EMARK]

    @property
    def intent(self):
        """
        access intent
        """
        return self[self.IMARK]


class POSET(DiGraph):
    """
    Implements a POSET useful for CBO
    A more relaxed implementation of the lattice
    """
    EXTENT_MARK = 'ex'
    INTENT_MARK = 'in'

    def __init__(self, transformer=None):
        super(POSET, self).__init__()
        self.infimum = 0
        self.supremum = -1
        Concept.EMARK = self.EXTENT_MARK
        Concept.IMARK = self.INTENT_MARK

        self.concept = self.node
        self._transformer = transformer

    def __getitem__(self, key):
        """
        Accesor to the lattice, access directly to the concept collection
        """
        return self.concept[key]

    def new_concept(self, concept_id, concept_data):
        """
        Adds a new concept to the lattice
        Wraps add_node
        """
        self.add_node(concept_id, Concept(concept_data))

    def new_formal_concept(self, extent, intent, concept_id=None):
        """
        Adds a new concept to the lattice
        Wraps add_node
        """
        if concept_id is None:
            concept_id = len(self.node)

        self.add_node(concept_id, Concept({
            self.EXTENT_MARK: extent,
            self.INTENT_MARK: intent
        }))
        return concept_id

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

    def as_dict(self, indices=False):
        """
        Returns a dict serializable version of the lattice
        latice: Lattice to serialize
        g_map: Maps objects' indices to labels
        m_map: Maps attributes' indices to labels
        """
        if indices or self._transformer is None:
            object_translator = lambda x: x
            attribute_translator = lambda x: x
        else:
            object_translator = self._transformer.real_objects
            attribute_translator = self._transformer.real_attributes

        concepts = {}
        ema = self.EXTENT_MARK
        ima = self.INTENT_MARK

        for concept in self.concepts():
            concept_data = {
                ema: object_translator(concept[1][ema]),
                ima: attribute_translator(concept[1][ima]),
                'sup': sorted(self.successors(concept[0])),
                'sub': sorted(self.predecessors(concept[0]))
            }
            concepts[concept[0]] = concept_data
        return concepts

class OnDiskPOSET(POSET):
    def __init__(self, transformer=None, **kwargs):
        super(OnDiskPOSET, self).__init__(transformer)
        self.output_path = kwargs.get('output_path', None)

        if self.output_path is None:
            self.output_path = "./"
        elif not self.output_path.endswith('/'):
            self.output_path += "/"

        self.output_fname = kwargs.get('output_fname', None)
        if self.output_fname is None:
            self.output_fname = "{}.csv".format(str(uuid.uuid4()))
        self.path = self.output_path+self.output_fname
        self.fout = open(self.path, 'w')

        self.writer = csv.writer(
            self.fout,
            delimiter='\t',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL
        )
        self.write_support = kwargs.get('write_support', True)
        self.write_extent = kwargs.get('write_extent', True)
        self.write_intent = kwargs.get('write_intent', True)

        # WRITE HEADERS
        if kwargs.get('write_headers', True):
            row = ['ID']
            if self.write_support:
                row.append("SUPPORT")
            if self.write_extent:
                row.append("EXTENT")
            if self.write_intent:
                row.append("INTENT")
            self.writer.writerow(row)

        if kwargs.get('indices', False) or self._transformer is None:
            
            self.object_translator = lambda x: x
            self.attribute_translator = lambda x: x
        else:
            self.object_translator = self._transformer.real_objects
            self.attribute_translator = self._transformer.real_attributes
        

    def new_formal_concept(self, extent, intent, concept_id=None):
        """
        Adds a new concept to the lattice
        Wraps add_node
        """
        if concept_id is None:
            concept_id = len(self.node)
        row = [concept_id]
        if self.write_support:
            row.append(len(extent))
        if self.write_extent:
            row.append(self.object_translator(extent))
        if self.write_intent:
            row.append(self.attribute_translator(intent))

        self.writer.writerow(row)
        # self.fout.flush()
        self.add_node(concept_id, Concept({
            self.EXTENT_MARK: len(extent),
            self.INTENT_MARK: None
        }))
        return concept_id
    def upper_neighbors(self, concept_id):
        raise NotImplementedError
    def lower_neighbors(self, concept_id):
        raise NotImplementedError
    def as_dict(self, indices=False):
        raise NotImplementedError
    def close(self):
        """
        Close output file and returns the path
        return str output_path
        """
        self.fout.close()
        return self.path
    


class ConceptLattice(POSET):
    """
    Wrapper for the DiGraph
    Adds some semantically sensitive methdos that wraps graph methods.
    Also adds functionality that belongs to a concept lattice rather than
    to a generic direcgted graph.
    """

    def new_concept(self, concept_id, concept_data):
        """
        Adds a new concept to the lattice
        Wraps add_node
        """
        super(ConceptLattice, self).new_concept(concept_id, concept_data)
        self.concept[concept_id]['not_visited'] = True

    def new_formal_concept(self, extent, intent, concept_id=None):
        """
        Adds a new concept to the lattice
        Wraps add_node
        """
        cid = super(ConceptLattice, self).new_formal_concept(
            extent, intent, concept_id)
        self.concept[cid]['not_visited'] = True
        return cid

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

################
"""
    Abstract class
"""
class Intent(object):
    """
    Shell Intent or Static Intent, it provides a shell for the 
    intent behavior, while the descriptions is stored somewhere else
    This avoids creating one object per actual intent
    However, this may require to make the description somehow more complex
    than it is now
    """
    _bottom = None
    _top = None
    TYPES = Enum("TYPES", "MIDDLE BOTTOM TOP")

    @classmethod
    def fix_desc(cls, desc):
        return desc

    @classmethod
    def to_string(cls, desc):
        """
        Returns a suitable representation
        If not, returns the actual representation
        """
        return str("{}({})".format(cls, desc))

    @classmethod
    def hash(cls, desc):
        """
        Hash pattern to index them
        """
        if desc == cls._bottom:
            return id(cls._bottom)
        if desc == cls._top:
            return id(cls._top)
        return hashlib.sha224(str(desc).encode('utf8')).hexdigest()

    @classmethod
    def copy(cls, desc):
        """
        Returns a copy of self
        """
        return copy.copy(desc)

    @classmethod
    def reset(cls):
        """
        PATTERNS HAVE SINGLETONS THAT NEED TO BE RESETED
        WHEN REUSING THEM, WHENEVER YOU CALCULATE PATTERN STRUCTURES
        MULTIPLE TIMES, YOU NEED TO RESET THEM BEFORE RE-USING
        THEM, NOT DOING THIS MAY LEAD TO INCONSISTENCIES
        """
        cls._top = None
        cls._bottom = None

    # IMPLEMENTATIONS: THESE NEXT METHODS SHOULD BE IMPLEMENTED BY ANY NEW REPRESENTATION
    @classmethod
    def bottom(cls, bot_rep=None):
        """
        returns the bottom of the intent representation.
        It may not exists in certain spaces.
        Returns Intent type
        """
        raise NotImplementedError

    @classmethod
    def top(cls, top_rep=None):
        """
        returns the top of the intent representation.
        It may not exists in certain spaces.
        Returns Intent type
        """
        raise NotImplementedError

    @classmethod
    def get_iterator(cls, desc):
        """
        Implements iterable over the description
        """
        raise NotImplementedError

    @classmethod
    def union(cls, desc1, desc2):
        """
        Returns the union of two representations
        Be aware that the union of two closed representations is not closed!
        This method should not care about closing the new representation

        For the case of sets, this is actually set union
        Returns a new united intent
        """
        raise NotImplementedError

    @classmethod
    def intersection(cls, desc1, desc2):
        """
        Intersects two intent representations
        For the case of sets, this is actually set intersection
        Returns a new intersected intent
        """
        raise NotImplementedError

    @classmethod
    def join(cls, desc1, desc2):
        """
        Joins two representations from the perspective of the lattice
        For the case of sets, this is actually set union
        Instead of returning a new intent, this modifies this intent
        by joining it with the other
        The other should remain unchanged
        """
        raise NotImplementedError

    @classmethod
    def meet(cls, desc1, desc2):
        """
        Meets two representations from the perspective of the lattice
        For the case of sets, this is actually set intersection
        Instead of returning a new intent, this modifies this intent
        by joining it with the other
        The other should remain unchanged
        """
        raise NotImplementedError

    @classmethod
    def is_empty(cls, desc):
        """
        Tests the notion of empty representation
        In the case of sets, this is if the cardinality is zero
        """
        raise NotImplementedError

    @classmethod
    def is_equal(cls, desc1, desc2):
        """
        Implements the == operator
        """
        raise NotImplementedError

    @classmethod
    def leq(cls, desc1, desc2):
        """
        Implements the < operator
        """
        raise NotImplementedError

    @classmethod
    def length(cls, desc):
        """
        Implements the len operator
        """
        raise NotImplementedError

    @classmethod
    def contains(cls, desc, key):
        """
        Implements "in" operator
        """
        raise NotImplementedError


class SetPattern(Intent):
    """
    Implements the shell set intent representation
    This is, standard FCA
    """
    _bottom = None
    _top = None

    @classmethod
    def bottom(cls, bot_rep=None):
        if cls._bottom is None:
            cls._bottom = frozenset([])
        return cls._bottom

    @classmethod
    def top(cls, top_rep=None):
        if cls._top is None:
            cls._top = set([])
        if top_rep is not None:
            cls._top.update(top_rep)
        return cls._top

    @classmethod
    def to_string(cls, desc):
        return str(sorted(desc))
    # IMPLEMENTATIONS

    @classmethod
    def union(cls, desc1, desc2):
        return desc1.union(desc2)

    @classmethod
    def intersection(cls, desc1, desc2):
        return desc1.intersection(desc2)

    @classmethod
    def leq(cls, desc1, desc2):
        return desc1.issubset(desc2)

    @classmethod
    def meet(cls, desc1, desc2):
        desc1 = desc1.intersection(desc2)

    @classmethod
    def join(cls, desc1, desc2):
        desc1.update(desc2)


    @classmethod
    def is_empty(cls, desc):
        return len(desc) == 0

    @classmethod
    def is_equal(cls, desc1, desc2):
        return desc1 == desc2

    @classmethod
    def length(cls, desc):
        return len(desc)

    @classmethod
    def contains(cls, desc, key):
        return key in desc

    @classmethod
    def get_iterator(cls, desc):
        for i in sorted(desc):
            yield i
