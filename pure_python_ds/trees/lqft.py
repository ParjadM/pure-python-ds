import hashlib
from typing import Any, Dict, Optional, Set

# Import the immutable nodes from your local package architecture
from pure_python_ds.nodes.lqft_nodes import CollisionNode, InternalNode, LeafNode, Snapshot

"""
==================================================================
 LQFT - Pure Python Reference Implementation (v2.0 Architecture)
 Architect: Parjad Minooei
 
 SYSTEMS ARCHITECTURE MILESTONES:
 1. LSM-Tree Design: O(1) Mutable Head for writes, O(log N) Persistent Body.
 2. Structural Sharing: Frozen dataclasses and interning pool for O(M log N) snapshots.
 3. Node Compaction: 32-way branching with bitmap indexing (popcount).
 4. Value Interning: Strings are deduplicated at the application level.
==================================================================
"""

class LQFTMap:
    def __init__(self):
        # 1. The Mutable Head (L0 MemTable - absorbs fast writes)
        self._mutable_head: Dict[str, str] = {}
        self._tombstones: Set[str] = set()

        # 2. The Persistent Canonical Body (SSTable - Immutable HAMT)
        self._committed_root: Optional[InternalNode] = None

        # 3. The Deduplication Pools
        self._value_pool: Dict[str, str] = {}
        self._node_pool: Dict[Any, Any] = {} # Structural Sharing Cache

        # 4. Snapshot Management
        self._generation: int = 0
        self._snapshots: Dict[int, Snapshot] = {}
        
        # Save initial empty state
        self._snapshots[0] = Snapshot(0, None)

    def _hash_key(self, key: str) -> int:
        """Returns a 64-bit integer hash."""
        return int(hashlib.md5(key.encode()).hexdigest()[:16], 16)

    def _intern_value(self, value: str) -> str:
        """Deduplicates repeated values to save memory."""
        if value not in self._value_pool:
            self._value_pool[value] = value
        return self._value_pool[value]

    def _intern_node(self, node: Any) -> Any:
        """Structural Sharing: If this exact node already exists in RAM, reuse it."""
        if node not in self._node_pool:
            self._node_pool[node] = node
        return self._node_pool[node]

    # =========================================================
    # CORE API: FAST MUTABLE OPERATIONS O(1)
    # =========================================================

    def insert(self, key: str, value: str) -> None:
        """O(1) Expected. Writes bypass the tree entirely."""
        interned_val = self._intern_value(value)
        self._mutable_head[key] = interned_val
        self._tombstones.discard(key)

    def delete(self, key: str) -> None:
        """O(1) Expected. Marks as deleted without traversing the tree."""
        if key in self._mutable_head:
            del self._mutable_head[key]
        self._tombstones.add(key)

    def search(self, key: str) -> Optional[str]:
        """O(1) or O(log N). Checks fast delta first, then persistent tree."""
        # 1. Check Mutable Delta
        if key in self._mutable_head:
            return self._mutable_head[key]
        
        # 2. Check Deletions
        if key in self._tombstones:
            return None

        # 3. Check Persistent Body
        if self._committed_root is None:
            return None
            
        key_hash = self._hash_key(key)
        return self._hamt_search(self._committed_root, key_hash, key, 0)

    # =========================================================
    # SNAPSHOT SYSTEM: O(M * log N) COMMIT PIPELINE
    # =========================================================

    def snapshot(self) -> int:
        """
        Merges the Mutable Head into a new, structurally shared Canonical Body.
        Returns a snapshot handle (generation ID).
        """
        if not self._mutable_head and not self._tombstones:
            return self._generation # Nothing changed

        new_root = self._committed_root

        # 1. Process Deletions (Tombstones)
        for key in self._tombstones:
            h = self._hash_key(key)
            new_root = self._hamt_delete(new_root, h, key, 0)

        # 2. Process Mutations (Upserts)
        for key, val in self._mutable_head.items():
            h = self._hash_key(key)
            new_root = self._hamt_put(new_root, h, key, val, 0)

        # 3. Rotate State
        self._generation += 1
        self._committed_root = new_root
        self._snapshots[self._generation] = Snapshot(self._generation, new_root)
        
        # 4. Clear Mutable Delta
        self._mutable_head.clear()
        self._tombstones.clear()

        return self._generation

    def rollback(self, generation: int) -> None:
        """Instantly restores the database to a historical state."""
        if generation not in self._snapshots:
            raise ValueError(f"Snapshot {generation} does not exist.")
        
        self._mutable_head.clear()
        self._tombstones.clear()
        self._generation = generation
        self._committed_root = self._snapshots[generation].root

    # =========================================================
    # HAMT INTERNALS: O(log_32 N) RECURSIVE ROUTING
    # =========================================================

    def _hamt_search(self, node: Any, key_hash: int, key: str, depth: int) -> Optional[str]:
        if node is None:
            return None
            
        if isinstance(node, LeafNode):
            return node.value if node.key == key else None
            
        if isinstance(node, CollisionNode):
            for leaf in node.leaves:
                if leaf.key == key: return leaf.value
            return None

        # Routing Logic for Internal Nodes
        shift = depth * 5
        if shift >= 64: return None # Max depth reached
        
        idx_in_level = (key_hash >> shift) & 0x1F
        bit = 1 << idx_in_level

        if (node.bitmap & bit) == 0:
            return None # Path does not exist

        # Popcount: Count the bits set *before* our bit to find the compacted array index
        # Python 3.10+ has int.bit_count()
        compact_idx = (node.bitmap & (bit - 1)).bit_count()
        return self._hamt_search(node.children[compact_idx], key_hash, key, depth + 1)

    def _hamt_put(self, node: Any, key_hash: int, key: str, value: str, depth: int) -> Any:
        # Case 1: Empty slot
        if node is None:
            return self._intern_node(LeafNode(key_hash, key, value))

        # Case 2: Hit an existing Leaf
        if isinstance(node, LeafNode):
            if node.key == key:
                # Exact match update
                return self._intern_node(LeafNode(key_hash, key, value))
            
            if node.key_hash == key_hash:
                # True 64-bit Hash Collision
                return self._intern_node(CollisionNode((node, LeafNode(key_hash, key, value))))
            
            # Hash mismatch: Branch out into an Internal Node
            new_internal = self._intern_node(InternalNode(0, ()))
            new_internal = self._hamt_put(new_internal, node.key_hash, node.key, node.value, depth)
            return self._hamt_put(new_internal, key_hash, key, value, depth)

        # Case 3: Hit a Collision Node
        if isinstance(node, CollisionNode):
            new_leaves = [l for l in node.leaves if l.key != key]
            new_leaves.append(LeafNode(key_hash, key, value))
            return self._intern_node(CollisionNode(tuple(new_leaves)))

        # Case 4: Traverse Internal Node
        shift = depth * 5
        idx_in_level = (key_hash >> shift) & 0x1F
        bit = 1 << idx_in_level
        compact_idx = (node.bitmap & (bit - 1)).bit_count()

        children_list = list(node.children)

        if (node.bitmap & bit) != 0:
            # Overwrite existing child path
            child = children_list[compact_idx]
            new_child = self._hamt_put(child, key_hash, key, value, depth + 1)
            if new_child is child: return node # No change
            children_list[compact_idx] = new_child
            new_bitmap = node.bitmap
        else:
            # Insert into sparse compacted array
            new_child = self._hamt_put(None, key_hash, key, value, depth + 1)
            children_list.insert(compact_idx, new_child)
            new_bitmap = node.bitmap | bit

        return self._intern_node(InternalNode(new_bitmap, tuple(children_list)))

    def _hamt_delete(self, node: Any, key_hash: int, key: str, depth: int) -> Any:
        if node is None:
            return None
            
        if isinstance(node, LeafNode):
            return None if node.key == key else node
            
        if isinstance(node, CollisionNode):
            new_leaves = tuple(l for l in node.leaves if l.key != key)
            if len(new_leaves) == 0: return None
            if len(new_leaves) == 1: return new_leaves[0]
            return self._intern_node(CollisionNode(new_leaves))

        shift = depth * 5
        idx_in_level = (key_hash >> shift) & 0x1F
        bit = 1 << idx_in_level

        if (node.bitmap & bit) == 0:
            return node # Not found

        compact_idx = (node.bitmap & (bit - 1)).bit_count()
        child = node.children[compact_idx]
        new_child = self._hamt_delete(child, key_hash, key, depth + 1)

        if new_child is child:
            return node

        children_list = list(node.children)
        if new_child is None:
            # Remove from compacted array
            children_list.pop(compact_idx)
            new_bitmap = node.bitmap & ~bit
            if not children_list: return None
            # Structural compression: if 1 leaf left, collapse the node
            if len(children_list) == 1 and isinstance(children_list[0], LeafNode):
                return children_list[0]
        else:
            children_list[compact_idx] = new_child
            new_bitmap = node.bitmap

        return self._intern_node(InternalNode(new_bitmap, tuple(children_list)))

    # =========================================================
    # DEBUG AND METRICS
    # =========================================================
    def get_stats(self) -> dict:
        return {
            "snapshots_retained": len(self._snapshots),
            "uncommitted_mutations": len(self._mutable_head) + len(self._tombstones),
            "unique_node_structures": len(self._node_pool),
            "unique_string_values": len(self._value_pool)
        }

