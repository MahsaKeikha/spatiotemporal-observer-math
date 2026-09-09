"""Innovation-whitened target covariance certification.

Proposition 56 changes the target estimator rather than tightening temporal
calibration. If a positive-definite temporal law is known, whiten the target
record first, transform the nuisance design by the same whitener, and only then
project the nuisance subspace. Under the separable Gaussian model this restores
an ordinary Wishart covariance with exactly N-q residual degrees of freedom.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from scipy.stats import chi2

from .matrix_chernoff import (
    GaussianWeightedWishartMatrixBound,
    gaussian_weighted_wishart_matrix_bound,
)
from .physical_relaxation import exponential_relaxation_markov_factorization


@dataclass(frozen=True)
class GaussianWhitenedProjectedCovarianceBound:
    """Matrix concentration after exact temporal whitening and nuisance removal."""

    sample_count: int
    nuisance_rank: int
    residual_degrees_of_freedom: int
    block_dimension: int
    block_count: int
    confidence: float
    covariance_bound: GaussianWeightedWishartMatrixBound


@dataclass(frozen=True)
class GaussianWhitenedScalarChiSquareBound:
    """Exact simultaneous scalar covariance interval after temporal whitening."""

    sample_count: int
    nuisance_rank: int
    residual_degrees_of_freedom: int
    block_count: int
    confidence: float
    lower_variance_ratio: float
    upper_variance_ratio: float
    relative_covariance_error: float


def _validated_design(nuisance_design: ArrayLike) -> np.ndarray:
    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim != 2:
        raise ValueError("nuisance_design must be a two-dimensional array")
    sample_count, nuisance_rank = design.shape
    if sample_count < 2 or nuisance_rank < 1 or nuisance_rank >= sample_count:
        raise ValueError(
            "nuisance_design must have between one and sample_count-1 columns"
        )
    if not np.all(np.isfinite(design)):
        raise ValueError("nuisance_design must be finite")
    if np.linalg.matrix_rank(design) != nuisance_rank:
        raise ValueError("nuisance_design must have full column rank")
    return design


def _validated_whitener(whitening_matrix: ArrayLike, sample_count: int) -> np.ndarray:
    whitening = np.asarray(whitening_matrix, dtype=float)
    if whitening.shape != (sample_count, sample_count):
        raise ValueError("whitening_matrix must be square on the sample axis")
    if not np.all(np.isfinite(whitening)):
        raise ValueError("whitening_matrix must be finite")
    if np.linalg.matrix_rank(whitening) != sample_count:
        raise ValueError("whitening_matrix must be nonsingular")
    return whitening


def whitened_nuisance_projector(
    whitening_matrix: ArrayLike,
    nuisance_design: ArrayLike,
) -> np.ndarray:
    """Return the Euclidean projector orthogonal to the whitened nuisance design."""
    design = _validated_design(nuisance_design)
    whitening = _validated_whitener(whitening_matrix, design.shape[0])
    transformed_design = whitening @ design
    basis, _ = np.linalg.qr(transformed_design, mode="reduced")
    projector = np.eye(design.shape[0]) - basis @ basis.T
    return 0.5 * (projector + projector.T)


def separable_gaussian_whitened_projected_covariance(
    samples: ArrayLike,
    whitening_matrix: ArrayLike,
    nuisance_design: ArrayLike,
) -> np.ndarray:
    """Estimate spatial covariance after exact temporal whitening.

    The input ``samples`` has shape ``(sample_count, spatial_dimension)``. If
    ``W R W.T = I`` for the true temporal covariance and the mean lies in the
    declared nuisance design, then

        (N-q) * Sigma_hat ~ Wishart_p(Sigma, N-q).
    """
    design = _validated_design(nuisance_design)
    whitening = _validated_whitener(whitening_matrix, design.shape[0])
    values = np.asarray(samples, dtype=float)
    if values.ndim != 2 or values.shape[0] != design.shape[0]:
        raise ValueError("samples must have one row per nuisance-design row")
    if values.shape[1] < 1 or not np.all(np.isfinite(values)):
        raise ValueError("samples must contain finite spatial observations")

    projector = whitened_nuisance_projector(whitening, design)
    whitened = whitening @ values
    residual_degrees = design.shape[0] - design.shape[1]
    estimate = whitened.T @ projector @ whitened / residual_degrees
    return 0.5 * (estimate + estimate.T)


def gaussian_whitened_projected_covariance_bound(
    nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianWhitenedProjectedCovarianceBound:
    """Certify the exact-whitened target covariance as an ordinary Wishart.

    Exact temporal whitening followed by projection of the transformed nuisance
    design leaves ``N-q`` independent Gaussian residual rows. Therefore the
    target covariance has the same law as a weighted Wishart with ``N-q`` unit
    temporal weights, regardless of the original temporal persistence.
    """
    design = _validated_design(nuisance_design)
    residual_degrees = design.shape[0] - design.shape[1]
    matrix_bound = gaussian_weighted_wishart_matrix_bound(
        block_dimension=block_dimension,
        block_count=block_count,
        temporal_eigenvalues=np.ones(residual_degrees, dtype=float),
        confidence=confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )
    return GaussianWhitenedProjectedCovarianceBound(
        sample_count=int(design.shape[0]),
        nuisance_rank=int(design.shape[1]),
        residual_degrees_of_freedom=int(residual_degrees),
        block_dimension=int(block_dimension),
        block_count=int(block_count),
        confidence=float(confidence),
        covariance_bound=matrix_bound,
    )


def gaussian_whitened_scalar_chi_square_bound(
    nuisance_design: ArrayLike,
    *,
    block_count: int = 1,
    confidence: float = 0.975,
) -> GaussianWhitenedScalarChiSquareBound:
    """Return an exact chi-square bound for scalar whitened covariance blocks.

    For each scalar block, ``d * sigma_hat / sigma`` is exactly chi-square with
    ``d=N-q`` degrees of freedom. A Bonferroni split over both tails and the
    declared number of blocks gives simultaneous coverage without requiring
    independence between blocks.
    """
    design = _validated_design(nuisance_design)
    if isinstance(block_count, bool) or not isinstance(block_count, (int, np.integer)):
        raise TypeError("block_count must be an integer")
    if block_count < 1:
        raise ValueError("block_count must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")

    residual_degrees = int(design.shape[0] - design.shape[1])
    tail_probability = (1.0 - confidence) / (2.0 * block_count)
    lower_ratio = float(chi2.ppf(tail_probability, residual_degrees) / residual_degrees)
    upper_ratio = float(
        chi2.ppf(1.0 - tail_probability, residual_degrees) / residual_degrees
    )
    relative_error = float(max(1.0 - lower_ratio, upper_ratio - 1.0))
    return GaussianWhitenedScalarChiSquareBound(
        sample_count=int(design.shape[0]),
        nuisance_rank=int(design.shape[1]),
        residual_degrees_of_freedom=residual_degrees,
        block_count=int(block_count),
        confidence=float(confidence),
        lower_variance_ratio=lower_ratio,
        upper_variance_ratio=upper_ratio,
        relative_covariance_error=relative_error,
    )


def exponential_relaxation_whitened_projected_covariance(
    samples: ArrayLike,
    sample_times: ArrayLike,
    relaxation_time: float,
    nuisance_design: ArrayLike,
) -> np.ndarray:
    """Apply Proposition 56 using the exact irregular-time relaxation whitener."""
    factorization = exponential_relaxation_markov_factorization(
        sample_times,
        relaxation_time,
    )
    return separable_gaussian_whitened_projected_covariance(
        samples,
        factorization.whitening_matrix,
        nuisance_design,
    )
