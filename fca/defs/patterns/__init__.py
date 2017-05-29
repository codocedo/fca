from fca.defs import SetPattern

class IcebergSetPattern(SetPattern):
    MIN_SUP = 0
    def __init__(self, desc):
        if len(desc) < self.MIN_SUP:
            desc = set([])
        super(IcebergSetPattern, self).__init__(desc)
    def intersection(self, other):
        assert IcebergSetPattern.MIN_SUP >= 0, 'MIN_SUP value should be a positive number'
        newdesc = self.desc.intersection(other.desc)
        if len(newdesc) < self.MIN_SUP:
            return self.bottom()
        else:
            return IcebergSetPattern(newdesc)

