from typing import Dict, List


def fibonacci(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """
    Computes the nth Fibonacci number using Top-Down DP (Memoization).
    O(n) time complexity vs O(2^n) recursive complexity.
    """
    if memo is None:
        memo = {}
    if n in memo:
        return memo[n]
    if n <= 1:
        return n

    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]


def knapsack(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Solves the 0-1 Knapsack problem.
    Returns the maximum value that can be put in a knapsack of capacity W.
    """
    n = len(values)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]], dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]


def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Finds the length of the longest common subsequence of two strings.
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]


def longest_increasing_subsequence(arr: List[int]) -> int:
    """
    Finds the length of the longest increasing subsequence.
    """
    if not arr:
        return 0

    dp = [1] * len(arr)
    for i in range(1, len(arr)):
        for j in range(0, i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)


def edit_distance(word1: str, word2: str) -> int:
    """
    Computes the Levenshtein minimum edit distance between two strings.
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],  # delete
                    dp[i][j - 1],  # insert
                    dp[i - 1][j - 1],  # replace
                )

    return dp[m][n]
