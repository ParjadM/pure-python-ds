from typing import Dict, Generic, Optional, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class _LRUNode(Generic[KT, VT]):
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: KT, value: VT):
        self.key = key
        self.value = value
        self.prev: Optional["_LRUNode[KT, VT]"] = None
        self.next: Optional["_LRUNode[KT, VT]"] = None


class LRUCache(Generic[KT, VT]):
    """
    Least Recently Used (LRU) Cache implementing O(1) get and put operations
    using a Hash Map and a Doubly Linked List.
    """

    __slots__ = ("capacity", "_cache", "_head", "_tail")

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0")
        self.capacity = capacity
        self._cache: Dict[KT, _LRUNode[KT, VT]] = {}

        # Dummy head and tail to avoid edge cases
        self._head = _LRUNode[KT, VT](None, None)  # type: ignore
        self._tail = _LRUNode[KT, VT](None, None)  # type: ignore
        self._head.next = self._tail
        self._tail.prev = self._head

    def __len__(self) -> int:
        return len(self._cache)

    def _remove_node(self, node: _LRUNode[KT, VT]) -> None:
        """Removes an existing node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: _LRUNode[KT, VT]) -> None:
        """Adds a node directly after the dummy head."""
        node.prev = self._head
        node.next = self._head.next

        if self._head.next:
            self._head.next.prev = node
        self._head.next = node

    def get(self, key: KT) -> Optional[VT]:
        """Gets value by key. Returns None if key doesn't exist."""
        if key not in self._cache:
            return None

        node = self._cache[key]
        self._remove_node(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: KT, value: VT) -> None:
        """Adds or updates a key-value pair in the cache."""
        if key in self._cache:
            node = self._cache[key]
            node.value = value
            self._remove_node(node)
            self._add_to_front(node)
        else:
            if len(self._cache) >= self.capacity:
                lru_node = self._tail.prev
                if lru_node and lru_node != self._head:
                    self._remove_node(lru_node)
                    del self._cache[lru_node.key]

            new_node = _LRUNode(key, value)
            self._cache[key] = new_node
            self._add_to_front(new_node)
