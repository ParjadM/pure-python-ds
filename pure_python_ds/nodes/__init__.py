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
    __slots__ = ['value', 'left', 'right']
    def __init__(self, value: T):
        self.value: T = value
        self.left: Optional['TreeNode[T]'] = None
        self.right: Optional['TreeNode[T]'] = None

    def __repr__(self) -> str:
        return f"TreeNode(value={self.value})"