import random
import time

from pure_python_ds.trees.avl_tree import AVLTree


def run_benchmark():
    # 1. Setup the testing data
    N = 50_000  # 50,000 items to insert
    SEARCH_COUNT = 1000  # 1,000 items to find
    print(f"--- Preparing Data: {N} elements ---")

    # Generate random unique numbers
    data = random.sample(range(1, N * 10), N)
    search_targets = random.sample(data, SEARCH_COUNT)

    # ---------------------------------------------------------
    # TEST 1: Python Native List
    # ---------------------------------------------------------
    list_ds = []

    # Benchmark List Insertion
    start_time = time.time()
    for num in data:
        list_ds.append(num)
    list_insert_time = time.time() - start_time

    # Benchmark List Search
    start_time = time.time()
    for target in search_targets:
        _ = target in list_ds
    list_search_time = time.time() - start_time

    # ---------------------------------------------------------
    # TEST 2: Your Custom AVL Tree
    # ---------------------------------------------------------
    avl = AVLTree[int]()

    # Benchmark AVL Insertion
    start_time = time.time()
    for num in data:
        avl.insert(num)
    avl_insert_time = time.time() - start_time

    # Benchmark AVL Search
    start_time = time.time()
    for target in search_targets:
        avl.search(target)  # Make sure your method is named 'search' or 'find'
    avl_search_time = time.time() - start_time

    # ---------------------------------------------------------
    # PRINT RESULTS (Formatted for MkDocs Markdown)
    # ---------------------------------------------------------
    print("\n### Benchmark Results")
    print("| Operation | Python `list` | `AVLTree` | Time Complexity |")
    print("|---|---|---|---|")
    print(
        f"| Insert {N} items | {list_insert_time:.4f} sec | {avl_insert_time:.4f} sec | List: $O(1)$ / AVL: $O(\\log n)$ |"
    )
    print(
        f"| Search {SEARCH_COUNT} items | {list_search_time:.4f} sec | {avl_search_time:.4f} sec | List: $O(n)$ / AVL: $O(\\log n)$ |"
    )

    if avl_search_time > 0:
        speedup = list_search_time / avl_search_time
        print(
            f"\n**Result:** The AVL Tree was **{speedup:.1f}x faster** at searching than a standard Python list!"
        )


if __name__ == "__main__":
    run_benchmark()
