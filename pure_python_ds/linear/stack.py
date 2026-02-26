from typing import Generic, TypeVar, Optional
from pure_python_ds.linear.singly_linked_list import SinglyLinkedList

T = TypeVar('T')

class Stack(Generic[T]):
    """A strictly typed, memory-optimized Stack (LIFO)."""
    
    def __init__(self):
        self._container = SinglyLinkedList[T]()

    def __len__(self) -> int:
        return len(self._container)

    def push(self, value: T) -> None:
        """Pushes an item onto the top of the stack in O(1) time."""
        self._container.prepend(value)

    def pop(self) -> Optional[T]:
        """Removes and returns the top item in O(1) time."""
        return self._container.remove_head()
        
    def __str__(self) -> str:
        return f"Stack Top -> {self._container}"