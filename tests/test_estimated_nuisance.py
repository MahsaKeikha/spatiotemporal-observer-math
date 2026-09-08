import numpy as np

from observer_math.estimated_nuisance import (
    gaussian_calibrated_ar1_projected_covariance_bound,
    gaussian_estimated_ar1_projected_covariance_bound,
    separable_gaussian_estimated_ar1_projected_covariance,
)
from observer_math.recovery import (
    gaussian_ar1_increment_autocorrelation_interval,
    gaussian_estimated_ar1_centered_covariance_bound,
)


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


def test_rank_one_projection_reproduces_proposition_43_bound():
    calibration = _simulate_ar1_channels(
        700, 16, 0.45, np.random.default_rng(20261012)
    )
    interval = gaussian_ar1_increment_autocorrelation_interval(
        calibration, declared_upper_bound=0.85, confidence=0.9875
    )
    centered = gaussian_estimated_ar1_centered_covariance_bound(
        4, 3, 800, interval, covariance_confidence=0.9875
    )
    projected = gaussian_estimated_ar1_projected_covariance_bound(
        4, 3, 800, 1, interval, covariance_confidence=0.9875
    )

    assert np.isclose(
        projected.projected_degrees_of_freedom_lower_bound,
        centered.centering_degrees_of_freedom_lower_bound,
    )
    assert np.isclose(
        projected.reference_projected_degrees_of_freedom,
        centered.reference_centering_degrees_of_freedom,
    )
    assert np.isclose(
        projected.oracle_normalized_covariance_error,
        centered.oracle_normalized_covariance_error,
    )
    assert np.isclose(projected.covariance_relative_error, centered.covariance_relative_error)


def test_estimated_ar1_projected_estimator_is_invariant_to_declared_nuisance_mean():
    rng = np.random.default_rng(20261013)
    sample_count = 300
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t, t**2))
    calibration = _simulate_ar1_channels(sample_count, 10, 0.3, rng)
    bound = gaussian_calibrated_ar1_projected_covariance_bound(
        3,
        1,
        sample_count,
        design.shape[1],
        calibration,
        declared_upper_bound=0.8,
        calibration_confidence=0.975,
        covariance_confidence=0.975,
    )
    observations = rng.normal(size=(sample_count, 3))
    extra = rng.normal(size=(design.shape[1], observations.shape[1]))

    base = separable_gaussian_estimated_ar1_projected_covariance(
        observations, design, bound
    )
    shifted = separable_gaussian_estimated_ar1_projected_covariance(
        observations + design @ extra, design, bound
    )

    assert np.allclose(base, shifted, atol=1e-12)


def test_end_to_end_projected_bound_covers_affine_target_with_estimated_ar1():
    rng = np.random.default_rng(20261014)
    phi = 0.45
    calibration = _simulate_ar1_channels(700, 20, phi, rng)
    sample_count = 850
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    spatial = np.array(
        [
            [1.0, 0.25, -0.08, 0.05],
            [0.25, 1.2, 0.16, -0.06],
            [-0.08, 0.16, 0.9, 0.14],
            [0.05, -0.06, 0.14, 1.05],
        ]
    )
    coefficients = np.array([[2.0, -1.0, 0.5, 2.5], [7.0, -5.0, 4.0, -6.0]])
    bound = gaussian_calibrated_ar1_projected_covariance_bound(
        spatial.shape[0],
        1,
        sample_count,
        design.shape[1],
        calibration,
        declared_upper_bound=0.85,
        calibration_confidence=0.975,
        covariance_confidence=0.975,
    )
    observations = _simulate_target(spatial, design, coefficients, phi, rng)
    estimate = separable_gaussian_estimated_ar1_projected_covariance(
        observations, design, bound
    )

    assert bound.autocorrelation_interval.lower_bound <= phi <= bound.autocorrelation_interval.upper_bound
    assert _relative_error(spatial, estimate) <= bound.covariance_relative_error
    assert np.isclose(bound.combined_confidence, 0.95)


def test_projected_bound_weakens_monotonically_with_nuisance_rank():
    calibration = _simulate_ar1_channels(
        600, 12, 0.4, np.random.default_rng(20261015)
    )
    interval = gaussian_ar1_increment_autocorrelation_interval(
        calibration, declared_upper_bound=0.85, confidence=0.975
    )
    errors = [
        gaussian_estimated_ar1_projected_covariance_bound(
            4, 2, 800, rank, interval, covariance_confidence=0.975
        ).covariance_relative_error
        for rank in (1, 2, 4, 8)
    ]

    assert np.all(np.diff(errors) > 0.0)


def test_calibration_upper_bound_controls_temporal_envelope_not_target_trend_size():
    rng = np.random.default_rng(20261016)
    calibration = _simulate_ar1_channels(500, 14, 0.35, rng)
    bound = gaussian_calibrated_ar1_projected_covariance_bound(
        3,
        1,
        600,
        2,
        calibration,
        declared_upper_bound=0.8,
        calibration_confidence=0.975,
        covariance_confidence=0.975,
    )
    t = np.linspace(-1.0, 1.0, 600)
    design = np.column_stack((np.ones_like(t), t))
    base = rng.normal(size=(600, 3))
    small = separable_gaussian_estimated_ar1_projected_covariance(
        base + design @ np.array([[0.0, 0.0, 0.0], [1.0, -1.0, 0.5]]),
        design,
        bound,
    )
    huge = separable_gaussian_estimated_ar1_projected_covariance(
        base + design @ np.array([[100.0, -50.0, 25.0], [1000.0, -800.0, 500.0]]),
        design,
        bound,
    )

    assert np.allclose(small, huge, atol=1e-10)
