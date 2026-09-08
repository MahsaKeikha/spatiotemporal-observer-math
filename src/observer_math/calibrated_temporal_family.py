"""Observable calibration for a two-parameter Gaussian temporal covariance family.

Proposition 50 estimates a confidence rectangle for the family

    R(phi, eta) = (1 - eta) R_phi + eta I

from independent standardized Gaussian calibration channels. Constant channel
means are allowed because the calibration statistics use lagged increments.
The resulting random parameter rectangle is then composed with Proposition 49
for an independent target record.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .compact_temporal_family import (
    GaussianAR1WhiteNoiseTemporalCover,
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    gaussian_ar1_white_noise_temporal_cover,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from .nuisance import temporal_nuisance_projector


@dataclass(frozen=True)
class GaussianIncrementCorrelationInterval:
    """Finite-sample interval for one lag correlation from increment energy."""

    lag: int
    sample_count: int
    channel_count: int
    pair_count_per_channel: int
    estimate: float
    error_radius: float
    lower_bound: float
    upper_bound: float
    declared_lower_bound: float
    declared_upper_bound: float
    increment_trace_bound: float
    increment_frobenius_norm_bound: float
    increment_spectral_norm_bound: float


@dataclass(frozen=True)
class GaussianAR1WhiteNoiseParameterInterval:
    """Simultaneous confidence rectangle for AR(1) correlation and white-noise mix."""

    sample_count: int
    channel_count: int
    confidence: float
    tail_parameter: float
    declared_autocorrelation_lower_bound: float
    declared_autocorrelation_upper_bound: float
    declared_white_noise_fraction_lower_bound: float
    declared_white_noise_fraction_upper_bound: float
    lag_one: GaussianIncrementCorrelationInterval
    lag_two: GaussianIncrementCorrelationInterval
    autocorrelation_lower_bound: float
    autocorrelation_upper_bound: float
    white_noise_fraction_lower_bound: float
    white_noise_fraction_upper_bound: float
    interval_intersects_declared_model: bool


@dataclass(frozen=True)
class GaussianCalibratedAR1WhiteNoiseMatrixChernoffBound:
    """End-to-end covariance certificate after two-parameter temporal calibration."""

    parameter_interval: GaussianAR1WhiteNoiseParameterInterval
    temporal_cover: GaussianAR1WhiteNoiseTemporalCover
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence_lower_bound: float
    requires_independent_target_record: bool


def _validated_parameter_box(
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float,
    upper_white_noise_fraction: float,
) -> tuple[float, float, float, float]:
    lower_phi = float(lower_autocorrelation)
    upper_phi = float(upper_autocorrelation)
    lower_eta = float(lower_white_noise_fraction)
    upper_eta = float(upper_white_noise_fraction)
    if not 0.0 < lower_phi <= upper_phi < 1.0:
        raise ValueError(
            "require 0 < lower_autocorrelation <= upper_autocorrelation < 1"
        )
    if not 0.0 <= lower_eta <= upper_eta < 1.0:
        raise ValueError(
            "require 0 <= lower_white_noise_fraction <= "
            "upper_white_noise_fraction < 1"
        )
    return lower_phi, upper_phi, lower_eta, upper_eta


def _declared_lag_correlation_bounds(
    lag: int,
    lower_phi: float,
    upper_phi: float,
    lower_eta: float,
    upper_eta: float,
) -> tuple[float, float]:
    lower = (1.0 - upper_eta) * lower_phi**lag
    upper = (1.0 - lower_eta) * upper_phi**lag
    return float(lower), float(upper)


def gaussian_ar1_white_noise_increment_norm_bounds(
    sample_count: int,
    lag: int,
    *,
    lower_autocorrelation: float,
    upper_white_noise_fraction: float,
) -> tuple[float, float, float]:
    """Return trace, Frobenius, and spectral bounds for lag-1 or lag-2 increments.

    The bounds exploit the increment filter directly. They do not upper-bound
    the increment covariance by the spectral norm of the original temporal
    covariance.
    """
    if isinstance(sample_count, bool) or not isinstance(
        sample_count, (int, np.integer)
    ):
        raise TypeError("sample_count must be an integer")
    if sample_count < 4:
        raise ValueError("sample_count must be at least four")
    if lag not in (1, 2):
        raise ValueError("lag must be one or two")

    lower_phi = float(lower_autocorrelation)
    upper_eta = float(upper_white_noise_fraction)
    if not 0.0 < lower_phi < 1.0:
        raise ValueError("lower_autocorrelation must lie in (0, 1)")
    if not 0.0 <= upper_eta < 1.0:
        raise ValueError("upper_white_noise_fraction must lie in [0, 1)")

    pair_count = sample_count - lag
    minimum_correlation = (1.0 - upper_eta) * lower_phi**lag
    trace_bound = 2.0 * pair_count * (1.0 - minimum_correlation)

    if lag == 1:
        ar1_increment_peak = (1.0 - lower_phi) / (1.0 + lower_phi)
    else:
        ar1_increment_peak = 1.0 - lower_phi**2
    spectral_bound = 4.0 * (
        (1.0 - upper_eta) * ar1_increment_peak + upper_eta
    )

    frobenius_bound = float(np.sqrt(trace_bound * spectral_bound))
    return float(trace_bound), frobenius_bound, float(spectral_bound)


def _increment_correlation_interval(
    values: np.ndarray,
    lag: int,
    *,
    lower_phi: float,
    upper_phi: float,
    lower_eta: float,
    upper_eta: float,
    tail_parameter: float,
) -> GaussianIncrementCorrelationInterval:
    sample_count, channel_count = values.shape
    pair_count = sample_count - lag
    differences = values[lag:] - values[:-lag]
    energy = float(np.sum(differences**2))
    estimate = float(1.0 - energy / (2.0 * channel_count * pair_count))

    trace_bound, frobenius_bound, spectral_bound = (
        gaussian_ar1_white_noise_increment_norm_bounds(
            sample_count,
            lag,
            lower_autocorrelation=lower_phi,
            upper_white_noise_fraction=upper_eta,
        )
    )
    error = float(
        frobenius_bound
        * np.sqrt(tail_parameter)
        / (np.sqrt(channel_count) * pair_count)
        + spectral_bound * tail_parameter / (channel_count * pair_count)
    )

    declared_lower, declared_upper = _declared_lag_correlation_bounds(
        lag,
        lower_phi,
        upper_phi,
        lower_eta,
        upper_eta,
    )
    lower = max(declared_lower, estimate - error)
    upper = min(declared_upper, estimate + error)

    return GaussianIncrementCorrelationInterval(
        lag=lag,
        sample_count=sample_count,
        channel_count=channel_count,
        pair_count_per_channel=pair_count,
        estimate=estimate,
        error_radius=error,
        lower_bound=float(lower),
        upper_bound=float(upper),
        declared_lower_bound=declared_lower,
        declared_upper_bound=declared_upper,
        increment_trace_bound=trace_bound,
        increment_frobenius_norm_bound=frobenius_bound,
        increment_spectral_norm_bound=spectral_bound,
    )


def gaussian_ar1_white_noise_increment_parameter_interval(
    standardized_observations: ArrayLike,
    *,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float = 0.0,
    upper_white_noise_fraction: float = 0.10,
    confidence: float = 0.9875,
) -> GaussianAR1WhiteNoiseParameterInterval:
    """Calibrate a simultaneous confidence rectangle for ``(phi, eta)``.

    Calibration channels must be independent standardized Gaussian channels
    sharing the same temporal covariance family. Each channel may have an
    arbitrary constant mean. The lagged increment statistics remove those
    means exactly.

    The lag correlations satisfy

        r1 = (1 - eta) phi
        r2 = (1 - eta) phi**2.

    Therefore ``phi = r2 / r1`` and ``eta = 1 - r1**2 / r2`` whenever the
    declared model has positive ``phi`` and ``eta < 1``.
    """
    lower_phi, upper_phi, lower_eta, upper_eta = _validated_parameter_box(
        lower_autocorrelation,
        upper_autocorrelation,
        lower_white_noise_fraction,
        upper_white_noise_fraction,
    )
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")

    values = np.asarray(standardized_observations, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or values.shape[0] < 4 or values.shape[1] < 1:
        raise ValueError(
            "standardized_observations must have shape (sample_count, channel_count) "
            "with sample_count at least four"
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("standardized_observations must be finite")

    tail = float(np.log(4.0 / (1.0 - confidence)))
    lag_one = _increment_correlation_interval(
        values,
        1,
        lower_phi=lower_phi,
        upper_phi=upper_phi,
        lower_eta=lower_eta,
        upper_eta=upper_eta,
        tail_parameter=tail,
    )
    lag_two = _increment_correlation_interval(
        values,
        2,
        lower_phi=lower_phi,
        upper_phi=upper_phi,
        lower_eta=lower_eta,
        upper_eta=upper_eta,
        tail_parameter=tail,
    )

    correlations_intersect = bool(
        lag_one.lower_bound <= lag_one.upper_bound
        and lag_two.lower_bound <= lag_two.upper_bound
        and lag_one.lower_bound > 0.0
        and lag_two.lower_bound > 0.0
    )

    if correlations_intersect:
        phi_lower = max(
            lower_phi,
            lag_two.lower_bound / lag_one.upper_bound,
        )
        phi_upper = min(
            upper_phi,
            lag_two.upper_bound / lag_one.lower_bound,
        )
        eta_lower = max(
            lower_eta,
            1.0 - lag_one.upper_bound**2 / lag_two.lower_bound,
        )
        eta_upper = min(
            upper_eta,
            1.0 - lag_one.lower_bound**2 / lag_two.upper_bound,
        )
        parameter_intersection = bool(
            phi_lower <= phi_upper and eta_lower <= eta_upper
        )
    else:
        phi_lower = np.nan
        phi_upper = np.nan
        eta_lower = np.nan
        eta_upper = np.nan
        parameter_intersection = False

    return GaussianAR1WhiteNoiseParameterInterval(
        sample_count=int(values.shape[0]),
        channel_count=int(values.shape[1]),
        confidence=float(confidence),
        tail_parameter=tail,
        declared_autocorrelation_lower_bound=lower_phi,
        declared_autocorrelation_upper_bound=upper_phi,
        declared_white_noise_fraction_lower_bound=lower_eta,
        declared_white_noise_fraction_upper_bound=upper_eta,
        lag_one=lag_one,
        lag_two=lag_two,
        autocorrelation_lower_bound=float(phi_lower),
        autocorrelation_upper_bound=float(phi_upper),
        white_noise_fraction_lower_bound=float(eta_lower),
        white_noise_fraction_upper_bound=float(eta_upper),
        interval_intersects_declared_model=parameter_intersection,
    )


def gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound(
    standardized_calibration_observations: ArrayLike,
    block_dimension: int,
    block_count: int,
    nuisance_design: ArrayLike,
    *,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    lower_white_noise_fraction: float = 0.0,
    upper_white_noise_fraction: float = 0.10,
    calibration_confidence: float = 0.9875,
    covariance_confidence: float = 0.9875,
    autocorrelation_grid_size: int = 17,
    white_noise_fraction_grid_size: int = 9,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianCalibratedAR1WhiteNoiseMatrixChernoffBound:
    """Compose two-parameter calibration with Proposition 49.

    The calibration observations and the eventual target covariance record must
    be independent. They share the same temporal parameters, but the target may
    have an arbitrary mean inside the supplied nuisance design.
    """
    interval = gaussian_ar1_white_noise_increment_parameter_interval(
        standardized_calibration_observations,
        lower_autocorrelation=lower_autocorrelation,
        upper_autocorrelation=upper_autocorrelation,
        lower_white_noise_fraction=lower_white_noise_fraction,
        upper_white_noise_fraction=upper_white_noise_fraction,
        confidence=calibration_confidence,
    )
    if not interval.interval_intersects_declared_model:
        raise ValueError(
            "the calibration intervals do not intersect the declared temporal model"
        )
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    phi_grid_size = (
        1
        if interval.autocorrelation_lower_bound
        == interval.autocorrelation_upper_bound
        else autocorrelation_grid_size
    )
    eta_grid_size = (
        1
        if interval.white_noise_fraction_lower_bound
        == interval.white_noise_fraction_upper_bound
        else white_noise_fraction_grid_size
    )
    cover = gaussian_ar1_white_noise_temporal_cover(
        nuisance_design,
        interval.autocorrelation_lower_bound,
        interval.autocorrelation_upper_bound,
        interval.white_noise_fraction_lower_bound,
        interval.white_noise_fraction_upper_bound,
        autocorrelation_grid_size=phi_grid_size,
        white_noise_fraction_grid_size=eta_grid_size,
    )
    covariance = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension,
        block_count,
        cover.temporal_covariance_grid,
        nuisance_design,
        eigenvalue_covering_radius=cover.projected_eigenvalue_covering_radius,
        normalization_covering_radius=cover.projected_normalization_covering_radius,
        confidence=covariance_confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )

    combined = float(calibration_confidence * covariance_confidence)
    return GaussianCalibratedAR1WhiteNoiseMatrixChernoffBound(
        parameter_interval=interval,
        temporal_cover=cover,
        covariance_bound=covariance,
        calibration_confidence=float(calibration_confidence),
        covariance_confidence=float(covariance_confidence),
        combined_confidence_lower_bound=combined,
        requires_independent_target_record=True,
    )


def separable_gaussian_calibrated_ar1_white_noise_projected_covariance(
    target_observations: ArrayLike,
    nuisance_design: ArrayLike,
    bound: GaussianCalibratedAR1WhiteNoiseMatrixChernoffBound,
) -> np.ndarray:
    """Estimate spatial covariance using Proposition 50's reference normalization."""
    values = np.asarray(target_observations, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or not np.all(np.isfinite(values)):
        raise ValueError("target_observations must be a finite one- or two-dimensional array")

    projector = temporal_nuisance_projector(nuisance_design)
    if projector.shape[0] != values.shape[0]:
        raise ValueError("nuisance_design and target_observations must share sample_count")
    degrees = bound.covariance_bound.reference_projected_degrees_of_freedom
    return (values.T @ projector @ values) / degrees
