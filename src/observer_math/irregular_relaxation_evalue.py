"""Finite-sample calibration of physical relaxation time on irregular grids.

This module extends Proposition 53 by combining its exact irregular-time Markov
factorization with the e-value strategy used earlier in Proposition 51. The
calibration model is deliberately narrow and explicit: independent standardized
zero-mean Gaussian channels share one exponential relaxation time and one common
irregular sampling schedule.

For a fixed candidate relaxation time tau, the exact Gaussian likelihood factors
through local innovations. A finite mixture density q is fixed before observing
the calibration data. Therefore e_tau = q / p_tau has expectation one when tau
is the true parameter, and Markov's inequality gives a finite-sample continuum
confidence set without a parameterwise union bound.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
from scipy.special import logsumexp

from .compact_temporal_family import (
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from .physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_operator_lipschitz_bound,
)


@dataclass(frozen=True)
class GaussianIrregularRelaxationEValueModel:
    """Observed-data object for a continuum confidence set in physical tau."""

    sample_times: np.ndarray
    sample_count: int
    channel_count: int
    confidence: float
    log_evalue_threshold: float
    declared_relaxation_time_lower_bound: float
    declared_relaxation_time_upper_bound: float
    mixture_relaxation_time_grid: np.ndarray
    mixture_point_count: int
    transition_sum_xx: np.ndarray
    transition_sum_xy: np.ndarray
    transition_sum_yy: np.ndarray
    log_mixture_density_kernel: float


@dataclass(frozen=True)
class GaussianIrregularRelaxationEValueGrid:
    """Diagnostic evaluation of the continuum e-value function on a fixed grid."""

    relaxation_time_grid: np.ndarray
    log_evalues: np.ndarray
    accepted_mask: np.ndarray
    accepted_point_count: int
    total_point_count: int
    accepted_relaxation_time_lower_bound: float
    accepted_relaxation_time_upper_bound: float


@dataclass(frozen=True)
class GaussianIrregularRelaxationEValueOuterCover:
    """Certified finite outer cover of the continuum relaxation-time set."""

    cell_edges: np.ndarray
    cell_centers: np.ndarray
    cell_radius: float
    log_evalues_at_centers: np.ndarray
    cell_log_likelihood_lipschitz_bounds: np.ndarray
    log_likelihood_lipschitz_bound: float
    retained_mask: np.ndarray
    retained_cell_count: int
    excluded_cell_count: int
    total_cell_count: int
    retained_relaxation_time_lower_bound: float
    retained_relaxation_time_upper_bound: float


@dataclass(frozen=True)
class GaussianIrregularRelaxationTargetBound:
    """Independent target covariance certificate after irregular tau calibration."""

    calibration_outer_cover: GaussianIrregularRelaxationEValueOuterCover
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence: float
    target_operator_lipschitz_bound: float
    target_eigenvalue_covering_radius: float
    target_normalization_covering_radius: float


def _validated_times(sample_times: ArrayLike) -> np.ndarray:
    times = np.asarray(sample_times, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("sample_times must be one-dimensional with at least two entries")
    if not np.all(np.isfinite(times)):
        raise ValueError("sample_times must be finite")
    if not np.all(np.diff(times) > 0.0):
        raise ValueError("sample_times must be strictly increasing")
    return times


def _validated_relaxation_interval(lower: float, upper: float) -> tuple[float, float]:
    lower_value = float(lower)
    upper_value = float(upper)
    if not np.isfinite(lower_value) or lower_value <= 0.0:
        raise ValueError("lower_relaxation_time must be finite and positive")
    if not np.isfinite(upper_value) or upper_value < lower_value:
        raise ValueError("upper_relaxation_time must be finite and at least the lower bound")
    return lower_value, upper_value


def _validated_grid_size(value: int, name: str, *, degenerate: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    minimum = 1 if degenerate else 2
    if value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return int(value)


def _parameter_grid(lower: float, upper: float, size: int) -> np.ndarray:
    if lower == upper:
        return np.array([lower], dtype=float)
    return np.linspace(lower, upper, size)


def _validated_observations(
    standardized_observations: ArrayLike,
    sample_count: int,
) -> np.ndarray:
    values = np.asarray(standardized_observations, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or values.shape[0] != sample_count or values.shape[1] < 1:
        raise ValueError(
            "standardized_observations must have shape (sample_count, channel_count)"
        )
    if not np.all(np.isfinite(values)):
        raise ValueError("standardized_observations must be finite")
    return values


def _transition_statistics(values: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    present = values[:-1]
    future = values[1:]
    sum_xx = np.sum(present * present, axis=1)
    sum_xy = np.sum(present * future, axis=1)
    sum_yy = np.sum(future * future, axis=1)
    return sum_xx, sum_xy, sum_yy


def _transition_parameters(
    sample_times: np.ndarray,
    relaxation_time: float,
) -> tuple[np.ndarray, np.ndarray]:
    tau = float(relaxation_time)
    if not np.isfinite(tau) or tau <= 0.0:
        raise ValueError("relaxation_time must be finite and positive")
    intervals = np.diff(sample_times)
    alpha = np.exp(-intervals / tau)
    innovation_variance = 1.0 - alpha * alpha
    return alpha, innovation_variance


def _log_likelihood_kernel_from_statistics(
    sample_times: np.ndarray,
    channel_count: int,
    sum_xx: np.ndarray,
    sum_xy: np.ndarray,
    sum_yy: np.ndarray,
    relaxation_time: float,
) -> float:
    alpha, variance = _transition_parameters(sample_times, relaxation_time)
    residual_sum_squares = sum_yy - 2.0 * alpha * sum_xy + alpha * alpha * sum_xx
    return float(
        -0.5 * channel_count * np.sum(np.log(variance))
        - 0.5 * np.sum(residual_sum_squares / variance)
    )


def gaussian_irregular_relaxation_log_likelihood_kernel(
    standardized_observations: ArrayLike,
    sample_times: ArrayLike,
    relaxation_time: float,
) -> float:
    """Return the tau-dependent exact Gaussian log-likelihood kernel.

    Terms that do not depend on tau, including the stationary N(0, 1) density of
    the first sample in each channel, are omitted. They cancel exactly in every
    likelihood ratio used by the e-value construction.
    """
    times = _validated_times(sample_times)
    values = _validated_observations(standardized_observations, times.size)
    sum_xx, sum_xy, sum_yy = _transition_statistics(values)
    return _log_likelihood_kernel_from_statistics(
        times,
        int(values.shape[1]),
        sum_xx,
        sum_xy,
        sum_yy,
        relaxation_time,
    )


def gaussian_irregular_relaxation_evalue_model(
    standardized_observations: ArrayLike,
    sample_times: ArrayLike,
    *,
    lower_relaxation_time: float,
    upper_relaxation_time: float,
    confidence: float = 0.975,
    mixture_relaxation_time_grid_size: int = 17,
) -> GaussianIrregularRelaxationEValueModel:
    """Build the exact irregular-time e-value model for a physical tau interval.

    Calibration channels must be independent standardized zero-mean Gaussian
    realizations with unit marginal variance, a common exponential relaxation
    time, and the supplied common timestamp grid. Unknown mean handling is not
    included in this theorem.
    """
    times = _validated_times(sample_times)
    lower, upper = _validated_relaxation_interval(
        lower_relaxation_time,
        upper_relaxation_time,
    )
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    values = _validated_observations(standardized_observations, times.size)
    grid_size = _validated_grid_size(
        mixture_relaxation_time_grid_size,
        "mixture_relaxation_time_grid_size",
        degenerate=lower == upper,
    )
    mixture_grid = _parameter_grid(lower, upper, grid_size)
    sum_xx, sum_xy, sum_yy = _transition_statistics(values)
    channel_count = int(values.shape[1])

    component_log_likelihoods = np.asarray(
        [
            _log_likelihood_kernel_from_statistics(
                times,
                channel_count,
                sum_xx,
                sum_xy,
                sum_yy,
                float(tau),
            )
            for tau in mixture_grid
        ],
        dtype=float,
    )
    log_mixture = float(
        logsumexp(component_log_likelihoods) - np.log(component_log_likelihoods.size)
    )

    return GaussianIrregularRelaxationEValueModel(
        sample_times=times.copy(),
        sample_count=int(times.size),
        channel_count=channel_count,
        confidence=float(confidence),
        log_evalue_threshold=float(np.log(1.0 / (1.0 - confidence))),
        declared_relaxation_time_lower_bound=lower,
        declared_relaxation_time_upper_bound=upper,
        mixture_relaxation_time_grid=mixture_grid,
        mixture_point_count=int(mixture_grid.size),
        transition_sum_xx=sum_xx,
        transition_sum_xy=sum_xy,
        transition_sum_yy=sum_yy,
        log_mixture_density_kernel=log_mixture,
    )


def gaussian_irregular_relaxation_log_evalue(
    model: GaussianIrregularRelaxationEValueModel,
    relaxation_time: float,
) -> float:
    """Evaluate log(q / p_tau) at any tau in the declared continuum interval."""
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    tau = float(relaxation_time)
    if not (
        model.declared_relaxation_time_lower_bound
        <= tau
        <= model.declared_relaxation_time_upper_bound
    ):
        raise ValueError("relaxation_time lies outside the declared model")
    log_likelihood = _log_likelihood_kernel_from_statistics(
        model.sample_times,
        model.channel_count,
        model.transition_sum_xx,
        model.transition_sum_xy,
        model.transition_sum_yy,
        tau,
    )
    return float(model.log_mixture_density_kernel - log_likelihood)


def gaussian_irregular_relaxation_evalue_grid(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    relaxation_time_grid_size: int = 201,
) -> GaussianIrregularRelaxationEValueGrid:
    """Evaluate the exact continuum e-value function on a diagnostic grid."""
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    size = _validated_grid_size(
        relaxation_time_grid_size,
        "relaxation_time_grid_size",
        degenerate=(
            model.declared_relaxation_time_lower_bound
            == model.declared_relaxation_time_upper_bound
        ),
    )
    grid = _parameter_grid(
        model.declared_relaxation_time_lower_bound,
        model.declared_relaxation_time_upper_bound,
        size,
    )
    log_evalues = np.asarray(
        [gaussian_irregular_relaxation_log_evalue(model, float(tau)) for tau in grid],
        dtype=float,
    )
    accepted = log_evalues < model.log_evalue_threshold
    accepted_count = int(np.sum(accepted))
    if accepted_count:
        accepted_grid = grid[accepted]
        lower = float(accepted_grid[0])
        upper = float(accepted_grid[-1])
    else:
        lower = np.nan
        upper = np.nan
    return GaussianIrregularRelaxationEValueGrid(
        relaxation_time_grid=grid,
        log_evalues=log_evalues,
        accepted_mask=accepted,
        accepted_point_count=accepted_count,
        total_point_count=int(grid.size),
        accepted_relaxation_time_lower_bound=lower,
        accepted_relaxation_time_upper_bound=upper,
    )


def _alpha_derivative_supremum(distance: float, lower: float, upper: float) -> float:
    candidate = float(np.clip(0.5 * distance, lower, upper))
    return float(distance * np.exp(-distance / candidate) / candidate**2)


def gaussian_irregular_relaxation_log_likelihood_lipschitz_bound(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    lower_relaxation_time: float | None = None,
    upper_relaxation_time: float | None = None,
) -> float:
    """Bound |d log p_tau / d tau| on a declared subinterval.

    The bound is deterministic conditional on the observed calibration record.
    It is used only for geometric containment of the already valid continuum
    e-value confidence set, so it consumes no additional probability budget.
    """
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    lower = (
        model.declared_relaxation_time_lower_bound
        if lower_relaxation_time is None
        else float(lower_relaxation_time)
    )
    upper = (
        model.declared_relaxation_time_upper_bound
        if upper_relaxation_time is None
        else float(upper_relaxation_time)
    )
    if not (
        model.declared_relaxation_time_lower_bound
        <= lower
        <= upper
        <= model.declared_relaxation_time_upper_bound
    ):
        raise ValueError("requested Lipschitz interval lies outside the declared model")

    distances = np.diff(model.sample_times)
    total = 0.0
    for index, distance in enumerate(distances):
        alpha_max = float(np.exp(-distance / upper))
        variance_min = 1.0 - alpha_max * alpha_max
        derivative_supremum = _alpha_derivative_supremum(float(distance), lower, upper)
        sum_xx = float(model.transition_sum_xx[index])
        sum_xy_abs = abs(float(model.transition_sum_xy[index]))
        sum_yy = float(model.transition_sum_yy[index])
        residual_upper = (
            sum_yy
            + 2.0 * alpha_max * sum_xy_abs
            + alpha_max * alpha_max * sum_xx
        )
        first_term = (
            model.channel_count * alpha_max + alpha_max * sum_xx + sum_xy_abs
        ) / variance_min
        second_term = alpha_max * residual_upper / (variance_min * variance_min)
        total += derivative_supremum * (first_term + second_term)
    return float(total)


def gaussian_irregular_relaxation_evalue_outer_cover(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    cell_count: int = 200,
) -> GaussianIrregularRelaxationEValueOuterCover:
    """Certify a finite outer cover of the continuum e-value confidence set.

    Each cell uses a derivative bound computed only over that cell. A cell is
    excluded only when the center log e-value minus the maximum possible
    within-cell decrease still exceeds the rejection threshold everywhere.
    """
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    if model.declared_relaxation_time_lower_bound == model.declared_relaxation_time_upper_bound:
        raise ValueError("outer-cover cells require a nondegenerate relaxation-time interval")
    count = _validated_grid_size(cell_count, "cell_count")
    edges = np.linspace(
        model.declared_relaxation_time_lower_bound,
        model.declared_relaxation_time_upper_bound,
        count + 1,
    )
    centers = 0.5 * (edges[:-1] + edges[1:])
    cell_radius = float(0.5 * (edges[1] - edges[0]))
    log_evalues = np.asarray(
        [gaussian_irregular_relaxation_log_evalue(model, float(tau)) for tau in centers],
        dtype=float,
    )
    cell_lipschitz = np.asarray(
        [
            gaussian_irregular_relaxation_log_likelihood_lipschitz_bound(
                model,
                lower_relaxation_time=float(edges[index]),
                upper_relaxation_time=float(edges[index + 1]),
            )
            for index in range(count)
        ],
        dtype=float,
    )
    lower_log_evalue = log_evalues - cell_lipschitz * cell_radius
    retained = lower_log_evalue < model.log_evalue_threshold
    retained_count = int(np.sum(retained))
    if retained_count:
        retained_indices = np.flatnonzero(retained)
        retained_lower = float(edges[retained_indices[0]])
        retained_upper = float(edges[retained_indices[-1] + 1])
    else:
        retained_lower = np.nan
        retained_upper = np.nan
    return GaussianIrregularRelaxationEValueOuterCover(
        cell_edges=edges,
        cell_centers=centers,
        cell_radius=cell_radius,
        log_evalues_at_centers=log_evalues,
        cell_log_likelihood_lipschitz_bounds=cell_lipschitz,
        log_likelihood_lipschitz_bound=float(np.max(cell_lipschitz)),
        retained_mask=retained,
        retained_cell_count=retained_count,
        excluded_cell_count=int(count - retained_count),
        total_cell_count=count,
        retained_relaxation_time_lower_bound=retained_lower,
        retained_relaxation_time_upper_bound=retained_upper,
    )


def gaussian_irregular_relaxation_target_matrix_chernoff_bound(
    model: GaussianIrregularRelaxationEValueModel,
    target_sample_times: ArrayLike,
    target_nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    outer_cover_cell_count: int = 200,
    covariance_confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianIrregularRelaxationTargetBound:
    """Compose irregular tau calibration with an independent target covariance bound."""
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")
    target_times = _validated_times(target_sample_times)
    design = np.asarray(target_nuisance_design, dtype=float)
    if design.ndim != 2 or design.shape[0] != target_times.size:
        raise ValueError("target_nuisance_design must have one row per target sample time")
    if design.shape[1] < 1 or design.shape[1] >= target_times.size:
        raise ValueError("target_nuisance_design must have rank between one and sample_count-1")
    if not np.all(np.isfinite(design)) or np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("target_nuisance_design must be finite and full column rank")

    outer = gaussian_irregular_relaxation_evalue_outer_cover(
        model,
        cell_count=outer_cover_cell_count,
    )
    if outer.retained_cell_count < 1:
        raise ValueError("the certified calibration outer cover retained no cells")
    retained_centers = outer.cell_centers[outer.retained_mask]
    temporal_grid = np.stack(
        [exponential_relaxation_covariance(target_times, float(tau)) for tau in retained_centers]
    )

    target_lipschitz = exponential_relaxation_operator_lipschitz_bound(
        target_times,
        model.declared_relaxation_time_lower_bound,
        model.declared_relaxation_time_upper_bound,
    )
    eigenvalue_radius = float(target_lipschitz * outer.cell_radius)
    nuisance_rank = int(design.shape[1])
    normalization_radius = float(nuisance_rank * eigenvalue_radius)

    covariance_bound = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension=block_dimension,
        block_count=block_count,
        temporal_covariance_grid=temporal_grid,
        nuisance_design=design,
        eigenvalue_covering_radius=eigenvalue_radius,
        normalization_covering_radius=normalization_radius,
        confidence=covariance_confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )
    return GaussianIrregularRelaxationTargetBound(
        calibration_outer_cover=outer,
        covariance_bound=covariance_bound,
        calibration_confidence=model.confidence,
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(model.confidence * covariance_confidence),
        target_operator_lipschitz_bound=target_lipschitz,
        target_eigenvalue_covering_radius=eigenvalue_radius,
        target_normalization_covering_radius=normalization_radius,
    )
