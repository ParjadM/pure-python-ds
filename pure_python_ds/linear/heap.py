from typing import List, TypeVar, Generic, Optional

T = TypeVar('T')

class MinHeap(Generic[T]):
    def __init__(self):
        self.heap: List[T] = []

    def push(self, val: T) -> None:
        self.heap.append(val)
        self._bubble_up(len(self.heap) - 1)

    def pop(self) -> Optional[T]:
        if len(self.heap) == 0: return None
        if len(self.heap) == 1: return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return root

    def _bubble_up(self, index: int):
        parent = (index - 1) // 2
        # Min-Heap check: Child < Parent
        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._bubble_up(parent)

    def _bubble_down(self, index: int):
        smallest = index
        left, right = 2 * index + 1, 2 * index + 2
        
        for child in [left, right]:
            if child < len(self.heap) and self.heap[child] < self.heap[smallest]:
                smallest = child
        
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._bubble_down(smallest)

    @property
    def size(self) -> int:
        return len(self.heap)
    @classmethod
    def heapify(cls, data: List[T]) -> 'MinHeap[T]':
        """Transforms an unsorted list into a MinHeap in O(n) time."""
        instance = cls()
        instance.heap = list(data)
        for i in range(len(instance.heap) // 2 - 1, -1, -1):
            instance._bubble_down(i)
        return instance

class MaxHeap(Generic[T]):
    """Native Max-Heap to avoid negating values for heapq-like logic."""
    def __init__(self):
        self.heap: List[T] = []

    def push(self, val: T) -> None:
        self.heap.append(val)
        self._bubble_up(len(self.heap) - 1)

    def pop(self) -> Optional[T]:
        if len(self.heap) == 0: return None
        if len(self.heap) == 1: return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return root

    def _bubble_up(self, index: int):
        parent = (index - 1) // 2
        # Max-Heap check: Child > Parent
        if index > 0 and self.heap[index] > self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._bubble_up(parent)

    def _bubble_down(self, index: int):
        largest = index
        left, right = 2 * index + 1, 2 * index + 2
        
        for child in [left, right]:
            # Max-Heap check: Child > Parent
            if child < len(self.heap) and self.heap[child] > self.heap[largest]:
                largest = child
        
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._bubble_down(largest)

    @property
    def size(self) -> int:
        return len(self.heap)

    @classmethod
    def heapify(cls, data: List[T]) -> 'MaxHeap[T]':
        """Transforms an unsorted list into a MaxHeap in O(n) time."""
        instance = cls()
        instance.heap = list(data)
        for i in range(len(instance.heap) // 2 - 1, -1, -1):
            instance._bubble_down(i)
        return instance