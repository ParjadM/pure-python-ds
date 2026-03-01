import pytest
from pure_python_ds.linear import Stack, Queue, MinHeap, HashTable, DoublyLinkedList
from pure_python_ds.trees import AVLTree, Trie, SegmentTree, RedBlackTree, BTree, BinarySearchTree
from pure_python_ds.graphs import Graph, DSU
from pure_python_ds.algorithms import merge_sort, binary_search, fibonacci

def test_algorithms():
    # Sorting & Searching
    arr = [34, 7, 23, 32, 5, 62]
    sorted_arr = merge_sort(arr)
    assert sorted_arr == [5, 7, 23, 32, 34, 62]
    assert binary_search(sorted_arr, 32) == 3
    
    # Dynamic Programming
    assert fibonacci(10) == 55

def test_specialist_trees():
    # Red-Black Tree
    rbt = RedBlackTree[int]()
    for x in range(1, 6): rbt.insert(x)
    assert rbt.root.value != 1 # Proves rotation occurred
    
    # B-Tree
    bt = BTree[int](3)
    for x in [10, 20, 5, 6, 12]: bt.insert(x)
    assert len(bt.root.keys) > 0

    # BST
    bst = BinarySearchTree[int]()
    bst.insert(5); bst.insert(3); bst.insert(7)
    assert bst.search(3) is not None

def test_linear_extras():
    # Doubly Linked List
    dll = DoublyLinkedList[int]()
    dll.append(1); dll.append(2)
    assert dll.head.value == 1
    assert dll.tail.value == 2

def test_graph_specialists():
    g = Graph[str](directed=True)
    g.add_edge("A", "B", -1)
    g.add_edge("B", "C", 4)
    g.add_edge("A", "C", 3)
    
    # Bellman-Ford
    bf = g.bellman_ford("A")
    assert bf["C"] == 3 # Path A->B->C is 3, A->C is 3
    
    # DSU
    dsu = DSU(10)
    dsu.union(1, 2)
    assert dsu.find(1) == dsu.find(2)