import numpy as np

from observer_math.finite_sample_boundary import finite_sample_boundary_point


def _factors():
    candidates = ((0, 1), (1, 2))
    local = np.array([
        [[0.72, 0.94, 0.82], [0.18, 0.88, 0.45]],
        [[0.70, 0.93, 0.80], [0.16, 0.86, 0.42]],
        [[0.68, 0.92, 0.78], [0.15, 0.85, 0.40]],
    ])
    transport = np.full((2, 2, 2, 2), 0.20)
    transport[:, 0, 0] = (0.94, 0.86)
    transport[:, 1, 1] = (0.75, 0.52)
    return local, transport, candidates


def test_p67_more_iid_residuals_tighten_covariance_radius():
    local, transport, candidates = _factors()
    kwargs = dict(
        block_dimension=5, block_count=6, confidence=0.95,
        local_factors=local, transport_factors=transport, candidates=candidates,
        paths={"W0": (0, 0, 0), "W1": (1, 1, 1)},
        node_count=3, subset_size=2, transport_weight=0.25,
    )
    a = finite_sample_boundary_point(200, **kwargs)
    b = finite_sample_boundary_point(1000, **kwargs)
    assert b.covariance_radius < a.covariance_radius
