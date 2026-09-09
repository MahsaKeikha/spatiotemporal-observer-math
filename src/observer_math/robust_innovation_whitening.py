"""Robust innovation-whitened covariance concentration over tau uncertainty.

Proposition 57 connects the finite-sample physical-time calibration layer to
Proposition 56. A single working relaxation time is used to whiten an
independent target record. If the true relaxation time lies in a certified
compact interval, the resulting transformed temporal covariance belongs to a
covered compact family. Proposition 49 can therefore certify the target
covariance uniformly over every true relaxation time in that interval.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .compact_temporal_family import (
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from .physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_markov_factorization,
    exponential_relaxation_operator_lipschitz_bound,
)


@dataclass(frozen=True)
class GaussianRobustInnovationWhitenedMatrixChernoffBound:
    """Uniform target certificate for one working whitener and a tau interval."""

    block_dimension: int
    block_count: int
    confidence: float
    sample_count: int
    nuisance_rank: int
    residual_degrees_of_freedom: int
    relaxation_time_lower_bound: float
    relaxation_time_upper_bound: float
    working_relaxation_time: float
    relaxation_time_grid_size: int
    maximum_relaxation_time_spacing: float
    raw_covariance_operator_lipschitz_bound: float
    whitening_operator_norm: float
    transformed_operator_lipschitz_bound: float
    transformed_normalization_lipschitz_bound: float
    transformed_eigenvalue_covering_radius: float
    transformed_normalization_covering_radius: float
    covariance_normalization: float
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound

    @property
    def covariance_relative_error(self) -> float:
        """Return the certified uniform relative covariance radius."""
        return self.covariance_bound.covariance_relative_error


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


def _validated_grid_size(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError("relaxation_time_grid_size must be an integer")
    if value < 2:
        raise ValueError("relaxation_time_grid_size must be at least two")
    return int(value)


def _entrywise_relaxation_derivative_supremum(
    distance: float,
    lower_relaxation_time: float,
    upper_relaxation_time: float,
) -> float:
    """Return sup_tau d exp(-d/tau)/tau^2 on one positive tau interval."""
    if distance <= 0.0:
        return 0.0
    candidate = float(
        np.clip(
            0.5 * distance,
            lower_relaxation_time,
            upper_relaxation_time,
        )
    )
    return float(distance * np.exp(-distance / candidate) / candidate**2)


def _projected_trace_lipschitz_bound(
    sample_times: np.ndarray,
    whitening: np.ndarray,
    transformed_design: np.ndarray,
    lower_relaxation_time: float,
    upper_relaxation_time: float,
) -> float:
    r"""Bound the derivative of the projected transformed temporal trace.

    Let

        C_tau = W0 R_tau W0.T

    and let ``P_G`` be the orthogonal projector onto the complement of the
    transformed nuisance design ``G=W0 H``. The normalization used by
    Proposition 49 is

        d(tau) = tr(P_G C_tau)
               = tr(M R_tau),
        M = W0.T P_G W0.

    For ``r_ij(tau)=exp(-|t_i-t_j|/tau)``, the derivative magnitude is

        |t_i-t_j| exp(-|t_i-t_j|/tau) / tau^2.

    Its exact scalar supremum over a compact positive tau interval occurs at
    ``tau=|t_i-t_j|/2`` clipped to that interval. Therefore

        |d'(tau)|
        <= sum_ij |M_ij| sup_tau |r'_ij(tau)|.

    This trace-specific deterministic bound is generally much tighter than the
    valid but crude rank-times-operator-radius inequality. It changes only the
    normalization cover; the operator/eigenvalue cover remains unchanged.
    """
    nuisance_basis, _ = np.linalg.qr(transformed_design, mode="reduced")
    projector = np.eye(sample_times.size) - nuisance_basis @ nuisance_basis.T
    trace_matrix = whitening.T @ projector @ whitening

    distances = np.abs(sample_times[:, None] - sample_times[None, :])
    derivative_suprema = np.zeros_like(distances)
    for row in range(sample_times.size):
        for column in range(sample_times.size):
            derivative_suprema[row, column] = (
                _entrywise_relaxation_derivative_supremum(
                    float(distances[row, column]),
                    lower_relaxation_time,
                    upper_relaxation_time,
                )
            )
    return float(np.sum(np.abs(trace_matrix) * derivative_suprema))


def gaussian_robust_innovation_whitened_matrix_chernoff_bound(
    sample_times: ArrayLike,
    nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    lower_relaxation_time: float,
    upper_relaxation_time: float,
    working_relaxation_time: float | None = None,
    relaxation_time_grid_size: int = 1025,
    confidence: float = 0.975,
    upper_theta_grid_size: int = 256,
    lower_theta_grid_size: int = 256,
) -> GaussianRobustInnovationWhitenedMatrixChernoffBound:
    r"""Certify one working innovation whitener over a compact true-tau interval.

    Let ``W0`` be the exact Proposition 53 whitener associated with a fixed
    working relaxation time ``tau0`` and let the true target covariance be
    ``R_tau`` for an unknown ``tau`` in the declared interval. In working
    innovation coordinates the temporal covariance is

        C_tau = W0 @ R_tau @ W0.T.

    Apply the same ``W0`` to the nuisance design. Proposition 49 then applies to
    the compact family ``{C_tau}`` after a certified finite cover.

    If ``L`` satisfies ``||R_tau-R_tau'||_2 <= L |tau-tau'|``, then

        ||C_tau-C_tau'||_2
        <= ||W0||_2^2 L |tau-tau'|.

    For a uniform grid, half the maximum grid spacing times that transformed
    Lipschitz constant is therefore a valid eigenvalue covering radius.

    The projected trace is certified separately. If ``P_G`` projects onto the
    transformed nuisance complement, then

        d(tau) = tr(P_G W0 R_tau W0.T).

    The implementation bounds ``|d'(tau)|`` directly using the exact scalar
    derivative suprema of the exponential kernel and the fixed matrix
    ``W0.T P_G W0``. Half the grid spacing times this trace-specific Lipschitz
    constant is a valid normalization covering radius. This is tighter than
    multiplying the operator radius by the full residual rank while preserving
    the same finite-sample uniform guarantee.

    The covariance estimator associated with the returned certificate must use
    ``covariance_normalization`` rather than automatically dividing by ``N-q``.
    This deterministic normalization is the midpoint of the certified projected
    trace range used by Proposition 49.
    """
    lower = float(lower_relaxation_time)
    upper = float(upper_relaxation_time)
    if not np.isfinite(lower) or lower <= 0.0:
        raise ValueError("lower_relaxation_time must be finite and positive")
    if not np.isfinite(upper) or upper < lower:
        raise ValueError("upper_relaxation_time must be finite and at least the lower bound")
    grid_size = _validated_grid_size(relaxation_time_grid_size)

    if working_relaxation_time is None:
        working = 0.5 * (lower + upper)
    else:
        working = float(working_relaxation_time)
    if not np.isfinite(working) or working <= 0.0:
        raise ValueError("working_relaxation_time must be finite and positive")

    factorization = exponential_relaxation_markov_factorization(sample_times, working)
    times = factorization.sample_times
    sample_count = int(times.size)
    design = _validated_design(nuisance_design, sample_count)
    nuisance_rank = int(design.shape[1])
    residual_rank = sample_count - nuisance_rank

    whitening = factorization.whitening_matrix
    transformed_design = whitening @ design
    whitening_norm = float(np.linalg.norm(whitening, ord=2))

    tau_grid = np.linspace(lower, upper, grid_size)
    transformed_grid = np.stack(
        [
            whitening
            @ exponential_relaxation_covariance(times, tau)
            @ whitening.T
            for tau in tau_grid
        ]
    )

    maximum_spacing = float(np.max(np.diff(tau_grid)))
    raw_lipschitz = exponential_relaxation_operator_lipschitz_bound(times, lower, upper)
    transformed_lipschitz = float(whitening_norm**2 * raw_lipschitz)
    normalization_lipschitz = _projected_trace_lipschitz_bound(
        times,
        whitening,
        transformed_design,
        lower,
        upper,
    )
    eigenvalue_radius = float(0.5 * maximum_spacing * transformed_lipschitz)
    normalization_radius = float(0.5 * maximum_spacing * normalization_lipschitz)

    covariance_bound = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension=block_dimension,
        block_count=block_count,
        temporal_covariance_grid=transformed_grid,
        nuisance_design=transformed_design,
        eigenvalue_covering_radius=eigenvalue_radius,
        normalization_covering_radius=normalization_radius,
        confidence=confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )

    return GaussianRobustInnovationWhitenedMatrixChernoffBound(
        block_dimension=int(block_dimension),
        block_count=int(block_count),
        confidence=float(confidence),
        sample_count=sample_count,
        nuisance_rank=nuisance_rank,
        residual_degrees_of_freedom=residual_rank,
        relaxation_time_lower_bound=lower,
        relaxation_time_upper_bound=upper,
        working_relaxation_time=working,
        relaxation_time_grid_size=grid_size,
        maximum_relaxation_time_spacing=maximum_spacing,
        raw_covariance_operator_lipschitz_bound=raw_lipschitz,
        whitening_operator_norm=whitening_norm,
        transformed_operator_lipschitz_bound=transformed_lipschitz,
        transformed_normalization_lipschitz_bound=normalization_lipschitz,
        transformed_eigenvalue_covering_radius=eigenvalue_radius,
        transformed_normalization_covering_radius=normalization_radius,
        covariance_normalization=float(
            covariance_bound.reference_projected_degrees_of_freedom
        ),
        covariance_bound=covariance_bound,
    )


def separable_gaussian_robust_innovation_whitened_covariance(
    values: ArrayLike,
    sample_times: ArrayLike,
    nuisance_design: ArrayLike,
    *,
    working_relaxation_time: float,
    covariance_normalization: float,
) -> np.ndarray:
    """Estimate spatial covariance using one fixed working innovation whitener."""
    factorization = exponential_relaxation_markov_factorization(
        sample_times,
        working_relaxation_time,
    )
    sample_count = int(factorization.sample_times.size)
    design = _validated_design(nuisance_design, sample_count)
    observations = _validated_values(values, sample_count)
    normalization = float(covariance_normalization)
    if not np.isfinite(normalization) or normalization <= 0.0:
        raise ValueError("covariance_normalization must be finite and positive")

    whitening = factorization.whitening_matrix
    transformed_design = whitening @ design
    transformed_values = whitening @ observations
    nuisance_basis, _ = np.linalg.qr(transformed_design, mode="reduced")
    residuals = transformed_values - nuisance_basis @ (
        nuisance_basis.T @ transformed_values
    )
    covariance = residuals.T @ residuals / normalization
    return 0.5 * (covariance + covariance.T)
