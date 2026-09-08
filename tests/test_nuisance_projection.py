import numpy as np

from observer_math.nuisance import (
    gaussian_ar1_projected_temporal_envelope,
    gaussian_projected_relative_covariance_error_bound,
    separable_gaussian_projected_covariance,
    temporal_nuisance_projector,
)


def _simulate_ar1(spatial_covariance, design, coefficients, autocorrelation, rng):
    sample_count = design.shape[0]
    dimension = spatial_covariance.shape[0]
    innovations = rng.normal(size=(sample_count, dimension)) @ np.linalg.cholesky(
        spatial_covariance
    ).T
    residual = np.empty_like(innovations)
    residual[0] = innovations[0]
    scale = np.sqrt(1.0 - autocorrelation**2)
    for index in range(1, sample_count):
        residual[index] = (
            autocorrelation * residual[index - 1] + scale * innovations[index]
        )
    return design @ coefficients + residual


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def test_temporal_nuisance_projector_is_orthogonal_and_annihilates_design():
    t = np.linspace(-1.0, 1.0, 25)
    design = np.column_stack((np.ones_like(t), t, t**2))
    projector = temporal_nuisance_projector(design)

    assert np.allclose(projector, projector.T)
    assert np.allclose(projector @ projector, projector)
    assert np.allclose(projector @ design, 0.0, atol=1e-12)


def test_projected_covariance_is_invariant_to_any_declared_nuisance_mean():
    rng = np.random.default_rng(20261008)
    observations = rng.normal(size=(80, 4))
    t = np.linspace(-1.0, 1.0, observations.shape[0])
    design = np.column_stack((np.ones_like(t), t, np.sin(np.pi * t)))
    coefficients = rng.normal(size=(design.shape[1], observations.shape[1]))
    envelope = gaussian_ar1_projected_temporal_envelope(80, 0.0, design)

    base = separable_gaussian_projected_covariance(
        observations, design, envelope.projected_degrees_of_freedom
    )
    shifted = separable_gaussian_projected_covariance(
        observations + design @ coefficients,
        design,
        envelope.projected_degrees_of_freedom,
    )

    assert np.allclose(base, shifted, atol=1e-12)


def test_constant_design_recovers_the_centered_iid_normalization():
    sample_count = 100
    design = np.ones((sample_count, 1))
    envelope = gaussian_ar1_projected_temporal_envelope(sample_count, 0.0, design)

    assert np.isclose(envelope.projected_degrees_of_freedom, sample_count - 1)
    assert np.isclose(envelope.projected_frobenius_norm, np.sqrt(sample_count - 1))
    assert np.isclose(envelope.projected_spectral_norm, 1.0)
    assert np.isclose(envelope.variance_effective_sample_size, sample_count - 1)
    assert np.isclose(envelope.operator_effective_sample_size, sample_count - 1)


def test_projected_radius_covers_affine_mean_under_dependent_gaussian_sampling():
    sample_count = 900
    autocorrelation = 0.65
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    spatial = np.array(
        [
            [1.0, 0.25, -0.10, 0.05],
            [0.25, 1.3, 0.20, -0.08],
            [-0.10, 0.20, 0.9, 0.18],
            [0.05, -0.08, 0.18, 1.1],
        ]
    )
    coefficients = np.array(
        [[2.0, -1.0, 0.5, 3.0], [4.0, -2.0, 1.5, -3.0]]
    )
    envelope = gaussian_ar1_projected_temporal_envelope(
        sample_count, autocorrelation, design
    )
    observations = _simulate_ar1(
        spatial,
        design,
        coefficients,
        autocorrelation,
        np.random.default_rng(20261009),
    )
    estimate = separable_gaussian_projected_covariance(
        observations, design, envelope.projected_degrees_of_freedom
    )
    radius = gaussian_projected_relative_covariance_error_bound(
        spatial.shape[0], 1, envelope, confidence=0.975
    )

    assert _relative_error(spatial, estimate) <= radius


def test_linear_projection_removes_bias_that_constant_centering_leaves():
    sample_count = 600
    autocorrelation = 0.5
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    spatial = np.eye(3)
    coefficients = np.array([[0.0, 0.0, 0.0], [8.0, -6.0, 5.0]])
    rng = np.random.default_rng(20261010)
    observations = _simulate_ar1(
        spatial, design, coefficients, autocorrelation, rng
    )
    envelope = gaussian_ar1_projected_temporal_envelope(
        sample_count, autocorrelation, design
    )
    projected = separable_gaussian_projected_covariance(
        observations, design, envelope.projected_degrees_of_freedom
    )
    centered_values = observations - np.mean(observations, axis=0, keepdims=True)
    centered = centered_values.T @ centered_values / (sample_count - 1)

    assert _relative_error(spatial, projected) < 0.35
    assert _relative_error(spatial, centered) > 5.0
