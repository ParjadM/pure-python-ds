from typing import Dict, Generic, Optional, TypeVar
from .lqft_nodes import LeafNode, InternalNode, CollisionNode, Snapshot

T = TypeVar("T")


class ListNode(Generic[T]):
    __slots__ = ["value", "next", "prev"]

    def __init__(self, value: T):
        self.value: T = value
        self.next: Optional["ListNode[T]"] = None
        self.prev: Optional["ListNode[T]"] = None


class TreeNode(Generic[T]):
    __slots__ = ["value", "left", "right", "height"]

    def __init__(self, value: T):
        self.value: T = value
        self.left: Optional["TreeNode[T]"] = None
        self.right: Optional["TreeNode[T]"] = None
        self.height: int = 1


class TrieNode:
    # FIXED: Added is_end_of_word to slots and init
    __slots__ = ["children", "is_end_of_word"]

    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end_of_word: bool = False
