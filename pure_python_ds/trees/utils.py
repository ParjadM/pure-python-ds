from typing import Optional, TypeVar

from pure_python_ds.nodes import TreeNode
from pure_python_ds.trees.binary_tree import BinaryTree
from pure_python_ds.trees.binary_search_tree import BinarySearchTree
from typing import Any
T = TypeVar("T")


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
        node.right = _build_balanced(vals[mid + 1 :])
        return node

    bst.root = _build_balanced(values)
    return bst


def visualize_binary_tree(
    node: object, prefix: str = "", is_left: bool = True, is_root: bool = True
) -> str:
    """
    Generates an ASCII visualization of a binary tree.
    """
    if node is None:
        return "None"

    # Safely extract the node's value whether the attribute is named .value or .val
    if hasattr(node, "value"):
        val = str(node.value)
    elif hasattr(node, "val"):
        val = str(node.val)
    else:
        val = str(node)

    if is_root:
        result = val + "\n"
        child_prefix = ""
    else:
        connector = "├── " if is_left else "└── "
        result = prefix + connector + val + "\n"
        child_prefix = prefix + ("│   " if is_left else "    ")

    left = getattr(node, "left", None)
    right = getattr(node, "right", None)

    if left is None and right is None:
        return result

    if left:
        result += visualize_binary_tree(left, child_prefix, True, False)
    elif right:
        result += child_prefix + "├── (None)\n"

    if right:
        result += visualize_binary_tree(right, child_prefix, False, False)
    elif left:
        result += child_prefix + "└── (None)\n"

    return result
