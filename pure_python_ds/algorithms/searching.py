from typing import List, TypeVar, Optional, Any

T = TypeVar('T')

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