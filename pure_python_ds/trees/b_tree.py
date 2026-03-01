from typing import Generic, TypeVar, Optional
from pure_python_ds.nodes.b_tree_node import BTreeNode

T = TypeVar('T')

class BTree(Generic[T]):
    def __init__(self, t: int):
        """
        t: Minimum degree (defines the range for number of keys).
        Every node besides root must have at least t-1 keys.
        Nodes can have at most 2t-1 keys.
        """
        self.root = BTreeNode(True)
        self.t = t

    def insert(self, k: T):
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, k)
        else:
            self._insert_non_full(root, k)

    def _insert_non_full(self, x: BTreeNode, k: T):
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == (2 * self.t) - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)

    def _split_child(self, x: BTreeNode, i: int):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t : (2 * t) - 1]
        y.keys = y.keys[0 : t - 1]
        if not y.leaf:
            z.children = y.children[t : 2 * t]
            y.children = y.children[0 : t]