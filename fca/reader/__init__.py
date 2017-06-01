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
    'SSV': lambda desc: set([i for i in desc.split()]),
    'CSV': lambda desc: set([i for i in desc.split(',')])
}



"""
****************************************
TRANSFOMERS
****************************************
"""
class Transformer(object):
    def __init__(self):
        pass
    def transform(self, entry):
        raise NotImplementedError
    def g_map(self):
        return {}
    def m_map(self):
        return {}

class List2SetTransformer(Transformer):
    def __init__(self):
        super(List2SetTransformer, self).__init__()
        self.objects = {}
        self.attributes = {}

    def transform(self, entry):
        self.objects.setdefault(entry[0], len(self.objects))
        atts = set([self.attributes.setdefault(att, len(self.attributes)) for att in entry[1]])
        return atts

    def g_map(self):
        return {j:i for i, j in self.objects.items()}

    def m_map(self):
        return {j:i for i, j in self.attributes.items()}

class List2IntervalsTransformer(Transformer):
    def __init__(self, data_type=int):
        super(List2IntervalsTransformer, self).__init__()
        self.data_type = data_type

    def transform(self, entry):
        interval = []
        for i in entry[1]:
            interval.append((self.data_type(i), self.data_type(i)))
        return interval



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

def read_representations(path, **params):
    params['filepath'] = path
    return InputManager(**params)


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

# REGISTER FILE MANAGERS
FMGRS = {
    'txt': ParseableManager,
    'cxt': CXTManager
}



class InputManager(object):
    """
    Data Streamer Manager
    """
    def __init__(self, transformer=List2SetTransformer(), **params):
        self.__representations = None
        self.transformer = transformer

        # Choose how to treat the file according to its extension
        fip = params['filepath']
        file_extension = fip[fip.rindex('.')+1:].lower()
        assert file_extension in FMGRS.keys(), 'File should be one of {}'.format(FMGRS.keys())
        self.__fmgr = FMGRS[file_extension](params['filepath'])


        if not params.get('transposed', False):
            self.__representations = self.__fmgr.entries()
        else:
            self.__representations = self.__fmgr.entries_transposed()

    @property
    def representations(self):
        lst = list(self.__representations)
        #print 'rep',lst
        for entry in lst:
            yield self.transformer.transform(entry)
         #self.__representations


class FormalContext(InputManager):
    """
    CONTEXT MANAGER
    """
    @property
    def objects(self):
        """
        getter for objects property
        """
        return self.__objects

    @property
    def attributes(self):
        """
        getter for attributes property
        """
        return self.__attributes


    def __init__(self, repr_parser, **params):
        """
        repr_parser: lambda function which returns a set of attributes
        """

        super(FormalContext, self).__init__(**params)
        # READ THE CONTEXT
        self.__representations = [repr_parser(rep) for rep in self.representations]
        # OBJ COUNTER
        self.n_objects = len(self.__representations)


        if self.__objects is None:
            self.__objects = range(self.n_objects)

        if self.__attributes is None:
            self.__attributes = sorted(reduce(lambda x, y: x.union(y), self.__representations))

        # MAP ATTRIBUTES TO INDICES
        self.m_map = {j:i for i, j in enumerate(self.__attributes)}

        # REGENERATE NEW CONTEXT WITH INDEXED ATTRIBUTES
        self.g_prime = [set([self.m_map[i] for i in j]) for j in self.__representations]
        # ATT COUNTER
        self.n_attributes = len(self.m_map)

        self.m_prime = {}
        # INVERTED CONTEXT
        for object_id, attributes in enumerate(self.__representations):
            for att in attributes:
                self.m_prime.setdefault(att, set([])).add(object_id)

