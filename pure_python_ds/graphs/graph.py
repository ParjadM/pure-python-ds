import heapq  # We'll use Python's built-in min-heap for O(log n) efficiency here
from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar

T = TypeVar("T")


class Graph(Generic[T]):
    def __init__(self, directed: bool = False):
        # Updated to store {vertex: {neighbor: weight}}
        self._adj_list: Dict[T, Dict[T, float]] = {}
        self.directed = directed

    def add_vertex(self, vertex: T) -> None:
        if vertex not in self._adj_list:
            self._adj_list[vertex] = {}

    def add_edge(self, v1: T, v2: T, weight: float = 1.0) -> None:
        """Adds a weighted edge. Defaults to 1.0 if not specified."""
        self.add_vertex(v1)
        self.add_vertex(v2)
        self._adj_list[v1][v2] = weight
        if not self.directed:
            self._adj_list[v2][v1] = weight

    def dijkstra(self, start: T) -> Dict[T, float]:
        """
        Greedy algorithm to find the shortest distance from 'start' to all other nodes.
        Returns a dictionary of {vertex: min_distance}.
        """
        # Distances from start to all other nodes are initially infinity
        distances = {vertex: float("inf") for vertex in self._adj_list}
        distances[start] = 0

        # Priority Queue: (distance, vertex)
        pq = [(0, start)]

        while pq:
            current_distance, current_vertex = heapq.heappop(pq)

            # If we found a longer path than we already recorded, skip it
            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self._adj_list[current_vertex].items():
                distance = current_distance + weight

                # If this path is shorter, update and push to PQ
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances

    def kruskal_mst(self) -> List[Tuple[T, T, float]]:
        """
        Finds the Minimum Spanning Tree using the library's DSU module.
        Returns a list of edges (v1, v2, weight) in the MST.
        """
        from pure_python_ds.graphs import DSU

        edges = []
        # Gather all unique edges
        for u in self._adj_list:
            for v, weight in self._adj_list[u].items():
                if self.directed or (v, u, weight) not in edges:
                    edges.append((u, v, weight))

        # Sort edges by weight
        edges.sort(key=lambda x: x[2])

        # Map vertices to integers for DSU
        nodes = list(self._adj_list.keys())
        node_to_idx = {node: i for i, node in enumerate(nodes)}

        dsu = DSU(len(nodes))
        mst = []

        for u, v, weight in edges:
            if dsu.find(node_to_idx[u]) != dsu.find(node_to_idx[v]):
                dsu.union(node_to_idx[u], node_to_idx[v])
                mst.append((u, v, weight))

        return mst

    def bellman_ford(self, start: T) -> Dict[T, float]:
        """
        Shortest path algorithm that handles negative weights.
        Returns distances or raises ValueError if a negative cycle is found.
        """
        distances = {vertex: float("inf") for vertex in self._adj_list}
        distances[start] = 0

        # Relax edges |V| - 1 times
        for _ in range(len(self._adj_list) - 1):
            for u in self._adj_list:
                for v, weight in self._adj_list[u].items():
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight

        # Check for negative cycles
        for u in self._adj_list:
            for v, weight in self._adj_list[u].items():
                if distances[u] + weight < distances[v]:
                    raise ValueError("Graph contains a negative weight cycle")

        return distances

    def has_edge(self, u: T, v: T) -> bool:
        """Returns True if there is an edge from u to v."""
        return u in self._adj_list and v in self._adj_list[u]
