from typing import List


class SegmentTree:
    def __init__(self, data: List[int]):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        # Build the tree
        for i in range(self.n):
            self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, value: int):
        """Update a value at a specific index in O(log n)."""
        index += self.n
        self.tree[index] = value
        while index > 1:
            self.tree[index >> 1] = self.tree[index] + self.tree[index ^ 1]
            index >>= 1

    def query(self, left: int, right: int) -> int:
        """Query the sum in range [left, right) in O(log n)."""
        res = 0
        left += self.n
        right += self.n
        while left < right:
            if left & 1:
                res += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                res += self.tree[right]
            left >>= 1
            right >>= 1
        return res
