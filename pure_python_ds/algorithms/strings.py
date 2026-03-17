from typing import List


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Knuth-Morris-Pratt (KMP) Algorithm.
    Returns all starting indices of the pattern in the text.
    """
    if not pattern:
        return [0] * (len(text) + 1)

    n, m = len(text), len(pattern)
    lps = [0] * m
    j = 0
    _compute_lps(pattern, m, lps)

    indices = []
    i = 0
    while i < n:
        if pattern[j] == text[i]:
            j += 1
            i += 1

        if j == m:
            indices.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return indices


def _compute_lps(pattern: str, m: int, lps: List[int]) -> None:
    len_prefix = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[len_prefix]:
            len_prefix += 1
            lps[i] = len_prefix
            i += 1
        else:
            if len_prefix != 0:
                len_prefix = lps[len_prefix - 1]
            else:
                lps[i] = 0
                i += 1


def rabin_karp(text: str, pattern: str) -> List[int]:
    """
    Rabin-Karp Algorithm for string matching.
    Returns all starting indices of the pattern in the text.
    Uses rolling hash to verify match candidates in expected O(N+M) time.
    """
    if not pattern:
        return [0] * (len(text) + 1)

    n, m = len(text), len(pattern)
    if m > n:
        return []

    d = 256  # No. of characters in the input alphabet
    q = 101  # A prime number for modulo
    h = 1

    for i in range(m - 1):
        h = (h * d) % q

    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    indices = []

    for i in range(n - m + 1):
        if p == t:
            match = True
            for j in range(m):
                if text[i + j] != pattern[j]:
                    match = False
                    break
            if match:
                indices.append(i)

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q

            if t < 0:
                t += q

    return indices
