import sys
import copy
from itertools import chain
from fca.reader import FormalContextManager
from fca.algorithms import lexo

class PatternEnumerator(object):
    """
    Abstract class for PatternEnumerator
    This class is used with a version of Pattern Structures that supports a PatternEnumerator.
    The PatternEnumerator should correspond to a pattern structure definition, however at
    point the implementations remain independent for performance issues.
    PatternEnumerator should provide a canonical test for descriptions.
    It also should keep a record of different enumerations as CbO is a recursive algorithm.
    Each recursion asks for a ticket from the enumerator, the enumerator assings a ticket to
    a new enumeration of the patterns.
    """
    def __init__(self, ctx):
        """
        Creates a new PatternEnumerator from a formal context
        """
        self.ctx = ctx
        self.tally = []
        self._ticket_number = 0
    
    @property
    def next_ticket_number(self):
        """
        Returns the next ticket number
        """
        return self._ticket_number + 1

    def bottom(self, pattern):
        """
        Returns a representation of the bottom description (if possible)
        as it is the first enumerated
        """
        raise NotImplementedError
    def new_ticket(self, old_ticket, depth=0):
        """
        Creates a new ticket for the current recursion and registers it in the tally
        @param old_ticket: int ticket number for the parent recursion
        @param depth: int depth in the recursion, used for debugging
        """
        self._ticket_number = self.next_ticket_number
        return self._ticket_number

    def pop_tally(self):
        self.tally.pop()
        self._ticket_number -= 1

    def next(self, ticket, current_description, depth=0):
        """
        Obtain the next element in the enumeration for the given ticket
        @param ticket: int ticket number for the current recursion
        @param current_description: ? current element in the enumeration
        @param depth: int depth in the recursion, used for debugging
        """
        raise NotImplementedError
    def next_objects(self, ticket, current_description, current_objects, depth=0):
        """
        Returns a list of candidate objects that respects the current description
        This list will be intersected with the extent of the previous recursion and thus,
        it does not need to be the exact list of objects that respects the
        current_description, but should at least not contain the objects
        that should be removed by going from the previous enumeration to 
        the current enumeration
        @param ticket: int ticket number for the current recursion
        @param current_description: ? current element in the enumeration
        @param depth: int depth in the recursion, used for debugging
        """
        raise NotImplementedError
    def canonical_test(self, ticket, current_element, new_element, depth=0):
        """
        Performs a canonical test to know if a new_element has already appeared
        in the enumeration
        @param ticket: int ticket number for the current recursion
        @param current_description: ? current element in the enumeration
        @param depth: int depth in the recursion, used for debugging
        return bool
        """
        raise NotImplementedError

#####################################################################################
#### SetObjectEnumerator
#####################################################################################

class SetObjectEnumerator(PatternEnumerator):
    """
    SetObjectEnumerator factors out some mechanics of classic CbO
    """
    def __init__(self, ctx):
        super(SetObjectEnumerator, self).__init__(ctx)
        self.bot_rep = set([]) # The bottom representation for Set Descriptions is an empty set
        self.first = 0 # First element at each enumeration
        self.end = len(self.ctx.attributes) # Last element at each enumeration
        self.calls = 0 # Registers the numbers of calls made to next
        self.tally.append(self.first) # Starts with a dummy element in the tally

    def bottom(self, pattern):
        return pattern.bottom(self.bot_rep)

    def new_ticket(self, old_ticket=0, depth=0):
        """
        Creates a new ticket and starts a new enumeration, 
        starts enumeration from the previous recursion enumeration
        """
        old_j = self.tally[old_ticket]
        self.tally.append(old_j)
        return super(SetObjectEnumerator, self).new_ticket(old_ticket, depth)


    def next(self, ticket, current_description, depth=0):
        """
        Gets the new element in the enumeration
        We return an element that is already tested that it does not appear in
        the description of the current recursion
        Before returning, we set the element to start the enumeration in the next next()
        """
        self.calls += 1
        for j in range(self.tally[ticket], self.end):
            if j not in current_description:
                self.tally[ticket] = j+1
                return j
        self.pop_tally()
        return None

    def next_objects(self, ticket, current_description, current_objects, depth=0):
        """
        In this case we return the objects that correspond to the current element
        in the enumeration
        """
        return current_objects.intersection(self.ctx.m_prime[current_description])

    def canonical_test(self, ticket, current_element, new_element, depth=0):
        """
        Applies canonical test to a description
        """
        mask = set(range(self.tally[ticket]))
        return lexo(current_element.intersection(mask), new_element.intersection(mask))

