from typing import Generic, TypeVar, Optional
from pure_python_ds.linear.singly_linked_list import SinglyLinkedList

T = TypeVar('T')

class Queue(Generic[T]):
    """A strictly typed, memory-optimized Queue (FIFO)."""
    
    def __init__(self):
        self._container = SinglyLinkedList[T]()

    def __len__(self) -> int:
        return len(self._container)

    def enqueue(self, value: T) -> None:
        """Adds an item to the back of the queue in O(1) time."""
        self._container.append(value)

    def dequeue(self) -> Optional[T]:
        """Removes and returns the front item in O(1) time."""
        return self._container.remove_head()
        
    def __str__(self) -> str:
        return f"Queue Front -> {self._container}"