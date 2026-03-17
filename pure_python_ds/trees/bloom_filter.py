import hashlib
import math
from typing import Any, List


class BloomFilter:
    """
    A strictly typed, space-efficient probabilistic data structure.
    Tells you if an element is *definitely not* in the set,
    or *probably* in the set.
    """

    __slots__ = ("size", "hash_count", "bit_array")

    def __init__(self, expected_items: int, false_positive_rate: float):
        """
        Initializes the Bloom Filter dynamically calculating optimal
        bit array size and number of hash functions.
        """
        if false_positive_rate <= 0 or false_positive_rate >= 1:
            raise ValueError(
                "False positive rate must be strictly between 0 and 1."
            )

        if expected_items <= 0:
            raise ValueError("Expected items must be greater than 0.")

        # Optimal size: m = -(n * ln(p)) / (ln(2)^2)
        self.size = int(
            -(expected_items * math.log(false_positive_rate))
            / (math.log(2) ** 2)
        )

        # Optimal number of hash functions: k = (m / n) * ln(2)
        self.hash_count = max(1, int((self.size / expected_items) * math.log(2)))

        # Initialize the bit array
        self.bit_array = [False] * self.size

    def _hashes(self, item: Any) -> List[int]:
        """Generates k multiple hash digests for the given item."""
        str_item = str(item).encode("utf-8")
        results = []
        for i in range(self.hash_count):
            # We seed the hash with the index `i` to simulate multiple independent hash functions
            digest = int(
                hashlib.md5(str_item + str(i).encode("utf-8")).hexdigest(), 16
            )
            results.append(digest % self.size)
        return results

    def add(self, item: Any) -> None:
        """Adds an item to the Bloom Filter."""
        for digest in self._hashes(item):
            self.bit_array[digest] = True

    def __contains__(self, item: Any) -> bool:
        """Checks if an item is possibly in the Bloom Filter."""
        for digest in self._hashes(item):
            if not self.bit_array[digest]:
                return False
        return True
