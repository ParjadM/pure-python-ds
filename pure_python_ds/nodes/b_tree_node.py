from typing import Any, List, Optional


class BTreeNode:
    __slots__ = ["keys", "children", "leaf"]

    def __init__(self, leaf: bool = False):
        self.keys: List[Any] = []
        self.children: List["BTreeNode"] = []
        self.leaf = leaf
