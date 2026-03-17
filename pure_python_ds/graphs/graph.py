import heapq
import math
from collections import deque
from typing import Any, Callable, Dict, Generic, List, Optional, Set, Tuple, TypeVar

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
        if start not in self._adj_list:
            raise ValueError(f"Start node '{start}' not found in graph.")

        # Distances from start to all other nodes are initially infinity
        distances = {vertex: float("inf") for vertex in self._adj_list}
        distances[start] = 0

        # Priority Queue: (distance, tie_breaker, vertex)
        tie_breaker = 0
        pq: List[Tuple[float, int, T]] = [(0.0, tie_breaker, start)]

        while pq:
            current_distance, _, current_vertex = heapq.heappop(pq)

            # If we found a longer path than we already recorded, skip it
            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self._adj_list[current_vertex].items():
                distance = current_distance + weight

                # If this path is shorter, update and push to PQ
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    tie_breaker += 1
                    heapq.heappush(pq, (distance, tie_breaker, neighbor))

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

    def bfs(self, start: T) -> List[T]:
        """
        Breadth-First Search. Returns the list of visited nodes in order.
        """
        if start not in self._adj_list:
            raise ValueError(f"Start node '{start}' not found in graph.")

        visited: Set[T] = set()
        queue = deque([start])
        order: List[T] = []

        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                order.append(node)
                for neighbor in self._adj_list.get(node, {}):
                    if neighbor not in visited:
                        queue.append(neighbor)
        return order

    def dfs(self, start: T) -> List[T]:
        """
        Depth-First Search (Iterative). Returns visited nodes in order.
        """
        if start not in self._adj_list:
            raise ValueError(f"Start node '{start}' not found in graph.")

        visited: Set[T] = set()
        stack = [start]
        order: List[T] = []

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                order.append(node)
                # To maintain standard DFS order, we add neighbors in reverse
                neighbors = list(self._adj_list.get(node, {}).keys())
                for neighbor in reversed(neighbors):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return order

    def prims_mst(self) -> List[Tuple[T, T, float]]:
        """
        Prim's Minimum Spanning Tree algorithm.
        Returns a list of edges (u, v, weight) forming the MST.
        """
        if not self._adj_list:
            return []

        start = next(iter(self._adj_list))
        visited = {start}
        mst = []
        pq: List[Tuple[float, int, T, T]] = []
        tie_breaker = 0

        for neighbor, weight in self._adj_list[start].items():
            tie_breaker += 1
            heapq.heappush(pq, (weight, tie_breaker, start, neighbor))

        while pq and len(visited) < len(self._adj_list):
            weight, _, u, v = heapq.heappop(pq)
            if v not in visited:
                visited.add(v)
                mst.append((u, v, weight))
                for next_neighbor, next_weight in self._adj_list[v].items():
                    if next_neighbor not in visited:
                        tie_breaker += 1
                        heapq.heappush(pq, (next_weight, tie_breaker, v, next_neighbor))

        return mst

    def a_star_search(self, start: T, goal: T, heuristic: Callable[[T], float]) -> List[T]:
        """
        A* Search algorithm.
        Returns the shortest path (list of nodes) from start to goal.
        """
        if start not in self._adj_list or goal not in self._adj_list:
            raise ValueError("Start or goal node not found in graph.")

        open_set: List[Tuple[float, int, T]] = [(heuristic(start), 0, start)]
        came_from: Dict[T, T] = {}

        g_score = {node: float("inf") for node in self._adj_list}
        g_score[start] = 0

        f_score = {node: float("inf") for node in self._adj_list}
        f_score[start] = heuristic(start)

        tie_breaker = 0

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1]

            for neighbor, weight in self._adj_list.get(current, {}).items():
                tentative_g_score = g_score[current] + weight

                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor)

                    tie_breaker += 1
                    heapq.heappush(open_set, (f_score[neighbor], tie_breaker, neighbor))

        return []


