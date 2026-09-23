import itertools

import numpy as np

from observer_math.action_intervals import path_action_interval
from observer_math.score_interval_graph import (
    compress_score_interval_graph,
    score_intervals_to_graph,
)


def test_p70_graph_path_intervals_equal_p64_explicit_intervals():
    local = np.array([[1.0, 0.5], [0.9, 0.4], [0.8, 0.3]])
    le = np.full_like(local, 0.05)
    trans = np.full((2, 2, 2), 0.2)
    te = np.full_like(trans, 0.03)
    cont = np.array([[0.0, 1.0], [1.0, 0.0]])
    chi, lam = 0.25, 0.1
    graph = score_intervals_to_graph(
        local, le, trans, te, cont,
        transport_weight=chi, continuity_weight=lam,
    )
    for path in itertools.product(range(2), repeat=3):
        p64 = path_action_interval(
            path, local, le, trans, te, cont,
            transport_weight=chi, continuity_weight=lam,
        ).interval
        lower = sum(graph.node_lower[t, j] for t, j in enumerate(path))
        upper = sum(graph.node_upper[t, j] for t, j in enumerate(path))
        lower += sum(graph.edge_lower[t, path[t], path[t + 1]] for t in range(2))
        upper += sum(graph.edge_upper[t, path[t], path[t + 1]] for t in range(2))
        assert np.isclose(lower, p64.lower)
        assert np.isclose(upper, p64.upper)


def test_p70_compression_runs_without_path_enumeration():
    local = np.array([[1.0, 0.1], [1.0, 0.1], [1.0, 0.1]])
    le = np.full_like(local, 0.01)
    trans = np.zeros((2, 2, 2))
    te = np.full_like(trans, 0.01)
    cont = np.zeros((2, 2))
    out = compress_score_interval_graph(
        local, le, trans, te, cont,
        transport_weight=0.25, continuity_weight=0.0,
    )
    assert out.retained_nodes.shape == local.shape
    assert np.all(out.retained_nodes[:, 0])
