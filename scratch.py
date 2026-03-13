from pure_python_ds.trees.avl_tree import AVLTree

# Let's force the AVL tree to do some heavy balancing
tree = AVLTree()
values = [50, 25, 75, 15, 30, 60, 85, 10, 20, 27, 55, 90]

for v in values:
    tree.insert(v)

print("🌲 Auto-Balanced AVL Tree:")
print(tree)