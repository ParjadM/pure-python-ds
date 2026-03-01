from pure_python_ds.linear import MinHeap, HashTable
from pure_python_ds.trees import Trie
from pure_python_ds.graphs import DSU

# Quick check on the new Heavy Hitters
print("--- Final V2.0 Integration Check ---")

# 1. Heap Check
h = MinHeap[int]()
h.push(10); h.push(5)
print(f"Heap Pop (should be 5): {h.pop()}")

# 2. Hash Table Check
ht = HashTable()
ht.set("goal", "McMaster")
print(f"Hash Get: {ht.get('goal')}")

# 3. Trie Check
t = Trie()
t.insert("code")
print(f"Trie Search 'code': {t.search('code')}")

# 4. DSU Check
d = DSU(5)
d.union(1, 2)
print(f"DSU Connected 1 & 2: {d.find(1) == d.find(2)}")