"""Projection tools for Gaussian separable covariance with temporal nuisance means.

This module generalizes constant mean removal to any fixed, predeclared temporal
nuisance subspace. It is deliberately independent of the observer score layer:
the resulting covariance radius can be passed to the existing dependent-Gaussian
screening functions.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class GaussianProjectedTemporalEnvelope:
    """Exact projected temporal normalization and norm envelope.

    If observations have separable covariance ``R tensor Sigma`` and their mean
    lies in the column space of a fixed design ``H``, residualization with the
    orthogonal projector ``P_H`` gives an unbiased spatial covariance estimator
    after division by ``trace(P_H R)``. The two projected norms determine the
    Gaussian quadratic-form concentration radius.
    """

    sample_count: int
    nuisance_rank: int
    projected_degrees_of_freedom: float
    projected_frobenius_norm: float
    projected_spectral_norm: float
    variance_effective_sample_size: float
    operator_effective_sample_size: float


def _validated_design(
    nuisance_design: ArrayLike, sample_count: int | None = None
) -> np.ndarray:
    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] < 1 or design.shape[1] < 1:
        raise ValueError("nuisance_design must have shape (sample_count, rank >= 1)")
    if sample_count is not None and design.shape[0] != sample_count:
        raise ValueError("nuisance_design and observations have different sample counts")
    if not np.all(np.isfinite(design)):
        raise ValueError("nuisance_design must be finite")
    rank = int(np.linalg.matrix_rank(design))
    if rank != design.shape[1]:
        raise ValueError("nuisance_design columns must be linearly independent")
    if rank >= design.shape[0]:
        raise ValueError("nuisance rank must be smaller than sample_count")
    return design


def temporal_nuisance_projector(nuisance_design: ArrayLike) -> np.ndarray:
    """Return the orthogonal projector that removes a fixed temporal design."""
    design = _validated_design(nuisance_design)
    basis, _ = np.linalg.qr(design, mode="reduced")
    projector = np.eye(design.shape[0]) - basis @ basis.T
    return 0.5 * (projector + projector.T)


def gaussian_projected_temporal_envelope(
    temporal_correlation: ArrayLike,
    nuisance_design: ArrayLike,
) -> GaussianProjectedTemporalEnvelope:
    """Compute the exact projected normalization and temporal norms.

    ``temporal_correlation`` is the temporal factor ``R`` in a separable
    Gaussian covariance ``R tensor Sigma``. It may be any finite symmetric
    positive-semidefinite matrix; unit diagonal is not required by the algebra.
    """
    temporal = np.asarray(temporal_correlation, dtype=float)
    if (
        temporal.ndim != 2
        or temporal.shape[0] != temporal.shape[1]
        or temporal.shape[0] < 2
    ):
        raise ValueError("temporal_correlation must be a square matrix of size at least two")
    if not np.all(np.isfinite(temporal)) or not np.allclose(
        temporal, temporal.T, rtol=1e-10, atol=1e-12
    ):
        raise ValueError("temporal_correlation must be finite and symmetric")
    eigenvalues = np.linalg.eigvalsh(temporal)
    tolerance = 1e-10 * max(1.0, float(np.max(np.abs(eigenvalues))))
    if eigenvalues[0] < -tolerance:
        raise ValueError("temporal_correlation must be positive semidefinite")

    design = _validated_design(nuisance_design, temporal.shape[0])
    projector = temporal_nuisance_projector(design)
    projected = projector @ temporal @ projector
    projected = 0.5 * (projected + projected.T)
    degrees = float(np.trace(projected))
    if not np.isfinite(degrees) or degrees <= 0.0:
        raise ValueError("projection leaves no positive covariance normalization")
    frobenius = float(np.linalg.norm(projected, ord="fro"))
    spectral = float(np.linalg.norm(projected, ord=2))
    if not frobenius > 0.0 or not spectral > 0.0:
        raise ValueError("projection leaves no positive temporal covariance")
    return GaussianProjectedTemporalEnvelope(
        sample_count=int(temporal.shape[0]),
        nuisance_rank=int(design.shape[1]),
        projected_degrees_of_freedom=degrees,
        projected_frobenius_norm=frobenius,
        projected_spectral_norm=spectral,
        variance_effective_sample_size=float(degrees**2 / frobenius**2),
        operator_effective_sample_size=float(degrees / spectral),
    )


def gaussian_ar1_projected_temporal_envelope(
    sample_count: int,
    autocorrelation: float,
    nuisance_design: ArrayLike,
) -> GaussianProjectedTemporalEnvelope:
    """Specialize the projected envelope to a stationary AR(1) temporal factor.

    This exact helper materializes the ``sample_count`` square correlation
    matrix and is intended for moderate record lengths and verification work.
    """
    if isinstance(sample_count, bool) or not isinstance(
        sample_count, (int, np.integer)
    ):
        raise TypeError("sample_count must be an integer")
    if sample_count < 2:
        raise ValueError("sample_count must be at least two")
    phi = float(autocorrelation)
    if not np.isfinite(phi) or not -1.0 < phi < 1.0:
        raise ValueError("autocorrelation must lie strictly between -1 and one")
    design = _validated_design(nuisance_design, sample_count)
    indices = np.arange(sample_count)
    temporal = phi ** np.abs(indices[:, None] - indices[None, :])
    return gaussian_projected_temporal_envelope(temporal, design)


def separable_gaussian_projected_covariance(
    observations: ArrayLike,
    nuisance_design: ArrayLike,
    projected_degrees_of_freedom: float,
) -> np.ndarray:
    """Estimate spatial covariance after removing a declared temporal nuisance.

    The unknown mean may be any matrix ``H B`` with ``H=nuisance_design`` and
    arbitrary coefficient matrix ``B``. Residualization is done by least
    squares without explicitly forming the dense projector.
    """
    values = np.asarray(observations, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 1:
        raise ValueError("observations must have shape (sample_count, dimension)")
    if not np.all(np.isfinite(values)):
        raise ValueError("observations must be finite")
    design = _validated_design(nuisance_design, values.shape[0])
    degrees = float(projected_degrees_of_freedom)
    if not np.isfinite(degrees) or degrees <= 0.0:
        raise ValueError("projected_degrees_of_freedom must be positive and finite")
    coefficients, _, _, _ = np.linalg.lstsq(design, values, rcond=None)
    residuals = values - design @ coefficients
    return residuals.T @ residuals / degrees


def gaussian_projected_relative_covariance_error_bound(
    block_dimension: int,
    block_count: int,
    envelope: GaussianProjectedTemporalEnvelope,
    *,
    confidence: float = 0.975,
) -> float:
    """Bound simultaneous relative covariance error after nuisance projection.

    This is Proposition 42's weighted Gaussian quadratic-form radius with the
    rank-one centering projector replaced by an arbitrary fixed orthogonal
    nuisance projector. It is condition-number free because the event is
    stated in population-whitened coordinates.
    """
    integer_values = (block_dimension, block_count)
    if any(
        isinstance(value, bool) or not isinstance(value, (int, np.integer))
        for value in integer_values
    ):
        raise TypeError("block_dimension and block_count must be integers")
    if block_dimension < 1 or block_count < 1:
        raise ValueError("block_dimension and block_count must be positive")
    if not isinstance(envelope, GaussianProjectedTemporalEnvelope):
        raise TypeError("envelope has the wrong type")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    tail = np.log(
        2.0 * block_count * 9.0**block_dimension / (1.0 - float(confidence))
    )
    return float(
        4.0
        * (
            envelope.projected_frobenius_norm * np.sqrt(tail)
            + envelope.projected_spectral_norm * tail
        )
        / envelope.projected_degrees_of_freedom
    )
