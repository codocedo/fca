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
import os
from itertools import chain


def read_representations(path, **params):
    """
    Wrapper for the following classes
    path: path to a context file
    params: configurations
    returns InputManager(**params)
    """
    params['filepath'] = path
    return InputManager(**params)

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
        pass
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
        return {}
    def m_map(self):
        """
        Returns a map to transform attributes symbols back to their
        original representation in the file
        """
        return {}

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
        self.objects.setdefault(entry[0], len(self.objects))
        atts = self.parse(entry[1])
        return atts

    def parse(self, lst):
        return set([self.attributes.setdefault(att, len(self.attributes)) for att in lst])

    def g_map(self):
        return {j:i for i, j in self.objects.items()}

    def m_map(self):
        return {j:i for i, j in self.attributes.items()}

    def original_intent(self, intent):
        m_map = self.m_map()
        return [m_map[i] for i in intent]

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
        self.objects = {}

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

    def g_map(self):
        return {j:i for i, j in self.objects.items()}

class List2PartitionsTransformer(List2IntervalsTransformer):
    """
    Transforms a list of values to a partition containing equivalence classes of indices
    [0,1,0,1,1] -> [set([0,2]), set([1,3,4])]
    """
    def parse(self, lst):
        hashes = {}
        for i, j in enumerate(lst):
            hashes.setdefault(j, []).append(i)
        return [set(i) for i in hashes.values()]
#****************************************
# File Syntax Managers
#****************************************
FILE_MANAGERS = {}

def register_file_manager(target_class):
    """
    Function that registers file managers, used in conjunction with
    the metaclass MCFileManager
    """
    FILE_MANAGERS[target_class.__name__] = target_class

class MCFileManager(type):
    """
    Metaclass used to register file managers
    """
    def __new__(mcs, clsname, bases, attrs):
        """
        cls: class
        clsname: classname
        """
        newclass = super(MCFileManager, mcs).__new__(mcs, clsname, bases, attrs)
        register_file_manager(newclass)  # here is your register function
        return newclass


class FileManager(object):
    """
    Abstract Class for File Managers
    OVERWRITE to implement a new file parser
    Implements metaclass to register new file managers

    entries() returns an array or iterator of space separated values

    configurations is a property used by the FileManager factory
    to configure which FileManager should be used.
    _cfgs should be a list of "style" and "extension"
    the first one indicating the style of the file, 1 line per object (oa),
    table file (tab), matrix, etc
    The "extension" should refer to the default extensions that the 
    file manager can be applied, e.g. txt, csv, cxt, etc.
    """
    __metaclass__ = MCFileManager
    _cfgs = []
    def __init__(self, filepath, **params):
        """
        Creates a new File Manager
        @param filepath: path to the file where the context is
        @param params: contain ad-hoc parameters for each type of file manager
        """
        assert filepath != '', "You must include a valid filepath for the input file"
        assert os.path.isfile(filepath), 'Input file: {} does not exist'.format(filepath)
        self.filepath = filepath
        
    @classmethod
    def configurations(cls):
        """
        Class method used by the File Manager factory
        @param cls: class type
        """
        return cls._cfgs

    def entries(self):
        """
        Returns an array or iterator of pairs (first, second)
        first value is an identifier of the line
        second value is a representation of the line
        """
        raise NotImplementedError()
    

    def entries_transposed(self):
        """
        Returns an array or iterator of pairs (first, second)
        first value is an identifier of the line
        second value is a representation of the line
        """
        raise NotImplementedError()



class ParseableManager(FileManager):
    """
    Default parser, this one deals with separated values
    and 1 line per object style of formal contexts (oa)
    By default we support space separated values (txt) and comma separated values (csv)
    """
    PARSERS = {
        'txt': lambda desc: [i for i in desc.split()],
        'csv': lambda desc: [i for i in desc.split(',')]
    }
    _cfgs = [('oa', 'txt'), ('oa', 'csv')]
    
    def __init__(self, filepath, **params):
        super(ParseableManager, self).__init__(filepath, **params)
        self.parser = params.get('parser', ParseableManager.PARSERS['txt'])
        # EXTENSION TO BE REGISTERED

    def entries(self):
        """
        Returns an array or iterator of strings with space separated values
        """
        with open(self.filepath, 'r') as fin:
            for line_i, line in enumerate(fin):
                yield (line_i, self.parser(line.replace('\n', '')))

    def entries_transposed(self):
        """
        Returns an array or iterator of strings with space separated values
        transposing the original formal context
        """
        new_representation = {}
        reps = list(self.entries())
        for obj, representation in reps:
            for attribute in representation:
                new_representation.setdefault(attribute, []).append(obj)
        for i, j in sorted(new_representation.items(), key=lambda s: s[0]):
            yield (i, j)


