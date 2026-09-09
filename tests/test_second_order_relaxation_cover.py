import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_log_evalue,
)
from observer_math.second_order_relaxation_cover import (
    gaussian_irregular_relaxation_log_likelihood_derivative,
    gaussian_irregular_relaxation_log_likelihood_second_derivative_bound,
    gaussian_irregular_relaxation_second_order_outer_cover,
    gaussian_irregular_relaxation_second_order_target_matrix_chernoff_bound,
)


def _simulate(
    sample_times: np.ndarray,
    relaxation_time: float,
    channel_count: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty((sample_times.size, channel_count), dtype=float)
    values[0] = rng.standard_normal(channel_count)
    alpha = np.exp(-np.diff(sample_times) / relaxation_time)
    for index, coefficient in enumerate(alpha):
        values[index + 1] = (
            coefficient * values[index]
            + np.sqrt(1.0 - coefficient * coefficient) * rng.standard_normal(channel_count)
        )
    return values


def _an_times() -> np.ndarray:
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


def _an_model():
    times = _an_times()
    values = _simulate(times, 0.78, 96, seed=20261110)
    return gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=0.40,
        upper_relaxation_time=1.25,
        confidence=0.975,
        mixture_relaxation_time_grid_size=21,
    )


def test_exact_likelihood_derivative_matches_centered_difference():
    model = _an_model()
    for tau in (0.48, 0.72, 0.95, 1.18):
        step = 1e-6
        exact = gaussian_irregular_relaxation_log_likelihood_derivative(model, tau)
        numerical = -(
            gaussian_irregular_relaxation_log_evalue(model, tau + step)
            - gaussian_irregular_relaxation_log_evalue(model, tau - step)
        ) / (2.0 * step)
        assert np.isclose(exact, numerical, atol=2e-5, rtol=2e-7)


def test_second_derivative_bound_dominates_dense_derivative_change():
    model = _an_model()
    intervals = ((0.42, 0.48), (0.66, 0.74), (0.80, 0.88), (1.05, 1.18))
    for lower, upper in intervals:
        bound = gaussian_irregular_relaxation_log_likelihood_second_derivative_bound(
            model,
            lower_relaxation_time=lower,
            upper_relaxation_time=upper,
        )
        grid = np.linspace(lower, upper, 201)
        derivatives = np.asarray(
            [gaussian_irregular_relaxation_log_likelihood_derivative(model, tau) for tau in grid]
        )
        slopes = np.abs(np.diff(derivatives) / np.diff(grid))
        assert np.max(slopes) <= bound * (1.0 + 1e-10)


def test_second_order_outer_cover_contains_dense_continuum_acceptance():
    model = _an_model()
    outer = gaussian_irregular_relaxation_second_order_outer_cover(model, cell_count=160)
    dense = np.linspace(0.40, 1.25, 6001)
    width = float(outer.cell_edges[1] - outer.cell_edges[0])

    accepted_count = 0
    for tau in dense:
        if gaussian_irregular_relaxation_log_evalue(model, float(tau)) >= model.log_evalue_threshold:
            continue
        accepted_count += 1
        index = min(int((tau - outer.cell_edges[0]) / width), outer.total_cell_count - 1)
        assert outer.retained_mask[index]

    assert accepted_count > 0
    assert outer.retained_cell_count > 0


def test_second_order_cover_sharply_improves_experiment_an_certificate():
    model = _an_model()
    first_order = gaussian_irregular_relaxation_evalue_outer_cover(model, cell_count=160)
    second_order = gaussian_irregular_relaxation_second_order_outer_cover(model, cell_count=160)

    assert first_order.retained_cell_count == 115
    assert second_order.retained_cell_count == 31
    assert np.isclose(second_order.retained_relaxation_time_lower_bound, 0.686875)
    assert np.isclose(second_order.retained_relaxation_time_upper_bound, 0.8515625)
    assert second_order.retained_cell_count < 0.3 * first_order.retained_cell_count


def test_second_order_cover_composes_with_independent_target_bound():
    model = _an_model()
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    target_times = np.concatenate(([0.0], np.cumsum(gaps)))
    centered = target_times - np.mean(target_times)
    design = np.column_stack((np.ones(target_times.size), centered))

    result = gaussian_irregular_relaxation_second_order_target_matrix_chernoff_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=160,
        covariance_confidence=0.975,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    assert np.isclose(result.combined_confidence, 0.975**2)
    assert result.calibration_outer_cover.retained_cell_count == 31
    assert result.target_eigenvalue_covering_radius > 0.0
    assert np.isfinite(result.covariance_bound.covariance_relative_error)
