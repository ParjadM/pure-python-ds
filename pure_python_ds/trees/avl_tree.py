from typing import Generic, TypeVar, Optional
from pure_python_ds.nodes import TreeNode
from pure_python_ds.trees.binary_search_tree import BinarySearchTree

T = TypeVar('T')

class AVLTree(BinarySearchTree[T]):
    """A strictly typed, self-balancing AVL Tree guaranteeing O(log n) operations."""

    def _get_height(self, node: Optional[TreeNode[T]]) -> int:
        if not node:
            return 0
        return node.height

    def _get_balance(self, node: Optional[TreeNode[T]]) -> int:
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _right_rotate(self, y: TreeNode[T]) -> TreeNode[T]:
        """Rotates the subtree to the right."""
        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        return x

    def _left_rotate(self, x: TreeNode[T]) -> TreeNode[T]:
        """Rotates the subtree to the left."""
        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        x.height = 1 + max(self._get_height(x.left), self._get_height(x.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def insert(self, value: T) -> None:
        """Public insert method that triggers the recursive balancing engine."""
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node: Optional[TreeNode[T]], value: T) -> TreeNode[T]:
        # 1. Normal BST Insert
        if not node:
            return TreeNode(value)
        elif value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node # Duplicate keys not allowed

        # 2. Update height of current node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # 3. Get the balance factor
        balance = self._get_balance(node)

        # 4. Mathematically balance the tree (The 4 Cases)
        # Left Left Case
        if balance > 1 and value < node.left.value:
            return self._right_rotate(node)
        # Right Right Case
        if balance < -1 and value > node.right.value:
            return self._left_rotate(node)
        # Left Right Case
        if balance > 1 and value > node.left.value:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        # Right Left Case
        if balance < -1 and value < node.right.value:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node