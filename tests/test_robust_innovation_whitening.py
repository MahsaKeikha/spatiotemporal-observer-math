import numpy as np

from observer_math.innovation_whitening import (
    gaussian_innovation_whitened_matrix_chernoff_bound,
)
from observer_math.physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_markov_factorization,
)
from observer_math.robust_innovation_whitening import (
    gaussian_robust_innovation_whitened_matrix_chernoff_bound,
    separable_gaussian_robust_innovation_whitened_covariance,
)


def _times(sample_count: int = 24) -> np.ndarray:
    gaps = np.resize(np.array([0.04, 0.07, 0.05, 0.09, 0.06], dtype=float), sample_count - 1)
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _design(times: np.ndarray) -> np.ndarray:
    return np.column_stack((np.ones(times.size), times - np.mean(times)))


def _simulate(times: np.ndarray, tau: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty(times.size, dtype=float)
    values[0] = rng.standard_normal()
    for index, gap in enumerate(np.diff(times)):
        alpha = np.exp(-gap / tau)
        values[index + 1] = (
            alpha * values[index]
            + np.sqrt(1.0 - alpha * alpha) * rng.standard_normal()
        )
    return values


def test_degenerate_tau_interval_reduces_to_exact_innovation_theorem() -> None:
    times = _times()
    design = _design(times)
    exact = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        relaxation_time=0.78,
        upper_theta_grid_size=128,
        lower_theta_grid_size=128,
    )
    robust = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        lower_relaxation_time=0.78,
        upper_relaxation_time=0.78,
        working_relaxation_time=0.78,
        relaxation_time_grid_size=3,
        upper_theta_grid_size=128,
        lower_theta_grid_size=128,
    )

    assert robust.transformed_eigenvalue_covering_radius == 0.0
    assert robust.transformed_normalization_covering_radius == 0.0
    assert np.isclose(robust.covariance_normalization, times.size - design.shape[1])
    assert np.isclose(
        robust.covariance_relative_error,
        exact.covariance_relative_error,
        atol=2e-12,
        rtol=0.0,
    )


def test_transformed_operator_cover_contains_dense_midpoint_checks() -> None:
    times = _times(18)
    design = _design(times)
    lower = 0.68
    upper = 0.86
    working = 0.77
    grid_size = 17
    bound = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        lower_relaxation_time=lower,
        upper_relaxation_time=upper,
        working_relaxation_time=working,
        relaxation_time_grid_size=grid_size,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    whitening = exponential_relaxation_markov_factorization(times, working).whitening_matrix
    tau_grid = np.linspace(lower, upper, grid_size)
    radius = bound.transformed_eigenvalue_covering_radius
    for left, right in zip(tau_grid[:-1], tau_grid[1:]):
        tau = 0.5 * (left + right)
        nearest = left
        transformed = whitening @ exponential_relaxation_covariance(times, tau) @ whitening.T
        covered = whitening @ exponential_relaxation_covariance(times, nearest) @ whitening.T
        assert np.linalg.norm(transformed - covered, ord=2) <= radius + 2e-12


def test_robust_covariance_is_invariant_to_declared_affine_nuisance() -> None:
    times = _times()
    design = _design(times)
    bound = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        lower_relaxation_time=0.70,
        upper_relaxation_time=0.84,
        working_relaxation_time=0.77,
        relaxation_time_grid_size=17,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )
    noise = _simulate(times, 0.79, seed=20264001)
    first = noise + design @ np.array([2.0, -0.5])
    second = noise + design @ np.array([-7.0, 3.2])

    covariance_first = separable_gaussian_robust_innovation_whitened_covariance(
        first,
        times,
        design,
        working_relaxation_time=bound.working_relaxation_time,
        covariance_normalization=bound.covariance_normalization,
    )
    covariance_second = separable_gaussian_robust_innovation_whitened_covariance(
        second,
        times,
        design,
        working_relaxation_time=bound.working_relaxation_time,
        covariance_normalization=bound.covariance_normalization,
    )

    assert np.allclose(covariance_first, covariance_second, atol=2e-13, rtol=0.0)


def test_robust_theorem_is_covariant_under_time_unit_changes() -> None:
    times = _times(16)
    design = _design(times)
    seconds = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        lower_relaxation_time=0.69,
        upper_relaxation_time=0.85,
        working_relaxation_time=0.77,
        relaxation_time_grid_size=17,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    scaled_times = 1000.0 * times
    scaled_design = _design(scaled_times)
    milliseconds = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        scaled_times,
        scaled_design,
        1,
        1,
        lower_relaxation_time=690.0,
        upper_relaxation_time=850.0,
        working_relaxation_time=770.0,
        relaxation_time_grid_size=17,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    assert np.isclose(
        seconds.covariance_relative_error,
        milliseconds.covariance_relative_error,
        atol=2e-12,
        rtol=0.0,
    )
    assert np.isclose(
        seconds.covariance_normalization,
        milliseconds.covariance_normalization,
        atol=2e-12,
        rtol=0.0,
    )
    assert np.isclose(
        seconds.transformed_eigenvalue_covering_radius,
        milliseconds.transformed_eigenvalue_covering_radius,
        atol=2e-12,
        rtol=0.0,
    )


def test_cover_radius_shrinks_linearly_when_tau_grid_is_refined() -> None:
    times = _times(14)
    design = _design(times)
    coarse = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        lower_relaxation_time=0.70,
        upper_relaxation_time=0.84,
        working_relaxation_time=0.77,
        relaxation_time_grid_size=9,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )
    fine = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        lower_relaxation_time=0.70,
        upper_relaxation_time=0.84,
        working_relaxation_time=0.77,
        relaxation_time_grid_size=17,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    assert np.isclose(
        fine.transformed_eigenvalue_covering_radius,
        0.5 * coarse.transformed_eigenvalue_covering_radius,
        atol=1e-14,
        rtol=1e-12,
    )
    assert np.isclose(
        fine.transformed_normalization_covering_radius,
        0.5 * coarse.transformed_normalization_covering_radius,
        atol=1e-14,
        rtol=1e-12,
    )
