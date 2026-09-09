import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_log_evalue,
    gaussian_irregular_relaxation_log_likelihood_kernel,
)
from observer_math.physical_relaxation import exponential_relaxation_covariance
from observer_math.second_order_relaxation import (
    gaussian_irregular_relaxation_log_likelihood_second_derivative,
    gaussian_irregular_relaxation_log_likelihood_second_derivative_bound,
    gaussian_irregular_relaxation_second_order_outer_cover,
    gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound,
)


def _simulate_irregular_relaxation(
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
            + np.sqrt(1.0 - coefficient * coefficient)
            * rng.standard_normal(channel_count)
        )
    return values


def _experiment_ao_calibration_times() -> np.ndarray:
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


def _experiment_ao_model():
    times = _experiment_ao_calibration_times()
    values = _simulate_irregular_relaxation(times, 0.78, 96, seed=20261110)
    model = gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=0.40,
        upper_relaxation_time=1.25,
        confidence=0.975,
        mixture_relaxation_time_grid_size=21,
    )
    return model


def _experiment_ao_target() -> tuple[np.ndarray, np.ndarray]:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10]),
        119,
    )
    times = np.concatenate(([0.0], np.cumsum(gaps)))
    centered = times - np.mean(times)
    design = np.column_stack((np.ones(times.size), centered))
    return times, design


def _projector(design: np.ndarray) -> np.ndarray:
    basis, _ = np.linalg.qr(design, mode="complete")
    complement = basis[:, design.shape[1] :]
    return complement @ complement.T


def test_exact_log_likelihood_second_derivative_matches_finite_difference():
    times = np.array([0.0, 0.04, 0.13, 0.31, 0.52, 0.91, 1.4, 2.0])
    values = _simulate_irregular_relaxation(times, 0.74, 17, seed=20261120)
    model = gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=0.45,
        upper_relaxation_time=1.10,
        confidence=0.95,
        mixture_relaxation_time_grid_size=11,
    )

    tau = 0.76
    step = 1e-4
    finite_difference = (
        gaussian_irregular_relaxation_log_likelihood_kernel(values, times, tau + step)
        - 2.0 * gaussian_irregular_relaxation_log_likelihood_kernel(values, times, tau)
        + gaussian_irregular_relaxation_log_likelihood_kernel(values, times, tau - step)
    ) / step**2
    exact = gaussian_irregular_relaxation_log_likelihood_second_derivative(model, tau)

    assert np.isclose(exact, finite_difference, atol=2e-3, rtol=2e-5)


def test_second_derivative_bound_controls_dense_interval():
    model = _experiment_ao_model()
    lower = 0.66
    upper = 0.90
    bound = gaussian_irregular_relaxation_log_likelihood_second_derivative_bound(
        model,
        lower_relaxation_time=lower,
        upper_relaxation_time=upper,
    )

    exact = np.asarray(
        [
            abs(
                gaussian_irregular_relaxation_log_likelihood_second_derivative(
                    model,
                    float(tau),
                )
            )
            for tau in np.linspace(lower, upper, 401)
        ]
    )
    assert np.max(exact) <= bound
    assert bound > 0.0


def test_second_order_cover_contains_continuum_and_improves_first_order_cover():
    model = _experiment_ao_model()
    second = gaussian_irregular_relaxation_second_order_outer_cover(
        model,
        cell_count=160,
    )
    first = gaussian_irregular_relaxation_evalue_outer_cover(model, cell_count=160)

    dense_grid = np.linspace(0.40, 1.25, 2001)
    width = float(second.cell_edges[1] - second.cell_edges[0])
    accepted_count = 0
    for tau in dense_grid:
        if gaussian_irregular_relaxation_log_evalue(model, float(tau)) >= model.log_evalue_threshold:
            continue
        accepted_count += 1
        index = min(
            int((tau - second.cell_edges[0]) / width),
            second.total_cell_count - 1,
        )
        assert second.retained_mask[index]

    true_index = min(
        int((0.78 - second.cell_edges[0]) / width),
        second.total_cell_count - 1,
    )
    assert accepted_count == 361
    assert second.retained_mask[true_index]
    assert second.retained_cell_count == 31
    assert first.retained_cell_count == 115
    assert np.all(second.retained_mask <= first.retained_mask)
    assert np.isclose(second.retained_relaxation_time_lower_bound, 0.686875)
    assert np.isclose(second.retained_relaxation_time_upper_bound, 0.8515625)


