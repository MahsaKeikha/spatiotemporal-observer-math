from itertools import product

import numpy as np

from observer_math.scalable_robust_evidence import minimize_factorized_evidence


def test_p75_matches_exhaustive_path_minimum():
    nodes = np.ones((3, 2), dtype=bool)
    edges = np.ones((2, 2, 2), dtype=bool)
    nf = np.array([[2.0, 3.0], [5.0, 1.5], [2.0, 4.0]])
    ef = np.array([[[1.0, 2.0], [0.8, 1.1]], [[1.3, 0.7], [2.0, 1.0]]])
    result = minimize_factorized_evidence(nodes, edges, nf, ef)
    values = {}
    for path in product(range(2), repeat=3):
        value = nf[0, path[0]]
        for t in range(1, 3):
            value *= ef[t - 1, path[t - 1], path[t]] * nf[t, path[t]]
        values[path] = value
    expected_path = min(values, key=values.get)
    assert np.isclose(result.robust_e_value, values[expected_path])
    assert result.minimizing_path == expected_path


def test_p75_rejects_nonpositive_factors():
    nodes = np.ones((2, 1), dtype=bool)
    edges = np.ones((1, 1, 1), dtype=bool)
    nf = np.array([[1.0], [0.0]])
    ef = np.ones((1, 1, 1))
    try:
        minimize_factorized_evidence(nodes, edges, nf, ef)
    except ValueError as exc:
        assert "strictly positive" in str(exc)
    else:
        raise AssertionError("expected ValueError")
