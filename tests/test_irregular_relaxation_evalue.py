import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_log_evalue,
    gaussian_irregular_relaxation_log_likelihood_kernel,
    gaussian_irregular_relaxation_log_likelihood_lipschitz_bound,
    gaussian_irregular_relaxation_target_matrix_chernoff_bound,
)
from observer_math.physical_relaxation import exponential_relaxation_covariance


def _simulate_irregular_relaxation(
    sample_times: np.ndarray,
    relaxation_time: float,
    channel_count: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty((sample_times.size, channel_count), dtype=float)
    values[0] = rng.standard_normal(channel_count)
    intervals = np.diff(sample_times)
    alpha = np.exp(-intervals / relaxation_time)
    for index, coefficient in enumerate(alpha):
        innovation_scale = np.sqrt(1.0 - coefficient * coefficient)
        values[index + 1] = (
            coefficient * values[index]
            + innovation_scale * rng.standard_normal(channel_count)
        )
    return values


def _dense_log_likelihood_kernel(
    values: np.ndarray,
    sample_times: np.ndarray,
    relaxation_time: float,
) -> float:
    covariance = exponential_relaxation_covariance(sample_times, relaxation_time)
    sign, log_determinant = np.linalg.slogdet(covariance)
    assert sign > 0.0
    scatter = values @ values.T
    quadratic = float(np.trace(np.linalg.solve(covariance, scatter)))
    return float(-0.5 * values.shape[1] * log_determinant - 0.5 * quadratic)


def test_local_innovation_likelihood_ratios_match_dense_gaussian_likelihood_ratios():
    times = np.array([0.0, 0.04, 0.13, 0.31, 0.52, 0.91, 1.4, 2.0])
    values = _simulate_irregular_relaxation(times, 0.72, 7, seed=20261101)

    tau_a = 0.58
    tau_b = 0.94
    local_a = gaussian_irregular_relaxation_log_likelihood_kernel(values, times, tau_a)
    local_b = gaussian_irregular_relaxation_log_likelihood_kernel(values, times, tau_b)
    dense_a = _dense_log_likelihood_kernel(values, times, tau_a)
    dense_b = _dense_log_likelihood_kernel(values, times, tau_b)

    assert np.isclose(local_a - local_b, dense_a - dense_b, atol=2e-11, rtol=2e-11)


def test_finite_mixture_evalue_density_is_algebraically_normalized():
    times = np.array([0.0, 0.06, 0.18, 0.35, 0.63, 1.05, 1.6])
    values = _simulate_irregular_relaxation(times, 0.8, 11, seed=20261102)
    model = gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=0.5,
        upper_relaxation_time=1.1,
        confidence=0.95,
        mixture_relaxation_time_grid_size=9,
    )

    component_log_evalues = np.asarray(
        [
            gaussian_irregular_relaxation_log_evalue(model, float(tau))
            for tau in model.mixture_relaxation_time_grid
        ]
    )
    assert np.isclose(np.mean(np.exp(-component_log_evalues)), 1.0, atol=2e-13, rtol=2e-13)


def test_irregular_tau_evalue_is_invariant_to_time_units():
    times_seconds = np.array([0.0, 0.05, 0.14, 0.29, 0.57, 0.96, 1.48, 2.2])
    values = _simulate_irregular_relaxation(times_seconds, 0.82, 13, seed=20261103)
    seconds = gaussian_irregular_relaxation_evalue_model(
        values,
        times_seconds,
        lower_relaxation_time=0.5,
        upper_relaxation_time=1.15,
        confidence=0.975,
        mixture_relaxation_time_grid_size=11,
    )

    scale = 1000.0
    milliseconds = gaussian_irregular_relaxation_evalue_model(
        values,
        scale * times_seconds,
        lower_relaxation_time=scale * 0.5,
        upper_relaxation_time=scale * 1.15,
        confidence=0.975,
        mixture_relaxation_time_grid_size=11,
    )

    for tau in np.linspace(0.5, 1.15, 17):
        log_e_seconds = gaussian_irregular_relaxation_log_evalue(seconds, float(tau))
        log_e_milliseconds = gaussian_irregular_relaxation_log_evalue(
            milliseconds,
            float(scale * tau),
        )
        assert np.isclose(log_e_seconds, log_e_milliseconds, atol=2e-12, rtol=2e-12)

    bound_seconds = gaussian_irregular_relaxation_log_likelihood_lipschitz_bound(seconds)
    bound_milliseconds = gaussian_irregular_relaxation_log_likelihood_lipschitz_bound(
        milliseconds
    )
    assert np.isclose(
        bound_seconds,
        scale * bound_milliseconds,
        atol=2e-10,
        rtol=2e-10,
    )


