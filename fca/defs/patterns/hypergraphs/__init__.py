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
import sys
from itertools import product, chain
from fca.defs import SIntent, Intent

class PartitionPattern(SIntent):
    """
    Description is a list of frozensets
    TOP: is a partition with a single element with all attributes
    BOTTOM: is a partition with one element per attribute
    """
    # the bottom will be a singleton
    _top = None
    _bottom = None

    @classmethod
    def fix_desc(cls, desc):
        return cls.sort_description(desc)

    @classmethod
    def intersection(cls, desc1, desc2):
        if desc2 == cls._top:
            return desc1
        new_desc = []
        counter = 0
        for i, j in product(desc1, desc2):
            x, y = (i, j) if len(i) < len(j) else (j, i)
            if x.issubset(y):
                new_desc.append(x)
                counter += len(x)
            else:
                intx = x.intersection(y)
                if bool(intx): # instead of len(x) > 0
                    new_desc.append(intx)
                    counter += len(intx)
        # print len(new_desc)
        if len(new_desc) == counter:
            return PartitionPattern.bottom(new_desc)
        return cls.fix_desc(new_desc)

    @classmethod
    def leq(cls, desc1, desc2):
        if desc1 == cls._bottom:
            return True
        if cls.length(desc1) < cls.length(desc2):
            return False
        for i in desc1:
            check = False
            for j in desc2:
                if len(i) > len(j):
                    break
                if i.issubset(j):
                    check = True
                    break
            if not check:
                return False
        return True

    @classmethod
    def is_equal(cls, desc1, desc2):
        if len(desc1) != len(desc2):
            return False
        for i, j in zip(desc1, desc2):
            if i != j:
                return False
        return True

    @classmethod
    def contains(cls, desc, key):
        return key in desc

    @classmethod
    def join(cls, desc1, desc2):
        print desc1, desc2
        desc1 = cls.fix_desc([desc1[0].union(chain(*desc2))])

    @classmethod
    def meet(cls, desc1, desc2):
        new_desc = []
        for i, j in product(desc1, desc2):
            intx = i.intersection(j)
            if bool(intx): # instead of len(x) > 0
                new_desc.append(intx)
        desc1 = cls.fix_desc(new_desc)

    @classmethod
    def length(cls, desc):
        return len([i for i in desc if len(i) > 0])

    @classmethod
    def is_empty(cls, desc):
        return len(desc) == 0

    @classmethod
    def get_iterator(cls, desc):
        for i in desc:
            yield i

    @classmethod
    def top(cls, top_rep=None):
        if cls._top is None:
            cls._top = [set([])]
        if top_rep is not None:
            cls._top[0].update(set(list(chain(*top_rep))))
        return cls._top

    @classmethod
    def bottom(cls, bot_rep=None):
        if cls._bottom is None:
            cls._bottom = []
        if bot_rep is not None:
            if bool(cls._bottom):
                cls.meet(cls._bottom, bot_rep)
            else:
                for i in bot_rep:
                    cls._bottom.append(i)
        return cls.fix_desc(cls._bottom)

    @classmethod
    def sort_description(cls, desc):
        desc.sort(key=lambda x: (len(x), sorted(x)), reverse=True)
        return desc

class TrimmedPartitionPattern(PartitionPattern):
    """
    Description is a list of frozensets
    Sets with 1 elements are deleted from the partition
    """
    # the bottom will be a singleton
    _top = None
    _bottom = None

    n_elements = 0

    @classmethod
    def leq(cls, desc1, desc2):
        if desc1 == cls._bottom:
            return True
        for i in desc1:
            check = False
            for j in desc2:
                if len(i) > len(j):
                    break
                if i.issubset(j):
                    check = True
                    break
            if not check:
                return False
        return True

    @classmethod
    def bottom(cls, bot_rep=None):
        if cls._bottom is None:
            cls._bottom = []
        if cls.n_elements != 0 and len(cls._bottom) != cls.n_elements:
            for i in range(cls.n_elements):
                cls._bottom.append(set([i]))
        return cls._bottom

    @classmethod
    def fix_desc(cls, desc):
        n_elements = sum([len(i) for i in desc])
        if cls.n_elements < n_elements:
            cls.n_elements = n_elements
        for i in range(len(desc)-1, -1, -1):
            if len(desc[i]) == 1:
                del desc[i]
        return cls.sort_description(desc)

    @classmethod
    def intersection(cls, desc1, desc2):
        new_desc = []
        counter = 0
        for i, j in product(desc1, desc2):
            x, y = (i, j) if len(i) < len(j) else (j, i)
            if x.issubset(y):
                new_desc.append(x)
                counter += len(x)
            else:
                intx = i.intersection(j)
                if len(intx) > 1: # instead of len(x) > 0
                    new_desc.append(intx)
                    counter += len(intx)

        if len(new_desc) == counter:
            return cls.bottom()
        return cls.fix_desc(new_desc)



