"""Design-specific AR(1) interval envelopes for nuisance-projected covariance.

Proposition 46 tightens Proposition 45 by using the actual declared temporal
nuisance design H, rather than only its rank. A finite grid over a calibrated
nonnegative AR(1) interval is made rigorous between grid points by analytic
Lipschitz bounds for the AR(1) Toeplitz matrix and its nuisance projection.
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
class GaussianAR1DesignUniformEnvelope:
    """Uniform projected temporal envelope over an AR(1) coefficient interval."""

    sample_count: int
    nuisance_rank: int
    lower_autocorrelation: float
    upper_autocorrelation: float
    grid_size: int
    maximum_grid_spacing: float
    projected_degrees_of_freedom_lower_bound: float
    projected_degrees_of_freedom_upper_bound: float
    projected_frobenius_norm_bound: float
    projected_spectral_norm_bound: float
    frobenius_lipschitz_bound: float
    spectral_lipschitz_bound: float
    rank_only_degrees_of_freedom_lower_bound: float
    global_frobenius_norm_bound: float
    global_spectral_norm_bound: float


@dataclass(frozen=True)
class GaussianEstimatedAR1DesignProjectedCovarianceBound:
    """Projected covariance bound using the actual nuisance-design geometry."""

    autocorrelation_interval: GaussianAR1AutocorrelationInterval
    design_envelope: GaussianAR1DesignUniformEnvelope
    covariance_confidence: float
    combined_confidence: float
    reference_projected_degrees_of_freedom: float
    oracle_normalized_covariance_error: float
    normalization_error: float
    covariance_relative_error: float
    variance_effective_sample_size_lower_bound: float
    operator_effective_sample_size_lower_bound: float


def _validated_design(nuisance_design: ArrayLike) -> np.ndarray:
    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] < 2 or design.shape[1] < 1:
        raise ValueError("nuisance_design must have shape (sample_count >= 2, rank >= 1)")
    if not np.all(np.isfinite(design)):
        raise ValueError("nuisance_design must be finite")
    rank = int(np.linalg.matrix_rank(design))
    if rank != design.shape[1]:
        raise ValueError("nuisance_design columns must be linearly independent")
    if rank >= design.shape[0]:
        raise ValueError("nuisance rank must be smaller than sample_count")
    return design


def _ar1_matrix(sample_count: int, autocorrelation: float) -> np.ndarray:
    indices = np.arange(sample_count)
    return autocorrelation ** np.abs(indices[:, None] - indices[None, :])


def _ar1_derivative_norm_bounds(sample_count: int, upper_autocorrelation: float) -> tuple[float, float]:
    """Return safe uniform Frobenius and spectral derivative bounds on [0, rho]."""
    rho = float(upper_autocorrelation)
    lags = np.arange(1, sample_count, dtype=float)
    if rho == 0.0:
        powers = np.zeros_like(lags)
        powers[0] = 1.0
    else:
        powers = rho ** (lags - 1.0)
    frobenius_squared = 2.0 * np.sum(
        (sample_count - lags) * lags**2 * powers**2
    )
    # Every row sum of |R'_phi| is bounded by the two-sided lag sum.
    spectral = 2.0 * np.sum(lags * powers)
    return float(np.sqrt(frobenius_squared)), float(spectral)


def gaussian_ar1_design_uniform_envelope(
    nuisance_design: ArrayLike,
    lower_autocorrelation: float,
    upper_autocorrelation: float,
    *,
    grid_size: int = 33,
) -> GaussianAR1DesignUniformEnvelope:
    """Certify projected AR(1) norms uniformly over a coefficient interval.

    The grid itself is not treated as proof of a continuum statement. If the
    largest grid spacing is ``h``, every coefficient in the interval is within
    ``h/2`` of a grid point. Analytic derivative bounds then inflate the grid
    extrema by a Lipschitz remainder.

    For ``Q`` spanning the nuisance space and ``P=I-QQ^T``, the normalization
    is ``d(phi)=tr(P R_phi)=N-tr(QQ^T R_phi)``. Therefore

    ``|d'(phi)| <= q ||R'_phi||_2``.

    Projection is contractive in Frobenius and spectral norm, so the same
    derivative envelopes control ``||P R_phi P||_F`` and ``||P R_phi P||_2``.
    The returned result also intersects these design-specific bounds with the
    rank-only/global bounds from Proposition 45, so it cannot lose those safe
    fallbacks merely because the grid is coarse.
    """
    design = _validated_design(nuisance_design)
    if isinstance(grid_size, bool) or not isinstance(grid_size, (int, np.integer)):
        raise TypeError("grid_size must be an integer")
    lower = float(lower_autocorrelation)
    upper = float(upper_autocorrelation)
    if not np.isfinite(lower) or not np.isfinite(upper):
        raise ValueError("autocorrelation interval must be finite")
    if not 0.0 <= lower <= upper < 1.0:
        raise ValueError("require 0 <= lower_autocorrelation <= upper_autocorrelation < 1")
    if lower < upper and grid_size < 2:
        raise ValueError("grid_size must be at least two for a nondegenerate interval")
    if lower == upper and grid_size < 1:
        raise ValueError("grid_size must be positive")

    sample_count, nuisance_rank = design.shape
    basis, _ = np.linalg.qr(design, mode="reduced")
    projector = np.eye(sample_count) - basis @ basis.T
    projector = 0.5 * (projector + projector.T)

    if lower == upper:
        grid = np.array([lower])
        spacing = 0.0
    else:
        grid = np.linspace(lower, upper, int(grid_size))
        spacing = float((upper - lower) / (grid.size - 1))

    degrees = []
    frobenius = []
    spectral = []
    for phi in grid:
        temporal = _ar1_matrix(sample_count, float(phi))
        projected = projector @ temporal @ projector
        projected = 0.5 * (projected + projected.T)
        degrees.append(float(np.trace(projected)))
        frobenius.append(float(np.linalg.norm(projected, ord="fro")))
        spectral.append(float(max(0.0, np.linalg.eigvalsh(projected)[-1])))

    frobenius_lipschitz, spectral_lipschitz = _ar1_derivative_norm_bounds(
        sample_count, upper
    )
    covering_radius = 0.5 * spacing
    design_degrees_lower = min(degrees) - nuisance_rank * spectral_lipschitz * covering_radius
    design_degrees_upper = max(degrees) + nuisance_rank * spectral_lipschitz * covering_radius
    design_frobenius_upper = max(frobenius) + frobenius_lipschitz * covering_radius
    design_spectral_upper = max(spectral) + spectral_lipschitz * covering_radius

    global_envelope = gaussian_ar1_temporal_correlation_envelope(sample_count, upper)
    rank_only_degrees_lower = float(
        sample_count - nuisance_rank * global_envelope.spectral_norm_bound
    )

    # Small outward inflation protects against ordinary floating-point extrema
    # being rounded inward. It is negligible relative to the analytic remainder.
    scale = max(1.0, float(sample_count), max(frobenius))
    roundoff = 128.0 * np.finfo(float).eps * sample_count * scale

    degrees_lower = max(
        rank_only_degrees_lower,
        design_degrees_lower - roundoff,
    )
    degrees_upper = min(
        float(sample_count),
        design_degrees_upper + roundoff,
    )
    frobenius_upper = min(
        float(global_envelope.frobenius_norm_bound),
        design_frobenius_upper + roundoff,
    )
    spectral_upper = min(
        float(global_envelope.spectral_norm_bound),
        design_spectral_upper + roundoff,
    )

    if not degrees_lower > 0.0:
        raise ValueError(
            "the interval envelope leaves no positive projected normalization; "
            "increase sample_count, reduce nuisance rank, tighten the AR(1) interval, "
            "or use a more informative declared design"
        )
    if degrees_upper < degrees_lower:
        raise RuntimeError("internal projected normalization bounds are inconsistent")

    return GaussianAR1DesignUniformEnvelope(
        sample_count=int(sample_count),
        nuisance_rank=int(nuisance_rank),
        lower_autocorrelation=lower,
        upper_autocorrelation=upper,
        grid_size=int(grid.size),
        maximum_grid_spacing=spacing,
        projected_degrees_of_freedom_lower_bound=float(degrees_lower),
        projected_degrees_of_freedom_upper_bound=float(degrees_upper),
        projected_frobenius_norm_bound=float(frobenius_upper),
        projected_spectral_norm_bound=float(spectral_upper),
        frobenius_lipschitz_bound=frobenius_lipschitz,
        spectral_lipschitz_bound=spectral_lipschitz,
        rank_only_degrees_of_freedom_lower_bound=rank_only_degrees_lower,
        global_frobenius_norm_bound=float(global_envelope.frobenius_norm_bound),
        global_spectral_norm_bound=float(global_envelope.spectral_norm_bound),
    )


def gaussian_estimated_ar1_design_projected_covariance_bound(
    block_dimension: int,
    block_count: int,
    nuisance_design: ArrayLike,
    autocorrelation_interval: GaussianAR1AutocorrelationInterval,
    *,
    covariance_confidence: float = 0.9875,
    grid_size: int = 33,
) -> GaussianEstimatedAR1DesignProjectedCovarianceBound:
    """Compose a calibrated AR(1) interval with the actual nuisance geometry."""
    if isinstance(block_dimension, bool) or not isinstance(block_dimension, (int, np.integer)):
        raise TypeError("block_dimension must be an integer")
    if isinstance(block_count, bool) or not isinstance(block_count, (int, np.integer)):
        raise TypeError("block_count must be an integer")
    if block_dimension < 1 or block_count < 1:
        raise ValueError("block_dimension and block_count must be positive")
    if not isinstance(autocorrelation_interval, GaussianAR1AutocorrelationInterval):
        raise TypeError("autocorrelation_interval has the wrong type")
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    envelope = gaussian_ar1_design_uniform_envelope(
        nuisance_design,
        autocorrelation_interval.lower_bound,
        autocorrelation_interval.upper_bound,
        grid_size=grid_size,
    )
    combined_confidence = (
        float(autocorrelation_interval.confidence) + float(covariance_confidence) - 1.0
    )
    if not combined_confidence > 0.0:
        raise ValueError("the union-bound combined confidence must be positive")

    degrees_lower = envelope.projected_degrees_of_freedom_lower_bound
    degrees_upper = envelope.projected_degrees_of_freedom_upper_bound
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
            envelope.projected_frobenius_norm_bound * np.sqrt(tail)
            + envelope.projected_spectral_norm_bound * tail
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

    return GaussianEstimatedAR1DesignProjectedCovarianceBound(
        autocorrelation_interval=autocorrelation_interval,
        design_envelope=envelope,
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(combined_confidence),
        reference_projected_degrees_of_freedom=float(reference_degrees),
        oracle_normalized_covariance_error=oracle_error,
        normalization_error=normalization_error,
        covariance_relative_error=covariance_error,
        variance_effective_sample_size_lower_bound=float(
            degrees_lower**2 / envelope.projected_frobenius_norm_bound**2
        ),
        operator_effective_sample_size_lower_bound=float(
            degrees_lower / envelope.projected_spectral_norm_bound
        ),
    )


def gaussian_calibrated_ar1_design_projected_covariance_bound(
    block_dimension: int,
    block_count: int,
    nuisance_design: ArrayLike,
    standardized_calibration_observations: ArrayLike,
    *,
    declared_upper_bound: float,
    calibration_confidence: float = 0.9875,
    covariance_confidence: float = 0.9875,
    grid_size: int = 33,
) -> GaussianEstimatedAR1DesignProjectedCovarianceBound:
    """End-to-end observable Proposition 46 calibration."""
    interval = gaussian_ar1_increment_autocorrelation_interval(
        standardized_calibration_observations,
        declared_upper_bound=declared_upper_bound,
        confidence=calibration_confidence,
    )
    return gaussian_estimated_ar1_design_projected_covariance_bound(
        block_dimension,
        block_count,
        nuisance_design,
        interval,
        covariance_confidence=covariance_confidence,
        grid_size=grid_size,
    )


def separable_gaussian_estimated_ar1_design_projected_covariance(
    observations: ArrayLike,
    nuisance_design: ArrayLike,
    bound: GaussianEstimatedAR1DesignProjectedCovarianceBound,
) -> np.ndarray:
    """Return the observable covariance estimator certified by Proposition 46."""
    if not isinstance(bound, GaussianEstimatedAR1DesignProjectedCovarianceBound):
        raise TypeError("bound has the wrong type")
    values = np.asarray(observations, dtype=float)
    design = _validated_design(nuisance_design)
    if values.ndim != 2 or values.shape[0] != design.shape[0]:
        raise ValueError("observations and nuisance_design must share the sample axis")
    envelope = bound.design_envelope
    if values.shape[0] != envelope.sample_count or design.shape[1] != envelope.nuisance_rank:
        raise ValueError("observations or nuisance_design do not match the bound dimensions")
    return separable_gaussian_projected_covariance(
        values,
        design,
        bound.reference_projected_degrees_of_freedom,
    )
