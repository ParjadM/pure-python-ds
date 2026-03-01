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
    def delete(self, key: T):
        """Removes a key from the BST using recursive restructuring."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return node

        if key < node.value:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.value:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Case 1: No child or 1 child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Case 2: Two children - find inorder successor (smallest in right subtree)
            temp = self._min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        return node

    def _min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current