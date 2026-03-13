import pytest

from pure_python_ds.graphs.disjoint_set import DisjointSet


def test_initialization() -> None:
    """Test initializing with and without items."""
    # Empty initialization
    ds = DisjointSet[int]()
    assert len(ds) == 0
    assert ds.count == 0

    # Initialization with items
    items = [1, 2, 3]
    ds = DisjointSet(items)
    assert len(ds) == 3
    assert ds.count == 3
    for item in items:
        assert item in ds


def test_add() -> None:
    """Test adding new and existing items."""
    ds = DisjointSet[str]()
    ds.add("A")
    assert "A" in ds
    assert ds.count == 1
    assert len(ds) == 1

    # Adding existing item should not change count or length
    ds.add("A")
    assert ds.count == 1
    assert len(ds) == 1

    ds.add("B")
    assert "B" in ds
    assert ds.count == 2


def test_find_error() -> None:
    """Test that finding a non-existent item raises KeyError."""
    ds = DisjointSet[int]([1, 2])
    assert ds.find(1) == 1

    with pytest.raises(KeyError):
        ds.find(99)


def test_union_and_connectivity() -> None:
    """Test basic union operations and connectivity checks."""
    ds = DisjointSet([1, 2, 3, 4])

    # Initially nothing is connected
    assert not ds.connected(1, 2)
    assert ds.count == 4

    # Union 1 and 2
    assert ds.union(1, 2) is True
    assert ds.connected(1, 2)
    assert ds.count == 3

    # Union 3 and 4
    assert ds.union(3, 4) is True
    assert ds.connected(3, 4)
    assert ds.count == 2

    # Union (1, 2) and (3, 4)
    assert ds.union(2, 4) is True
    assert ds.connected(1, 4)  # Transitive property
    assert ds.count == 1

    # Union already connected elements (cycle detection)
    assert ds.union(1, 3) is False
    assert ds.count == 1


def test_union_by_rank_logic() -> None:
    """
    Test that union-by-rank correctly attaches shorter trees to taller trees.
    We inspect internal state (_rank, _parent) to verify structural branches.
    """
    ds = DisjointSet([1, 2, 3, 4, 5, 6])

    # 1. Equal rank union (0 vs 0) -> Rank increments
    ds.union(1, 2)
    root_1 = ds.find(1)
    assert ds._rank[root_1] == 1

    # 2. Lower rank into Higher rank
    # {1, 2} has rank 1. {3} has rank 0.
    # Union should attach 3 to the root of {1, 2}.
    ds.union(3, 1)
    assert ds._parent[3] == root_1
    assert ds._rank[root_1] == 1  # Rank shouldn't increase

    # 3. Higher rank into Lower rank (swapped arguments)
    # {4} has rank 0. {1, 2, 3} has rank 1.
    ds.union(root_1, 4)
    assert ds._parent[4] == root_1


def test_path_compression() -> None:
    """Test that find operation flattens the tree structure."""
    ds = DisjointSet(range(5))

    # Manually construct a deep chain: 0 -> 1 -> 2 -> 3 -> 4
    # (Simulating a worst-case tree without union-by-rank)
    ds._parent[0] = 1
    ds._parent[1] = 2
    ds._parent[2] = 3
    ds._parent[3] = 4

    # Calling find(0) should traverse up to 4, and compress the path
    assert ds.find(0) == 4
    assert ds._parent[0] == 4  # 0 should now point directly to root
    assert ds._parent[1] == 4  # 1 should also point directly to root
