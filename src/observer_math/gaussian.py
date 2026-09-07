"""Exact information quantities for stationary Gaussian dynamical systems."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.linalg import solve_discrete_lyapunov

FloatMatrix = NDArray[np.float64]
FloatArray = NDArray[np.float64]
_LOG_2 = np.log(2.0)


def as_square(matrix: ArrayLike, *, name: str) -> FloatMatrix:
    """Return a finite, symmetric-compatible square matrix."""
    result = np.asarray(matrix, dtype=float)
    if result.ndim != 2 or result.shape[0] != result.shape[1]:
        raise ValueError(f"{name} must be a square matrix")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must contain only finite values")
    return result


def symmetrize(matrix: ArrayLike) -> FloatMatrix:
    """Remove numerical asymmetry without changing the intended covariance."""
    value = np.asarray(matrix, dtype=float)
    return 0.5 * (value + value.T)


def stable_logdet(matrix: ArrayLike, *, floor: float = 1e-12) -> float:
    """Compute log(det(matrix)) after a documented eigenvalue floor."""
    eigenvalues = np.linalg.eigvalsh(symmetrize(matrix))
    if eigenvalues[-1] <= 0:
        raise ValueError("covariance must have at least one positive eigenvalue")
    scale_floor = floor * max(1.0, float(eigenvalues[-1]))
    return float(np.log(np.clip(eigenvalues, scale_floor, None)).sum())


def stationary_covariance(transition: ArrayLike, noise_covariance: ArrayLike) -> FloatMatrix:
    """Solve Sigma = A Sigma A.T + Q for a stable discrete-time system."""
    transition = as_square(transition, name="transition")
    noise_covariance = as_square(noise_covariance, name="noise_covariance")
    if transition.shape != noise_covariance.shape:
        raise ValueError("transition and noise_covariance must have equal dimensions")
    spectral_radius = float(np.max(np.abs(np.linalg.eigvals(transition))))
    if spectral_radius >= 1.0:
        raise ValueError("transition must have spectral radius below one")
    covariance = solve_discrete_lyapunov(transition, symmetrize(noise_covariance))
    return symmetrize(covariance)


def two_time_covariance(
    transition: ArrayLike,
    noise_covariance: ArrayLike,
    *,
    lag: int = 1,
) -> FloatMatrix:
    """Return Cov([X_t, X_(t+lag)]) for a stationary linear Gaussian process."""
    if lag < 1:
        raise ValueError("lag must be a positive integer")
    transition = as_square(transition, name="transition")
    covariance = stationary_covariance(transition, noise_covariance)
    lag_transition = np.linalg.matrix_power(transition, lag)
    cross_covariance = covariance @ lag_transition.T
    return symmetrize(
        np.block(
            [
                [covariance, cross_covariance],
                [cross_covariance.T, covariance],
            ]
        )
    )


def _principal(covariance: FloatMatrix, indices: Sequence[int]) -> FloatMatrix:
    index = np.asarray(tuple(indices), dtype=int)
    return covariance[np.ix_(index, index)]


def gaussian_mutual_information(
    covariance: ArrayLike,
    x: Sequence[int],
    y: Sequence[int],
) -> float:
    """Return I(X;Y) in bits from a joint Gaussian covariance matrix."""
    covariance = as_square(covariance, name="covariance")
    x, y = tuple(x), tuple(y)
    if not x or not y:
        return 0.0
    xy = x + y
    value = 0.5 * (
        stable_logdet(_principal(covariance, x))
        + stable_logdet(_principal(covariance, y))
        - stable_logdet(_principal(covariance, xy))
    ) / _LOG_2
    return max(0.0, float(value))


def gaussian_conditional_mutual_information(
    covariance: ArrayLike,
    x: Sequence[int],
    y: Sequence[int],
    given: Sequence[int],
) -> float:
    """Return I(X;Y|Z) in bits from a joint Gaussian covariance matrix."""
    covariance = as_square(covariance, name="covariance")
    x, y, given = tuple(x), tuple(y), tuple(given)
    if not given:
        return gaussian_mutual_information(covariance, x, y)
    xz, yz, xyz = x + given, y + given, x + y + given
    value = 0.5 * (
        stable_logdet(_principal(covariance, xz))
        + stable_logdet(_principal(covariance, yz))
        - stable_logdet(_principal(covariance, given))
        - stable_logdet(_principal(covariance, xyz))
    ) / _LOG_2
    return max(0.0, float(value))


def predictive_persistence(
    two_time_cov: ArrayLike,
    subset: Sequence[int],
) -> float:
    """Mean squared time-lagged canonical correlation, bounded in [0, 1]."""
    covariance = as_square(two_time_cov, name="two_time_cov")
    dimension = covariance.shape[0] // 2
    subset = tuple(subset)
    present = _principal(covariance, subset)
    future_indices = tuple(dimension + index for index in subset)
    future = _principal(covariance, future_indices)
    cross = covariance[np.ix_(np.asarray(subset), np.asarray(future_indices))]

    return canonical_persistence(present, future, cross)


def _inverse_sqrt(matrix: FloatMatrix) -> FloatMatrix:
    values, vectors = np.linalg.eigh(symmetrize(matrix))
    floor = 1e-12 * max(1.0, float(values[-1]))
    return (vectors * (1.0 / np.sqrt(np.clip(values, floor, None)))) @ vectors.T


def canonical_correlations(
    source_covariance: ArrayLike,
    target_covariance: ArrayLike,
    cross_covariance: ArrayLike,
) -> FloatArray:
    """Canonical correlations between two Gaussian random vectors.

    These singular values are invariant under invertible linear changes of
    coordinates within either vector. This makes them suitable for comparing
    representations whose bases change through time.
    """
    source_covariance = as_square(source_covariance, name="source_covariance")
    target_covariance = as_square(target_covariance, name="target_covariance")
    cross_covariance = np.asarray(cross_covariance, dtype=float)
    expected = (source_covariance.shape[0], target_covariance.shape[0])
    if cross_covariance.shape != expected:
        raise ValueError(f"cross_covariance must have shape {expected}")
    whitened = (
        _inverse_sqrt(source_covariance)
        @ cross_covariance
        @ _inverse_sqrt(target_covariance)
    )
    values = np.linalg.svd(whitened, compute_uv=False)
    return np.clip(values, 0.0, 1.0)


def canonical_persistence(
    source_covariance: ArrayLike,
    target_covariance: ArrayLike,
    cross_covariance: ArrayLike,
) -> float:
    """Mean squared canonical correlation, bounded in [0, 1]."""
    correlations = canonical_correlations(
        source_covariance, target_covariance, cross_covariance
    )
    if correlations.size == 0:
        return 0.0
    return float(np.mean(correlations**2))
