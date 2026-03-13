import heapq
import math
from collections import deque
from typing import Any, Dict, Generic, List, Optional, Set, Tuple, TypeVar

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
        from pure_python_ds.graphs.disjoint_set import DisjointSet

        edges = []
        # Gather all unique edges
        for u in self._adj_list:
            for v, weight in self._adj_list[u].items():
                if self.directed or (v, u, weight) not in edges:
                    edges.append((u, v, weight))

        # Sort edges by weight
        edges.sort(key=lambda x: x[2])

        dsu = DisjointSet[T](self._adj_list.keys())
        mst = []

        for u, v, weight in edges:
            if dsu.union(u, v):
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

    def topological_sort(self) -> List[Any]:
        """
        Performs a topological sort on a Directed Acyclic Graph (DAG)
        using Kahn's Algorithm.

        Returns:
            A list of vertices in topologically sorted order.

        Raises:
            ValueError: If the graph contains a cycle (sort is impossible).
        """
        # 1. Initialize all in-degrees to 0
        in_degree = {node: 0 for node in self._adj_list}

        # 2. Calculate actual in-degrees
        for node in self._adj_list:
            for neighbor in self._adj_list[node]:
                if neighbor not in in_degree:
                    in_degree[neighbor] = 0
                in_degree[neighbor] += 1

        # 3. Queue nodes with no incoming dependencies (in-degree == 0)
        queue = deque([node for node in in_degree if in_degree[node] == 0])
        sorted_order = []

        # 4. Process the queue
        while queue:
            current = queue.popleft()
            sorted_order.append(current)

            # Reduce the in-degree of all neighbors by 1
            for neighbor in self._adj_list.get(current, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 5. Cycle Detection: If we didn't process every node, there's a loop
        if len(sorted_order) != len(in_degree):
            raise ValueError(
                "Graph contains a cycle; topological sort is not possible."
            )

        return sorted_order

    def dijkstra(self, start_node: Any) -> Dict[Any, float]:
        """
        Computes the shortest path from a starting node to all other reachable nodes.
        """
        distances = {node: math.inf for node in self._adj_list}
        if start_node not in distances:
            raise ValueError(f"Start node '{start_node}' not found in graph.")

        distances[start_node] = 0
        pq = [(0, start_node)]

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            if current_distance > distances[current_node]:
                continue

            # Grab neighbors (handles both Lists and Dictionaries safely)
            neighbors = self._adj_list.get(current_node, [])
            iterator = neighbors.items() if isinstance(neighbors, dict) else neighbors

            for edge in iterator:
                # If it's a tuple from dict.items() or a tuple in a list
                if isinstance(edge, tuple) and len(edge) == 2:
                    neighbor, weight = edge
                else:
                    neighbor = edge
                    weight = 1

                distance = current_distance + weight

                if distance < distances.get(neighbor, math.inf):
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances
