import numpy as np

from observer_math.calibrated_temporal_family import (
    gaussian_ar1_white_noise_increment_norm_bounds,
    gaussian_ar1_white_noise_increment_parameter_interval,
    gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound,
    separable_gaussian_calibrated_ar1_white_noise_projected_covariance,
)


def _ar1_matrix(sample_count, phi):
    indices = np.arange(sample_count)
    return phi ** np.abs(indices[:, None] - indices[None, :])


def _temporal_member(sample_count, phi, eta):
    return (1.0 - eta) * _ar1_matrix(sample_count, phi) + eta * np.eye(sample_count)


def _increment_operator(sample_count, lag):
    operator = np.zeros((sample_count - lag, sample_count))
    rows = np.arange(sample_count - lag)
    operator[rows, rows] = -1.0
    operator[rows, rows + lag] = 1.0
    return operator


def _affine_design(sample_count):
    time = np.linspace(-1.0, 1.0, sample_count)
    return np.column_stack((np.ones_like(time), time))


def _simulate_calibration(sample_count, channel_count, phi, eta, seed=0):
    rng = np.random.default_rng(seed)
    temporal = _temporal_member(sample_count, phi, eta)
    factor = np.linalg.cholesky(temporal)
    return factor @ rng.standard_normal((sample_count, channel_count))


def test_increment_specific_norm_bounds_dominate_dense_exact_covariances():
    sample_count = 36
    lower_phi = 0.30
    upper_eta = 0.08

    for lag in (1, 2):
        trace_bound, frobenius_bound, spectral_bound = (
            gaussian_ar1_white_noise_increment_norm_bounds(
                sample_count,
                lag,
                lower_autocorrelation=lower_phi,
                upper_white_noise_fraction=upper_eta,
            )
        )
        operator = _increment_operator(sample_count, lag)
        for phi in np.linspace(lower_phi, 0.72, 9):
            for eta in np.linspace(0.0, upper_eta, 5):
                temporal = _temporal_member(sample_count, float(phi), float(eta))
                increments = operator @ temporal @ operator.T

                assert np.trace(increments) <= trace_bound + 1e-10
                assert np.linalg.norm(increments, ord="fro") <= frobenius_bound + 1e-10
                assert np.linalg.norm(increments, ord=2) <= spectral_bound + 1e-10


def test_constant_channel_offsets_cancel_from_two_lag_calibration():
    values = _simulate_calibration(90, 12, 0.52, 0.04, seed=11)
    offsets = np.linspace(-40.0, 70.0, values.shape[1])

    base = gaussian_ar1_white_noise_increment_parameter_interval(
        values,
        lower_autocorrelation=0.30,
        upper_autocorrelation=0.75,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.10,
        confidence=0.99,
    )
    shifted = gaussian_ar1_white_noise_increment_parameter_interval(
        values + offsets[None, :],
        lower_autocorrelation=0.30,
        upper_autocorrelation=0.75,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.10,
        confidence=0.99,
    )

    assert np.isclose(base.lag_one.estimate, shifted.lag_one.estimate, atol=1e-13)
    assert np.isclose(base.lag_two.estimate, shifted.lag_two.estimate, atol=1e-13)
    assert np.isclose(
        base.autocorrelation_lower_bound,
        shifted.autocorrelation_lower_bound,
        atol=1e-13,
    )
    assert np.isclose(
        base.autocorrelation_upper_bound,
        shifted.autocorrelation_upper_bound,
        atol=1e-13,
    )
    assert np.isclose(
        base.white_noise_fraction_lower_bound,
        shifted.white_noise_fraction_lower_bound,
        atol=1e-13,
    )
    assert np.isclose(
        base.white_noise_fraction_upper_bound,
        shifted.white_noise_fraction_upper_bound,
        atol=1e-13,
    )


def test_seeded_two_parameter_interval_contains_generating_pair():
    true_phi = 0.55
    true_eta = 0.04
    calibration = _simulate_calibration(180, 200, true_phi, true_eta, seed=123)

    interval = gaussian_ar1_white_noise_increment_parameter_interval(
        calibration,
        lower_autocorrelation=0.35,
        upper_autocorrelation=0.75,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.10,
        confidence=0.999,
    )

    assert interval.interval_intersects_declared_model
    assert interval.lag_one.lower_bound <= (1.0 - true_eta) * true_phi
    assert (1.0 - true_eta) * true_phi <= interval.lag_one.upper_bound
    assert interval.lag_two.lower_bound <= (1.0 - true_eta) * true_phi**2
    assert (1.0 - true_eta) * true_phi**2 <= interval.lag_two.upper_bound
    assert interval.autocorrelation_lower_bound <= true_phi <= interval.autocorrelation_upper_bound
    assert (
        interval.white_noise_fraction_lower_bound
        <= true_eta
        <= interval.white_noise_fraction_upper_bound
    )


def test_calibrated_matrix_bound_has_explicit_independent_record_confidence():
    calibration = _simulate_calibration(110, 96, 0.58, 0.03, seed=31)
    design = _affine_design(72)

    bound = gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound(
        calibration,
        3,
        1,
        design,
        lower_autocorrelation=0.35,
        upper_autocorrelation=0.75,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.08,
        calibration_confidence=0.99,
        covariance_confidence=0.98,
        autocorrelation_grid_size=7,
        white_noise_fraction_grid_size=5,
        upper_theta_grid_size=128,
        lower_theta_grid_size=128,
    )

    assert bound.requires_independent_target_record
    assert np.isclose(bound.combined_confidence_lower_bound, 0.99 * 0.98)
    assert (
        0.35
        <= bound.parameter_interval.autocorrelation_lower_bound
        <= bound.parameter_interval.autocorrelation_upper_bound
        <= 0.75
    )
    assert (
        0.0
        <= bound.parameter_interval.white_noise_fraction_lower_bound
        <= bound.parameter_interval.white_noise_fraction_upper_bound
        <= 0.08
    )
    assert bound.covariance_bound.covariance_relative_error > 0.0


def test_projected_covariance_is_invariant_to_declared_affine_nuisance_mean():
    calibration = _simulate_calibration(100, 80, 0.50, 0.02, seed=17)
    sample_count = 64
    design = _affine_design(sample_count)
    bound = gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound(
        calibration,
        3,
        1,
        design,
        lower_autocorrelation=0.30,
        upper_autocorrelation=0.70,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.08,
        calibration_confidence=0.99,
        covariance_confidence=0.98,
        autocorrelation_grid_size=7,
        white_noise_fraction_grid_size=5,
        upper_theta_grid_size=128,
        lower_theta_grid_size=128,
    )

    rng = np.random.default_rng(9)
    target = rng.standard_normal((sample_count, 3))
    nuisance_coefficients = np.array([[15.0, -4.0, 8.0], [30.0, 12.0, -20.0]])
    shifted = target + design @ nuisance_coefficients

    base_covariance = separable_gaussian_calibrated_ar1_white_noise_projected_covariance(
        target,
        design,
        bound,
    )
    shifted_covariance = (
        separable_gaussian_calibrated_ar1_white_noise_projected_covariance(
            shifted,
            design,
            bound,
        )
    )

    assert np.allclose(base_covariance, shifted_covariance, rtol=1e-11, atol=1e-11)
