from dataclasses import dataclass
from typing import Any, Optional, Tuple

@dataclass(frozen=True)
class LeafNode:
    key_hash: int
    key: str
    value: str

@dataclass(frozen=True)
class InternalNode:
    bitmap: int
    children: Tuple[Any, ...]

@dataclass(frozen=True)
class CollisionNode:
    leaves: Tuple[LeafNode, ...]

class Snapshot:
    def __init__(self, generation: int, root: Optional[InternalNode]):
        self.generation = generation
        self.root = root
        self.timestamp = __import__('time').time()