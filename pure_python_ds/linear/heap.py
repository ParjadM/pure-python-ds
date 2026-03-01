from typing import List, TypeVar, Generic

T = TypeVar('T')

class MinHeap(Generic[T]):
    def __init__(self):
        self.heap: List[T] = []

    def push(self, val: T):
        self.heap.append(val)
        self._bubble_up(len(self.heap) - 1)

    def pop(self) -> T:
        if len(self.heap) == 0: return None
        if len(self.heap) == 1: return self.heap.pop()
        
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return root

    def _bubble_up(self, index: int):
        parent = (index - 1) // 2
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