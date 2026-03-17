import pytest
from pure_python_ds.algorithms.sorting import (
    heap_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    radix_sort,
)


@pytest.fixture
def sample_arrays():
    return [
        [],
        [1],
        [3, 1, 2],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 1, 4, 1, 5, 9, 2, 6, 5],
        [-1, -5, 0, 10, -3],
    ]


@pytest.fixture
def radix_arrays():
    return [
        [],
        [0],
        [5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5],
        [3, 1, 4, 1, 5, 9, 2, 6, 5],
        [100, 1, 10, 50, 200, 9],
    ]


def test_merge_sort(sample_arrays):
    for arr in sample_arrays:
        assert merge_sort(arr) == sorted(arr)


def test_quick_sort(sample_arrays):
    for arr in sample_arrays:
        assert quick_sort(arr) == sorted(arr)


def test_insertion_sort(sample_arrays):
    for arr in sample_arrays:
        assert insertion_sort(arr) == sorted(arr)


def test_heap_sort(sample_arrays):
    for arr in sample_arrays:
        assert heap_sort(arr) == sorted(arr)


def test_radix_sort(radix_arrays):
    for arr in radix_arrays:
        assert radix_sort(arr) == sorted(arr)
