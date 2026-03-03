# pure-python-ds 🚀
**A strictly-typed, 100% test-covered, and benchmarked Data Structures & Algorithms library.**

[![Python Version](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/ParjadM/pure-python-ds/actions/workflows/ci.yml/badge.svg)](https://github.com/ParjadM/pure-python-ds/actions)

## 🏗️ Architecture & Engineering
This library is engineered for **Systems Architects** and developers who require predictable performance and strict type safety. Every structure is built using Python's `__slots__` to ensure a minimal memory footprint and high-speed attribute access.

[Image of a software architecture diagram showing layers of data structures and algorithms]

## 🛡️ Technical Milestones
* **100% Test Coverage:** Verified 100% line coverage across the entire core library using `pytest` and `coverage.py`.
* **Performance Benchmarked:** Custom AVL Tree implementation demonstrated search operations up to **436x faster** than standard Python list lookups in large-scale datasets.
* **Type Safety:** 100% `mypy` compliance with strict type hinting for all inputs and return values.

## 🛠️ Key Features
### 1. Linear Structures
* **Linked Lists:** Singly and Doubly Linked Lists with $O(1)$ head/tail operations.
* **Stacks & Queues:** Built on optimized nodes for strict LIFO/FIFO behavior.
* **Hash Tables:** Linear probing implementation with dynamic resizing.

### 2. Hierarchical & Network Structures
* **AVL Trees:** Self-balancing trees with rotation logic guaranteeing $O(\log n)$ performance.
* **Red-Black Trees:** Memory-optimized nodes with $O(\log n)$ height guarantees.
* **Graphs:** Adjacency-list based supporting Dijkstra’s, Bellman-Ford, and Kruskal’s (via custom DSU).

### 3. Advanced Data Structures
* **Segment Trees:** Range Query/Point Update in $O(\log n)$.
* **Tries:** Space-efficient prefix trees for string operations.
* **Heaps:** Min/Max Binary Heaps for $O(1)$ priority access.