class CXTManager(ParseableManager):
    """
    Manages a CXT context file
    used by other FCA tools such as ConExp and Toscana
    """
    _cfgs = [('oa','cxt')]
    def __init__(self, filepath, **params):
        super(CXTManager, self).__init__(self, filepath)
    
    def entries(self):
        """
        READS A CXT FILE
        NOT THOUGHT FOR STREAMING
        READ THE FILE ENTIRELY AND THEN PROCESS IT
        """
        with open(self.filepath, 'r') as fin:
            cxt_type = None
            objects = []
            attributes = []
            n_objects = -1
            n_attributes = -1
            representations = []
            for line in fin:
                line = line.replace('\n', '')
                if not line.startswith('#') and line != '':
                    if cxt_type is None:
                        cxt_type = line
                    elif n_objects == -1:
                        n_objects = int(line)
                    elif n_attributes == -1:
                        n_attributes = int(line)
                    elif len(objects) != n_objects:
                        objects.append(line)
                    elif len(attributes) != n_attributes:
                        attributes.append(line)
                    else:
                        out = []
                        for i, j in enumerate(line.strip()):
                            if j.lower() == 'x':
                                out.append(attributes[i])
                        representations.append((objects[len(representations)], out))
        return representations





class TableManager(ParseableManager):
    """
    Numerical data where each of the M entries is a row with N values
    Used for database entries:
    example:
    1 1 2 4
    1 2 2 3
    3 2 1 1
    With 3 objects and 4 attributes
    Values can be space separated (txt) or comma separated (cv)
    """
    _cfgs = [('tab', 'txt'), ('tab', 'csv')]
    def __init__(self, filepath, **params):
        super(TableManager, self).__init__(filepath, parser=ParseableManager.PARSERS[params['extension']])

    def entries_transposed(self):
        """
        Transposition occurs like matrix transposition
        """
        new_representation = []
        reps = [i[1] for i in self.entries()]
        for coli in range(len(reps[0])):
            new_representation.append([i[coli] for i in reps])
        for i, j in enumerate(new_representation):
            yield (i, j)
       
class FileManagerFactory(object):
    """
    FileManagerFactory allows creating a suitable FileManager
    given the characteristics of the file and the options provided
    by the user. Uses the registry created by the metclass
    """
    def __init__(self, filename, **kwargs):
        """
        @param filename: str file name to be analyzed
        @param extension: str allows the user to specify an extension, if not provided it is obtained from filename
        @param style: str style of the file, oa: one object per line with separated symbols for attributes, tab: matrix format
        @kwargs: optional parameters to configure the FileManager

        """
        self._extensions = {}
        for cls in FILE_MANAGERS.values():
            for style_extension in cls.configurations():
                self._extensions[style_extension] = cls
        self._file_manager = None
        self._extension = ''
        self._style = 'oa' # By default, style is object-attribute
        if kwargs.get('extension', False):
            # If the user has forced an extension, we'll treat the file using it
            self._extension = kwargs['extension']
        else:
            # If the user didn't force an extension, we'll obtain it from the file and
            # try to use it to process the file
            self._extension = filename[filename.rindex('.')+1:].lower()
            kwargs['extension'] = self._extension
        if kwargs.get('style', False):
            # If the user has specified a file-style, we'll treat the file using it
            self._style = kwargs['style']
        assert (self._style, self._extension) in self._extensions, 'File should be one in {}'.format(self._extensions)
        self.filename = filename
        self.kwargs = kwargs

    @property
    def file_manager(self):
        """
        Builds the file manager configured at creation
        """
        return self._extensions[(self._style, self._extension)](self.filename, **self.kwargs)

#****************************************
# Input Managers
#****************************************
class InputManager(object):
    """
    Data Streamer Manager
    """
    def __init__(self, filepath, transposed=False, transformer=None, file_manager_params=None):
        self.transformer = transformer if transformer is not None else List2SetTransformer()
        self._representations = None

        # Choose the parser if it has not been provided according to the extension
        file_manager_params = file_manager_params if file_manager_params is not None else {}

        self.__fmgr = FileManagerFactory(filepath, **file_manager_params).file_manager

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


class PatternStructureManager(InputManager):
    """
    Pattern structure representation
    It only index object representations for Close By One
    """
    def __init__(self, **params):
        super(PatternStructureManager, self).__init__(**params)
        # Calculate g prime
        self.g_prime = {i[0]:self.transformer.transform(i) for i in self._representations}
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

class FormalContextManager(PatternStructureManager):
    """
    CONTEXT MANAGER
    Extends PatternStructure by indexing attribute representations as well
    """
    def __init__(self, **params):
        super(FormalContextManager, self).__init__(**params)

        self.m_prime = {}
        # Calculate m_prime
        for object_id, attributes in self.g_prime.items():
            for att in attributes:
                self.m_prime.setdefault(att, set([])).add(object_id)

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

#****************************************
# Deprecated methods
#****************************************
def read_object_list(path):
    with open(path, 'r') as f:
        lines = f.read().split('\n')
        objects = []
        for line in lines:
            if line != '':
                objects.append(set([int(i) for i in line.split()]))
        return objects


def read_map(path):
    lines = file(path).read().split('#\n')
    objects = {j:i.strip() for j, i in enumerate(lines[0].split('\n')) if i.strip() != ''}
    attributes = {j:i.strip() for j, i in enumerate(lines[1].split('\n')) if i.strip() != ''}
    return objects, attributes