def lst_intersection(lst1, lst2):
    a, b = lst1, lst2 if len(lst1) <= len(lst2) else lst2, lst1
    result = []
    b_marker = 0
    for i in a:
        for k in range(b_marker, len(b)):
            if i == b[k]:
                result.append(i)
                b_marker = k+1
                break
            elif i > b[k]:
                b_marker = k+1
                break
    return result

def unique_listing(lst):
    lst.sort()
    for i in range(len(lst)-1, -1, -1):
        if lst[i] == lst[i-1]:
            del lst[i]
    return sorted(lst)

def lst_intersection(lst1, lst2):
    (lst_a, lst_b) = (lst1, lst2) if len(lst1) <= len(lst2) else (lst2, lst1)
    result = []
    b_marker = 0
    for i in lst_a:
        # print '\t=>',i
        for k in range(b_marker, len(lst_b)):
            # print '\t\t=>',k, lst_b[k]
            if i == lst_b[k]:
                result.append(i)
                b_marker = k+1
                break
            elif i < lst_b[k]:
                b_marker = k
                break
    return result

def lst_subset(lst_a, lst_b):
    b_marker = 0
    for i in lst_a:
        # print '\t=>',i
        found = False
        for k in range(b_marker, len(lst_b)):
            # print '\t\t=>',k, lst_b[k]
            if i == lst_b[k]:
                b_marker = k+1
                found = True
                break
            elif i < lst_b[k]:
                break
        if not found:
            return False
    return True

def translate(desc):
    groups = {}
    for i, j in enumerate(desc):
        groups.setdefault(j, []).append(i)
    singles = [[i] for i in groups.get(-1, [])]
    # print singles, groups
    return [groups[i] for i in groups.keys() if i >= 0] + singles

class LstTrimmedPartitionPattern(PartitionPattern):
    """
    Description is a list of frozensets
    Sets with 1 elements are deleted from the partition
    """
    # the bottom will be a singleton
    _top = None
    _bottom = None

    def __init__(self, desc):
        self.length = len(desc)#sum([len(i) for i in self.desc])
        self.n_elements = sum([len(i) for i in desc])
        desc = [i for i in desc if len(i) > 1]
        super(LstTrimmedPartitionPattern, self).__init__(desc)
        self.desc = LstTrimmedPartitionPattern.sort_desc(desc)

    def intersection(self, other):
        new_desc = []

        for i, j in product(self.desc, other.desc):
            intx = lst_intersection(i, j)
            if len(intx) > 1: # instead of len(x) > 0
                new_desc.append(intx)

        if not bool(new_desc):
            new_pattern =  LstTrimmedPartitionPattern.bottom()
        else:
            new_pattern =  LstTrimmedPartitionPattern(new_desc)

        new_pattern.length += self.n_elements - sum([len(i) for i in new_desc])
        new_pattern.n_elements = self.n_elements
        return new_pattern

    def __i_le__(self, other):
        for i in self.desc:
            check = False
            for j in other.desc:
                if len(i) > len(j):
                    break
                elif lst_subset(i, j):
                    check = True
                    break
            if not check:
                return False
        return True

    def __i_len__(self):
        return self.length

    @staticmethod
    def sort_desc(desc):
        """
        Sort desc, necessary to ensure optimized comparisons
        """
        return sorted(desc, key=len(x), reverse=True)

