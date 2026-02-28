from typing import Dict

def fibonacci(n: int, memo: Dict[int, int] = None) -> int:
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