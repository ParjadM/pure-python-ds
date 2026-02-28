from typing import Generic, TypeVar, Optional, Generator
from pure_python_ds.nodes import TreeNode
from pure_python_ds.linear import Queue

T = TypeVar('T')

class BinaryTree(Generic[T]):
    """A strictly typed base Binary Tree with zero-memory generator traversals."""
    
    def __init__(self):
        self.root: Optional[TreeNode[T]] = None

    def insert(self, value: T) -> None:
        """Level-order insertion utilizing our custom memory-optimized Queue."""
        new_node = TreeNode(value)
        if not self.root:
            self.root = new_node
            return
        
        # Look at this! We are using your custom Queue from Phase 2.
        q = Queue[TreeNode[T]]()
        q.enqueue(self.root)
        
        while len(q) > 0:
            current = q.dequeue()
            
            if not current.left:
                current.left = new_node
                return
            else:
                q.enqueue(current.left)
                
            if not current.right:
                current.right = new_node
                return
            else:
                q.enqueue(current.right)

    def inorder(self) -> Generator[T, None, None]:
        """Left -> Root -> Right traversal"""
        def _traverse(node: Optional[TreeNode[T]]) -> Generator[T, None, None]:
            if node:
                yield from _traverse(node.left)
                yield node.value
                yield from _traverse(node.right)
        yield from _traverse(self.root)

    def preorder(self) -> Generator[T, None, None]:
        """Root -> Left -> Right traversal"""
        def _traverse(node: Optional[TreeNode[T]]) -> Generator[T, None, None]:
            if node:
                yield node.value
                yield from _traverse(node.left)
                yield from _traverse(node.right)
        yield from _traverse(self.root)

    def postorder(self) -> Generator[T, None, None]:
        """Left -> Right -> Root traversal"""
        def _traverse(node: Optional[TreeNode[T]]) -> Generator[T, None, None]:
            if node:
                yield from _traverse(node.left)
                yield from _traverse(node.right)
                yield node.value
        yield from _traverse(self.root)