#####################################################################################
#### IntervalObjectEnumerator
#####################################################################################

class IntervalObjectEnumerator(PatternEnumerator):
    """
    IntervalObjectEnumerator implements the enumeration part of the CbO for
    Interval Patterns
    The enumeration of intervals is done by a method called left-right-branching
    through which, given an interval [a,b] we first enumerate
    [a, b-1] which we call left branching and then
    [a-1, b] which we call right branching
    The enumeration goes left-branching->right_branching, however through
    CbO recursion, in between both branching we apply the same mechanisnm until the
    lenght of the interval is 0
    Example:
    [1,4]-l>[1,3]-l>[1,2]-l>[1,1]
                         -r>[2,2]
                 -r>[2,3]-l>[2,2]
                         -r>[3,3]
         -r>[2,4]-l>[2,3]-l>[2,2]
                         -r>[3,3]
                 -r>[3,4]-l>[3,3]
                         -r>[4,4]
    Clearly, this leads to redundant interval enumerations which can simply avoided
    by restricting branching to just right-branching after a right-branching
    Thus, we have
    [1,4]-l>[1,3]-l>[1,2]-l>[1,1]
                         -r>[2,2]
                 -r>[2,3]
                         -r>[3,3]
         -r>[2,4]

                 -r>[3,4]
                         -r>[4,4]
    Which yields no redundant intervals
    Clearly, as we are dealing with n-dimensional vectors of intervals, we apply
    this mechanism from dimension 0 to dimension (n-1)
    We keep a record of the next branching and the dimension to apply it to in tally
    thus, the first enumeration is 'l', 0
    *********************************
    Since evaluating interval subsumption is an expensive task, instead we keep track
    of the objects to be removed from the extent by the "next enumeration" by
    keeping a table of the values for each dimension that objects take
    For example, the database
    1 2 3
    2 3 4
    2 3 4
    Generates the table:
    {
        0: {
            1:set([0]),
            2:set([1, 2])
           },
        1: {
            2:set([0]),
            3:set([1, 2])
        },
        2: {
            3:set([0]),
            4:set([1, 2])
        }
    }
    The table indicates that in dimension 0, value 1 is held by objects 0,
    while value 2 is held by objects 1 and 2, and so on
    When we apply a branching action, this is what happens
    <[1, 2], [2, 3], [3, 4]> with ('l', 0) yields <[1, 1], [2, 3], [3, 4]>
    we keep value 2 extracted from dimension 1, so we know that the new extent
    cannot have objects set([1, 2])
    next_objects() returns set([0, 1, 2]) - set([1, 2]) = set([0])
    since these objects will be intersected with the previous extent
    this result is good enough
    *********************************
    When the dimension being processed is over 0, then only shinkings in that
    dimension will be "new" and the canonical test should pass for this new
    description
    e.g.
    
    <[1, 2], [2, 3], [3, 4]> with ('l', 1) yields <[1, 2], [2, 2], [3, 4]>
    Let the closure of this interval vector be:
    <[1, 1], [2, 2], [3, 4]>, then we know this interval should have already been 
    calculated as dimension 0 has "shrinked" (and thus, should have been already
    found)
    Otherwise, if the closure of the interval would be:
    <[1, 2], [2, 2], [3, 3]>, then there is no problem and the canonical
    test can pass
    """
    def __init__(self, ctx):
        super(IntervalObjectEnumerator, self).__init__(ctx)


        self.whole_g = set(ctx.objects) # A set with all the objects

        self.object_table = {} # Keeps an object_table of dimensions->Values->Objects
        for obj, desc in ctx.g_prime.items():
            for i, interval in enumerate(desc):
                self.object_table.setdefault(i, {}).setdefault(interval[0], set([])).add(obj)


        self.bot_rep = [] # Bottom representation is the largest possible interval
        for dim in self.object_table:
            values = sorted(self.object_table[dim].keys())
            self.bot_rep.append((values[0], values[-1]))

        # First action: Taking the value from the left of the first dimension
        # the last value in the triple is the value taken out of the 
        # interval, inially is set to zero
        self.first = (False, 0, 0)

        # USUALLY THE TALLY KEEPS TRACK OF THE NEXT ACTION
        # IN THIS CASE WE WILL ALSO KEEP TRACK OF THE PREVIOUS ACTION
        
        self.tally.append(self.first) # Dummy element in the tally
        self.calls = 0

    def bottom(self, pattern):
        return pattern.bottom(self.bot_rep)

    def canonical_test(self, ticket, current_element, new_element, depth=0):
        """
        Given X=<i_1, i_2, i_3 ..., i_n> and Y=<j_1, j_2, j_3, ..., j_n>
        where i's and j's are intervals [l, r] where length([l, r]) = r-l
        then canonical_test(X, Y) == True iff
        X <= Y w.r.t. interval vector pattern order and
        \forall k \in {1, n} we have that length(i_k) <= length(j_k)
        
        The first condition is supposed to be true in this call and we do not
        verify it

        Notice that we "trunk" the vectors using the dimension from 
        the current enumeration to test the canonical order

        e.g.
        canonical_test(<[1, 3], [4, 5]>, <[1, 2], [3, 5]>) is False
        """
        dim = self.tally[ticket][1] - int(self.tally[ticket][0])
        
        for i in range(0, dim):
            le1, ri1 = current_element[i]
            le2, ri2 = new_element[i]
            if ri1-le1 > ri2 - le2:
                return False
        return True

    def new_ticket(self, old_ticket, depth=0):
        """
        We create a new ticket for the new action in the recursion
        It should start in the same dimension, and the same branch
        The same branch because after right-branching we require right-branching
        to avoid for redundant intervals
        left-branching after left-branching is ok becuase left-branching is
        the first action, right-branching can be executed but will be
        checked next. The last action for the new_ticket starts empty
        """
        
        branch, old_dim = self.tally[old_ticket][:2]
        self.tally.append((not branch, old_dim - int(branch), 0))
        return super(IntervalObjectEnumerator, self).new_ticket(old_ticket, depth)

    def next(self, ticket, current_description, depth=0):
        """
        Next element in the enumeration follows the logic described
        in the doc of the class __init__
        """
        self.calls += 1
        next_description = copy.copy(current_description)

        # obtain the action, dimension and branching to apply
        
        branching, current_dimension = self.tally[ticket][:2]

        '''
        We check for the dimension to process, if the current dimension has achieved
        zero-length, then we should start processing the next dimension and
        reset the branching if it was set for right-branching
        '''
        while current_dimension < len(current_description) and \
        current_description[current_dimension][1] - current_description[current_dimension][0] == 0:
            current_dimension += 1
            branching = True
        # If the we have run out of dimensions, the enumeration has ended
        if current_dimension == len(current_description):
            self.pop_tally()
            return None

        '''
        BRANCHINGS: at this point we know the dimension to process and that it is is not
        a zero-length interval
        
        Left branching means that the next description will be "shrinked"
        by the right [a, b] -> [a, b-1]
        We apply this in the current_dimension and create the next action,
        i.e. right-branching in the current dimension
        We also keep tally of the value removed for next_objects
        ************************************************
        Right branching means that the next description will be "shrinked"
        by the left [a, b] -> [a-1, b]
        We apply this in the current_dimension and create the next action,
        i.e. left-branching in the next dimension
        Recall that this next action is the one in the current recursion
        the actual next action executed will be built through new_ticket
        '''
        next_description[current_dimension] = (
            current_description[current_dimension][0] + int(not branching),
            current_description[current_dimension][1] - int(branching)
        )

        self.tally[ticket] = (
            (
                not branching,
                current_dimension + int(not branching),
                current_description[current_dimension][int(branching)]
            )
        )
        return next_description

    def next_objects(self, ticket, current_description, current_objects, depth=0):
        branch, dim, value = self.tally[ticket]
        dim -= int(branch)
        return current_objects - self.object_table[dim][value]


