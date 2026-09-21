import numpy as np

from examples.worldtube_active_measurement_bridge import (
    disagreement_weights,
    jaccard_distance,
    ranked_worldtubes,
    select_predictive_channel,
)


def test_jaccard_distance_exact_values():
    assert jaccard_distance((0, 1, 2), (0, 1, 2)) == 0.0
    assert np.isclose(jaccard_distance((0, 1, 2), (1, 2, 3)), 0.5)


def test_ranked_worldtubes_returns_distinct_top_two():
    candidates = ((0,), (1,))
    local = np.array([[2.0, 1.0], [2.0, 1.5]])
    transport = np.zeros((1, 2, 2))
    best, best_score, second, second_score = ranked_worldtubes(
        local, candidates, transport, transport_weight=0.0, continuity_weight=0.0
    )
    assert best != second
    assert best_score >= second_score


def test_disagreement_weights_follow_path_geometry():
    best = ((0, 1, 2), (1, 2, 3))
    second = ((1, 2, 3), (2, 3, 4))
    q = disagreement_weights(best, second)
    assert np.isclose(q[0], 0.5)
    assert np.isclose(q[4], 0.5)
    assert np.isclose(q[2], 0.0)


def test_predictive_channel_requires_structural_and_statistical_difference():
    best = ((0, 1),)
    second = ((1, 2),)
    mu_p = np.array([0.8, 0.0, 0.3])
    mu_r = np.array([0.0, 0.0, 0.3])
    var = np.ones(3)
    sensor, utility = select_predictive_channel(best, second, mu_p, mu_r, var)
    assert sensor == 0
    assert utility[2] == 0.0


def test_equivalent_predictive_laws_return_no_sensor():
    best = ((0, 1),)
    second = ((1, 2),)
    mu = np.array([0.2, 0.2, 0.2])
    sensor, utility = select_predictive_channel(best, second, mu, mu, np.ones(3))
    assert sensor is None
    assert np.allclose(utility, 0.0)
