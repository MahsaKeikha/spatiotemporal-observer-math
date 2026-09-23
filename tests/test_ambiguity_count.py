import itertools

import numpy as np

from observer_math.ambiguity_count import count_retained_paths


def test_p71_dynamic_path_count_matches_exhaustive_enumeration():
    nodes = np.array([[1, 1, 0], [1, 1, 1], [1, 0, 1]], dtype=bool)
    edges = np.array([
        [[1, 1, 0], [0, 1, 1], [0, 0, 0]],
        [[1, 0, 1], [1, 0, 0], [0, 0, 1]],
    ], dtype=bool)
    result = count_retained_paths(nodes, edges)
    explicit = 0
    for path in itertools.product(range(3), repeat=3):
        valid = all(nodes[t, path[t]] for t in range(3))
        valid = valid and all(edges[t, path[t], path[t + 1]] for t in range(2))
        explicit += int(valid)
    assert result.total_paths == explicit


def test_p71_counts_large_complete_graph_exactly():
    t_count, c_count = 5, 35
    result = count_retained_paths(
        np.ones((t_count, c_count), dtype=bool),
        np.ones((t_count - 1, c_count, c_count), dtype=bool),
    )
    assert result.total_paths == 35**5
