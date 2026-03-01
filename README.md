# pure-python-ds 🚀

A high-performance, strictly-typed, and memory-optimized Data Structures and Algorithms library built in Pure Python.

## 🏗️ Architecture Overview

This library was designed with a focus on **Systems Architecture**. By utilizing Python's `__slots__`, every node in this library is memory-optimized to reduce overhead, making it suitable for educational deep-dives and performance-sensitive prototyping.

[Image of a software architecture diagram showing layers of data structures and algorithms]

## 🛠️ Key Features

### 1. Linear Data Structures
* **Linked Lists:** Singly and Doubly Linked Lists with $O(1)$ head/tail operations.
* **Stacks & Queues:** Built on top of optimized linked nodes for strict LIFO/FIFO behavior.

### 2. Hierarchical & Network Structures
* **Binary Search Trees (BST):** Standard ordered trees with recursive and iterative implementations.
* **AVL Trees:** Self-balancing trees using rotation logic to guarantee $O(\log n)$ performance.
* **Graphs:** Adjacency-list based implementation supporting both Directed and Undirected networks.

### 3. Advanced Algorithms
* **Pathfinding:** Dijkstra's Algorithm for finding shortest paths in weighted graphs.
* **Sorting:** $O(n \log n)$ Merge Sort implementation.
* **Searching:** $O(\log n)$ Binary Search.
* **Dynamic Programming:** Memoized Fibonacci and sub-problem optimization.

[Image of a perfectly balanced Binary Search Tree demonstrating O(log n) structure]

## 🚀 Installation

Since the package is in "Editable" mode, you can install it locally to use across your entire system:

```bash
git clone [https://github.com/ParjadM/pure-python-ds.git](https://github.com/ParjadM/pure-python-ds.git)
cd pure-python-ds
pip install -e .