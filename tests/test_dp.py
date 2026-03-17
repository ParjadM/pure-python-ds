from pure_python_ds.algorithms.dp import (
    edit_distance,
    fibonacci,
    knapsack,
    longest_common_subsequence,
    longest_increasing_subsequence,
)


def test_fibonacci():
    assert fibonacci(0) == 0
    assert fibonacci(1) == 1
    assert fibonacci(10) == 55


def test_knapsack():
    weights = [10, 20, 30]
    values = [60, 100, 120]
    capacity = 50
    assert knapsack(weights, values, capacity) == 220
    assert knapsack([1, 2, 3], [10, 15, 40], 6) == 65
    assert knapsack([], [], 50) == 0


def test_longest_common_subsequence():
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "abc") == 3
    assert longest_common_subsequence("abc", "def") == 0


def test_longest_increasing_subsequence():
    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert longest_increasing_subsequence([0, 1, 0, 3, 2, 3]) == 4
    assert longest_increasing_subsequence([7, 7, 7, 7, 7, 7, 7]) == 1
    assert longest_increasing_subsequence([]) == 0


def test_edit_distance():
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "a") == 1
    assert edit_distance("a", "") == 1
    assert edit_distance("", "") == 0
