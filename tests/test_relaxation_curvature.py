import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_log_evalue,
)
from observer_math.relaxation_curvature import (
    gaussian_irregular_relaxation_log_evalue_derivative,
    gaussian_irregular_relaxation_log_evalue_second_derivative_bound,
    gaussian_irregular_relaxation_quadratic_outer_cover,
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


def _model(scale: float = 1.0):
    times = scale * np.array(
        [0.0, 0.04, 0.11, 0.21, 0.35, 0.54, 0.78, 1.08, 1.45, 1.91]
    )
    values = _simulate(times, scale * 0.76, 48, seed=20261130)
    return gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=scale * 0.42,
        upper_relaxation_time=scale * 1.10,
        confidence=0.95,
        mixture_relaxation_time_grid_size=15,
    )


def test_exact_log_evalue_derivative_matches_centered_difference():
    model = _model()
    for tau in (0.50, 0.68, 0.82, 1.00):
        step = 2e-6
        numerical = (
            gaussian_irregular_relaxation_log_evalue(model, tau + step)
            - gaussian_irregular_relaxation_log_evalue(model, tau - step)
        ) / (2.0 * step)
        exact = gaussian_irregular_relaxation_log_evalue_derivative(model, tau)
        assert np.isclose(exact, numerical, atol=2e-5, rtol=2e-6)


def test_second_derivative_bound_dominates_dense_numerical_curvature():
    model = _model()
    lower = 0.58
    upper = 0.90
    bound = gaussian_irregular_relaxation_log_evalue_second_derivative_bound(
        model,
        lower_relaxation_time=lower,
        upper_relaxation_time=upper,
    )
    grid = np.linspace(lower + 2e-4, upper - 2e-4, 81)
    step = 5e-5
    numerical = []
    for tau in grid:
        left = gaussian_irregular_relaxation_log_evalue_derivative(model, tau - step)
        right = gaussian_irregular_relaxation_log_evalue_derivative(model, tau + step)
        numerical.append(abs((right - left) / (2.0 * step)))
    assert max(numerical) <= bound * (1.0 + 2e-5)


def test_quadratic_outer_cover_contains_dense_continuum_acceptance_set():
    model = _model()
    cover = gaussian_irregular_relaxation_quadratic_outer_cover(model, cell_count=80)
    dense = np.linspace(0.42, 1.10, 1601)
    width = float(cover.cell_edges[1] - cover.cell_edges[0])
    accepted_count = 0
    for tau in dense:
        if gaussian_irregular_relaxation_log_evalue(model, float(tau)) >= model.log_evalue_threshold:
            continue
        accepted_count += 1
        index = min(int((tau - cover.cell_edges[0]) / width), cover.total_cell_count - 1)
        assert cover.retained_mask[index]
    assert accepted_count > 0
    assert cover.retained_cell_count > 0


def test_quadratic_cover_is_no_wider_than_first_order_cover_on_same_cells():
    model = _model()
    first_order = gaussian_irregular_relaxation_evalue_outer_cover(model, cell_count=80)
    quadratic = gaussian_irregular_relaxation_quadratic_outer_cover(model, cell_count=80)
    first_width = (
        first_order.retained_relaxation_time_upper_bound
        - first_order.retained_relaxation_time_lower_bound
    )
    quadratic_width = (
        quadratic.retained_relaxation_time_upper_bound
        - quadratic.retained_relaxation_time_lower_bound
    )
    assert quadratic_width <= first_width + 1e-15
    assert quadratic.retained_cell_count <= first_order.retained_cell_count


def test_quadratic_certificate_rescales_exactly_with_time_units():
    seconds = _model(scale=1.0)
    milliseconds = _model(scale=1000.0)

    tau = 0.78
    derivative_seconds = gaussian_irregular_relaxation_log_evalue_derivative(seconds, tau)
    derivative_milliseconds = gaussian_irregular_relaxation_log_evalue_derivative(
        milliseconds,
        1000.0 * tau,
    )
    assert np.isclose(
        derivative_milliseconds,
        derivative_seconds / 1000.0,
        atol=2e-12,
        rtol=2e-11,
    )

    curvature_seconds = gaussian_irregular_relaxation_log_evalue_second_derivative_bound(
        seconds,
        lower_relaxation_time=0.60,
        upper_relaxation_time=0.90,
    )
    curvature_milliseconds = gaussian_irregular_relaxation_log_evalue_second_derivative_bound(
        milliseconds,
        lower_relaxation_time=600.0,
        upper_relaxation_time=900.0,
    )
    assert np.isclose(
        curvature_milliseconds,
        curvature_seconds / 1_000_000.0,
        atol=2e-12,
        rtol=2e-10,
    )

    cover_seconds = gaussian_irregular_relaxation_quadratic_outer_cover(seconds, cell_count=80)
    cover_milliseconds = gaussian_irregular_relaxation_quadratic_outer_cover(
        milliseconds,
        cell_count=80,
    )
    assert np.array_equal(cover_seconds.retained_mask, cover_milliseconds.retained_mask)
    assert np.isclose(
        cover_milliseconds.retained_relaxation_time_lower_bound,
        1000.0 * cover_seconds.retained_relaxation_time_lower_bound,
    )
    assert np.isclose(
        cover_milliseconds.retained_relaxation_time_upper_bound,
        1000.0 * cover_seconds.retained_relaxation_time_upper_bound,
    )
