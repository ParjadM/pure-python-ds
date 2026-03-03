# Pure Python Data Structures

![Build Status](https://github.com/ParjadM/pure-python-ds/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen.svg)

Welcome to **Pure Python Data Structures**! This is a comprehensive, strictly typed, and thoroughly tested algorithms and data structures library built completely from scratch in Python 3.12.

## Features
* **Zero External Dependencies:** Built entirely with Python's standard library.
* **Strictly Typed:** Full Type Hinting support for IDE auto-completion.
* **100% Test Coverage:** Exhaustively tested edge cases, including complex tree rotations.

## Getting Started
Navigate through the tabs above to explore the Linear Structures, Trees, and Graph algorithms.

## Performance Benchmarks
We pit our custom `AVLTree` against Python's highly optimized native `list` to demonstrate the power of logarithmic time complexity. 

**Test Parameters:** Insert 50,000 integers, then search for 1,000 random targets.

| Operation | Python `list` | `AVLTree` | Time Complexity |
|---|---|---|---|
| **Insert 50,000 items** | 0.0020 sec | 0.8998 sec | List: $O(1)$ / AVL: $O(\log n)$ |
| **Search 1,000 items** | 0.9141 sec | 0.0021 sec | List: $O(n)$ / AVL: $O(\log n)$ |

**Result:** The AVL Tree was **436.2x faster** at searching than a standard Python list!