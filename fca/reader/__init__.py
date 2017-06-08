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

PARSERS = {
    'SSV': lambda desc: [i for i in desc.split()],
    'CSV': lambda desc: [i for i in desc.split(',')]
}


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
****************************************
TRANSFOMERS
****************************************
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


#****************************************
# File Managers
#****************************************

class FileManager(object):
    """
    OVERWRITE to implement a new file parser
    By default, this one deals with space separated values
    get_representations returns an array or iterator of space separated values
    """
    def __init__(self, filepath):
        assert filepath != '', "You must include a valid filepath for the input file"
        assert os.path.isfile(filepath), 'Input file: {} does not exist'.format(filepath)
        self.filepath = filepath
    def entries(self):
        """
        Return an array or iterator of pairs (first, second)
        first value is an identifier of the line
        second value is a representation of the line
        """
        raise NotImplementedError()

    def entries_transposed(self):
        """
        Return an array or iterator of pairs (first, second)
        first value is an identifier of the line
        second value is a representation of the line
        """
        new_representation = {}
        reps = list(self.entries())
        #print reps
        for obj, representation in reps:
            for attribute in representation:
                new_representation.setdefault(attribute, []).append(obj)
        #print new_representation
        for i, j in sorted(new_representation.items(), key=lambda s: s[0]):
            yield (i, j)

class ParseableManager(FileManager):
    """
    OVERWRITE to implement a new file parser
    By default, this one deals with space separated values
    get_representations returns an array or iterator of space separated values
    """
    def __init__(self, filepath, parser=PARSERS['SSV']):
        super(ParseableManager, self).__init__(filepath)
        self.parser = parser

    def entries(self):
        """
        Return an array or iterator of strings with space separated values
        """

        with open(self.filepath, 'r') as fin:
            for line_i, line in enumerate(fin):
                yield (line_i, self.parser(line.replace('\n', '')))




class CXTManager(FileManager):
    """
    Manages a CXT context file
    """
    def entries(self):
        """
        READS A CXT FILE
        NOT FOR THOUGHT FOR STREAMING
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



# REGISTER FILE MANAGERS
FMGRS = {
    'txt': ParseableManager,
    'cxt': CXTManager
}


#****************************************
# Input Managers
#****************************************
class InputManager(object):
    """
    Data Streamer Manager
    """
    def __init__(self, transformer=None, **params):
        self.transformer = transformer if transformer is not None else List2SetTransformer()
        self._representations = None
        
        # Choose how to treat the file according to its extension
        fip = params['filepath']
        file_extension = fip[fip.rindex('.')+1:].lower()
        assert file_extension in FMGRS.keys(), 'File should be one of {}'.format(FMGRS.keys())
        self.__fmgr = FMGRS[file_extension](params['filepath'])

        if not params.get('transposed', False):
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


class FormalContextManager(InputManager):
    """
    CONTEXT MANAGER
    """
    def __init__(self, **params):
        super(FormalContextManager, self).__init__(**params)
        # READ THE CONTEXT

        self.g_prime = {i[0]:self.transformer.transform(i) for i in self._representations}

        # OBJ COUNTER
        self.n_objects = len(self.g_prime)

        self.m_prime = {}
        # INVERTED CONTEXT
        for object_id, attributes in self.g_prime.items():
            for att in attributes:
                self.m_prime.setdefault(att, set([])).add(object_id)

        # MAP ATTRIBUTES TO INDICES

        # REGENERATE NEW CONTEXT WITH INDEXED ATTRIBUTES

        # ATT COUNTER
        self.n_attributes = len(self.m_prime)

    @property
    def objects(self):
        '''
        Returns the available indices of objects
        returns list
        '''
        return sorted(self.g_prime.keys())
    @property
    def attributes(self):
        '''
        Return the available indices for attributes
        returns list
        '''
        return sorted(self.m_prime.keys())

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