def test_certified_outer_cover_contains_dense_continuum_acceptance_check():
    times = np.array([0.0, 0.03, 0.09, 0.21, 0.38, 0.66, 1.02, 1.49, 2.05])
    values = _simulate_irregular_relaxation(times, 0.76, 24, seed=20261104)
    model = gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=0.45,
        upper_relaxation_time=1.15,
        confidence=0.95,
        mixture_relaxation_time_grid_size=13,
    )
    outer = gaussian_irregular_relaxation_evalue_outer_cover(model, cell_count=80)

    dense_grid = np.linspace(0.45, 1.15, 1601)
    width = float(outer.cell_edges[1] - outer.cell_edges[0])
    accepted_count = 0
    for tau in dense_grid:
        accepted = (
            gaussian_irregular_relaxation_log_evalue(model, float(tau))
            < model.log_evalue_threshold
        )
        if not accepted:
            continue
        accepted_count += 1
        index = min(int((tau - outer.cell_edges[0]) / width), outer.total_cell_count - 1)
        assert outer.retained_mask[index]

    full_interval_bound = gaussian_irregular_relaxation_log_likelihood_lipschitz_bound(model)
    assert accepted_count > 0
    assert outer.retained_cell_count > 0
    assert np.max(outer.cell_log_likelihood_lipschitz_bounds) <= full_interval_bound + 1e-12


def test_calibrated_irregular_tau_family_composes_with_independent_target_bound():
    calibration_times = np.array([0.0, 0.04, 0.12, 0.26, 0.49, 0.82, 1.24, 1.78])
    true_tau = 0.7
    calibration_values = _simulate_irregular_relaxation(
        calibration_times,
        true_tau,
        30,
        seed=20261105,
    )
    model = gaussian_irregular_relaxation_evalue_model(
        calibration_values,
        calibration_times,
        lower_relaxation_time=0.45,
        upper_relaxation_time=1.0,
        confidence=0.95,
        mixture_relaxation_time_grid_size=11,
    )

    target_times = np.array(
        [0.0, 0.05, 0.11, 0.19, 0.31, 0.48, 0.72, 1.01, 1.37, 1.8, 2.3]
    )
    centered = target_times - np.mean(target_times)
    design = np.column_stack((np.ones(target_times.size), centered))
    result = gaussian_irregular_relaxation_target_matrix_chernoff_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=60,
        covariance_confidence=0.95,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    assert np.isclose(result.combined_confidence, 0.95**2)
    assert result.calibration_outer_cover.retained_cell_count > 0
    assert result.target_eigenvalue_covering_radius > 0.0
    assert np.isclose(
        result.target_normalization_covering_radius,
        2.0 * result.target_eigenvalue_covering_radius,
    )
    assert np.isfinite(result.covariance_bound.covariance_relative_error)

    dense_grid = np.linspace(0.45, 1.0, 401)
    retained_centers = result.calibration_outer_cover.cell_centers[
        result.calibration_outer_cover.retained_mask
    ]
    for tau in dense_grid:
        if gaussian_irregular_relaxation_log_evalue(model, float(tau)) >= model.log_evalue_threshold:
            continue
        exact = exponential_relaxation_covariance(target_times, float(tau))
        errors = [
            np.linalg.norm(
                exact - exponential_relaxation_covariance(target_times, float(center)),
                ord=2,
            )
            for center in retained_centers
        ]
        assert min(errors) <= result.target_eigenvalue_covering_radius + 3e-12
