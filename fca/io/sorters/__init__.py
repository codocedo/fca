class Sorter(object):
    def __init__(self):
        self.processing_order = []

    def sort(self, g_prime):
        """
        Generates a new g_prime
        using sorting function
        """
        raise NotImplementedError

class PartitionSorter(Sorter):
    """
    Partitions should be sorted by the number of elements they contain
    in ascending order
    """
    def sort(self, g_prime):
        for i, j in sorted([(len(j), i) for i, j in g_prime.items()], reverse=True):
            self.processing_order.append(j)
        return {i:g_prime[j] for i, j in enumerate(self.processing_order)}
