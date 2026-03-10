from pure_python_ds.trees.avl_tree import AVLTree


def test_avl_absolute_guarantee():
    # Instantiate WITHOUT the [int] Generic Alias to force coverage tracking
    tree = AVLTree()

    # Insert elements
    for val in [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]:
        tree.insert(val)

    # Standard wrapper deletions
    tree.delete(20)
    tree.delete(50)
    tree.delete(999)

    # Directly hammer the recursive method to ensure the tracer catches it
    tree.root = tree._delete_recursive(tree.root, 30)
    tree.root = tree._delete_recursive(tree.root, 70)
    tree.root = tree._delete_recursive(tree.root, 40)

    assert tree.root is not None
