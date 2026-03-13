import pytest

from pure_python_ds.algorithms import binary_search
from pure_python_ds.graphs import DisjointSet, Graph
from pure_python_ds.linear import (
    DoublyLinkedList,
    HashTable,
    MaxHeap,
    MinHeap,
    Queue,
    SinglyLinkedList,
)
from pure_python_ds.nodes import TrieNode
from pure_python_ds.nodes.b_tree_node import BTreeNode
from pure_python_ds.nodes.rb_node import RBNode
from pure_python_ds.trees import (
    AVLTree,
    BinarySearchTree,
    BinaryTree,
    BTree,
    RedBlackTree,
    Trie,
)


def test_remaining_linear_and_algo_branches():
    assert binary_search([1, 2, 3], 0) == -1

    q = Queue[int]()
    q.enqueue(1)
    assert "Queue Front" in str(q)

    dll = DoublyLinkedList[int]()
    dll.append(1)
    dll.append(2)
    assert dll.remove(1) is True
    assert dll.head is not None and dll.head.prev is None

    sll = SinglyLinkedList[int]()
    sll.prepend(1)
    sll.prepend(2)
    assert sll.remove(999) is False

    ht = HashTable(size=1)
    ht.set("dup", 1)
    ht.set("dup", 2)
    assert ht.get("dup") == 2

    minh = MinHeap[int]()
    maxh = MaxHeap[int]()
    minh.push(3)
    maxh.push(3)
    assert minh.size == 1
    assert maxh.size == 1


def test_remaining_graph_and_dsu_branches():
    dsu = DisjointSet(range(3))
    dsu.union(0, 1)
    dsu.union(2, 1)
    assert dsu.find(2) == dsu.find(0)

    g = Graph[str](directed=True)
    g.add_edge("A", "B", 10)
    g.add_edge("A", "C", 1)
    g.add_edge("C", "B", 1)
    assert g.dijkstra("A")["B"] == 2
    assert g.has_edge("Z", "Q") is False

    neg = Graph[str](directed=True)
    neg.add_edge("A", "B", 1)
    neg.add_edge("B", "C", -2)
    neg.add_edge("C", "A", 0)
    with pytest.raises(ValueError):
        neg.bellman_ford("A")


def test_remaining_tree_and_node_branches():
    trie_node = TrieNode()
    assert trie_node.children == {}
    assert trie_node.is_end_of_word is False

    trie = Trie()
    trie.insert("car")
    assert trie.search("car") is True
    trie.delete("car")
    assert trie.search("car") is False
    trie.delete("zzz")

    bt_empty = BinaryTree[int]()
    bt_empty.insert(5)
    assert bt_empty.root is not None and bt_empty.root.value == 5

    bst = BinarySearchTree[int]()
    for v in [10, 5, 15, 3, 12, 11]:
        bst.insert(v)
    assert bst.find(3) is True
    assert bst._delete_recursive(None, 1) is None
    bst.delete(1)
    bst.delete(5)
    assert bst._min_value_node(bst.root.right).value == 11

    btree = BTree[int](t=2)
    leaf = BTreeNode(True)
    leaf.keys = [10, 20]
    btree._insert_non_full(leaf, 5)
    assert leaf.keys == [5, 10, 20]

    internal = BTreeNode(False)
    internal.keys = [10, 20]
    internal.children = [BTreeNode(True), BTreeNode(True), BTreeNode(True)]
    btree._insert_non_full(internal, 5)
    assert internal.children[0].keys == [5]

    avl = AVLTree[int]()
    assert avl._get_balance(None) == 0
    avl.insert(10)
    avl.insert(10)
    assert avl.search(10) == 10

    avl_ll = AVLTree[int]()
    for v in [30, 20, 10]:
        avl_ll.insert(v)
    assert avl_ll.root is not None and avl_ll.root.value == 20

    avl_rl = AVLTree[int]()
    for v in [10, 30, 20]:
        avl_rl.insert(v)
    assert avl_rl.root is not None and avl_rl.root.value == 20

    avl_del = AVLTree[int]()
    avl_del.insert(20)
    avl_del.insert(10)
    avl_del.delete(20)
    assert avl_del.search(20) is None

    rbt_lr = RedBlackTree[int]()
    for v in [10, 5, 7]:
        rbt_lr.insert(v)
    assert rbt_lr.root != rbt_lr.NULL

    rbt_rl = RedBlackTree[int]()
    for v in [10, 15, 13]:
        rbt_rl.insert(v)
    assert rbt_rl.root != rbt_rl.NULL

    rbt_rot = RedBlackTree[int]()
    null = rbt_rot.NULL

    p = RBNode(50)
    x = RBNode(30)
    y = RBNode(40)
    p.parent = None
    p.left = x
    p.right = null
    x.parent = p
    x.left = null
    x.right = y
    y.parent = x
    y.left = null
    y.right = null
    rbt_rot.root = p
    rbt_rot._left_rotate(x)
    assert p.left == y

    p2 = RBNode(80)
    x2 = RBNode(60)
    y2 = RBNode(40)
    yr = RBNode(50)
    p2.parent = None
    p2.left = x2
    p2.right = null
    x2.parent = p2
    x2.left = y2
    x2.right = null
    y2.parent = x2
    y2.left = null
    y2.right = yr
    yr.parent = y2
    yr.left = null
    yr.right = null
    rbt_rot.root = p2
    rbt_rot._right_rotate(x2)
    assert p2.left == y2
    assert yr.parent == x2