#####################################################################################
#### MultiSetObjectEnumerator
#####################################################################################

class MultiSetObjectEnumerator(PatternEnumerator):
    """
    MultiSetObjectEnumerator factors out some mechanics of classic CbO
    The enumeration of partitions is a straghtforward method
    We begin with the finest partition of the set of attributes M
    which we wil denote as a|b|c|d with 4 attributes
    To enumerate, we manage 2 positions over the partition, a fixed point and 
    an iterator, both in [0, 3]
    When these values are (0,1), respectively we have that the first element
    of the partition is merged with the first element of the partion and
    thus a|b|c|...|m with (0, 1) yields ab|c|..|m
    The next element in the current recursion is (0, 2) however, the next
    element in the proceeding recursion is (0, 1) as well
    Let us denote by (r, f, i) the recursion, fixed element and iterator
    numbers, then the enumeration follows for the finest partition a|b|c
    a|b|c -(0,0,1)> (ab|c) -(1,0,1)> (abc) 
          -(0,0,2)> (ac|b) -(1,0,1)> (abc)
          -(0,1,2)> (a|bc) -(1,0,1)> (abc)
    
    We can avoid some redundant enumerations 
    
    
    """
    def __init__(self, ctx):
        super(MultiSetObjectEnumerator, self).__init__(ctx)
        self.signatures = [] # Keeps an object_table of dimensions->Values->Objects
        self.reps = {}
        self.len_rep = 0
        print self.ctx.g_prime
        for desc in ctx.g_prime.values():
            # self.bot_rep = sorted([set([i]) for i in chain(*desc)])
            desc.sort()
            for i, atts in enumerate(sorted(desc, key=min)):
                for att in atts:
                    self.reps.setdefault(att, []).append(i)
            # print sorted(desc, key=lambda s: min(s))
            # break
        # print ()
        self.len_rep = len(self.reps[self.reps.keys()[0]])
        part = {}
        for k, v in self.reps.items():
            part.setdefault(tuple(v), []).append(k)
        self.row_sets = {}
        for desc in ctx.g_prime.values():
            # self.bot_rep = sorted([set([i]) for i in chain(*desc)])
            desc.sort()
            for i, atts in enumerate(sorted(desc, key=min)):
                for att in atts:
                    self.row_sets.setdefault(att, set([]))
                    self.row_sets[att].add((len(self.row_sets[att]),i))


        print self.row_sets
        print self.reps
        # print()
        # print part
        # exit()
        # print self.reps
        # print ctx.g_prime
        self.bot_rep = sorted([set(v) for v in part.values()])
        self.trials = 0
        self.first = (0, 1) # First element at each enumeration
        self.end = len(self.bot_rep) # Last element at each enumeration
        self.calls = 0 # Registers the numbers of calls made to next
        self.tally.append(self.first) # Starts with a dummy element in the tally
        self.g_prime = ctx.g_prime
        self.cache = {}
        self.last_discarted = [[None, None]]
        # self.signatures.append([copy.copy(self.reps[0]), copy.copy(self.reps[0])])

    def bottom(self, pattern):
        return pattern.bottom(self.bot_rep)

    def new_ticket(self, old_ticket=0, depth=0):
        """
        Creates a new ticket and starts a new enumeration,
        starts enumeration from the previous recursion enumeration
        """
        old_j = self.tally[old_ticket]
        self.tally.append((old_j[0], old_j[0]+1))
        self.last_discarted.append([self.last_discarted[old_ticket][1], None])
        # self.signatures.append([copy.copy(self.signatures[old_ticket][1]), None])
        return super(MultiSetObjectEnumerator, self).new_ticket(old_ticket, depth)

    def index(self, desc, extent=None):
        key = tuple(sorted(desc))
        if self.cache.get(key,False):
            return self.cache[key]
        index = copy.copy(desc)
        for obj in self.g_prime.keys() if extent is None else extent:
            partition = self.g_prime[obj]
            for part in partition:
                if desc.issubset(part):
                    index.update(part)
                    break
        self.cache[key] = index
        return index

    def make_signature(self, atts):
        # print "SIGNATURE", atts
        # import random
        # satts = sorted(atts)
        # out = copy.copy(self.reps[satts[0]])
        # for att in satts[1:]:
        #     out = [s1 if s1==s2 else -1 for s1, s2 in zip(out, self.reps[att])]
        
        # if len(atts)>3:
            # print satts
            # print self.reps
            # print '=='
            # print '\t',
        for i in range(self.len_rep):
            yield reduce(lambda x, y: x if x==y else -1, [self.reps[att][i] for att in atts])
            # print [self.reps[att][i] for att in atts]
            # print ''
            # print '\t',atts,out
        # return out
        # exit()

    def next(self, ticket, current_description, depth=0, extent=None):
        """
        Gets the new element in the enumeration
        We return an element that is already tested that it does not appear in
        the description of the current recursion
        Before returning, we set the element to start the enumeration in the next next()
        """
        self.calls += 1
        
        # print ticket,

        sys.stdout.flush()
        current_position, current_element = self.tally[ticket]
        eliminate = self.last_discarted[ticket][0]
        # print ''
        # print current_description
        # print ticket, current_position, current_element, self.last_discarted[ticket]
        if eliminate is not None:
            for j in range(current_element, len(current_description)):
                # print "::", current_description
                # print "::", eliminate, current_description[j]
                if max(eliminate) < min (current_description[j]):
                    current_element = j
                    break
        self.last_discarted[ticket][0] = None
        # current_signature = self.make_signature(current_description[current_position])
        # print extent, self.tally
        for i in range(current_position, len(current_description) - 1):
            # current_signature = self.make_signature(current_description[i])
            # last_element = max(current_description[current_position])
            # j = 0
            # # print ''
            # # print 'LE', current_element, last_element
            # for j in range(current_element, len(current_description)):
            #     # print '\t::>', j, current_description[j], min(current_description[j])
            #     if last_element < min(current_description[j]):
            #         current_element = j
            #         break
            # # print 'E', current_element, last_element

            index = self.index(current_description[i], extent)

            print '\r=>',current_description[i],
            # sys.stdout.flush()

            for j in range(current_element, len(current_description)):
                print "{:100s}".format(str(current_description[j])),
                sys.stdout.flush()
                if not current_description[j].issubset(index):
                    continue
                self.trials +=1
                next_description = current_description[:i] + [current_description[i].union(current_description[j])] + current_description[i+1:j] + current_description[j+1:]

                # for ki, k in enumerate(current_description):
                #     if ki == i:
                #         next_description.append(current_description[i].union(current_description[j]))
                #     elif ki != j:
                #         next_description.append(current_description[i])
                # print '\t'*depth+'=>', next_description
                self.tally[ticket] = (i, j+1)
                # self.signatures[ticket][1] = copy.copy(current_signature)
                # for ki, k in enumerate(joint_signature):
                #     if not k:
                #         self.signatures[ticket][1][ki] = -1
                # self.signatures[ticket][0] = current_signature
                # print '\t'*depth+'->', 'Old Signature {} ==> New Signature {}'.format(current_signature, self.signatures[ticket][1])
                # print '\t'*depth+'->',self.signatures[ticket]
                # print "NEXT DESCRIPTION", next_description
                # exit()
                # print self.trials
                # print '.', 
                # sys.stdout.flush()
                self.last_discarted[ticket][1] = current_description[j]
                return next_description

            current_element = i+2
            # current_signature = [a if a == -1 else b for a,b in zip(current_signature, self.make_signature(current_description[i+1]))]

            # TODO: WE CAN PUT SOME KIND OF MIN SUP THRESHOLD HERE
            # if sum([a >= 0 for a in current_signature]) < 6:
            #     print sum([a >= 0 for a in current_signature]), current_signature
            #     break

        self.pop_tally()
        # self.signatures.pop()
        # print self.trials
        return None

    def next_objects(self, ticket, current_description, current_objects, depth=0):
        """
        In this case we return the objects that correspond to the current element
        in the enumeration
        """
        current_position, current_element = self.tally[ticket]
        nobjects = [i[0] for i in reduce(lambda x, y: x.intersection(y), [self.row_sets[i] for i in current_description[current_position]])]
        return current_objects.intersection(nobjects)#, current_objects, out

        # current_position, current_element = self.tally[ticket]
        # current_signature = self.make_signature(current_description[current_position])

        # out = current_objects.intersection(
        #     set([i for i, j in enumerate(current_signature) if j != -1])
        # )
        
        # return out


    def canonical_test(self, ticket, current_element, new_element, depth=0):
        """
        Applies canonical test to a description
        """
        # print current_element, new_element,
        fixed_position, iterator = self.tally[ticket]
        for i in range(0, fixed_position):
            part1 = current_element[i]
            part2 = new_element[i]
            if len(part2) > len(part1):
                # print False
                return False
        
        # print(current_element.desc[fixed_position].union(current_element.desc[iterator-1]), new_element.desc[fixed_position], lexo(current_element.desc[fixed_position].union(current_element.desc[iterator-1]), new_element.desc[fixed_position]))
        # print lexo(current_element[fixed_position].union(current_element[iterator-1]), new_element[fixed_position])
        return lexo(current_element[fixed_position].union(current_element[iterator-1]), new_element[fixed_position])
        # return True