from typing import Generic, TypeVar, Optional
from pure_python_ds.nodes import TreeNode
from pure_python_ds.trees.binary_tree import BinaryTree

T = TypeVar('T')

class BinarySearchTree(BinaryTree[T]):
    """A strictly typed, memory-optimized Binary Search Tree."""

    def insert(self, value: T) -> None:
        """Iterative O(log n) insertion to maintain strict order."""
        new_node = TreeNode(value)
        if not self.root:
            self.root = new_node
            return

        current = self.root
        while True:
            if value < current.value:
                if not current.left:
                    current.left = new_node
                    return
                current = current.left
            elif value > current.value:
                if not current.right:
                    current.right = new_node
                    return
                current = current.right
            else:
                # Value already exists; ignoring duplicates for strict BST rules
                return

    def find(self, value: T) -> bool:
        """Iterative O(log n) search returning True if value exists."""
        current = self.root
        while current:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def search(self, key: T) -> Optional[T]:
        """Searches for a key in the BST and returns the value if found."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        if node is None or node.value == key:
            return node
        
        if key < node.value:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    def delete(self, key: T) -> None:
        """Removes a key from the BST. Targets 100% coverage for deletion logic."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node: Optional[TreeNode[T]], key: T) -> Optional[TreeNode[T]]:
        if not node:
            return None

        if key < node.value:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.value:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Case 1 & 2: Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Case 3: Node with two children
            # Get the inorder successor (smallest in the right subtree)
            successor = self._min_value_node(node.right)
            node.value = successor.value
            # Delete the inorder successor
            node.right = self._delete_recursive(node.right, successor.value)

        return node

    def _min_value_node(self, node: TreeNode[T]) -> TreeNode[T]:
        current = node
        while current.left:
            current = current.left
        return current