from typing import TypeVar, Optional
from pure_python_ds.nodes import TreeNode
from pure_python_ds.trees.binary_tree import BinaryTree
from pure_python_ds.trees.binary_search_tree import BinarySearchTree

T = TypeVar('T')

def convert_to_bst(tree: BinaryTree[T]) -> BinarySearchTree[T]:
    """Converts an unstructured Binary Tree into a perfectly balanced BST."""
    # 1. Extract values using your zero-memory generator and sort them
    values = sorted(list(tree.inorder()))
    
    # 2. Rebuild a perfectly balanced tree using binary recursion
    bst = BinarySearchTree[T]()
    
    def _build_balanced(vals: list[T]) -> Optional[TreeNode[T]]:
        if not vals:
            return None
        mid = len(vals) // 2
        node = TreeNode(vals[mid])
        node.left = _build_balanced(vals[:mid])
        node.right = _build_balanced(vals[mid+1:])
        return node
        
    bst.root = _build_balanced(values)
    return bst