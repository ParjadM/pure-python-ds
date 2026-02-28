from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class ListNode(Generic[T]):
    __slots__ = ['value', 'next', 'prev']
    def __init__(self, value: T):
        self.value: T = value
        self.next: Optional['ListNode[T]'] = None
        self.prev: Optional['ListNode[T]'] = None

    def __repr__(self) -> str:
        return f"ListNode(value={self.value})"

class TreeNode(Generic[T]):
    # SYSTEM UPGRADE: Added 'height' for O(1) AVL balance calculations
    __slots__ = ['value', 'left', 'right', 'height']
    
    def __init__(self, value: T):
        self.value: T = value
        self.left: Optional['TreeNode[T]'] = None
        self.right: Optional['TreeNode[T]'] = None
        self.height: int = 1  # New nodes start at height 1

    def __repr__(self) -> str:
        return f"TreeNode(value={self.value}, height={self.height})"