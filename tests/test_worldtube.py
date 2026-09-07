import numpy as np

from observer_math.worldtube import certify_worldtube, optimize_worldtube, structural_transport


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


def test_certificate_finds_exact_runner_up_and_positive_radius():
    candidates = ((0,), (1,))
    local = np.array([[1.0, 0.1], [0.2, 1.1]])
    transport = np.array([[[0.0, 0.6], [0.0, 0.0]]])

    certificate = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=0.5,
        continuity_weight=0.0,
    )

    # Exhaustive actions: (0,1)=2.4, (0,0)=1.2, (1,1)=1.2, (1,0)=0.3.
    assert certificate.result.candidate_indices == (0, 1)
    assert np.isclose(certificate.result.total_action, 2.4)
    assert np.isclose(certificate.runner_up_action, 1.2)
    assert np.isclose(certificate.action_margin, 1.2)
    assert np.isclose(certificate.uniform_score_radius, 1.2 / 5.0)


def test_perturbation_below_certificate_radius_preserves_path():
    candidates = ((0,), (1,))
    local = np.array([[0.9, 0.2], [0.1, 0.95], [0.2, 1.0]])
    transport = np.zeros((2, 2, 2))
    transport[:, 0, 1] = 0.4
    certificate = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=0.3,
        continuity_weight=0.0,
    )
    epsilon = certificate.uniform_score_radius * 0.4
    rng = np.random.default_rng(4)
    perturbed_local = local + rng.uniform(-epsilon, epsilon, local.shape)
    perturbed_transport = transport + rng.uniform(-epsilon, epsilon, transport.shape)

    perturbed = optimize_worldtube(
        perturbed_local,
        candidates,
        transport_scores=perturbed_transport,
        transport_weight=0.3,
        continuity_weight=0.0,
    )
    assert perturbed.candidate_indices == certificate.result.candidate_indices
