import pytest

from pure_python_ds.graphs.graph import Graph


@pytest.fixture
def graph():
    g = Graph(directed=False)
    g.add_edge("A", "B", 1)
    g.add_edge("A", "C", 4)
    g.add_edge("B", "C", 2)
    g.add_edge("B", "D", 5)
    g.add_edge("C", "D", 1)
    return g


def test_bfs(graph):
    order = graph.bfs("A")
    assert order == ["A", "B", "C", "D"] or order == ["A", "C", "B", "D"]
    assert len(order) == 4


def test_dfs(graph):
    order = graph.dfs("A")
    assert "A" in order
    assert len(order) == 4


def test_prims_mst(graph):
    mst = graph.prims_mst()
    assert len(mst) == 3
    # mst edges could be (A, B, 1), (B, C, 2), (C, D, 1) -> total weight 4
    total_weight = sum(weight for _, _, weight in mst)
    assert total_weight == 4


def test_a_star_search(graph):
    def heuristic(node):
        h = {"A": 3, "B": 2, "C": 1, "D": 0}
        return h.get(node, 0)

    path = graph.a_star_search("A", "D", heuristic)
    assert path == ["A", "B", "C", "D"]
