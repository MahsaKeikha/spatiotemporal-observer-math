"""Exact innovation-whitened target covariance concentration.

Proposition 56 uses the local irregular-grid Markov factorization from
Proposition 53 to remove known temporal correlation before covariance
estimation. For a known physical relaxation time, the lower-bidiagonal
innovation whitener turns the declared exponential temporal covariance into the
identity. After applying the same whitener to a predeclared nuisance design,
ordinary least-squares residualization in innovation coordinates leaves exactly
N-q independent Gaussian residual degrees of freedom.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .matrix_chernoff import (
    GaussianWeightedWishartMatrixBound,
    gaussian_weighted_wishart_matrix_bound,
)
from .physical_relaxation import exponential_relaxation_markov_factorization


@dataclass(frozen=True)
class GaussianInnovationWhitenedMatrixChernoffBound:
    """Known-relaxation-time covariance certificate in innovation coordinates."""

    block_dimension: int
    block_count: int
    confidence: float
    sample_count: int
    nuisance_rank: int
    residual_degrees_of_freedom: int
    relaxation_time: float
    whitening_nonzero_count: int
    precision_nonzero_count: int
    covariance_bound: GaussianWeightedWishartMatrixBound

    @property
    def covariance_relative_error(self) -> float:
        """Return the certified relative covariance operator-norm radius."""
        return self.covariance_bound.relative_covariance_error


def _validated_design(values: ArrayLike, sample_count: int) -> np.ndarray:
    design = np.asarray(values, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] != sample_count:
        raise ValueError("nuisance_design must have one row per sample time")
    if design.shape[1] < 1 or design.shape[1] >= sample_count:
        raise ValueError("nuisance_design must have rank between one and sample_count-1")
    if not np.all(np.isfinite(design)):
        raise ValueError("nuisance_design must be finite")
    if np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("nuisance_design must have full column rank")
    return design


def _validated_values(values: ArrayLike, sample_count: int) -> np.ndarray:
    observations = np.asarray(values, dtype=float)
    if observations.ndim == 1:
        observations = observations[:, None]
    if observations.ndim != 2 or observations.shape[0] != sample_count:
        raise ValueError("values must have one row per sample time")
    if observations.shape[1] < 1 or not np.all(np.isfinite(observations)):
        raise ValueError("values must contain at least one finite measurement channel")
    return observations


def separable_gaussian_innovation_whitened_covariance(
    values: ArrayLike,
    sample_times: ArrayLike,
    nuisance_design: ArrayLike,
    relaxation_time: float,
) -> np.ndarray:
    r"""Estimate spatial covariance after exact temporal innovation whitening.

    The declared target model is

        Y = H B + E,
        vec(E) ~ N(0, R_tau \otimes Gamma),

    where ``R_tau`` is the exponential relaxation covariance on the supplied
    timestamps. Let ``W_tau R_tau W_tau.T = I`` be the exact lower-bidiagonal
    whitener from Proposition 53 and let ``G = W_tau H``. In innovation
    coordinates, ``W_tau Y = G B + Z`` with independent Gaussian rows of
    covariance ``Gamma``.

    Residualizing against ``G`` and dividing by ``N-q`` therefore gives an
    exactly unbiased spatial covariance estimator. The construction is the
    generalized least-squares residual covariance written in local innovation
    coordinates.
    """
    factorization = exponential_relaxation_markov_factorization(
        sample_times,
        relaxation_time,
    )
    sample_count = int(factorization.sample_times.size)
    design = _validated_design(nuisance_design, sample_count)
    observations = _validated_values(values, sample_count)

    whitening = factorization.whitening_matrix
    transformed_design = whitening @ design
    transformed_values = whitening @ observations

    # W_tau is invertible, so a full-rank H remains full rank after whitening.
    nuisance_basis, _ = np.linalg.qr(transformed_design, mode="reduced")
    residuals = transformed_values - nuisance_basis @ (
        nuisance_basis.T @ transformed_values
    )
    residual_degrees = sample_count - design.shape[1]
    covariance = residuals.T @ residuals / float(residual_degrees)
    return 0.5 * (covariance + covariance.T)


def gaussian_innovation_whitened_matrix_chernoff_bound(
    sample_times: ArrayLike,
    nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    relaxation_time: float,
    confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianInnovationWhitenedMatrixChernoffBound:
    """Certify target covariance after exact known-tau innovation whitening.

    Once the true declared relaxation time is supplied, Proposition 53 gives an
    exact temporal whitener. Applying it to both the measurements and nuisance
    design yields an ordinary Gaussian linear model with independent rows.

    If the nuisance rank is ``q`` and the sample count is ``N``, orthogonal
    residualization leaves ``r=N-q`` independent Gaussian residual coordinates.
    Consequently

        r * Gamma_hat ~ Wishart_d(Gamma, r),

    and Proposition 47 applies with exactly ``r`` unit temporal weights. No
    temporal spectral-norm or effective-sample-size penalty remains.
    """
    factorization = exponential_relaxation_markov_factorization(
        sample_times,
        relaxation_time,
    )
    sample_count = int(factorization.sample_times.size)
    design = _validated_design(nuisance_design, sample_count)
    residual_degrees = sample_count - design.shape[1]

    covariance_bound = gaussian_weighted_wishart_matrix_bound(
        block_dimension,
        block_count,
        np.ones(residual_degrees, dtype=float),
        confidence=confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )

    whitening = factorization.whitening_matrix
    precision = factorization.precision_matrix
    tolerance = 1e-14
    return GaussianInnovationWhitenedMatrixChernoffBound(
        block_dimension=int(block_dimension),
        block_count=int(block_count),
        confidence=float(confidence),
        sample_count=sample_count,
        nuisance_rank=int(design.shape[1]),
        residual_degrees_of_freedom=int(residual_degrees),
        relaxation_time=float(factorization.relaxation_time),
        whitening_nonzero_count=int(np.count_nonzero(np.abs(whitening) > tolerance)),
        precision_nonzero_count=int(np.count_nonzero(np.abs(precision) > tolerance)),
        covariance_bound=covariance_bound,
    )
