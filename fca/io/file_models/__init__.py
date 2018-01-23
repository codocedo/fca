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
import os

#****************************************
# File Syntax Models
#****************************************
FILE_MANAGERS = {}

def register_file_manager(target_class):
    """
    Function that registers file managers, used in conjunction with
    the metaclass MCFileModel
    """
    FILE_MANAGERS[target_class.__name__] = target_class

class MCFileModel(type):
    """
    Metaclass used to register file managers
    """
    def __new__(mcs, clsname, bases, attrs):
        """
        cls: class
        clsname: classname
        """
        newclass = super(MCFileModel, mcs).__new__(mcs, clsname, bases, attrs)
        register_file_manager(newclass)  # here is your register function
        return newclass


class FileModel(object):
    """
    Abstract Class for File Models
    OVERWRITE to implement a new file parser
    Implements metaclass to register new file managers

    entries() returns an array or iterator of space separated values

    configurations is a property used by the FileModel factory
    to configure which FileModel should be used.
    _cfgs should be a list of "style" and "extension"
    the first one indicating the style of the file, 1 line per object (oa),
    table file (tab), matrix, etc
    The "extension" should refer to the default extensions that the 
    file manager can be applied, e.g. txt, csv, cxt, etc.
    """
    __metaclass__ = MCFileModel
    _cfgs = []
    def __init__(self, filepath, **params):
        """
        Creates a new File Model
        @param filepath: path to the file where the context is
        @param params: contain ad-hoc parameters for each type of file manager
        """
        assert filepath != '', "You must include a valid filepath for the input file"
        assert os.path.isfile(filepath), 'Input file: {} does not exist'.format(filepath)
        self.filepath = filepath

    @classmethod
    def configurations(cls):
        """
        Class method used by the File Model factory
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



class ParseableModel(FileModel):
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
        super(ParseableModel, self).__init__(filepath, **params)
        ext = params.get('extension', 'txt')
        self.parser = params.get('parser', ParseableModel.PARSERS[ext])
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


class CXTModel(ParseableModel):
    """
    Manages a CXT context file
    used by other FCA tools such as ConExp and Toscana
    """
    _cfgs = [('oa','cxt')]
    def __init__(self, filepath, **params):
        super(CXTModel, self).__init__(filepath)

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





class TableModel(ParseableModel):
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
        super(TableModel, self).__init__(filepath, **params)

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

class FileModelFactory(object):
    """
    FileModelFactory allows creating a suitable FileModel
    given the characteristics of the file and the options provided
    by the user. Uses the registry created by the metclass
    """
    def __init__(self, filename, **kwargs):
        """
        @param filename: str file name to be analyzed
        @param extension: str allows the user to specify an extension, if not provided it is obtained from filename
        @param style: str style of the file, oa: one object per line with separated symbols for attributes, tab: matrix format
        @kwargs: optional parameters to configure the FileModel

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
        assert (self._style, self._extension) in self._extensions, 'Style and Extension {} should be one in {}'.format((self._style, self._extension), self._extensions)
        self.filename = filename
        self.kwargs = kwargs

    @property
    def file_manager(self):
        """
        Builds the file manager configured at creation
        """
        return self._extensions[(self._style, self._extension)](self.filename, **self.kwargs)
