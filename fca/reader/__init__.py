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

from itertools import chain

def read_plain(path):
    with open(path, 'r') as fin:
        for line in fin:
            yield line.replace('\n', '')

def read_cxt(path):
    with open(path, 'r') as fin:
        cxt_type = None
        G = -1
        M = -1
        Gs = []
        Ms = []
        for line in fin:
            line = line.replace('\n', '')
            if not line.startswith('#') and line != '':
                if cxt_type is None:
                    cxt_type = line
                elif G == -1:
                    G = int(line)
                elif M == -1:
                    M = int(line)
                elif len(Gs) != G:
                    Gs.append(line)
                elif len(Ms) != M:
                    Ms.append(line)
                else:
                    out = ''
                    for i, j in enumerate(line.strip()):
                        if j.lower() == 'x':
                            out += "{} ".format(i)
                    yield out.strip()



def read_representations(path):
    if path.endswith('.txt'):
        return read_plain(path)
    elif path.endswith('.cxt'):
        return read_cxt(path)


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
