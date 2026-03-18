class UFDS:
    def __init__(self, n):
        """
        Initialize Union-Find Disjoint Set (UFDS) with n elements.
        """
        self.parents = list(range(n))
        self.ranks = [0] * n
        self.sizes = [1] * n
        self.numdisjoint = n

    def find(self, x):
        """
        Find the representative of the set containing x with path compression.
        """
        if self.parents[x] != x:
            self.parents[x] = self.find(self.parents[x])  # Path compression
        return self.parents[x]

    def union(self, a, b):
        """
        Union the sets containing a and b.
        """
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return

        # Union by rank
        if self.ranks[root_a] < self.ranks[root_b]:
            self.parents[root_a] = root_b
            self.sizes[root_b] += self.sizes[root_a]
        else:
            self.parents[root_b] = root_a
            self.sizes[root_a] += self.sizes[root_b]
            if self.ranks[root_a] == self.ranks[root_b]:
                self.ranks[root_a] += 1

        self.numdisjoint -= 1

    def size(self, x):
        """
        Return the size of the set containing x.
        """
        return self.sizes[self.find(x)]

    def is_same_set(self, a, b):
        """
        Check if a and b are in the same set.
        """
        return self.find(a) == self.find(b)
