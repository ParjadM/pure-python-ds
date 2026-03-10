from pure_python_ds.trees.avl_tree import AVLTree


def test_avl_search_performance(benchmark):
    # 1. Setup Phase: Build a large tree
    tree = AVLTree()
    for i in range(10000):
        tree.insert(i)

    # 2. Execution Phase: Benchmark the search operation
    result = benchmark(tree.search, 9999)

    # 3. Verification: Ensure it returns the value we searched for
    assert result == 9999
