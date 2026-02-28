from typing import List, TypeVar, Optional

T = TypeVar('T')

def binary_search(arr: List[T], target: T) -> Optional[int]:
    """
    Perform O(log n) Binary Search on a sorted list.
    Returns the index of the target, or None if not found.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return None