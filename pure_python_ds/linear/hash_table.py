from typing import Any, List, Optional

from pure_python_ds.linear.singly_linked_list import SinglyLinkedList


class HashTable:
    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[Optional[SinglyLinkedList]] = [None] * size

    def _hash(self, key: str) -> int:
        return sum(ord(char) for char in key) % self.size

    def set(self, key: str, value: Any):
        index = self._hash(key)
        lst = self.table[index]
        if lst is None:
            lst = SinglyLinkedList()
            self.table[index] = lst

        # Check if key exists to update, else append
        current = lst.head
        while current:
            if current.value[0] == key:
                current.value = (key, value)
                return
            current = current.next
        lst.append((key, value))

    def get(self, key: str) -> Any:
        index = self._hash(key)
        lst = self.table[index]
        if lst is None:
            return None
        current = lst.head
        while current:
            if current.value[0] == key:
                return current.value[1]
            current = current.next
        return None
