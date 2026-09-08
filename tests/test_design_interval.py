import numpy as np
import pytest

from observer_math.design_interval import (
    gaussian_ar1_design_uniform_envelope,
    gaussian_calibrated_ar1_design_projected_covariance_bound,
    gaussian_estimated_ar1_design_projected_covariance_bound,
    separable_gaussian_estimated_ar1_design_projected_covariance,
)
from observer_math.estimated_nuisance import (
    gaussian_estimated_ar1_projected_covariance_bound,
)
from observer_math.nuisance import gaussian_ar1_projected_temporal_envelope
from observer_math.recovery import GaussianAR1AutocorrelationInterval


def _interval(sample_count, lower, upper, confidence=0.975):
    return GaussianAR1AutocorrelationInterval(
        sample_count=sample_count,
        channel_count=12,
        confidence=confidence,
        declared_upper_bound=max(upper, 0.9),
        estimate=0.5 * (lower + upper),
        error_radius=0.5 * (upper - lower),
        lower_bound=lower,
        upper_bound=upper,
        interval_intersects_declared_model=True,
    )


def _cosine_design(sample_count, rank):
    index = np.arange(sample_count, dtype=float)
    columns = [np.ones(sample_count)]
    for frequency in range(1, rank):
        columns.append(np.cos(np.pi * frequency * (index + 0.5) / sample_count))
    return np.column_stack(columns)


def _simulate_ar1_channels(sample_count, channel_count, phi, rng):
    innovations = rng.normal(size=(sample_count, channel_count))
    values = np.empty_like(innovations)
    values[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, sample_count):
        values[index] = phi * values[index - 1] + scale * innovations[index]
    return values


def _simulate_target(spatial, design, coefficients, phi, rng):
    innovations = rng.normal(size=(design.shape[0], spatial.shape[0]))
    innovations = innovations @ np.linalg.cholesky(spatial).T
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


def test_uniform_design_envelope_contains_dense_continuum_check():
    sample_count = 30
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t, np.sin(np.pi * t)))
    envelope = gaussian_ar1_design_uniform_envelope(
        design, 0.20, 0.75, grid_size=9
    )

    for phi in np.linspace(0.20, 0.75, 101):
        exact = gaussian_ar1_projected_temporal_envelope(
            sample_count, float(phi), design
        )
        assert (
            envelope.projected_degrees_of_freedom_lower_bound
            <= exact.projected_degrees_of_freedom
            <= envelope.projected_degrees_of_freedom_upper_bound
        )
        assert exact.projected_frobenius_norm <= envelope.projected_frobenius_norm_bound
        assert exact.projected_spectral_norm <= envelope.projected_spectral_norm_bound


def test_degenerate_interval_recovers_exact_design_geometry_up_to_roundoff():
    sample_count = 40
    design = _cosine_design(sample_count, 5)
    phi = 0.55
    exact = gaussian_ar1_projected_temporal_envelope(sample_count, phi, design)
    envelope = gaussian_ar1_design_uniform_envelope(
        design, phi, phi, grid_size=1
    )

    assert envelope.projected_degrees_of_freedom_lower_bound <= exact.projected_degrees_of_freedom
    assert envelope.projected_degrees_of_freedom_upper_bound >= exact.projected_degrees_of_freedom
    assert envelope.projected_frobenius_norm_bound >= exact.projected_frobenius_norm
    assert envelope.projected_spectral_norm_bound >= exact.projected_spectral_norm
    assert np.isclose(
        envelope.projected_degrees_of_freedom_lower_bound,
        exact.projected_degrees_of_freedom,
        rtol=1e-10,
        atol=1e-10,
    )


def test_design_specific_bound_tightens_rank_only_proposition_45():
    sample_count = 80
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    interval = _interval(500, 0.30, 0.60)

    rank_only = gaussian_estimated_ar1_projected_covariance_bound(
        4, 1, sample_count, design.shape[1], interval, covariance_confidence=0.975
    )
    design_specific = gaussian_estimated_ar1_design_projected_covariance_bound(
        4,
        1,
        design,
        interval,
        covariance_confidence=0.975,
        grid_size=33,
    )

    assert (
        design_specific.design_envelope.projected_degrees_of_freedom_lower_bound
        >= rank_only.projected_degrees_of_freedom_lower_bound
    )
    assert (
        design_specific.design_envelope.projected_frobenius_norm_bound
        <= rank_only.temporal_frobenius_norm_bound
    )
    assert (
        design_specific.design_envelope.projected_spectral_norm_bound
        <= rank_only.temporal_spectral_norm_bound
    )
    assert design_specific.covariance_relative_error <= rank_only.covariance_relative_error


def test_design_geometry_can_certify_when_rank_only_normalization_is_vacuous():
    sample_count = 60
    design = _cosine_design(sample_count, 9)
    interval = _interval(500, 0.65, 0.75)

    with pytest.raises(ValueError, match="no positive projected normalization"):
        gaussian_estimated_ar1_projected_covariance_bound(
            3,
            1,
            sample_count,
            design.shape[1],
            interval,
            covariance_confidence=0.975,
        )

    design_specific = gaussian_estimated_ar1_design_projected_covariance_bound(
        3,
        1,
        design,
        interval,
        covariance_confidence=0.975,
        grid_size=17,
    )
    assert design_specific.design_envelope.rank_only_degrees_of_freedom_lower_bound < 0.0
    assert design_specific.design_envelope.projected_degrees_of_freedom_lower_bound > 15.0
    assert np.isfinite(design_specific.covariance_relative_error)


def test_end_to_end_calibrated_design_bound_covers_affine_target():
    rng = np.random.default_rng(20261021)
    phi = 0.50
    calibration = _simulate_ar1_channels(500, 20, phi, rng)
    sample_count = 180
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    spatial = np.array(
        [
            [1.0, 0.22, -0.07],
            [0.22, 1.15, 0.13],
            [-0.07, 0.13, 0.92],
        ]
    )
    coefficients = np.array([[3.0, -2.0, 1.0], [8.0, -6.0, 5.0]])
    bound = gaussian_calibrated_ar1_design_projected_covariance_bound(
        3,
        1,
        design,
        calibration,
        declared_upper_bound=0.85,
        calibration_confidence=0.975,
        covariance_confidence=0.975,
        grid_size=17,
    )
    observations = _simulate_target(spatial, design, coefficients, phi, rng)
    estimate = separable_gaussian_estimated_ar1_design_projected_covariance(
        observations, design, bound
    )

    interval = bound.autocorrelation_interval
    assert interval.lower_bound <= phi <= interval.upper_bound
    assert _relative_error(spatial, estimate) <= bound.covariance_relative_error
    assert np.isclose(bound.combined_confidence, 0.95)
