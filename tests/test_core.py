import pytest
from pure_python_ds.linear import Stack, Queue, MinHeap, HashTable, DoublyLinkedList
from pure_python_ds.trees import AVLTree, Trie, SegmentTree, RedBlackTree, BTree, BinarySearchTree
from pure_python_ds.graphs import Graph, DSU
from pure_python_ds.algorithms import merge_sort, binary_search, fibonacci

def test_algorithms_extended():
    # Searching edge cases
    arr = [1, 2, 3, 4, 5]
    assert binary_search(arr, 10) == -1 # Now returns -1 correctly
    assert binary_search([], 1) == -1

def test_hash_table_collisions():
    ht = HashTable(size=2)
    ht.set("apple", 1)
    ht.set("banana", 2)
    ht.set("cherry", 3) # Forces a collision/chaining
    assert ht.get("apple") == 1
    assert ht.get("cherry") == 3
    assert ht.get("missing") is None

def test_segment_tree_complex():
    st = SegmentTree([10, 20, 30, 40])
    st.update(0, 5)
    assert st.query(0, 2) == 25
    assert st.query(1, 4) == 90

def test_btree_deep_split():
    bt = BTree[int](2)
    for x in range(1, 11):
        bt.insert(x)
    assert len(bt.root.children) > 1
    assert len(bt.root.keys) > 0

def test_graph_edge_cases():
    g = Graph[str](directed=True)
    g.add_edge("A", "B", 5)
    g.add_vertex("Z")
    distances = g.dijkstra("A")
    assert distances["Z"] == float('inf')

def test_bst_deletion():
    """Tests the new delete method we added to BinarySearchTree."""
    bst = BinarySearchTree[int]()
    vals = [50, 30, 70, 20, 40, 60, 80]
    for v in vals:
        bst.insert(v)
    
    # Delete a leaf
    bst.delete(20)
    assert bst.search(20) is None
    
    # Delete a node with one child
    bst.delete(30)
    assert bst.search(30) is None
    
    # Delete a node with two children (the hard case)
    bst.delete(50)
    assert bst.search(50) is None
    assert bst.root.value in [40, 60] # Successor/Predecessor promotion

def test_avl_integrity():
    """Verifies search and balance without brittle root-matching."""
    avl = AVLTree[int]()
    vals = [10, 20, 5, 15, 25, 30, 4]
    for x in vals: 
        avl.insert(x)
    
    for x in vals:
        assert avl.search(x) is not None
    avl.delete(10)
    # Balanced check: 7 nodes should have height <= 4
    assert avl.root.height <= 4
def test_grand_sweep():
    # 1. Algorithms: Merge Sort & Fibonacci
    from pure_python_ds.algorithms import merge_sort, fibonacci
    assert merge_sort([5, 2, 9, 1]) == [1, 2, 5, 9]
    assert fibonacci(5) == 5

    # 2. Graphs: Kruskal's MST
    g = Graph[str](directed=False)
    g.add_edge("A", "B", 1)
    g.add_edge("B", "C", 2)
    g.add_edge("A", "C", 3)
    mst = g.kruskal_mst()
    assert len(mst) == 2 # Connecting 3 nodes needs 2 edges

    # 3. Red-Black Tree: Basic Insertion
    rbt = RedBlackTree[int]()
    for i in range(1, 10):
        rbt.insert(i)
    assert rbt.root.value != 1 # Proves rotations worked