def test_second_order_cover_is_invariant_to_time_units():
    times = _experiment_ao_calibration_times()
    values = _simulate_irregular_relaxation(times, 0.78, 48, seed=20261121)
    seconds = gaussian_irregular_relaxation_evalue_model(
        values,
        times,
        lower_relaxation_time=0.40,
        upper_relaxation_time=1.25,
        confidence=0.95,
        mixture_relaxation_time_grid_size=15,
    )
    scale = 1000.0
    milliseconds = gaussian_irregular_relaxation_evalue_model(
        values,
        scale * times,
        lower_relaxation_time=scale * 0.40,
        upper_relaxation_time=scale * 1.25,
        confidence=0.95,
        mixture_relaxation_time_grid_size=15,
    )

    seconds_cover = gaussian_irregular_relaxation_second_order_outer_cover(
        seconds,
        cell_count=80,
    )
    milliseconds_cover = gaussian_irregular_relaxation_second_order_outer_cover(
        milliseconds,
        cell_count=80,
    )

    assert np.array_equal(seconds_cover.retained_mask, milliseconds_cover.retained_mask)
    assert np.allclose(
        scale * seconds_cover.cell_edges,
        milliseconds_cover.cell_edges,
        atol=2e-12,
        rtol=2e-12,
    )
    assert np.allclose(
        seconds_cover.cell_interpolation_error_bounds,
        milliseconds_cover.cell_interpolation_error_bounds,
        atol=2e-10,
        rtol=2e-10,
    )


def test_reference_whitened_taylor_radii_cover_dense_retained_family():
    model = _experiment_ao_model()
    target_times, target_design = _experiment_ao_target()
    result = gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound(
        model,
        target_times,
        target_design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=160,
        covariance_confidence=0.975,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    whitening = result.reference_whitening_matrix
    transformed_design = result.transformed_nuisance_design
    projector = _projector(transformed_design)
    outer = result.calibration_outer_cover
    retained_indices = np.flatnonzero(outer.retained_mask)

    for index in retained_indices[::5]:
        lower = float(outer.cell_edges[index])
        upper = float(outer.cell_edges[index + 1])
        center = float(outer.cell_centers[index])
        center_covariance = (
            whitening
            @ exponential_relaxation_covariance(target_times, center)
            @ whitening.T
        )
        center_degrees = float(np.trace(projector @ center_covariance))
        for tau in np.linspace(lower, upper, 9):
            covariance = (
                whitening
                @ exponential_relaxation_covariance(target_times, float(tau))
                @ whitening.T
            )
            assert (
                np.linalg.norm(covariance - center_covariance, ord=2)
                <= result.temporal_covering_radius + 2e-11
            )
            degrees = float(np.trace(projector @ covariance))
            assert (
                abs(degrees - center_degrees)
                <= result.normalization_covering_radius + 2e-11
            )


def test_experiment_ao_reference_whitening_enters_subunit_covariance_regime():
    model = _experiment_ao_model()
    target_times, target_design = _experiment_ao_target()
    result = gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound(
        model,
        target_times,
        target_design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=160,
        covariance_confidence=0.975,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    identity_check = (
        result.reference_whitening_matrix
        @ exponential_relaxation_covariance(
            target_times,
            result.reference_relaxation_time,
        )
        @ result.reference_whitening_matrix.T
    )

    assert np.allclose(identity_check, np.eye(target_times.size), atol=3e-13, rtol=3e-13)
    assert np.isclose(result.combined_confidence, 0.975**2)
    assert result.calibration_outer_cover.retained_cell_count == 31
    assert np.isclose(result.reference_relaxation_time, 0.76921875)
    assert np.isclose(result.temporal_covering_radius, 0.008495864441166396)
    assert np.isclose(result.normalization_covering_radius, 0.4669981838440142)
    assert np.isclose(
        result.covariance_bound.covariance_relative_error,
        0.6899552435608667,
        atol=2e-10,
        rtol=2e-10,
    )
    assert result.covariance_bound.covariance_relative_error < 1.0
