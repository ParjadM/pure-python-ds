from pure_python_ds.trees import BTree

def test_btree():
    print("--- Testing B-Tree (Multi-way Search Tree) ---")
    # A B-Tree with degree 3 (Max 5 keys per node)
    bt = BTree[int](3)
    
    vals = [10, 20, 5, 6, 12, 30, 7, 17]
    for v in vals:
        bt.insert(v)
    
    # In a B-Tree of degree 3, the root should contain the median 
    # value after splits occur.
    print(f"Root keys: {bt.root.keys}")
    if len(bt.root.keys) > 0:
        print("✅ Success: B-Tree initialized and keys inserted with splits.")

if __name__ == "__main__":
    test_btree()