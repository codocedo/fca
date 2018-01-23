from fca.io.transformers import List2SetTransformer
from fca.io.file_models import FileModelFactory

#****************************************
# Input Models
#****************************************
class InputModel(object):
    """
    Data Streamer Model
    """
    def __init__(self, filepath, transposed=False, transformer=None, file_manager_params=None, **params):
        self.transformer = transformer if transformer is not None else List2SetTransformer()
        self._representations = None

        # Choose the parser if it has not been provided according to the extension
        file_manager_params = file_manager_params if file_manager_params is not None else {}

        self.__fmgr = FileModelFactory(filepath, **file_manager_params).file_manager

        if not transposed:
            self._representations = self.__fmgr.entries()
        else:
            self._representations = self.__fmgr.entries_transposed()

    @property
    def representations(self):
        """
        Returns transformed representations obtained
        from file managers
        """
        for entry in self._representations:
            yield self.transformer.transform(entry)

#****************************************
# Pattern Structure Model
#****************************************
class PatternStructureModel(InputModel):
    """
    Pattern structure representation
    It only index object representations for Close By One
    """
    def __init__(self, **params):
        super(PatternStructureModel, self).__init__(**params)
        self.sorter = params.get('sorter', None)
        # Calculate g prime
        self.g_prime = {i[0]:self.transformer.transform(i) for i in self._representations}

        if self.sorter is not None:
            self.g_prime = self.sorter.sort(self.g_prime)
        # OBJ COUNTER
        self.n_objects = len(self.g_prime)

    @property
    def objects(self):
        '''
        Returns the available indices of objects
        returns list
        '''
        return sorted(self.g_prime.keys())

    def extent_prime(self, extent):
        '''
        Implements A' given A subseteq G
        '''
        if not bool(extent):
            return reduce(lambda x, y: x.union(y),
                          self.g_prime.values())
        return reduce(lambda x, y: x.intersection(y),
                      [self.g_prime[g] for g in extent])


#****************************************
# Formal Context Model
#****************************************
class FormalContextModel(PatternStructureModel):
    """
    CONTEXT MANAGER
    Extends PatternStructure by indexing attribute representations as well
    """
    def __init__(self, **params):
        super(FormalContextModel, self).__init__(**params)

        self.m_prime = {}
        # Calculate m_prime
        for object_id, attributes in self.g_prime.items():
            for att in attributes:
                self.m_prime.setdefault(
                    att,
                    set([])
                ).add(
                    object_id
                )
        # ATT COUNTER
        self.n_attributes = len(self.m_prime)

    @property
    def attributes(self):
        '''
        Return the available indices for attributes
        returns list
        '''
        return sorted(self.m_prime.keys())

    def intent_prime(self, intent):
        '''
        Implements B' given B subseteq M
        '''
        if not bool(intent):
            return self.g_prime.keys()
        return reduce(lambda x, y: x.intersection(y),
                      [self.m_prime[m] for m in intent])