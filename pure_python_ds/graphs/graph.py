from typing import Generic, TypeVar, Optional, Set, Dict, List, Tuple
import heapq # We'll use Python's built-in min-heap for O(log n) efficiency here

T = TypeVar('T')

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
        distances = {vertex: float('inf') for vertex in self._adj_list}
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