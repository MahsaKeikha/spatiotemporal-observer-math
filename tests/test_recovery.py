import numpy as np

from observer_math import (
    componentwise_recovery_bound,
    finite_sample_recovery_bound,
    gaussian_cmi_covariance_error_bound,
    optimize_worldtube,
)
from observer_math.gaussian import gaussian_conditional_mutual_information


def test_positive_componentwise_margins_imply_planted_optimum():
    candidates = ((0,), (1,))
    local = np.array([[1.0, 0.1], [0.2, 0.9], [0.1, 1.1]])
    transport = np.zeros((2, 2, 2))
    transport[0, 0, 1] = 0.7
    transport[1, 1, 1] = 0.7
    planted = (0, 1, 1)

    bound = componentwise_recovery_bound(
        local,
        candidates,
        planted,
        transport_scores=transport,
        transport_weight=0.5,
        continuity_weight=0.0,
    )
    optimum = optimize_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=0.5,
        continuity_weight=0.0,
    )

    assert bound.guarantees_unique_recovery
    assert bound.minimum_margin > 0.0
    assert optimum.candidate_indices == planted


def test_componentwise_condition_can_fail_when_path_is_still_optimal():
    candidates = ((0,), (1,))
    local = np.array([[2.0, 0.0], [2.0, 0.0]])
    transport = np.zeros((1, 2, 2))
    transport[0, 1, 1] = 3.0
    planted = (0, 0)

    bound = componentwise_recovery_bound(
        local,
        candidates,
        planted,
        transport_scores=transport,
        transport_weight=1.0,
        continuity_weight=0.0,
    )
    optimum = optimize_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=1.0,
        continuity_weight=0.0,
    )

    assert not bound.guarantees_unique_recovery
    assert optimum.candidate_indices == planted


def test_finite_sample_bound_has_correct_threshold():
    passing = finite_sample_recovery_bound(
        0.5,
        4,
        local_score_error=0.02,
        transport_score_error=0.01,
        transport_weight=0.5,
    )
    failing = finite_sample_recovery_bound(
        0.1,
        4,
        local_score_error=0.02,
        transport_score_error=0.01,
        transport_weight=0.5,
    )

    assert np.isclose(passing.maximum_action_gap_error, 0.19)
    assert passing.guarantees_population_path
    assert not failing.guarantees_population_path


def test_cmi_covariance_error_bound_covers_direct_perturbation():
    covariance = np.array(
        [
            [1.5, 0.2, 0.1],
            [0.2, 1.2, -0.1],
            [0.1, -0.1, 1.0],
        ]
    )
    perturbation = np.array(
        [
            [0.01, -0.004, 0.002],
            [-0.004, -0.008, 0.003],
            [0.002, 0.003, 0.006],
        ]
    )
    estimated = covariance + perturbation
    actual_error = abs(
        gaussian_conditional_mutual_information(estimated, (0,), (1,), (2,))
        - gaussian_conditional_mutual_information(covariance, (0,), (1,), (2,))
    )
    bound = gaussian_cmi_covariance_error_bound(
        1,
        1,
        1,
        minimum_eigenvalue=float(np.linalg.eigvalsh(covariance)[0]),
        covariance_spectral_error=float(np.linalg.norm(perturbation, ord=2)),
    )

    assert actual_error <= bound
