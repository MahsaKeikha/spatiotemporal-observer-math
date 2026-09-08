"""Estimated AR(1) calibration for nuisance-projected Gaussian covariance.

Proposition 45 composes the increment-energy AR(1) confidence interval from
Proposition 43 with the fixed temporal nuisance projection from Proposition 44.
The target record may therefore have an arbitrary unknown mean inside a fixed,
predeclared temporal design while the temporal dependence is calibrated from
standardized Gaussian channels sharing the same nonnegative AR(1) coefficient.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .nuisance import separable_gaussian_projected_covariance
from .recovery import (
    GaussianAR1AutocorrelationInterval,
    gaussian_ar1_increment_autocorrelation_interval,
    gaussian_ar1_temporal_correlation_envelope,
)


@dataclass(frozen=True)
class GaussianEstimatedAR1ProjectedCovarianceBound:
    """Finite-sample projected covariance bound with estimated AR(1) dependence."""

    autocorrelation_interval: GaussianAR1AutocorrelationInterval
    covariance_confidence: float
    combined_confidence: float
    covariance_sample_count: int
    nuisance_rank: int
    projected_degrees_of_freedom_lower_bound: float
    projected_degrees_of_freedom_upper_bound: float
    reference_projected_degrees_of_freedom: float
    temporal_frobenius_norm_bound: float
    temporal_spectral_norm_bound: float
    oracle_normalized_covariance_error: float
    normalization_error: float
    covariance_relative_error: float
    variance_effective_sample_size_lower_bound: float
    operator_effective_sample_size_lower_bound: float


def gaussian_estimated_ar1_projected_covariance_bound(
    block_dimension: int,
    block_count: int,
    covariance_sample_count: int,
    nuisance_rank: int,
    autocorrelation_interval: GaussianAR1AutocorrelationInterval,
    *,
    covariance_confidence: float = 0.9875,
) -> GaussianEstimatedAR1ProjectedCovarianceBound:
    """Compose an AR(1) confidence interval with a rank-q nuisance projection.

    On the event that the true nonnegative AR(1) coefficient is no larger than
    ``autocorrelation_interval.upper_bound``, the AR(1) temporal correlation
    matrix ``R`` obeys the Proposition 43 Frobenius and spectral envelopes.
    For an orthogonal nuisance projector ``P`` of rank ``N-q``,

    ``tr(P R) >= N - q ||R||_2`` and ``tr(P R) <= N``.

    Moreover ``||P R P||_F <= ||R||_F`` and
    ``||P R P||_2 <= ||R||_2``. These deterministic inequalities turn the
    unknown projected normalization into a finite interval. The practical
    estimator divides the projected sum of squares by the midpoint of that
    interval, and the returned relative error includes both Gaussian
    concentration and normalization uncertainty.
    """
    integer_values = (block_dimension, block_count, covariance_sample_count, nuisance_rank)
    if any(
        isinstance(value, bool) or not isinstance(value, (int, np.integer))
        for value in integer_values
    ):
        raise TypeError(
            "block_dimension, block_count, covariance_sample_count, and nuisance_rank "
            "must be integers"
        )
    if block_dimension < 1 or block_count < 1:
        raise ValueError("block_dimension and block_count must be positive")
    if covariance_sample_count < 2:
        raise ValueError("covariance_sample_count must be at least two")
    if not 1 <= nuisance_rank < covariance_sample_count:
        raise ValueError("require 1 <= nuisance_rank < covariance_sample_count")
    if not isinstance(autocorrelation_interval, GaussianAR1AutocorrelationInterval):
        raise TypeError("autocorrelation_interval has the wrong type")
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    combined_confidence = (
        autocorrelation_interval.confidence + float(covariance_confidence) - 1.0
    )
    if not combined_confidence > 0.0:
        raise ValueError("the union-bound combined confidence must be positive")

    temporal = gaussian_ar1_temporal_correlation_envelope(
        covariance_sample_count, autocorrelation_interval.upper_bound
    )
    degrees_lower = float(
        covariance_sample_count - nuisance_rank * temporal.spectral_norm_bound
    )
    degrees_upper = float(covariance_sample_count)
    if not degrees_lower > 0.0:
        raise ValueError(
            "the estimated temporal envelope and nuisance rank leave no positive "
            "projected normalization"
        )
    reference_degrees = 0.5 * (degrees_lower + degrees_upper)

    tail = float(
        np.log(
            2.0
            * block_count
            * 9.0**block_dimension
            / (1.0 - float(covariance_confidence))
        )
    )
    oracle_error = float(
        4.0
        * (
            temporal.frobenius_norm_bound * np.sqrt(tail)
            + temporal.spectral_norm_bound * tail
        )
        / degrees_lower
    )

    quotient_lower = degrees_lower / reference_degrees
    quotient_upper = degrees_upper / reference_degrees
    normalization_error = float(
        max(abs(quotient_lower - 1.0), abs(quotient_upper - 1.0))
    )
    covariance_error = float(
        max(
            abs(quotient_lower - 1.0) + quotient_lower * oracle_error,
            abs(quotient_upper - 1.0) + quotient_upper * oracle_error,
        )
    )

    return GaussianEstimatedAR1ProjectedCovarianceBound(
        autocorrelation_interval=autocorrelation_interval,
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(combined_confidence),
        covariance_sample_count=int(covariance_sample_count),
        nuisance_rank=int(nuisance_rank),
        projected_degrees_of_freedom_lower_bound=degrees_lower,
        projected_degrees_of_freedom_upper_bound=degrees_upper,
        reference_projected_degrees_of_freedom=float(reference_degrees),
        temporal_frobenius_norm_bound=float(temporal.frobenius_norm_bound),
        temporal_spectral_norm_bound=float(temporal.spectral_norm_bound),
        oracle_normalized_covariance_error=oracle_error,
        normalization_error=normalization_error,
        covariance_relative_error=covariance_error,
        variance_effective_sample_size_lower_bound=float(
            degrees_lower**2 / temporal.frobenius_norm_bound**2
        ),
        operator_effective_sample_size_lower_bound=float(
            degrees_lower / temporal.spectral_norm_bound
        ),
    )


def gaussian_calibrated_ar1_projected_covariance_bound(
    block_dimension: int,
    block_count: int,
    covariance_sample_count: int,
    nuisance_rank: int,
    standardized_calibration_observations: ArrayLike,
    *,
    declared_upper_bound: float,
    calibration_confidence: float = 0.9875,
    covariance_confidence: float = 0.9875,
) -> GaussianEstimatedAR1ProjectedCovarianceBound:
    """End-to-end Proposition 45 bound from observable calibration channels.

    Calibration channels must satisfy Proposition 43's assumptions: each is a
    standardized stationary Gaussian AR(1) channel with unit marginal variance,
    a constant unknown mean, and the channels share one nonnegative AR(1)
    coefficient. The target covariance record may instead have any mean in its
    fixed declared nuisance subspace.
    """
    interval = gaussian_ar1_increment_autocorrelation_interval(
        standardized_calibration_observations,
        declared_upper_bound=declared_upper_bound,
        confidence=calibration_confidence,
    )
    return gaussian_estimated_ar1_projected_covariance_bound(
        block_dimension,
        block_count,
        covariance_sample_count,
        nuisance_rank,
        interval,
        covariance_confidence=covariance_confidence,
    )


def separable_gaussian_estimated_ar1_projected_covariance(
    observations: ArrayLike,
    nuisance_design: ArrayLike,
    bound: GaussianEstimatedAR1ProjectedCovarianceBound,
) -> np.ndarray:
    """Return the observable covariance estimator certified by Proposition 45."""
    if not isinstance(bound, GaussianEstimatedAR1ProjectedCovarianceBound):
        raise TypeError("bound has the wrong type")
    values = np.asarray(observations, dtype=float)
    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if values.ndim != 2 or design.ndim != 2:
        raise ValueError("observations and nuisance_design must be matrices")
    if values.shape[0] != bound.covariance_sample_count:
        raise ValueError("observations do not match bound.covariance_sample_count")
    if design.shape[0] != values.shape[0] or design.shape[1] != bound.nuisance_rank:
        raise ValueError("nuisance_design does not match the bound dimensions")
    return separable_gaussian_projected_covariance(
        values,
        design,
        bound.reference_projected_degrees_of_freedom,
    )
