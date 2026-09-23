import itertools

import numpy as np

from observer_math.graph_pruning import certified_graph_compression


def _path_bounds(path, node, edge):
    value = sum(node[t, j] for t, j in enumerate(path))
    value += sum(edge[t, path[t], path[t + 1]] for t in range(len(path) - 1))
    return value


def test_p69_graph_pruning_matches_explicit_safe_path_logic():
    nl = np.array([[3.0, 1.0], [3.0, 1.0], [3.0, 1.0]])
    nu = nl + 0.2
    el = np.zeros((2, 2, 2))
    eu = np.full((2, 2, 2), 0.1)
    out = certified_graph_compression(nl, nu, el, eu)
    paths = list(itertools.product(range(2), repeat=3))
    lower = {p: _path_bounds(p, nl, el) for p in paths}
    upper = {p: _path_bounds(p, nu, eu) for p in paths}
    best_lower = max(lower.values())
    for t in range(3):
        for j in range(2):
            explicit = max(upper[p] for p in paths if p[t] == j)
            assert out.node_upper_max_marginals[t, j] == explicit
            assert out.retained_nodes[t, j] == (explicit >= best_lower)
    for t in range(2):
        for i in range(2):
            for j in range(2):
                explicit = max(
                    upper[p] for p in paths if p[t] == i and p[t + 1] == j
                )
                assert out.edge_upper_max_marginals[t, i, j] == explicit
                assert out.retained_edges[t, i, j] == (explicit >= best_lower)
