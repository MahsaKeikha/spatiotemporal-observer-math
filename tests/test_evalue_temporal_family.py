import numpy as np

from observer_math.calibrated_temporal_family import (
    gaussian_ar1_white_noise_increment_parameter_interval,
)
from observer_math.evalue_temporal_family import (
    gaussian_ar1_white_noise_evalue_grid,
    gaussian_ar1_white_noise_evalue_model,
    gaussian_ar1_white_noise_log_evalue,
    gaussian_helmert_contrast,
)


def _temporal_covariance(sample_count, phi, eta):
    indices = np.arange(sample_count)
    ar1 = phi ** np.abs(indices[:, None] - indices[None, :])
    return (1.0 - eta) * ar1 + eta * np.eye(sample_count)


def _simulate_calibration(sample_count, channel_count, phi, eta, seed):
    rng = np.random.default_rng(seed)
    temporal = _temporal_covariance(sample_count, phi, eta)
    values = np.linalg.cholesky(temporal) @ rng.normal(
        size=(sample_count, channel_count)
    )
    offsets = rng.normal(scale=4.0, size=channel_count)
    return values + offsets[None, :]


def test_helmert_contrast_is_orthonormal_and_removes_constant_mean():
    contrast = gaussian_helmert_contrast(12)

    assert contrast.shape == (11, 12)
    assert np.allclose(contrast @ contrast.T, np.eye(11), atol=1e-12)
    assert np.allclose(contrast @ np.ones(12), 0.0, atol=1e-12)


def test_evalue_model_is_exactly_invariant_to_channelwise_constant_offsets():
    values = _simulate_calibration(40, 24, 0.60, 0.04, seed=20261021)
    rng = np.random.default_rng(20261022)
    extra_offsets = rng.normal(scale=30.0, size=values.shape[1])

    base = gaussian_ar1_white_noise_evalue_model(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.80,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.25,
        contrast_dimension=10,
        mixture_autocorrelation_grid_size=7,
        mixture_white_noise_fraction_grid_size=5,
    )
    shifted = gaussian_ar1_white_noise_evalue_model(
        values + extra_offsets[None, :],
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.80,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.25,
        contrast_dimension=10,
        mixture_autocorrelation_grid_size=7,
        mixture_white_noise_fraction_grid_size=5,
    )

    assert np.allclose(base.residual_scatter, shifted.residual_scatter, atol=1e-10)
    assert np.isclose(
        base.log_mixture_density_kernel,
        shifted.log_mixture_density_kernel,
        atol=1e-10,
    )
    assert np.isclose(
        gaussian_ar1_white_noise_log_evalue(base, 0.61, 0.05),
        gaussian_ar1_white_noise_log_evalue(shifted, 0.61, 0.05),
        atol=1e-10,
    )


def test_scalar_density_ratio_has_unit_expectation_under_true_parameter():
    contrast = gaussian_helmert_contrast(2, contrast_dimension=1)
    phi_grid = np.array([0.35, 0.55, 0.75])
    eta_grid = np.array([0.0, 0.10])
    true_phi = 0.60
    true_eta = 0.04

    def variance(phi, eta):
        temporal = _temporal_covariance(2, phi, eta)
        return float((contrast @ temporal @ contrast.T)[0, 0])

    true_variance = variance(true_phi, true_eta)
    component_variances = np.array(
        [variance(phi, eta) for phi in phi_grid for eta in eta_grid]
    )
    points = np.linspace(-10.0, 10.0, 40001)
    true_density = np.exp(-0.5 * points**2 / true_variance) / np.sqrt(
        2.0 * np.pi * true_variance
    )
    mixture_density = np.mean(
        [
            np.exp(-0.5 * points**2 / component_variance)
            / np.sqrt(2.0 * np.pi * component_variance)
            for component_variance in component_variances
        ],
        axis=0,
    )
    evalue = mixture_density / true_density
    expectation = np.trapezoid(true_density * evalue, points)

    assert np.isclose(expectation, 1.0, atol=2e-6)


def test_seeded_true_parameter_belongs_to_pointwise_evalue_confidence_set():
    values = _simulate_calibration(60, 64, 0.60, 0.04, seed=20261023)
    model = gaussian_ar1_white_noise_evalue_model(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.80,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.25,
        contrast_dimension=12,
        mixture_autocorrelation_grid_size=7,
        mixture_white_noise_fraction_grid_size=5,
        confidence=0.9875,
    )

    assert gaussian_ar1_white_noise_log_evalue(model, 0.60, 0.04) < (
        model.log_evalue_threshold
    )


def test_evalue_grid_exposes_tighter_joint_geometry_than_lag_rectangle():
    values = _simulate_calibration(100, 128, 0.60, 0.04, seed=123)
    model = gaussian_ar1_white_noise_evalue_model(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.80,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.25,
        contrast_dimension=15,
        mixture_autocorrelation_grid_size=7,
        mixture_white_noise_fraction_grid_size=5,
        confidence=0.9875,
    )
    evaluation = gaussian_ar1_white_noise_evalue_grid(
        model,
        autocorrelation_grid_size=25,
        white_noise_fraction_grid_size=21,
    )
    rectangle = gaussian_ar1_white_noise_increment_parameter_interval(
        values,
        lower_autocorrelation=0.40,
        upper_autocorrelation=0.80,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.25,
        confidence=0.9875,
    )

    evalue_phi_width = (
        evaluation.accepted_autocorrelation_upper_bound
        - evaluation.accepted_autocorrelation_lower_bound
    )
    rectangle_phi_width = (
        rectangle.autocorrelation_upper_bound - rectangle.autocorrelation_lower_bound
    )
    evalue_eta_width = (
        evaluation.accepted_white_noise_fraction_upper_bound
        - evaluation.accepted_white_noise_fraction_lower_bound
    )
    rectangle_eta_width = (
        rectangle.white_noise_fraction_upper_bound
        - rectangle.white_noise_fraction_lower_bound
    )

    assert evaluation.accepted_point_count > 0
    assert evalue_phi_width < rectangle_phi_width
    assert evalue_eta_width < rectangle_eta_width
