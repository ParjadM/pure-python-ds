from pure_python_ds.trees import SegmentTree

# Mocking the LeetCode Problem: Range Sum Query - Mutable
# Problem: Given an array nums, handle multiple queries of:
# 1. Update the value of an element at a given index.
# 2. Return the sum of elements between two indices.


def solve_leetcode_307():
    print("--- LeetCode 307 Simulation ---")

    # Input from LeetCode
    nums = [1, 3, 5]

    # Using YOUR library to solve it
    obj = SegmentTree(nums)

    # Query: sumRange(0, 2) -> 1 + 3 + 5
    param_1 = obj.query(0, 3)  # Our query is [left, right), so 0, 3
    print(f"Query (0, 2): {param_1}")  # Expected: 9

    # Update: update(1, 2) -> nums is now [1, 2, 5]
    obj.update(1, 2)
    print("Updated index 1 to value 2.")

    # Query: sumRange(0, 2) -> 1 + 2 + 5
    param_2 = obj.query(0, 3)
    print(f"Query (0, 2) after update: {param_2}")  # Expected: 8


if __name__ == "__main__":
    solve_leetcode_307()
