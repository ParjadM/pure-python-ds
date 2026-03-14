import hashlib
import runpy
from unittest.mock import patch

import pytest

from pure_python_ds.nodes.lqft_nodes import CollisionNode, InternalNode, LeafNode
from pure_python_ds.trees.lqft import LQFTMap


def real_hash(key: str) -> int:
    """Fallback hashing function identical to the real LQFTMap._hash_key."""
    return int(hashlib.md5(key.encode()).hexdigest()[:16], 16)


def test_mutable_head_crud():
    """Test fast O(1) mutations before any snapshot is taken."""
    db = LQFTMap()
    assert db.search("k1") is None

    db.insert("k1", "v1")
    assert db.search("k1") == "v1"

    # Update existing
    db.insert("k1", "v1_updated")
    assert db.search("k1") == "v1_updated"

    # Delete existing
    db.delete("k1")
    assert db.search("k1") is None

    # Delete non-existent
    db.delete("k2")
    assert db.search("k2") is None


def test_snapshot_and_rollback():
    """Test historical state management."""
    db = LQFTMap()
    db.insert("k1", "v1")
    gen1 = db.snapshot()

    db.insert("k2", "v2")
    db.insert("k1", "v1_mod")
    gen2 = db.snapshot()

    assert db.search("k1") == "v1_mod"
    assert db.search("k2") == "v2"

    # Rollback to Gen 1
    db.rollback(gen1)
    assert db.search("k1") == "v1"
    assert db.search("k2") is None

    with pytest.raises(ValueError, match="Snapshot 999 does not exist."):
        db.rollback(999)


def test_empty_snapshot():
    """Verify snapshot() correctly detects when nothing has changed."""
    db = LQFTMap()
    gen = db.snapshot()
    assert gen == 0


def test_snapshot_with_useless_delete():
    """Test deletion of a non-existent key going into a snapshot."""
    db = LQFTMap()
    db.insert("k1", "v1")
    db.snapshot()

    db.delete("k_non_existent")
    db.snapshot()
    assert db.search("k1") == "v1"


def test_hamt_hash_collision():
    """Force two distinct keys to have the exact same hash, triggering CollisionNode."""
    db = LQFTMap()
    with patch.object(db, "_hash_key", return_value=42):
        db.insert("k1", "v1")
        db.insert("k2", "v2")
        db.snapshot()

        assert db.search("k1") == "v1"
        assert db.search("k2") == "v2"
        assert db.search("k3") is None  # Search miss on CollisionNode


def test_hamt_collision_node_expansion_and_deletion():
    """Test operations that mutate and shrink an existing CollisionNode."""
    db = LQFTMap()
    with patch.object(db, "_hash_key", return_value=42):
        db.insert("k1", "v1")
        db.insert("k2", "v2")
        db.snapshot()

        # Expansion (Append to CollisionNode)
        db.insert("k3", "v3")
        db.snapshot()
        assert db.search("k3") == "v3"

        # Exact match update inside CollisionNode
        db.insert("k1", "v1_mod")
        db.snapshot()
        assert db.search("k1") == "v1_mod"

        # Deletion shrinking the node
        db.delete("k1")
        db.snapshot()
        assert db.search("k1") is None

        # Last deletion collapses it back into a standard LeafNode
        db.delete("k2")
        db.snapshot()
        assert db.search("k2") is None
        assert db.search("k3") == "v3"


def test_collision_node_zero_leaves_manual():
    """Edge Case: Force branch execution of 'if len(new_leaves) == 0' in CollisionNode."""
    db = LQFTMap()
    # Create an invalid state where a CollisionNode only holds 1 leaf
    bad_node = CollisionNode((LeafNode(42, "k1", "v1"),))
    db._committed_root = bad_node
    db._tombstones.add("k1")
    db.snapshot()
    assert db.search("k1") is None


def test_delete_hash_collision_miss():
    """Search and delete misses against a LeafNode with an identical hash."""
    db = LQFTMap()
    with patch.object(db, "_hash_key", return_value=42):
        db.insert("k1", "v1")
        db.snapshot()

        db.delete("k2")
        db.snapshot()
        assert db.search("k1") == "v1"
        assert db.search("k2") is None


