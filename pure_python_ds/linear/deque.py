from typing import Any, Generic, Iterable, Optional, TypeVar

from pure_python_ds.linear.doubly_linked_list import DoublyLinkedList

T = TypeVar("T")


class Deque(Generic[T]):
    """
    A strictly typed Double-Ended Queue (Deque) Implementation.
    Built upon the existing DoublyLinkedList for O(1) push/pop on both ends.
    """

    __slots__ = ("_list",)

    def __init__(self, iterable: Optional[Iterable[T]] = None):
        self._list: DoublyLinkedList[T] = DoublyLinkedList()
        if iterable is not None:
            for item in iterable:
                self.append(item)

    def __len__(self) -> int:
        return len(self._list)

    def is_empty(self) -> bool:
        return self._list.is_empty()

    def append(self, item: T) -> None:
        """Adds an item to the right end."""
        self._list.append(item)

    def appendleft(self, item: T) -> None:
        """Adds an item to the left end."""
        self._list.prepend(item)

    def pop(self) -> T:
        """Removes and returns an item from the right end."""
        if self.is_empty():
            raise IndexError("pop from an empty deque")
        # DoublyLinkedList pop removes from the tail
        val = self._list.remove_tail()
        return val  # type: ignore

    def popleft(self) -> T:
        """Removes and returns an item from the left end."""
        if self.is_empty():
            raise IndexError("popleft from an empty deque")
        val = self._list.remove_head()
        return val  # type: ignore

    def peek(self) -> T:
        """Returns the item at the right end without removing it."""
        if self.is_empty():
            raise IndexError("peek from an empty deque")
        return self._list.tail.value  # type: ignore

    def peekleft(self) -> T:
        """Returns the item at the left end without removing it."""
        if self.is_empty():
            raise IndexError("peekleft from an empty deque")
        return self._list.head.value  # type: ignore

    def clear(self) -> None:
        """Removes all elements from the deque."""
        self._list = DoublyLinkedList()

    def __repr__(self) -> str:
        items = []
        current = self._list.head
        while current:
            items.append(repr(current.value))
            current = current.next
        return f"Deque([{', '.join(items)}])"
