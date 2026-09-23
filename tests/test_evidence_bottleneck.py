import numpy as np

from observer_math.evidence_bottleneck import (
    localize_path_evidence_bottlenecks,
    required_single_factor_multiplier,
)


def test_p76_localizes_smallest_factor_on_limiting_path():
    path = (0, 1, 0)
    nodes = np.array([[2.0, 9.0], [8.0, 1.2], [3.0, 7.0]])
    edges = np.ones((2, 2, 2))
    edges[0, 0, 1] = 0.5
    edges[1, 1, 0] = 4.0
    ranked = localize_path_evidence_bottlenecks(path, nodes, edges)
    assert ranked[0].kind == "edge"
    assert ranked[0].time == 0
    assert ranked[0].source == 0
    assert ranked[0].target == 1
    assert np.isclose(ranked[0].factor, 0.5)


def test_p76_required_single_factor_multiplier():
    assert np.isclose(required_single_factor_multiplier(5.0, 20.0), 4.0)
    assert np.isclose(required_single_factor_multiplier(25.0, 20.0), 1.0)
