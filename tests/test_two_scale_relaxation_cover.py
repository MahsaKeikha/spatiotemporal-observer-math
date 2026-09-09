import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_log_evalue,
)
from observer_math.physical_relaxation import exponential_relaxation_covariance
from observer_math.two_scale_relaxation_cover import (
    gaussian_irregular_relaxation_two_scale_target_bound,
    gaussian_optimized_irregular_relaxation_two_scale_target_bound,
)


def _simulate(times: np.ndarray, tau: float, channels: int, seed: int) -> np.ndarray:
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


def _problem(scale: float = 1.0):
    calibration_times = scale * np.array(
        [0.0, 0.04, 0.11, 0.20, 0.34, 0.51, 0.73, 1.02, 1.36, 1.77]
    )
    values = _simulate(calibration_times, scale * 0.74, 36, seed=20261120)
    model = gaussian_irregular_relaxation_evalue_model(
        values,
        calibration_times,
        lower_relaxation_time=scale * 0.42,
        upper_relaxation_time=scale * 1.08,
        confidence=0.95,
        mixture_relaxation_time_grid_size=13,
    )
    target_times = scale * np.array(
        [0.0, 0.03, 0.09, 0.17, 0.29, 0.46, 0.68, 0.95, 1.29, 1.70, 2.18]
    )
    centered = target_times - np.mean(target_times)
    design = np.column_stack((np.ones(target_times.size), centered / scale))
    return model, target_times, design


def test_two_scale_cover_contains_dense_accepted_family_in_operator_norm():
    model, target_times, design = _problem()
    result = gaussian_irregular_relaxation_two_scale_target_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        calibration_outer_cover_cell_count=120,
        target_cover_point_count=11,
        covariance_confidence=0.95,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    dense = np.linspace(0.42, 1.08, 401)
    accepted = [
        float(tau)
        for tau in dense
        if gaussian_irregular_relaxation_log_evalue(model, float(tau))
        < model.log_evalue_threshold
    ]
    assert accepted
    for tau in accepted:
        assert result.retained_relaxation_time_lower_bound <= tau
        assert tau <= result.retained_relaxation_time_upper_bound
        exact = exponential_relaxation_covariance(target_times, tau)
        errors = [
            np.linalg.norm(
                exact - exponential_relaxation_covariance(target_times, float(center)),
                ord=2,
            )
            for center in result.target_cover_relaxation_times
        ]
        assert min(errors) <= result.target_eigenvalue_covering_radius + 2e-11


def test_two_scale_normalization_radius_tracks_nuisance_rank():
    model, target_times, design = _problem()
    result = gaussian_irregular_relaxation_two_scale_target_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        calibration_outer_cover_cell_count=80,
        target_cover_point_count=9,
        covariance_confidence=0.95,
        upper_theta_grid_size=32,
        lower_theta_grid_size=32,
    )
    assert np.isclose(
        result.target_normalization_covering_radius,
        design.shape[1] * result.target_eigenvalue_covering_radius,
    )
    assert np.isclose(result.combined_confidence, 0.95**2)
    assert result.target_cover_point_count == 9


def test_finer_target_cover_reduces_geometric_covering_radius():
    model, target_times, design = _problem()
    coarse = gaussian_irregular_relaxation_two_scale_target_bound(
        model,
        target_times,
        design,
        1,
        1,
        calibration_outer_cover_cell_count=80,
        target_cover_point_count=7,
        covariance_confidence=0.95,
        upper_theta_grid_size=32,
        lower_theta_grid_size=32,
    )
    fine = gaussian_irregular_relaxation_two_scale_target_bound(
        model,
        target_times,
        design,
        1,
        1,
        calibration_outer_cover_cell_count=80,
        target_cover_point_count=19,
        covariance_confidence=0.95,
        upper_theta_grid_size=32,
        lower_theta_grid_size=32,
    )
    assert fine.target_parameter_covering_radius < coarse.target_parameter_covering_radius
    assert fine.target_eigenvalue_covering_radius < coarse.target_eigenvalue_covering_radius


def test_optimizer_selects_smallest_candidate_covariance_radius():
    model, target_times, design = _problem()
    optimized = gaussian_optimized_irregular_relaxation_two_scale_target_bound(
        model,
        target_times,
        design,
        1,
        1,
        calibration_outer_cover_cell_count=80,
        candidate_target_cover_point_counts=(5, 9, 17),
        covariance_confidence=0.95,
        upper_theta_grid_size=32,
        lower_theta_grid_size=32,
    )
    assert optimized.selected_index == int(
        np.argmin(optimized.candidate_covariance_relative_errors)
    )
    assert np.isclose(
        optimized.selected.covariance_bound.covariance_relative_error,
        np.min(optimized.candidate_covariance_relative_errors),
    )


def test_two_scale_certificate_is_invariant_to_time_units():
    seconds = _problem(scale=1.0)
    milliseconds = _problem(scale=1000.0)
    result_seconds = gaussian_irregular_relaxation_two_scale_target_bound(
        *seconds,
        block_dimension=1,
        block_count=1,
        calibration_outer_cover_cell_count=80,
        target_cover_point_count=11,
        covariance_confidence=0.95,
        upper_theta_grid_size=32,
        lower_theta_grid_size=32,
    )
    result_milliseconds = gaussian_irregular_relaxation_two_scale_target_bound(
        *milliseconds,
        block_dimension=1,
        block_count=1,
        calibration_outer_cover_cell_count=80,
        target_cover_point_count=11,
        covariance_confidence=0.95,
        upper_theta_grid_size=32,
        lower_theta_grid_size=32,
    )

    assert np.isclose(
        result_milliseconds.retained_relaxation_time_width,
        1000.0 * result_seconds.retained_relaxation_time_width,
    )
    assert np.isclose(
        result_milliseconds.target_parameter_covering_radius,
        1000.0 * result_seconds.target_parameter_covering_radius,
    )
    assert np.isclose(
        result_milliseconds.target_eigenvalue_covering_radius,
        result_seconds.target_eigenvalue_covering_radius,
        atol=2e-11,
        rtol=2e-11,
    )
    assert np.isclose(
        result_milliseconds.covariance_bound.covariance_relative_error,
        result_seconds.covariance_bound.covariance_relative_error,
        atol=2e-10,
        rtol=2e-10,
    )
