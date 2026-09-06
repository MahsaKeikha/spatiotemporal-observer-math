import numpy as np

from observer_math.worldtube import optimize_worldtube, structural_transport


def test_worldtube_tracks_moving_optimum():
    candidates = ((0, 1), (1, 2), (2, 3))
    local = np.array(
        [
            [0.9, 0.2, 0.1],
            [0.3, 0.9, 0.2],
            [0.1, 0.3, 0.9],
        ]
    )
    transport = np.zeros((2, 3, 3))
    transport[0, 0, 1] = 1.0
    transport[1, 1, 2] = 1.0
    result = optimize_worldtube(local, candidates, transport_scores=transport)
    assert result.path == candidates


def test_structural_transport_is_bounded_and_directional():
    transition = np.array([[0.8, 0.0], [0.7, 0.1]])
    assert 0.0 <= structural_transport(transition, (0,), (1,)) <= 1.0
    assert structural_transport(transition, (0,), (1,)) > structural_transport(
        transition, (1,), (0,)
    )
