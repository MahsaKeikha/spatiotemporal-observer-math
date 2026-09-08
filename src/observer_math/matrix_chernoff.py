"""Matrix-Laplace concentration for weighted Gaussian Wishart covariance.

Proposition 47 replaces the 1/4-sphere-net reduction used in the earlier
weighted Gaussian covariance bounds by an exact matrix exponential moment for
rank-one Gaussian summands. The resulting finite-sample operator-norm bound
uses the full eigenvalue profile of the temporal quadratic form.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .nuisance import temporal_nuisance_projector


@dataclass(frozen=True)
class GaussianWeightedWishartMatrixBound:
    """Two-sided operator-norm bound for a weighted Gaussian sample covariance."""

    block_dimension: int
    block_count: int
    confidence: float
    temporal_rank: int
    temporal_trace: float
    temporal_frobenius_norm: float
    temporal_spectral_norm: float
    upper_deviation: float
    lower_deviation: float
    relative_covariance_error: float
    upper_dimensionless_theta: float
    lower_dimensionless_theta: float
    upper_theta_grid_size: int
    lower_theta_grid_size: int


def _validated_weights(temporal_eigenvalues: ArrayLike) -> np.ndarray:
    weights = np.asarray(temporal_eigenvalues, dtype=float).reshape(-1)
    if weights.size < 1 or not np.all(np.isfinite(weights)):
        raise ValueError("temporal_eigenvalues must contain finite values")
    scale = max(1.0, float(np.max(np.abs(weights))))
    tolerance = 1e-12 * scale
    if np.min(weights) < -tolerance:
        raise ValueError("temporal_eigenvalues must be nonnegative")
    weights = np.maximum(weights, 0.0)
    positive = weights[weights > tolerance]
    if positive.size == 0:
        raise ValueError("temporal_eigenvalues must have positive trace")
    return positive


def _validated_grid_size(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    if value < 64:
        raise ValueError(f"{name} must be at least 64")
    return int(value)


def _log_scalar_gaussian_matrix_mgf(
    dimension: int,
    scaled_theta_weights: np.ndarray,
    *,
    upper_tail: bool,
) -> np.ndarray:
    """Log of the scalar matrix mgf for lambda (g g^T - I).

    Rotational invariance gives

    E exp(a (g g^T - I)) = c_m(a) I.

    For the upper tail, ``a`` must lie in [0, 1/2). For the lower tail we apply
    the same calculation to ``-lambda(g g^T-I)`` and there is no finite upper
    restriction on ``a``.
    """
    x = np.asarray(scaled_theta_weights, dtype=float)
    if upper_tail:
        if np.any(x < 0.0) or np.any(x >= 0.5):
            raise ValueError("upper-tail theta*lambda values must lie in [0, 1/2)")
        log_chi = -0.5 * dimension * np.log1p(-2.0 * x)
        sign_term = -x
    else:
        if np.any(x < 0.0):
            raise ValueError("lower-tail theta*lambda values must be nonnegative")
        log_chi = -0.5 * dimension * np.log1p(2.0 * x)
        sign_term = x

    if dimension == 1:
        log_bracket = log_chi
    else:
        log_bracket = (
            np.logaddexp(np.log(float(dimension - 1)), log_chi)
            - np.log(float(dimension))
        )
    return sign_term + log_bracket


def gaussian_weighted_wishart_matrix_bound(
    block_dimension: int,
    block_count: int,
    temporal_eigenvalues: ArrayLike,
    *,
    confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianWeightedWishartMatrixBound:
    """Certify a weighted Gaussian covariance by matrix Laplace concentration.

    Let ``g_i ~ N(0, I_m)`` be independent and let nonnegative ``lambda_i`` be
    the supplied temporal eigenvalues. Define

    ``S = sum_i lambda_i g_i g_i^T / sum_i lambda_i``.

    The function returns ``epsilon`` such that, simultaneously over the declared
    number of covariance blocks,

    ``||S - I||_2 <= epsilon``

    with at least the requested confidence.

    Each candidate value of the matrix-Laplace parameter gives a rigorous
    Chernoff bound. The finite parameter grids therefore affect tightness only,
    not validity: taking the minimum over any deterministic set of valid theta
    values remains a valid upper bound on the tail probability.
    """
    if isinstance(block_dimension, bool) or not isinstance(block_dimension, (int, np.integer)):
        raise TypeError("block_dimension must be an integer")
    if isinstance(block_count, bool) or not isinstance(block_count, (int, np.integer)):
        raise TypeError("block_count must be an integer")
    if block_dimension < 1 or block_count < 1:
        raise ValueError("block_dimension and block_count must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    upper_grid_size = _validated_grid_size(upper_theta_grid_size, "upper_theta_grid_size")
    lower_grid_size = _validated_grid_size(lower_theta_grid_size, "lower_theta_grid_size")
    weights = _validated_weights(temporal_eigenvalues)

    trace = float(np.sum(weights))
    frobenius = float(np.linalg.norm(weights))
    spectral = float(np.max(weights))
    log_prefactor = float(
        np.log(2.0 * block_count * block_dimension / (1.0 - confidence))
    )

    upper_x = np.geomspace(1e-8, 0.499999, upper_grid_size)
    upper_values = np.empty_like(upper_x)
    for index, x in enumerate(upper_x):
        theta = x / spectral
        log_mgf = float(
            np.sum(
                _log_scalar_gaussian_matrix_mgf(
                    block_dimension,
                    theta * weights,
                    upper_tail=True,
                )
            )
        )
        upper_values[index] = (log_prefactor + log_mgf) / theta
    upper_index = int(np.argmin(upper_values))
    upper_deviation = float(upper_values[upper_index] / trace)

    lower_x = np.geomspace(1e-8, 1e3, lower_grid_size)
    lower_values = np.empty_like(lower_x)
    for index, x in enumerate(lower_x):
        theta = x / spectral
        log_mgf = float(
            np.sum(
                _log_scalar_gaussian_matrix_mgf(
                    block_dimension,
                    theta * weights,
                    upper_tail=False,
                )
            )
        )
        lower_values[index] = (log_prefactor + log_mgf) / theta
    lower_index = int(np.argmin(lower_values))
    # S is positive semidefinite, so its downward relative deviation from I can
    # never exceed one. This deterministic fact safely caps the Chernoff value.
    lower_deviation = float(min(1.0, lower_values[lower_index] / trace))

    return GaussianWeightedWishartMatrixBound(
        block_dimension=int(block_dimension),
        block_count=int(block_count),
        confidence=float(confidence),
        temporal_rank=int(weights.size),
        temporal_trace=trace,
        temporal_frobenius_norm=frobenius,
        temporal_spectral_norm=spectral,
        upper_deviation=upper_deviation,
        lower_deviation=lower_deviation,
        relative_covariance_error=float(max(upper_deviation, lower_deviation)),
        upper_dimensionless_theta=float(upper_x[upper_index]),
        lower_dimensionless_theta=float(lower_x[lower_index]),
        upper_theta_grid_size=upper_grid_size,
        lower_theta_grid_size=lower_grid_size,
    )


def projected_temporal_eigenvalues(
    temporal_covariance: ArrayLike,
    nuisance_design: ArrayLike,
) -> np.ndarray:
    """Return the positive eigenvalues of P_H R P_H."""
    temporal = np.asarray(temporal_covariance, dtype=float)
    if temporal.ndim != 2 or temporal.shape[0] != temporal.shape[1]:
        raise ValueError("temporal_covariance must be square")
    if not np.all(np.isfinite(temporal)):
        raise ValueError("temporal_covariance must be finite")
    temporal = 0.5 * (temporal + temporal.T)
    projector = temporal_nuisance_projector(nuisance_design)
    if projector.shape != temporal.shape:
        raise ValueError("temporal_covariance and nuisance_design have incompatible sample axes")
    projected = projector @ temporal @ projector
    projected = 0.5 * (projected + projected.T)
    eigenvalues = np.linalg.eigvalsh(projected)
    tolerance = 1e-11 * max(1.0, float(np.max(np.abs(eigenvalues))))
    if np.min(eigenvalues) < -tolerance:
        raise ValueError("projected temporal covariance is not positive semidefinite")
    return np.maximum(eigenvalues[eigenvalues > tolerance], 0.0)


def gaussian_projected_weighted_wishart_matrix_bound(
    block_dimension: int,
    block_count: int,
    temporal_covariance: ArrayLike,
    nuisance_design: ArrayLike,
    *,
    confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianWeightedWishartMatrixBound:
    """Apply Proposition 47 directly to a known temporal covariance and design."""
    eigenvalues = projected_temporal_eigenvalues(
        temporal_covariance,
        nuisance_design,
    )
    return gaussian_weighted_wishart_matrix_bound(
        block_dimension,
        block_count,
        eigenvalues,
        confidence=confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )
