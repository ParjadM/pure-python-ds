"""
Disjoint Set Union (DSU) implementation.
"""

from collections.abc import Hashable, Iterable
from typing import Generic, Optional, TypeVar

T = TypeVar("T", bound=Hashable)


class DisjointSet(Generic[T]):
    """
    A Disjoint Set Union (DSU) or Union-Find data structure.

    This data structure keeps track of a set of elements partitioned into a number
    of disjoint (non-overlapping) subsets. It provides near-constant-time
    operations to add new sets, merge existing sets, and determine whether
    elements are in the same set.

    Optimizations used:
    - Path Compression: Flattens the structure of the tree whenever find is used.
    - Union by Rank: Attaches the shorter tree to the root of the taller tree.
    """

    def __init__(self, items: Optional[Iterable[T]] = None) -> None:
        self._parent: dict[T, T] = {}
        self._rank: dict[T, int] = {}
        self._count: int = 0  # Number of disjoint sets

        if items:
            for item in items:
                self.add(item)

    @property
    def count(self) -> int:
        """Return the number of disjoint sets."""
        return self._count

    def add(self, item: T) -> None:
        """
        Add a new element to the set.

        If the element already exists, this operation does nothing.
        """
        if item not in self._parent:
            self._parent[item] = item
            self._rank[item] = 0
            self._count += 1

    def find(self, item: T) -> T:
        """
        Find the representative of the set containing the item.

        Applies path compression.
        """
        if item not in self._parent:
            raise KeyError(f"Item {item!r} not found in DisjointSet")

        if self._parent[item] != item:
            self._parent[item] = self.find(self._parent[item])
        return self._parent[item]

    def union(self, item1: T, item2: T) -> bool:
        """
        Union the sets containing item1 and item2.

        Returns True if a merge happened, False if they were already in the same set.
        Applies union by rank.
        """
        root1 = self.find(item1)
        root2 = self.find(item2)

        if root1 != root2:
            # Union by rank
            if self._rank[root1] < self._rank[root2]:
                self._parent[root1] = root2
            elif self._rank[root1] > self._rank[root2]:
                self._parent[root2] = root1
            else:
                self._parent[root2] = root1
                self._rank[root1] += 1

            self._count -= 1
            return True

        return False

    def connected(self, item1: T, item2: T) -> bool:
        """Check if two items are in the same set."""
        return self.find(item1) == self.find(item2)

    def __contains__(self, item: T) -> bool:
        """Check if an item is in the Disjoint Set."""
        return item in self._parent

    def __len__(self) -> int:
        """Return the number of elements in the Disjoint Set."""
        return len(self._parent)
