import pytest

from pure_python_ds.linear.lru_cache import LRUCache
from pure_python_ds.linear.priority_queue import PriorityQueue
from pure_python_ds.trees.bloom_filter import BloomFilter


def test_lru_cache():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) is None
    cache.put(4, 4)  # evicts key 1
    assert cache.get(1) is None
    assert cache.get(3) == 3
    assert cache.get(4) == 4


def test_priority_queue():
    pq = PriorityQueue()
    pq.push(3, "Task 3")
    pq.push(1, "Task 1")
    pq.push(2, "Task 2")

    assert len(pq) == 3
    assert pq.peek() == (1, "Task 1")
    assert pq.pop() == (1, "Task 1")
    assert pq.pop() == (2, "Task 2")
    assert pq.pop() == (3, "Task 3")

    assert pq.is_empty()
    with pytest.raises(IndexError):
        pq.pop()
    with pytest.raises(IndexError):
        pq.peek()


def test_bloom_filter():
    bf = BloomFilter(100, 0.05)
    bf.add("test_item")
    assert "test_item" in bf

    # False positives might occur, but with a good hashing distribution
    # and these parameters it's highly highly likely not to hit one here.
    assert "random_item" not in bf

    with pytest.raises(ValueError):
        BloomFilter(100, 1.5)

    with pytest.raises(ValueError):
        BloomFilter(-5, 0.05)
