import heapq
from typing import List, TypeVar

T = TypeVar("T")


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


def quick_sort(arr: List[T]) -> List[T]:
    """
    Perform an O(n log n) expected Quick Sort on a list.
    Returns a new sorted list.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def insertion_sort(arr: List[T]) -> List[T]:
    """
    Perform an O(n^2) Insertion Sort on a list.
    Efficient for small or nearly sorted arrays.
    Returns a new sorted list.
    """
    result = arr.copy()
    for i in range(1, len(result)):
        key = result[i]
        j = i - 1
        while j >= 0 and result[j] > key:
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = key
    return result


def heap_sort(arr: List[T]) -> List[T]:
    """
    Perform an O(n log n) Heap Sort on a list.
    Returns a new sorted list.
    """
    heap = arr.copy()
    heapq.heapify(heap)
    return [heapq.heappop(heap) for _ in range(len(heap))]


def radix_sort(arr: List[int]) -> List[int]:
    """
    Perform an O(nk) Radix Sort on a list of non-negative integers.
    Returns a new sorted list.
    """
    if not arr:
        return []

    max_val = max(arr)
    exp = 1
    result = arr.copy()

    while max_val // exp > 0:
        _counting_sort_by_digit(result, exp)
        exp *= 10

    return result


def _counting_sort_by_digit(arr: List[int], exp: int) -> None:
    """Helper for radix_sort to sort by a specific digit."""
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1

    for i in range(n):
        arr[i] = output[i]
