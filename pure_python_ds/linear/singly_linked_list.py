from typing import Generic, TypeVar, Optional, Generator
from pure_python_ds.nodes import ListNode

# Define the generic type variable
T = TypeVar('T')

class SinglyLinkedList(Generic[T]):
    """
    A strictly typed, memory-optimized Singly Linked List.
    """
    def __init__(self):
        self.head: Optional[ListNode[T]] = None
        self.tail: Optional[ListNode[T]] = None
        self._length: int = 0
        
    def __str__(self) -> str:
        """
        Provides a visual representation of the Linked List.
        Example: Future -> Systems -> Architect -> None
        """
        # We leverage our own generator to seamlessly loop through the values
        values = [str(node_val) for node_val in self]
        values.append("None")
        return " -> ".join(values)
    def __len__(self) -> int:
        """Allows the user to call len(linked_list) in O(1) time."""
        return self._length

    def append(self, value: T) -> None:
        """Adds a new node to the end of the list in O(1) time."""
        new_node = ListNode(value)
        if not self.head or not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._length += 1

    def prepend(self, value: T) -> None:
        """Adds a new node to the beginning of the list in O(1) time."""
        new_node = ListNode(value)
        if not self.head or not self.tail:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        self._length += 1

    def __iter__(self) -> Generator[T, None, None]:
        """
        Generator-based traversal. 
        Allows users to run: `for val in linked_list:` with O(1) memory overhead.
        """
        current = self.head
        while current:
            yield current.value
            current = current.next