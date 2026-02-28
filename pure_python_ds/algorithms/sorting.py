from typing import List, TypeVar

T = TypeVar('T')

def merge_sort(arr: List[T]) -> List[T]:
    """
    Perform an O(n log n) Merge Sort on a list.
    Returns a new sorted list.
    """
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    # Recursive split
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return _merge(left, right)

def _merge(left: List[T], right: List[T]) -> List[T]:
    """Helper method to merge two sorted lists into one."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result