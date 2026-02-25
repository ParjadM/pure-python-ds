# pure-python-ds

A strictly typed, memory-optimized, pure Python Data Structures and Algorithms (DSA) monorepo. 

## Why This Package?
Unlike existing packages that are bloated with GUI tools or reliant on heavy C-extensions, `pure-python-ds` is built for modern enterprise environments:
- **Zero Dependencies:** Installs flawlessly on any OS or lightweight Docker container.
- **Strict Typing:** Built with Python 3.9+ `typing.Generic` and `TypeVar` for compile-time safety.
- **Memory Optimized:** Utilizes `__slots__` to prevent dynamic dictionary allocation, reducing memory footprint by ~50%.
- **Lazy Evaluation:** Uses Generator-based traversals (`yield`) to keep peak memory at zero during massive BFS/DFS operations.

## Architecture
This is a monolithic repository compartmentalized into distinct, decoupled sub-modules:
- `pure_python_ds.nodes` (Typed primitive data containers)
- `pure_python_ds.linear` (Stacks, Queues, Linked Lists)
- `pure_python_ds.trees` (BST, AVL, Tries)
- `pure_python_ds.graphs` (Directed, Undirected, Topological Sorts)

*(Installation and API documentation coming in v1.0.0)*