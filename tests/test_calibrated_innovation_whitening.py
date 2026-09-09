import numpy as np

from observer_math.calibrated_innovation_whitening import (
    gaussian_calibrated_innovation_confidence_tube,
    innovation_whitened_covariance_path,
    scalar_relative_covariance_interval,
)
from observer_math.innovation_whitening import (
    gaussian_innovation_whitened_matrix_chernoff_bound,
    separable_gaussian_innovation_whitened_covariance,
)
from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
)


def _calibration_times() -> np.ndarray:
    gaps = np.array(
        [
            0.03,
            0.05,
            0.08,
            0.04,
            0.11,
            0.07,
            0.15,
            0.06,
            0.09,
            0.13,
            0.05,
            0.17,
            0.08,
            0.12,
            0.04,
            0.10,
            0.14,
            0.06,
            0.18,
            0.07,
            0.09,
            0.16,
            0.05,
            0.11,
            0.20,
            0.08,
            0.13,
            0.06,
            0.15,
            0.09,
            0.12,
        ],
        dtype=float,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _simulate_channels(times: np.ndarray, tau: float, channels: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty((times.size, channels), dtype=float)
    values[0] = rng.standard_normal(channels)
    for index, gap in enumerate(np.diff(times)):
        alpha = np.exp(-gap / tau)
        values[index + 1] = (
            alpha * values[index]
            + np.sqrt(1.0 - alpha * alpha) * rng.standard_normal(channels)
        )
    return values


def _calibration_model():
    times = _calibration_times()
    values = _simulate_channels(times, 0.78, 96, seed=20261110)
    return gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=0.40,
        upper_relaxation_time=1.25,
        confidence=0.975,
        mixture_relaxation_time_grid_size=21,
    )


def _target_times() -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _design(times: np.ndarray) -> np.ndarray:
    centered = times - np.mean(times)
    return np.column_stack((np.ones(times.size), centered))


def _simulate_target(times: np.ndarray, tau: float, seed: int) -> np.ndarray:
    return _simulate_channels(times, tau, 1, seed=seed)[:, 0]


def test_calibrated_innovation_tube_matches_proposition_55_checkpoint() -> None:
    model = _calibration_model()
    times = _target_times()
    tube = gaussian_calibrated_innovation_confidence_tube(
        model,
        times,
        _design(times),
        1,
        1,
        calibration_cell_count=160,
        covariance_confidence=0.975,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    assert tube.calibration_outer_cover.retained_cell_count == 31
    assert np.isclose(tube.retained_relaxation_time_lower_bound, 0.686875)
    assert np.isclose(tube.retained_relaxation_time_upper_bound, 0.8515625)
    assert tube.residual_degrees_of_freedom == 118
    assert np.isclose(tube.combined_confidence, 0.975**2)


def test_proposition_57_preserves_the_proposition_56_candidate_radius() -> None:
    model = _calibration_model()
    times = _target_times()
    design = _design(times)
    tube = gaussian_calibrated_innovation_confidence_tube(
        model,
        times,
        design,
        1,
        1,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )
    known_tau = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        1,
        1,
        relaxation_time=0.78,
        confidence=0.975,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )

    assert np.isclose(
        tube.covariance_relative_error,
        known_tau.covariance_relative_error,
        atol=1e-14,
        rtol=0.0,
    )
    assert tube.covariance_relative_error < 1.0


def test_covariance_path_contains_the_exact_true_tau_estimator() -> None:
    times = _target_times()
    design = _design(times)
    values = _simulate_target(times, 0.78, seed=20264000) + design @ np.array([3.0, -0.7])
    candidates = np.array([0.70, 0.78, 0.84])

    path = innovation_whitened_covariance_path(values, times, design, candidates)
    direct = separable_gaussian_innovation_whitened_covariance(
        values,
        times,
        design,
        0.78,
    )

    assert path.shape == (3, 1, 1)
    assert np.allclose(path[1], direct, atol=1e-14, rtol=0.0)


def test_scalar_relative_ball_has_the_correct_inverse_form() -> None:
    lower, upper = scalar_relative_covariance_interval(0.90, 0.40)

    assert np.isclose(lower, 0.90 / 1.40)
    assert np.isclose(upper, 0.90 / 0.60)
    assert lower < 0.90 < upper


def test_calibrated_tube_is_covariant_under_time_unit_changes() -> None:
    model = _calibration_model()
    times = _target_times()
    design = _design(times)
    values = _simulate_target(times, 0.78, seed=20264001) + design @ np.array([1.5, -0.4])
    candidates = np.array([0.70, 0.78, 0.84])

    seconds = innovation_whitened_covariance_path(values, times, design, candidates)

    scaled_times = 1000.0 * times
    scaled_design = _design(scaled_times)
    scaled_values = _simulate_target(scaled_times, 780.0, seed=20264001) + scaled_design @ np.array(
        [1.5, -0.0004]
    )
    milliseconds = innovation_whitened_covariance_path(
        scaled_values,
        scaled_times,
        scaled_design,
        1000.0 * candidates,
    )

    assert np.allclose(seconds, milliseconds, atol=2e-13, rtol=0.0)
    tube = gaussian_calibrated_innovation_confidence_tube(
        model,
        times,
        design,
        1,
        1,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    assert tube.covariance_relative_error < 0.45
