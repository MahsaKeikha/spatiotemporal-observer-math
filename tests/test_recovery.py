import numpy as np

from observer_math import (
    canonical_persistence_covariance_error_bound,
    componentwise_recovery_bound,
    finite_sample_recovery_bound,
    gaussian_cmi_covariance_error_bound,
    gaussian_path_recovery_bound,
    minimum_gaussian_sample_size,
    optimize_worldtube,
)
from observer_math.gaussian import canonical_persistence, gaussian_conditional_mutual_information


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


def test_canonical_persistence_bound_covers_direct_perturbation():
    covariance = np.array(
        [
            [1.4, 0.1, 0.35, 0.05],
            [0.1, 1.1, -0.02, 0.28],
            [0.35, -0.02, 1.3, 0.08],
            [0.05, 0.28, 0.08, 1.2],
        ]
    )
    perturbation = np.array(
        [
            [0.008, 0.001, -0.003, 0.002],
            [0.001, -0.006, 0.002, -0.001],
            [-0.003, 0.002, 0.007, 0.001],
            [0.002, -0.001, 0.001, -0.005],
        ]
    )
    estimated = covariance + perturbation
    population_value = canonical_persistence(
        covariance[:2, :2], covariance[2:, 2:], covariance[:2, 2:]
    )
    estimated_value = canonical_persistence(
        estimated[:2, :2], estimated[2:, 2:], estimated[:2, 2:]
    )
    bound = canonical_persistence_covariance_error_bound(
        minimum_eigenvalue=float(np.linalg.eigvalsh(covariance)[0]),
        maximum_eigenvalue=float(np.linalg.eigvalsh(covariance)[-1]),
        covariance_spectral_error=float(np.linalg.norm(perturbation, ord=2)),
    )

    assert abs(estimated_value - population_value) <= bound


def test_end_to_end_gaussian_bound_improves_with_sample_size():
    small = gaussian_path_recovery_bound(
        0.5,
        2,
        1,
        2,
        10_000,
        minimum_joint_eigenvalue=0.5,
        maximum_joint_eigenvalue=1.0,
        confidence=0.95,
        transport_weight=0.2,
    )
    large = gaussian_path_recovery_bound(
        0.5,
        2,
        1,
        2,
        10**12,
        minimum_joint_eigenvalue=0.5,
        maximum_joint_eigenvalue=1.0,
        confidence=0.95,
        transport_weight=0.2,
    )
    minimum = minimum_gaussian_sample_size(
        0.5,
        2,
        1,
        2,
        minimum_joint_eigenvalue=0.5,
        maximum_joint_eigenvalue=1.0,
        confidence=0.95,
        transport_weight=0.2,
    )

    assert large.maximum_action_gap_error < small.maximum_action_gap_error
    assert not small.guarantees_population_path
    assert large.guarantees_population_path
    assert minimum is not None
    below = gaussian_path_recovery_bound(
        0.5,
        2,
        1,
        2,
        minimum - 1,
        minimum_joint_eigenvalue=0.5,
        maximum_joint_eigenvalue=1.0,
        confidence=0.95,
        transport_weight=0.2,
    )
    assert not below.guarantees_population_path
