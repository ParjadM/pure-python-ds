from typing import Generic, TypeVar, Optional, Set, Dict, List
from pure_python_ds.linear import Queue, Stack

T = TypeVar('T')

class Graph(Generic[T]):
    """A strictly typed Graph engine utilizing an Adjacency List."""
    
    def __init__(self, directed: bool = False):
        self._adj_list: Dict[T, Set[T]] = {}
        self.directed = directed

    def add_vertex(self, vertex: T) -> None:
        """Adds a new vertex to the graph if it doesn't exist."""
        if vertex not in self._adj_list:
            self._adj_list[vertex] = set()

    def add_edge(self, v1: T, v2: T) -> None:
        """Adds an edge between two vertices. Automatically adds vertices if missing."""
        self.add_vertex(v1)
        self.add_vertex(v2)
        
        self._adj_list[v1].add(v2)
        if not self.directed:
            self._adj_list[v2].add(v1)

    def bfs(self, start_vertex: T) -> List[T]:
        """Breadth-First Search: Shortest path traversal using your custom Queue."""
        if start_vertex not in self._adj_list:
            return []
            
        visited = set()
        traversal = []
        queue = Queue[T]()
        
        queue.enqueue(start_vertex)
        visited.add(start_vertex)
        
        while len(queue) > 0:
            current = queue.dequeue()
            traversal.append(current)
            
            for neighbor in sorted(self._adj_list[current]): # Sort for deterministic output
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)
                    
        return traversal

    def dfs(self, start_vertex: T) -> List[T]:
        """Depth-First Search: Exhaustive branch traversal using your custom Stack."""
        if start_vertex not in self._adj_list:
            return []
            
        visited = set()
        traversal = []
        stack = Stack[T]()
        
        stack.push(start_vertex)
        
        while len(stack) > 0:
            current = stack.pop()
            
            if current not in visited:
                visited.add(current)
                traversal.append(current)
                # Reverse sort neighbors so they are processed in order due to LIFO stack
                for neighbor in sorted(self._adj_list[current], reverse=True):
                    if neighbor not in visited:
                        stack.push(neighbor)
                        
        return traversal
    def has_cycle(self) -> bool:
        """
        Detects if the graph contains a cycle using DFS.
        Works for both Directed and Undirected graphs.
        """
        visited = set()
        rec_stack = set() # Nodes currently in the current DFS path

        def _check_cycle(v: T, parent: Optional[T]) -> bool:
            visited.add(v)
            rec_stack.add(v)

            for neighbor in self._adj_list[v]:
                # For undirected graphs, we don't count the edge back to the parent as a cycle
                if not self.directed and neighbor == parent:
                    continue
                
                if neighbor in rec_stack:
                    return True
                if neighbor not in visited:
                    if _check_cycle(neighbor, v):
                        return True

            rec_stack.remove(v)
            return False

        for node in list(self._adj_list.keys()):
            if node not in visited:
                if _check_cycle(node, None):
                    return True
        return False