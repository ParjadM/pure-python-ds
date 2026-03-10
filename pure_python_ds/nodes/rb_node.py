from enum import Enum
from typing import Any, Optional


class Color(Enum):
    RED = 0
    BLACK = 1


class RBNode:
    __slots__ = ["value", "left", "right", "parent", "color"]

    def __init__(self, value: Any):
        self.value = value
        self.left: Optional["RBNode"] = None
        self.right: Optional["RBNode"] = None
        self.parent: Optional["RBNode"] = None
        self.color = Color.RED
