"""
**********************************************************
TRANSFOMERS: Transform list of symbols to representations
suitable for patterns structures
**********************************************************
"""
class Transformer(object):
    """
    Abstract transformer
    Should take the output of FileManager's
    and transform it into a suitable format for
    a pattern
    """
    def __init__(self):
        # OBJECTS AND INDEX (INVERTED MAP)
        self.objects = {}
        self.object_index = {}
        # ATTRIBUTES AND INDEX (INVERTED MAP)
        self.attributes = {}
        self.attribute_index = {}

    def register_object(self, obj):
        """
        Registers object generating an inverted map for recovery
        
        obj: real object
        return object index
        """
        self.object_index[self.objects.setdefault(obj, len(self.objects))] = obj
        return self.objects[obj]

    def register_attribute(self, att):
        """
        Registers attribute generating an inverted map for recovery
        att: real attribute
        return attribute index
        """
        self.attribute_index[self.attributes.setdefault(att, len(self.attributes))] = att
        return self.attributes[att]

    def real_objects(self, args):
        """
        Returns the real objects behind the indexed representation
        args: list of object indices
        return list of objects
        """
        if not bool(args):
            return args
        return sorted([self.object_index.get(i, i) for i in args])

    def real_attributes(self, args):
        """
        Returns the real attributes behind the indexed representation
        args: list of attribute indices
        return list of attributes
        """
        if not bool(args):
            return args
        return sorted([self.attribute_index.get(i, i) for i in args])

    def transform(self, entry):
        """
        transform an entry into a suitable format for a pattern implementation
        entry: list of pairs (obj, lst)
        """
        raise NotImplementedError
    def parse(self, lst):
        """
        parse list in an entry
        lst list of symbols
        """
        raise NotImplementedError
    def g_map(self):
        """
        Returns a map to transform objects symbols back to their
        original representation in the file
        """
        return self.object_index
    def m_map(self):
        """
        Returns a map to transform attributes symbols back to their
        original representation in the file
        """
        return self.attribute_index

class List2SetTransformer(Transformer):
    """
    Transform a list of symbols into a set of integers
    It registers a map to transform intergers back to symbols
    """
    def __init__(self):
        """
        Keepts a map of symbols to integers
        for attributes and objects
        """
        super(List2SetTransformer, self).__init__()
        self.objects = {}
        self.attributes = {}

    def transform(self, entry):
        """
        Transforms entry pair (object representation, list of attribute symbols)
        into a set of integers suitable for SetPattern
        It registers each symbol to the corresponding index
        entry: (object, list)
        """
        self.register_object(entry[0])
        atts = self.parse(entry[1])
        return atts

    def parse(self, lst):
        return set([self.register_attribute(att) for att in lst])

class List2IntervalsTransformer(Transformer):
    """
    Transform a list of symbols into a list of intervals
    of numerical values (int, double or float)
    """
    def __init__(self, data_type=int):
        """
        Configures a data type to cast interval values
        """
        super(List2IntervalsTransformer, self).__init__()
        self.data_type = data_type

    def transform(self, entry):
        """
        entry: (object, list)
        returns [(i, i)]
        """
        self.objects.setdefault(entry[0], len(self.objects))
        return self.parse(entry[1])

    def parse(self, lst):
        interval = []
        for i in lst:
            interval.append((self.data_type(i), self.data_type(i)))
        return interval


class List2PartitionsTransformer(List2IntervalsTransformer):
    """
    Transforms a list of values to a partition containing equivalence classes of indices
    [0,1,0,1,1] -> [set([0,2]), set([1,3,4])]
    """

    def __init__(self, transposed=False):
        """
        Configures a data type to cast interval values
        """
        super(List2PartitionsTransformer, self).__init__(int)
        if transposed:
            self.real_objects = self.real_partition
        else:
            self.real_attributes = self.real_partition

    def real_partition(self, args):
        """
        Outputs the partition the partition
        args: list of sets that represents the partition

        return list of tuples
        """
        
        return sorted([tuple(sorted(i)) for i in args])

    def parse(self, lst):
        hashes = {}
        for i, j in enumerate(lst):
            hashes.setdefault(j, []).append(i)
        return [set(i) for i in hashes.values()]