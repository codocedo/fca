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
