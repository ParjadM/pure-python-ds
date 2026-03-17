from pure_python_ds.algorithms.strings import kmp_search, rabin_karp


def test_kmp_search():
    assert kmp_search("AABAACAADAABAABA", "AABA") == [0, 9, 12]
    assert kmp_search("hello world", "world") == [6]
    assert kmp_search("aaaa", "a") == [0, 1, 2, 3]
    assert kmp_search("aaaa", "aa") == [0, 1, 2]
    assert kmp_search("", "") == [0]
    assert kmp_search("abc", "") == [0, 0, 0, 0]


def test_rabin_karp():
    assert rabin_karp("AABAACAADAABAABA", "AABA") == [0, 9, 12]
    assert rabin_karp("hello world", "world") == [6]
    assert rabin_karp("aaaa", "a") == [0, 1, 2, 3]
    assert rabin_karp("aaaa", "aa") == [0, 1, 2]
    assert rabin_karp("", "") == [0]
    assert rabin_karp("abc", "") == [0, 0, 0, 0]