# ---------------------------------------------------------
# Example Usage / Test Harness
# ---------------------------------------------------------
if __name__ == "__main__":
    db = LQFTMap()
    
    # 1. Fast Mutable Ingestion (O(1) into Dictionary)
    print("[*] Ingesting transient data...")
    for i in range(100):
        db.insert(f"user_{i}", "status_active")
    
    print(f"Stats Pre-Commit: {db.get_stats()}")
    
    # 2. Taking a Snapshot (Flushing Delta into Persistent HAMT)
    print("\n[*] Taking Snapshot v1...")
    v1_handle = db.snapshot()
    print(f"Stats Post-Commit: {db.get_stats()}")
    
    # 3. Modifying Data and taking Snapshot v2
    print("\n[*] Updating user_1 and user_2, deleting user_5...")
    db.insert("user_1", "status_banned")
    db.insert("user_2", "status_admin")
    db.delete("user_5")
    v2_handle = db.snapshot()
    
    # 4. Proving Structural Sharing
    # Notice how "unique_node_structures" grows very slowly! We didn't duplicate 100 users.
    print(f"Stats Post V2: {db.get_stats()}")
    print(f"User 1 current status: {db.search('user_1')}")
    print(f"User 5 current status: {db.search('user_5')}")
    
    # 5. Instant Rollback
    print("\n[*] Rolling back to Snapshot v1...")
    db.rollback(v1_handle)
    print(f"User 1 restored status: {db.search('user_1')}")
    print(f"User 5 restored status: {db.search('user_5')}")