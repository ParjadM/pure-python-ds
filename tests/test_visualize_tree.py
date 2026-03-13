from pure_python_ds.trees.utils import visualize_binary_tree
from pure_python_ds.trees.avl_tree import AVLTree
from pure_python_ds.trees.binary_search_tree import BinarySearchTree

class DummyNode:
    """Isolated node class for testing visualization logic."""

    def __init__(self, value=None, left=None, right=None, use_val=False):
        if use_val:
            self.val = value
        else:
            self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        # Fallback if neither .value nor .val is found (for the test)
        return "Node"


class VallessNode:
    """Node with no .value or .val attributes to test string fallback."""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.data)


def test_visualize_none():
    """Test with None input."""
    assert visualize_binary_tree(None) == "None"


def test_visualize_root_only():
    """Test a tree with only a root node."""
    root = DummyNode(1)
    output = visualize_binary_tree(root)
    assert output.strip() == "1"


def test_visualize_left_only():
    """Test a tree with only a left child. Should trigger right placeholder."""
    root = DummyNode(1)
    root.left = DummyNode(2)

    expected = (
        "1\n"
        "├── 2\n"
        "└── (None)\n"
    )
    assert visualize_binary_tree(root) == expected


def test_visualize_right_only():
    """Test a tree with only a right child. Should trigger left placeholder."""
    root = DummyNode(1)
    root.right = DummyNode(3)

    expected = (
        "1\n"
        "├── (None)\n"
        "└── 3\n"
    )
    assert visualize_binary_tree(root) == expected


def test_visualize_balanced():
    """Test a perfectly balanced 3-node tree."""
    #    1
    #  2   3
    root = DummyNode(1)
    root.left = DummyNode(2)
    root.right = DummyNode(3)

    expected = (
        "1\n"
        "├── 2\n"
        "└── 3\n"
    )
    assert visualize_binary_tree(root) == expected


def test_attribute_precedence():
    """Test extracting .value, .val, and fallback to str(node)."""
    # 1. Test .val attribute
    node_val = DummyNode(10, use_val=True)
    assert "10" in visualize_binary_tree(node_val)

    # 2. Test .value attribute
    node_value = DummyNode(20, use_val=False)
    assert "20" in visualize_binary_tree(node_value)

    # 3. Test no .value or .val (fallback to __str__)
    node_str = VallessNode(99)
    assert "99" in visualize_binary_tree(node_str)
def test_tree_str_magic_methods():
    # 1. Test empty tree
    empty_bst = BinarySearchTree()
    assert str(empty_bst) == ""

    # 2. Test standard BST
    bst = BinarySearchTree()
    bst.insert(10)
    bst.insert(5)
    bst.insert(15)
    
    bst_str = str(bst)
    assert "10" in bst_str
    assert "├── 5" in bst_str
    assert "└── 15" in bst_str

    # 3. Test AVL Tree (Proves the visualizer works with auto-balancing)
    avl = AVLTree()
    avl.insert(10)
    avl.insert(20)
    avl.insert(30) # This should trigger a left rotation, making 20 the root
    
    avl_str = str(avl)
    assert avl_str.startswith("20") # 20 must be at the very top
    assert "├── 10" in avl_str
    assert "└── 30" in avl_str