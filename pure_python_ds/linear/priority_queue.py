from typing import Any, Generic, Iterable, Optional, Tuple, TypeVar

from pure_python_ds.linear.heap import MinHeap

T = TypeVar("T")


class PriorityQueue(Generic[T]):
    """
    Priority Queue implementation backed by a MinHeap.
    Elements are surfaced based on priority (lower priority number = dequeued first).
    """

    __slots__ = ("_heap",)

    def __init__(self, iterable: Optional[Iterable[Tuple[int, T]]] = None):
        self._heap: MinHeap[Tuple[int, T]] = MinHeap()
        if iterable is not None:
            for item in iterable:
                self.push(*item)

    def __len__(self) -> int:
        return self._heap.size

    def is_empty(self) -> bool:
        return self._heap.size == 0

    def push(self, priority: int, item: T) -> None:
        """Push an item with a given priority into the queue."""
        self._heap.push((priority, item))

    def pop(self) -> Tuple[int, T]:
        """Remove and return the highest priority item (lowest priority number)."""
        if self.is_empty():
            raise IndexError("pop from an empty priority queue")
        # extract_min handles raising IndexError in the heap logic, but just in case:
        val = self._heap.pop()
        if val is None:
            raise IndexError("pop from an empty priority queue")
        return val

    def peek(self) -> Tuple[int, T]:
        """Return the highest priority item without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty priority queue")
        val = self._heap.heap[0]
        if val is None:
            raise IndexError("peek from an empty priority queue")
        return val
