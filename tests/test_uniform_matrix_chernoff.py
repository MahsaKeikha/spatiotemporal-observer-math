import numpy as np

from observer_math.design_interval import (
    gaussian_ar1_design_uniform_envelope,
)
from observer_math.matrix_chernoff import (
    gaussian_projected_weighted_wishart_matrix_bound,
)
from observer_math.uniform_matrix_chernoff import (
    gaussian_ar1_uniform_matrix_chernoff_bound,
    gaussian_calibrated_ar1_uniform_matrix_chernoff_bound,
    separable_gaussian_calibrated_ar1_uniform_matrix_covariance,
)


def _ar1_matrix(sample_count, phi):
    indices = np.arange(sample_count)
    return phi ** np.abs(indices[:, None] - indices[None, :])


def _simulate_ar1_channels(sample_count, channel_count, phi, rng):
    innovations = rng.normal(size=(sample_count, channel_count))
    values = np.empty_like(innovations)
    values[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, sample_count):
        values[index] = phi * values[index - 1] + scale * innovations[index]
    return values


def _simulate_target(spatial, design, coefficients, phi, rng):
    innovations = rng.normal(size=(design.shape[0], spatial.shape[0])) @ np.linalg.cholesky(
        spatial
    ).T
    residual = np.empty_like(innovations)
    residual[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, design.shape[0]):
        residual[index] = phi * residual[index - 1] + scale * innovations[index]
    return design @ coefficients + residual


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def _sphere_net_design_radius(dimension, block_count, design, lower, upper, confidence):
    envelope = gaussian_ar1_design_uniform_envelope(
        design,
        lower,
        upper,
        grid_size=33,
    )
    tail = np.log(2.0 * block_count * 9.0**dimension / (1.0 - confidence))
    oracle = 4.0 * (
        envelope.projected_frobenius_norm_bound * np.sqrt(tail)
        + envelope.projected_spectral_norm_bound * tail
    ) / envelope.projected_degrees_of_freedom_lower_bound
    d_lower = envelope.projected_degrees_of_freedom_lower_bound
    d_upper = envelope.projected_degrees_of_freedom_upper_bound
    d_star = 0.5 * (d_lower + d_upper)
    a = d_lower / d_star
    b = d_upper / d_star
    return float(
        max(
            abs(a - 1.0) + a * oracle,
            abs(b - 1.0) + b * oracle,
        )
    )


def test_degenerate_interval_recovers_known_phi_matrix_bound():
    sample_count = 90
    phi = 0.55
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    temporal = _ar1_matrix(sample_count, phi)

    exact = gaussian_projected_weighted_wishart_matrix_bound(
        4,
        2,
        temporal,
        design,
        confidence=0.975,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )
    uniform = gaussian_ar1_uniform_matrix_chernoff_bound(
        4,
        2,
        design,
        phi,
        phi,
        confidence=0.975,
        phi_grid_size=1,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    assert np.isclose(uniform.oracle_upper_deviation, exact.upper_deviation, rtol=1e-10, atol=1e-10)
    assert np.isclose(uniform.oracle_lower_deviation, exact.lower_deviation, rtol=1e-10, atol=1e-10)
    assert np.isclose(uniform.covariance_relative_error, exact.relative_covariance_error, rtol=1e-9, atol=1e-9)


def test_uniform_oracle_radius_contains_dense_exact_phi_bounds():
    sample_count = 80
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t, t**2))
    lower, upper = 0.35, 0.72
    uniform = gaussian_ar1_uniform_matrix_chernoff_bound(
        4,
        1,
        design,
        lower,
        upper,
        confidence=0.975,
        phi_grid_size=17,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )

    exact_radii = []
    for phi in np.linspace(lower, upper, 41):
        exact = gaussian_projected_weighted_wishart_matrix_bound(
            4,
            1,
            _ar1_matrix(sample_count, float(phi)),
            design,
            confidence=0.975,
            upper_theta_grid_size=512,
            lower_theta_grid_size=512,
        )
        exact_radii.append(exact.relative_covariance_error)

    assert max(exact_radii) <= uniform.oracle_relative_error + 1e-10


def test_end_to_end_calibrated_uniform_matrix_bound_covers_affine_target():
    rng = np.random.default_rng(20261021)
    phi = 0.45
    sample_count = 140
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    calibration = _simulate_ar1_channels(300, 24, phi, rng)
    spatial = np.array(
        [
            [1.0, 0.22, -0.08],
            [0.22, 1.15, 0.14],
            [-0.08, 0.14, 0.92],
        ]
    )
    coefficients = np.array([[2.0, -1.0, 0.5], [5.0, -4.0, 3.0]])

    bound = gaussian_calibrated_ar1_uniform_matrix_chernoff_bound(
        3,
        1,
        design,
        calibration,
        declared_upper_bound=0.8,
        calibration_confidence=0.975,
        covariance_confidence=0.975,
        phi_grid_size=17,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )
    observations = _simulate_target(spatial, design, coefficients, phi, rng)
    estimate = separable_gaussian_calibrated_ar1_uniform_matrix_covariance(
        observations,
        design,
        bound,
    )

    interval = bound.autocorrelation_interval
    assert interval.lower_bound <= phi <= interval.upper_bound
    assert _relative_error(spatial, estimate) <= bound.covariance_relative_error
    assert np.isclose(bound.combined_confidence, 0.95)


def test_uniform_matrix_bound_is_tighter_than_design_sphere_net_in_strong_correlation():
    sample_count = 120
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    lower, upper = 0.60, 0.72
    confidence = 0.975

    sphere = _sphere_net_design_radius(4, 1, design, lower, upper, confidence)
    matrix = gaussian_ar1_uniform_matrix_chernoff_bound(
        4,
        1,
        design,
        lower,
        upper,
        confidence=confidence,
        phi_grid_size=33,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    assert matrix.covariance_relative_error < sphere


def test_wider_ar1_interval_does_not_improve_uniform_matrix_certificate():
    sample_count = 90
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))

    narrow = gaussian_ar1_uniform_matrix_chernoff_bound(
        3,
        1,
        design,
        0.45,
        0.55,
        confidence=0.95,
        phi_grid_size=33,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )
    wide = gaussian_ar1_uniform_matrix_chernoff_bound(
        3,
        1,
        design,
        0.35,
        0.65,
        confidence=0.95,
        phi_grid_size=33,
        upper_theta_grid_size=512,
        lower_theta_grid_size=512,
    )

    assert wide.covariance_relative_error >= narrow.covariance_relative_error
