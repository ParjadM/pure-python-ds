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
        if not self.table[index]:
            self.table[index] = SinglyLinkedList()
        
        # Check if key exists to update, else append
        current = self.table[index].head
        while current:
            if current.value[0] == key:
                current.value = (key, value)
                return
            current = current.next
        self.table[index].append((key, value))

    def get(self, key: str) -> Any:
        index = self._hash(key)
        if not self.table[index]: return None
        current = self.table[index].head
        while current:
            if current.value[0] == key: return current.value[1]
            current = current.next
        return None