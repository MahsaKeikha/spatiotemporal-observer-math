import numpy as np

from observer_math import (
    interval_class_covariance_path_recovery_bound,
    residual_class_covariance_path_recovery_bound,
)


def _problem(residual=1e-4):
    time_count = 3
    class_count = 2
    local = np.full((time_count, class_count, 3), 0.12)
    local[:, 1] = 0.9
    transport = np.full((2, class_count, class_count, 2), 0.12)
    transport[:, 1, 1] = 0.86
    multiplicities = np.tile(np.array([5, 1]), (time_count, 1))
    planted = (1, 1, 1)
    feasible = np.ones((2, class_count, class_count), dtype=bool)
    continuity_lower = np.zeros((2, class_count, class_count))
    planted_distances = np.full(2, 0.2)
    local_residuals = np.full((time_count, class_count), residual)
    transport_residuals = np.full((2, class_count, class_count), residual)
    local_sampling = np.full((time_count, class_count), 1e-6)
    transport_sampling = np.full((2, class_count, class_count), 1e-6)
    return {
        "local": local,
        "transport": transport,
        "multiplicities": multiplicities,
        "planted": planted,
        "feasible": feasible,
        "continuity_lower": continuity_lower,
        "planted_distances": planted_distances,
        "local_residuals": local_residuals,
        "transport_residuals": transport_residuals,
        "local_sampling": local_sampling,
        "transport_sampling": transport_sampling,
    }


def _certificate(problem):
    return residual_class_covariance_path_recovery_bound(
        problem["local"],
        problem["transport"],
        problem["multiplicities"],
        problem["planted"],
        problem["feasible"],
        problem["continuity_lower"],
        problem["planted_distances"],
        node_count=8,
        subset_size=2,
        local_covariance_residual_bounds=problem["local_residuals"],
        representative_minimum_block_eigenvalues=np.ones(
            problem["local_residuals"].shape
        ),
        representative_maximum_block_eigenvalues=np.full(
            problem["local_residuals"].shape, 2.0
        ),
        transport_covariance_residual_bounds=problem["transport_residuals"],
        representative_minimum_transport_eigenvalues=np.ones(
            problem["transport_residuals"].shape
        ),
        representative_maximum_transport_eigenvalues=np.full(
            problem["transport_residuals"].shape, 2.0
        ),
        covariance_spectral_errors=problem["local_sampling"],
        transport_covariance_spectral_errors=problem["transport_sampling"],
        transport_weight=0.1,
        continuity_weight=0.02,
    )


def test_residual_wrapper_matches_direct_interval_certificate():
    problem = _problem()
    result = _certificate(problem)
    direct = interval_class_covariance_path_recovery_bound(
        result.local_factor_lower_bounds,
        result.local_factor_upper_bounds,
        result.transport_factor_lower_bounds,
        result.transport_factor_upper_bounds,
        problem["multiplicities"],
        problem["planted"],
        problem["feasible"],
        problem["continuity_lower"],
        problem["planted_distances"],
        node_count=8,
        subset_size=2,
        covariance_spectral_errors=problem["local_sampling"],
        minimum_block_eigenvalues=result.minimum_member_block_eigenvalues,
        maximum_block_eigenvalues=result.maximum_member_block_eigenvalues,
        transport_covariance_spectral_errors=problem["transport_sampling"],
        minimum_transport_block_eigenvalues=(
            result.minimum_member_transport_eigenvalues
        ),
        maximum_transport_block_eigenvalues=(
            result.maximum_member_transport_eigenvalues
        ),
        transport_weight=0.1,
        continuity_weight=0.02,
    )

    assert np.isclose(result.recovery.recovery_slack, direct.recovery_slack)
    assert result.recovery.adversarial_class_path == direct.adversarial_class_path
    assert np.allclose(result.minimum_member_block_eigenvalues, 1.0 - 1e-4)
    assert np.allclose(result.maximum_member_block_eigenvalues, 2.0 + 1e-4)
    assert result.recovery.guarantees_population_path


def test_larger_covariance_residuals_cannot_improve_recovery_slack():
    narrow = _certificate(_problem(residual=1e-5))
    wide = _certificate(_problem(residual=1e-3))

    assert wide.recovery.recovery_slack <= narrow.recovery.recovery_slack
    assert np.all(
        wide.local_heterogeneity_factor_errors
        >= narrow.local_heterogeneity_factor_errors
    )
    assert np.all(
        wide.transport_heterogeneity_factor_errors
        >= narrow.transport_heterogeneity_factor_errors
    )


def test_residual_wrapper_rejects_radius_at_representative_eigenvalue_floor():
    problem = _problem()
    problem["local_residuals"][0, 0] = 1.0

    with np.testing.assert_raises_regex(ValueError, "smaller"):
        _certificate(problem)
