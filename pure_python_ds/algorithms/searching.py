import math
from typing import Any, List, Optional, TypeVar

T = TypeVar("T")


def binary_search(arr: List[Any], target: Any) -> int:
    """
    Performs an iterative binary search on a sorted list.
    Returns the index of the target if found, else -1.
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

    return -1


def linear_search(arr: List[Any], target: Any) -> int:
    """
    Performs an O(n) linear search on a list.
    Returns the index of the target if found, else -1.
    """
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1


def jump_search(arr: List[Any], target: Any) -> int:
    """
    Performs an O(sqrt(n)) jump search on a sorted list.
    Returns the index of the target if found, else -1.
    """
    n = len(arr)
    if n == 0:
        return -1
        
    step = int(math.sqrt(n))
    prev = 0

    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1

    while prev < min(step, n) and arr[prev] < target:
        prev += 1

    if prev < min(step, n) and arr[prev] == target:
        return prev

    return -1


def exponential_search(arr: List[Any], target: Any) -> int:
    """
    Performs an O(log i) exponential search on a sorted list.
    Returns the index of the target if found, else -1.
    """
    if not arr:
        return -1

    if arr[0] == target:
        return 0

    n = len(arr)
    i = 1
    while i < n and arr[i] <= target:
        i = i * 2

    # Perform binary search on the found range
    low = i // 2
    high = min(i, n - 1)

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1
