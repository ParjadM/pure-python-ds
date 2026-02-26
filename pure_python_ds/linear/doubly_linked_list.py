from typing import Generic, TypeVar, Optional, Generator
from pure_python_ds.nodes import ListNode

T = TypeVar('T')

class DoublyLinkedList(Generic[T]):
    """A strictly typed, memory-optimized Doubly Linked List."""
    
    def __init__(self):
        self.head: Optional[ListNode[T]] = None
        self.tail: Optional[ListNode[T]] = None
        self._length: int = 0

    def __len__(self) -> int:
        return self._length

    def append(self, value: T) -> None:
        """Adds a node to the end in O(1) time."""
        new_node = ListNode(value)
        if not self.head or not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self._length += 1

    def prepend(self, value: T) -> None:
        """Adds a node to the beginning in O(1) time."""
        new_node = ListNode(value)
        if not self.head or not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self._length += 1

    def remove_tail(self) -> Optional[T]:
        """Removes the last node in O(1) time (Impossible in Singly Linked Lists!)."""
        if not self.tail:
            return None
            
        value = self.tail.value
        if self.head is self.tail: # Only one element
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None # Sever the tie
            
        self._length -= 1
        return value

    def __iter__(self) -> Generator[T, None, None]:
        """Forward generator traversal."""
        current = self.head
        while current:
            yield current.value
            current = current.next

    def __str__(self) -> str:
        """Visual representation showing bidirectional pointers."""
        values = [str(val) for val in self]
        return "None <- " + " <-> ".join(values) + " -> None" if values else "Empty List"