def test_hamt_structural_compression():
    """Test the HAMT collapsing empty InternalNodes back into LeafNodes."""
    db = LQFTMap()

    def fake_hash(k):
        if k == "k1": return 1   # Level 0 = 1, Level 1 = 0
        if k == "k2": return 33  # Level 0 = 1, Level 1 = 1
        return real_hash(k)

    with patch.object(db, "_hash_key", side_effect=fake_hash):
        db.insert("k1", "v1")
        db.insert("k2", "v2")
        db.snapshot()

        # Deleting k2 leaves only k1 inside the child, collapsing the InternalNode
        db.delete("k2")
        db.snapshot()
        assert db.search("k2") is None
        assert db.search("k1") == "v1"

        # Delete k1 leaves children_list empty, returning None directly
        db.delete("k1")
        db.snapshot()
        assert db.search("k1") is None


def test_delete_collapse_false_condition():
    """Ensure the collapse block is skipped if the remaining node is not a LeafNode."""
    db = LQFTMap()

    def fake_hash(k):
        if k == "k1": return 1   # Level 0 = 1, Level 1 = 0
        if k == "k2": return 33  # Level 0 = 1, Level 1 = 1
        if k == "k3": return 33  # Collision with k2 at Level 1
        return real_hash(k)

    with patch.object(db, "_hash_key", side_effect=fake_hash):
        db.insert("k1", "v1")
        db.insert("k2", "v2")
        db.insert("k3", "v3")
        db.snapshot()

        # Deleting k1 leaves the Level 0 child with an InternalNode. It should NOT collapse.
        db.delete("k1")
        db.snapshot()

        assert db.search("k2") == "v2"
        assert db.search("k3") == "v3"
        assert db.search("k1") is None


def test_identical_insert_put_internal_node():
    """Hit branch `if new_child is child: return node` inside _hamt_put via identical upserts."""
    db = LQFTMap()

    def fake_hash(k):
        if k == "k1": return 1
        if k == "k2": return 33
        return real_hash(k)

    with patch.object(db, "_hash_key", side_effect=fake_hash):
        db.insert("k1", "v1")
        db.insert("k2", "v2")
        db.snapshot()

        db.insert("k1", "v1")
        db.snapshot()
        assert db.search("k1") == "v1"


def test_delete_internal_node_miss():
    """Misses within an InternalNode structure due to bitmap skipping."""
    db = LQFTMap()

    def fake_hash(k):
        if k == "k1": return 1
        if k == "k2": return 33
        if k == "k3": return 65  # Level 0 = 1, Level 1 = 2 (Which has a 0 bit)
        return real_hash(k)

    with patch.object(db, "_hash_key", side_effect=fake_hash):
        db.insert("k1", "v1")
        db.insert("k2", "v2")
        db.snapshot()

        # Level 1 miss
        db.delete("k3")
        db.snapshot()
        assert db.search("k3") is None
        assert db.search("k1") == "v1"

        # Level 0 miss
        db.delete("k4")
        db.snapshot()
        assert db.search("k4") is None


def test_hamt_search_max_depth():
    """Force the deepest branch depth limitation artificially."""
    db = LQFTMap()
    node = InternalNode(1, (LeafNode(0, "k", "v"),))
    assert db._hamt_search(node, 0, "k", 13) is None


def test_metrics():
    """Verify dictionary structure of the metrics property."""
    db = LQFTMap()
    db.insert("k1", "v1")
    db.snapshot()
    stats = db.get_stats()
    assert "snapshots_retained" in stats
    assert "uncommitted_mutations" in stats
    assert "unique_node_structures" in stats
    assert "unique_string_values" in stats
    assert stats["snapshots_retained"] == 2


def test_hamt_search_none_direct():
    """Directly hit the None base case in _hamt_search."""
    db = LQFTMap()
    assert db._hamt_search(None, 123, "k", 0) is None


def test_hamt_delete_none_direct():
    """Directly hit the None base case in _hamt_delete."""
    db = LQFTMap()
    assert db._hamt_delete(None, 123, "k", 0) is None


def test_lqft_main_block():
    """Execute the __main__ block for full 100% coverage."""
    # This runs the module inside the test environment simulating python -m
    with pytest.warns(RuntimeWarning, match="found in sys.modules"):
        runpy.run_module("pure_python_ds.trees.lqft", run_name="__main__")