class SignaturePartitionPattern(Intent):
    """
    Description is a list of frozensets
    """
    # the bottom will be a singleton
    _top = None
    _bottom = None

    def __init__(self, desc):
        # signature = [0]*sum([len(i) for i in desc])
        # for i, j in enumerate(desc):
        #     for k in j:
        #         signature[k] = i
        # print desc
        # self.length = len(set(desc)) 
        super(SignaturePartitionPattern, self).__init__(desc)

    def intersection(self, other):
        # print self, 'intersection', other,
        # groups = {}
        new_signature = []#[-1]*len(self.desc)
        # for k, (i, j) in enumerate(zip(self.desc, other.desc)):
        #     if i >= 0 and j >= 0:
        #         groups.setdefault((i, j), []).append(k)
        # not_bot = True
        # for i, j in enumerate(sorted(groups.keys())):
        #     if len(groups[j]) > 1:
        #         not_bot = False
        #         for k in groups[j]:
        #             new_signature[k] = i
        symbols = {}
        syc = {}
        for k, (i, j) in enumerate(zip(self.desc, other.desc)):
            new_signature.append(symbols.setdefault((i,j), len(symbols)))
            syc[(i,j)] = syc.get((i,j), 0) + 1 

        return  SignaturePartitionPattern(new_signature)
        # if not_bot:
        #     new_pattern =  SignaturePartitionPattern.bottom([-1]*len(self.desc))
        # else:
        #     new_pattern =  SignaturePartitionPattern(new_signature)
        # # print groups
        # if -1 in new_signature:
        #     new_pattern.length += len([i for i in new_signature if i == -1]) - 1
        # # new_pattern.length = len(groups)# - 1 + len(groups.get(-1, []))
        # return new_pattern



    def __i_le__(self, other):
        """
        Coarse <= Granular
        """
        # print translate(self.desc), '<=', translate(other.desc),
        # print self.desc, '<=', other.desc,
        if other.__type__ == Intent.TYPES.BOTTOM and self.__type__.__type__ != Intent.TYPES.BOTTOM:
            return False
        checker = {}
        for position, value in enumerate(self.desc):
            # print self.desc[position], other.desc[position], value, checker.get(value, False), bool(checker.get(value, False)), checker.get(value, False) != self.desc[position]
            if checker.get(value, None) is not None and checker[value] != other.desc[position]:
                # print "FALSE"
                return False
            checker[value] = other.desc[position]
        # print "TRUE"
        return True
    

    def __i_eq__(self, other):
        # print translate(self.desc), '==', translate(other.desc),
        # print self.desc, '==', other.desc,
        checker_l = {}
        checker_r = {}
        for left, right in zip(self.desc, other.desc):
            left_check = checker_l.get(left, None) is not None and checker_l[left] != right
            right_check = checker_r.get(right, None) is not None and checker_r[right] != left
            if not right_check or not left_check:
                # print "FALSE"
                return False
            checker_l[left] = right
            checker_r[right] = left
        # print "TRUE"
        return True


    @classmethod
    def top(cls, top_rep=None):
        if cls._top is None:
            if top_rep is None:
                cls._top = cls([])
            else:
                cls._top = cls([0]*sum([len(i) for i in top_rep[0]]))

            cls._top.__i_le__ = lambda s: False
            cls._top.__type__ = Intent.TYPES.TOP
            cls._top.__i_eq__ = lambda s: s.__type__ == Intent.TYPES.TOP
        else:
            if top_rep is not None:
                cls._top.desc = top_rep
        return cls._top

    @classmethod
    def bottom(cls, bot_rep=None):
        """
        The bottom is a singleton
        """
        if cls._bottom is None:
            if bot_rep is None:
                cls._bottom = cls([-1])
            else:
                cls._bottom = cls(bot_rep)
            cls._bottom.__i_le__ = lambda s: True
            cls._bottom.is_empty = lambda: True
            cls._bottom.__type__ = Intent.TYPES.BOTTOM
            cls._bottom.__i_eq__ = lambda s: s.__type__ == Intent.TYPES.BOTTOM or s.desc == cls._bottom.desc
            cls._bottom.intersection = lambda s: cls._bottom
            return cls._bottom
        else:
            if bot_rep is not None:
                cls._bottom.desc = bot_rep
            return cls._bottom

    def repr(self):
        return translate(self.desc)

    def __i_len__(self):
        return len(set(self.desc))
        # return self.length#len(translate(self.desc))

    def __i_iter__(self):
        for i in translate(self.desc):
            yield tuple(sorted(i))

    # def __i_contains__(self, key):
    #     return key in self.desc

    # def join(self, other):
    #     self.desc = [self.desc[0].union(chain(*other.desc))]

    # def meet(self, other):
    #     raise NotImplementedError

    

    

    # def is_empty(self):
    #     return len(self) == 0

    

    # @classmethod
    # def bottom(cls, bot_rep=None):
    #     """
    #     The bottom is a singleton
    #     """
    #     if cls._bottom is None:
    #         if bot_rep is None:
    #             bot_rep = [frozenset([])]
    #         cls._bottom = cls(bot_rep)
    #         cls._bottom.__i_le__ = lambda s: True
    #         cls._bottom.is_empty = lambda: True
    #         cls._bottom.__type__ = Intent.TYPES.BOTTOM
    #         cls._bottom.__i_eq__ = lambda s: s.__type__ == Intent.TYPES.BOTTOM or s.desc == cls._bottom.desc
    #         cls._bottom.intersection = lambda s: cls._bottom
    #         return cls._bottom
    #     else:
    #         cls._bottom.desc = bot_rep
    #         return cls._bottom


    # @staticmethod
    # def sort_desc(desc):
    #     """
    #     Sort desc, necessary to ensure optimized comparisons
    #     """
    #     return sorted(desc, key=lambda x: sorted(x))

