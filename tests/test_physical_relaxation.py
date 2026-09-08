import numpy as np

from observer_math.physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_markov_factorization,
    exponential_relaxation_operator_lipschitz_bound,
    exponential_relaxation_temporal_cover,
    gaussian_relaxation_time_matrix_chernoff_bound,
    relaxation_autocorrelation,
    relaxation_time_from_autocorrelation,
    uniform_exponential_relaxation_covariance,
)


def test_uniform_relaxation_covariance_is_exact_ar1_sampling():
    sample_count = 11
    sample_interval = 0.2
    relaxation_time = 0.75
    phi = relaxation_autocorrelation(sample_interval, relaxation_time)

    covariance = uniform_exponential_relaxation_covariance(
        sample_count,
        sample_interval,
        relaxation_time,
    )
    indices = np.arange(sample_count)
    expected = phi ** np.abs(indices[:, None] - indices[None, :])

    assert np.allclose(covariance, expected, atol=1e-13, rtol=1e-13)


def test_coarse_subsampling_preserves_one_physical_relaxation_time():
    sample_interval = 0.1
    relaxation_time = 0.8
    fine = uniform_exponential_relaxation_covariance(16, sample_interval, relaxation_time)
    coarse_from_fine = fine[::3, ::3]
    coarse_direct = uniform_exponential_relaxation_covariance(
        coarse_from_fine.shape[0],
        3.0 * sample_interval,
        relaxation_time,
    )

    phi_fine = relaxation_autocorrelation(sample_interval, relaxation_time)
    phi_coarse = relaxation_autocorrelation(3.0 * sample_interval, relaxation_time)

    assert np.isclose(phi_coarse, phi_fine**3, atol=1e-14, rtol=1e-14)
    assert np.allclose(coarse_from_fine, coarse_direct, atol=1e-13, rtol=1e-13)


def test_relaxation_time_is_invariant_to_sampling_interval_and_time_units():
    relaxation_time = 1.7
    for sample_interval in (0.05, 0.2, 0.8):
        phi = relaxation_autocorrelation(sample_interval, relaxation_time)
        recovered = relaxation_time_from_autocorrelation(phi, sample_interval)
        assert np.isclose(recovered, relaxation_time, atol=1e-13, rtol=1e-13)

    times = np.array([0.0, 0.07, 0.19, 0.42, 0.91, 1.6])
    covariance_seconds = exponential_relaxation_covariance(times, relaxation_time)
    scale = 1000.0
    covariance_milliseconds = exponential_relaxation_covariance(
        scale * times,
        scale * relaxation_time,
    )
    assert np.allclose(
        covariance_seconds,
        covariance_milliseconds,
        atol=1e-13,
        rtol=1e-13,
    )


def test_irregular_sampling_covariance_is_symmetric_positive_semidefinite():
    times = np.array([0.0, 0.04, 0.17, 0.31, 0.88, 1.03, 1.9, 2.7])
    covariance = exponential_relaxation_covariance(times, 0.62)

    assert np.allclose(covariance, covariance.T, atol=1e-14)
    assert np.allclose(np.diag(covariance), 1.0, atol=1e-14)
    assert np.linalg.eigvalsh(covariance)[0] > -1e-12
    assert np.isclose(covariance[1, 4], np.exp(-(0.88 - 0.04) / 0.62))


def test_relaxation_lipschitz_bound_controls_dense_between_grid_values():
    times = np.array([0.0, 0.05, 0.13, 0.27, 0.52, 0.93, 1.45, 2.1])
    lower = 0.45
    upper = 1.15
    design = np.column_stack((np.ones(times.size), times))
    cover = exponential_relaxation_temporal_cover(
        times,
        design,
        lower_relaxation_time=lower,
        upper_relaxation_time=upper,
        relaxation_time_grid_size=17,
    )

    direct_lipschitz = exponential_relaxation_operator_lipschitz_bound(times, lower, upper)
    assert np.isclose(cover.operator_lipschitz_bound, direct_lipschitz)

    for tau in np.linspace(lower, upper, 141):
        nearest_index = int(np.argmin(np.abs(cover.relaxation_time_grid - tau)))
        nearest_tau = float(cover.relaxation_time_grid[nearest_index])
        exact = exponential_relaxation_covariance(times, tau)
        center = cover.temporal_covariance_grid[nearest_index]
        error = float(np.linalg.norm(exact - center, ord=2))
        local_limit = direct_lipschitz * abs(tau - nearest_tau)
        assert error <= local_limit + 2e-12
        assert error <= cover.raw_operator_covering_radius + 2e-12


