import pytest

from pure_python_ds.algorithms.searching import (
    binary_search,
    exponential_search,
    jump_search,
    linear_search,
)


@pytest.fixture
def sorted_arrays():
    return [
        ([], 5, -1),
        ([1], 1, 0),
        ([1], 2, -1),
        ([1, 2, 3, 4, 5], 3, 2),
        ([1, 2, 3, 4, 5], 6, -1),
        ([1, 2, 3, 4, 5], 0, -1),
        ([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 80, 7),
    ]


@pytest.fixture
def unsorted_array_for_linear():
    return [
        ([], 5, -1),
        ([3, 1, 4, 1, 5, 9, 2, 6, 5], 9, 5),
        ([3, 1, 4, 1, 5, 9, 2, 6, 5], 10, -1),
    ]


def test_binary_search(sorted_arrays):
    for arr, target, expected in sorted_arrays:
        assert binary_search(arr, target) == expected


def test_jump_search(sorted_arrays):
    for arr, target, expected in sorted_arrays:
        assert jump_search(arr, target) == expected


def test_exponential_search(sorted_arrays):
    for arr, target, expected in sorted_arrays:
        assert exponential_search(arr, target) == expected


def test_linear_search(sorted_arrays, unsorted_array_for_linear):
    for arr, target, expected in sorted_arrays:
        assert linear_search(arr, target) == expected
    for arr, target, expected in unsorted_array_for_linear:
        assert linear_search(arr, target) == expected