class ToleranceBlockPattern(PartitionPattern):
    """
    Description is a list of frozensets
    """
    # the bottom will be a singleton
    _top = None
    _bottom = None

    def __init__(self, desc):
        super(ToleranceBlockPattern, self).__init__(ToleranceBlockPattern.sort_desc(desc))
        self.desc = ToleranceBlockPattern.sort_desc(self.desc)

    # def intersection(self, other):
    #     new_desc = []
    #     # if len(self.desc)*len(other.desc) > 100:
    #     #     print len(self.desc)*len(other.desc),
    #     #     print len(self.desc), len(other.desc), [len(i) for i in self.desc], [len(i) for i in other.desc]
    #     result = []
    #     for i, j in product(self.desc, other.desc):
    #         result.append(i.intersection(j))
    #     clean = []
    #     for i in range(0, len(result)-1):
    #         if len(result[i]) <= 1:
    #             continue
    #         for j in range(i+1, len(result)):
    #             if result[i].issubset(result[j]):
    #                 clean.append(i)
    #                 break
    #     for i in sorted(clean, reverse=True):
    #         del result[i]
            
    #     return ToleranceBlockPattern(result)
        
    #     for i, j in product(self.desc, other.desc):
    #         intx = i.intersection(j)
    #         if len(intx) > 1: # instead of len(x) > 0
    #             add = True
    #             for k in range(len(new_desc)):
    #                 if intx.issubset(new_desc[k]):
    #                     add=False
    #                     break
    #                 if new_desc[k].issubset(intx):
    #                     new_desc[k] = intx
    #                     add=False
    #                     break
    #             if add:
    #                 new_desc.append(intx)
    #     return ToleranceBlockPattern(new_desc)

    def intersection(self, other):
        buf = []
        new_desc = []
        for i, j in product(self.desc, other.desc):
            intx = i.intersection(j)
            if len(intx) > 1: # instead of len(x) > 0
                buf.append(intx)
        buf.sort(key=lambda x: len(x))
        # print [len(i) for i in buf]
        for i in range(0, len(buf)-1):
            add = True
            for j in range(i+1, len(buf)):
                if buf[i].issubset(buf[j]):
                    add = False
                    break
            if add:
                new_desc.append(buf[i])
        # print [len(i) for i in new_desc]
        return ToleranceBlockPattern(new_desc)

    # def intersection(self, other):
    #     new_desc = []
        
    #     for i, j in product(self.desc, other.desc):
    #         intx = i.intersection(j)
    #         if len(intx) > 1: # instead of len(x) > 0
    #             add = True
    #             for k in range(len(new_desc)):
    #                 if intx.issubset(new_desc[k]):
    #                     add=False
    #                     break
    #                 elif new_desc[k].issubset(intx):
    #                     new_desc[k] = intx
    #                     add=False
    #                     break
    #             if add:
    #                 new_desc.append(intx)
                
    #     # print len(new_desc)
        
    #     return ToleranceBlockPattern(new_desc)

    def __i_le__(self, other):
        for i in self.desc:
            check = False
            for j in other.desc:
                if len(i) > len(j):
                    break
                elif i.issubset(j):
                    check = True
                    break
            if not check:
                return False
        return True

    def __i_eq__(self, other):
        raise NotImplementedError

    def __i_len__(self):
        return len(self.desc)

    def __i_contains__(self, key):
        raise NotImplementedError
    
    @staticmethod
    def sort_desc(desc):
        """
        Sort desc, necessary to ensure optimized comparisons
        """
        return sorted(desc, key=lambda x: len(x), reverse=True)