def test_relaxation_time_cover_composes_with_proposition_49():
    sample_count = 36
    sample_interval = 0.1
    times = sample_interval * np.arange(sample_count)
    centered_time = times - np.mean(times)
    design = np.column_stack((np.ones(sample_count), centered_time))

    result = gaussian_relaxation_time_matrix_chernoff_bound(
        times,
        design,
        block_dimension=1,
        block_count=1,
        lower_relaxation_time=0.55,
        upper_relaxation_time=0.9,
        relaxation_time_grid_size=17,
        confidence=0.95,
        upper_theta_grid_size=64,
        lower_theta_grid_size=64,
    )

    cover = result.temporal_cover
    bound = result.covariance_bound
    assert cover.nuisance_rank == 2
    assert cover.raw_operator_covering_radius > 0.0
    assert np.isclose(
        cover.projected_normalization_covering_radius,
        2.0 * cover.raw_operator_covering_radius,
    )
    assert bound.cover_point_count == 17
    assert np.isfinite(bound.covariance_relative_error)
    assert bound.projected_degrees_of_freedom_lower_bound > 0.0

    projector = np.eye(sample_count) - design @ np.linalg.inv(design.T @ design) @ design.T
    for tau in np.linspace(0.55, 0.9, 51):
        nearest_index = int(np.argmin(np.abs(cover.relaxation_time_grid - tau)))
        exact = exponential_relaxation_covariance(times, tau)
        center = cover.temporal_covariance_grid[nearest_index]
        delta = exact - center
        assert np.linalg.norm(delta, ord=2) <= cover.raw_operator_covering_radius + 2e-12
        normalization_error = abs(float(np.trace(projector @ delta)))
        assert normalization_error <= cover.projected_normalization_covering_radius + 2e-12


def test_irregular_markov_step_products_reproduce_every_covariance_entry():
    times = np.array([0.0, 0.03, 0.14, 0.38, 0.44, 1.1, 1.75, 2.6])
    relaxation_time = 0.73
    factorization = exponential_relaxation_markov_factorization(times, relaxation_time)
    covariance = exponential_relaxation_covariance(times, relaxation_time)

    for left in range(times.size):
        for right in range(left + 1, times.size):
            product = float(np.prod(factorization.step_correlations[left:right]))
            assert np.isclose(product, covariance[left, right], atol=2e-14, rtol=2e-14)


def test_irregular_markov_precision_is_exact_inverse_covariance():
    times = np.array([0.0, 0.06, 0.19, 0.55, 0.72, 1.31, 2.05])
    relaxation_time = 0.81
    factorization = exponential_relaxation_markov_factorization(times, relaxation_time)
    covariance = exponential_relaxation_covariance(times, relaxation_time)

    identity = factorization.precision_matrix @ covariance
    assert np.allclose(identity, np.eye(times.size), atol=3e-13, rtol=3e-13)

    off_band = factorization.precision_matrix.copy()
    for row in range(times.size):
        for column in range(times.size):
            if abs(row - column) <= 1:
                off_band[row, column] = 0.0
    assert np.count_nonzero(off_band) == 0


def test_irregular_markov_whitener_makes_temporal_covariance_identity():
    times = np.array([0.0, 0.08, 0.17, 0.51, 0.9, 1.02, 1.88, 2.4])
    relaxation_time = 0.64
    factorization = exponential_relaxation_markov_factorization(times, relaxation_time)
    covariance = exponential_relaxation_covariance(times, relaxation_time)

    whitened = factorization.whitening_matrix @ covariance @ factorization.whitening_matrix.T
    assert np.allclose(whitened, np.eye(times.size), atol=3e-13, rtol=3e-13)
    assert np.allclose(
        factorization.precision_matrix,
        factorization.whitening_matrix.T @ factorization.whitening_matrix,
        atol=3e-13,
        rtol=3e-13,
    )


def test_irregular_markov_log_determinant_matches_dense_covariance():
    times = np.array([0.0, 0.04, 0.16, 0.33, 0.78, 1.4, 1.58, 2.9])
    relaxation_time = 0.92
    factorization = exponential_relaxation_markov_factorization(times, relaxation_time)
    covariance = exponential_relaxation_covariance(times, relaxation_time)

    sign, dense_log_determinant = np.linalg.slogdet(covariance)
    assert sign == 1.0
    assert np.isclose(
        factorization.covariance_log_determinant,
        dense_log_determinant,
        atol=3e-13,
        rtol=3e-13,
    )


def test_irregular_markov_semigroup_survives_deleting_an_intermediate_sample():
    times = np.array([0.0, 0.17, 0.49])
    relaxation_time = 0.77
    fine = exponential_relaxation_markov_factorization(times, relaxation_time)
    coarse = exponential_relaxation_markov_factorization(times[[0, 2]], relaxation_time)

    composed_correlation = fine.step_correlations[0] * fine.step_correlations[1]
    assert np.isclose(
        composed_correlation,
        coarse.step_correlations[0],
        atol=2e-14,
        rtol=2e-14,
    )

    composed_variance = (
        fine.step_correlations[1] ** 2 * fine.innovation_variances[0]
        + fine.innovation_variances[1]
    )
    assert np.isclose(
        composed_variance,
        coarse.innovation_variances[0],
        atol=2e-14,
        rtol=2e-14,
    )
