import numpy as np

from observer_math.innovation_whitening import (
    gaussian_innovation_whitened_matrix_chernoff_bound,
    separable_gaussian_innovation_whitened_covariance,
)
from observer_math.matrix_chernoff import gaussian_weighted_wishart_matrix_bound


def _target_times() -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _design(times: np.ndarray) -> np.ndarray:
    centered = times - np.mean(times)
    return np.column_stack((np.ones(times.size), centered))


def _simulate_standardized(times: np.ndarray, tau: float, seed: int) -> np.ndarray:
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


def test_innovation_covariance_is_invariant_to_declared_affine_nuisance() -> None:
    times = _target_times()
    design = _design(times)
    noise = _simulate_standardized(times, 0.78, seed=20261201)
    first = noise + design @ np.array([2.5, -0.7])
    second = noise + design @ np.array([-8.0, 4.25])

    covariance_first = separable_gaussian_innovation_whitened_covariance(
        first,
        times,
        design,
        0.78,
    )
    covariance_second = separable_gaussian_innovation_whitened_covariance(
        second,
        times,
        design,
        0.78,
    )

    assert np.allclose(covariance_first, covariance_second, atol=2e-13, rtol=0.0)


def test_innovation_whitened_bound_crosses_the_experiment_ap_threshold() -> None:
    times = _target_times()
    bound = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        _design(times),
        block_dimension=1,
        block_count=1,
        relaxation_time=0.78,
        confidence=0.975,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    assert bound.sample_count == 120
    assert bound.nuisance_rank == 2
    assert bound.residual_degrees_of_freedom == 118
    assert 0.43 < bound.covariance_relative_error < 0.44
    assert bound.covariance_relative_error < 1.0


def test_proposition_56_reduces_exactly_to_unit_weight_proposition_47() -> None:
    times = _target_times()
    bound = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        _design(times),
        block_dimension=4,
        block_count=2,
        relaxation_time=0.78,
        confidence=0.975,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )
    direct = gaussian_weighted_wishart_matrix_bound(
        4,
        2,
        np.ones(118),
        confidence=0.975,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )

    assert np.isclose(
        bound.covariance_relative_error,
        direct.relative_covariance_error,
        atol=1e-14,
        rtol=0.0,
    )
    assert bound.covariance_bound.temporal_rank == 118
    assert bound.covariance_bound.temporal_spectral_norm == 1.0


def test_innovation_whitening_is_covariant_under_time_unit_changes() -> None:
    times = _target_times()
    design = _design(times)
    values = _simulate_standardized(times, 0.78, seed=20261202) + design @ np.array([1.2, 0.3])

    covariance_seconds = separable_gaussian_innovation_whitened_covariance(
        values,
        times,
        design,
        0.78,
    )

    scaled_times = 1000.0 * times
    scaled_design = _design(scaled_times)
    scaled_values = _simulate_standardized(
        scaled_times,
        780.0,
        seed=20261202,
    ) + scaled_design @ np.array([1.2, 0.0003])
    covariance_milliseconds = separable_gaussian_innovation_whitened_covariance(
        scaled_values,
        scaled_times,
        scaled_design,
        780.0,
    )

    seconds_bound = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        relaxation_time=0.78,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    milliseconds_bound = gaussian_innovation_whitened_matrix_chernoff_bound(
        scaled_times,
        scaled_design,
        1,
        1,
        relaxation_time=780.0,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    assert np.allclose(covariance_seconds, covariance_milliseconds, atol=2e-13, rtol=0.0)
    assert np.isclose(
        seconds_bound.covariance_relative_error,
        milliseconds_bound.covariance_relative_error,
        atol=1e-14,
        rtol=0.0,
    )


def test_seeded_scalar_coverage_is_consistent_with_the_certified_radius() -> None:
    times = _target_times()
    design = _design(times)
    bound = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        relaxation_time=0.78,
        confidence=0.975,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )

    covered = 0
    trial_count = 256
    for trial in range(trial_count):
        noise = _simulate_standardized(times, 0.78, seed=20262000 + trial)
        values = noise + design @ np.array([3.0, -0.7])
        estimate = separable_gaussian_innovation_whitened_covariance(
            values,
            times,
            design,
            0.78,
        )
        error = abs(float(estimate[0, 0]) - 1.0)
        covered += int(error <= bound.covariance_relative_error)

    assert covered / trial_count >= 0.97
