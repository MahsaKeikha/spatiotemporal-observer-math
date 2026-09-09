"""Second-order certification for irregular-time relaxation calibration.

This module sharpens Proposition 53B without changing its finite-sample e-value
coverage statement. The exact irregular-time log likelihood is differentiated
analytically in the physical relaxation time. A deterministic cell-local bound
on its second derivative then gives a Taylor upper bound for the likelihood,
which yields a tighter certified outer cover of the continuum confidence set.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .compact_temporal_family import (
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from .irregular_relaxation_evalue import (
    GaussianIrregularRelaxationEValueModel,
    gaussian_irregular_relaxation_log_evalue,
)
from .physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_operator_lipschitz_bound,
)


@dataclass(frozen=True)
class GaussianIrregularRelaxationSecondOrderOuterCover:
    """Certified outer cover using a cell-local second-order likelihood bound."""

    cell_edges: np.ndarray
    cell_centers: np.ndarray
    cell_radius: float
    log_evalues_at_centers: np.ndarray
    log_likelihood_derivatives_at_centers: np.ndarray
    cell_log_likelihood_second_derivative_bounds: np.ndarray
    cell_log_evalue_lower_bounds: np.ndarray
    retained_mask: np.ndarray
    retained_cell_count: int
    excluded_cell_count: int
    total_cell_count: int
    retained_relaxation_time_lower_bound: float
    retained_relaxation_time_upper_bound: float


@dataclass(frozen=True)
class GaussianIrregularRelaxationSecondOrderTargetBound:
    """Independent target covariance certificate after second-order tau calibration."""

    calibration_outer_cover: GaussianIrregularRelaxationSecondOrderOuterCover
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence: float
    target_operator_lipschitz_bound: float
    target_eigenvalue_covering_radius: float
    target_normalization_covering_radius: float


def _validated_model(model: GaussianIrregularRelaxationEValueModel) -> None:
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")


def _validated_interval(
    model: GaussianIrregularRelaxationEValueModel,
    lower_relaxation_time: float | None,
    upper_relaxation_time: float | None,
) -> tuple[float, float]:
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
        raise ValueError("requested interval lies outside the declared model")
    return lower, upper


def _validated_cell_count(cell_count: int) -> int:
    if isinstance(cell_count, bool) or not isinstance(cell_count, (int, np.integer)):
        raise TypeError("cell_count must be an integer")
    if cell_count < 2:
        raise ValueError("cell_count must be at least 2")
    return int(cell_count)


def _alpha_first_derivative_supremum(distance: float, lower: float, upper: float) -> float:
    """Return sup |d exp(-distance/tau) / d tau| on an interval."""
    x_lower = distance / upper
    x_upper = distance / lower
    candidates = [x_lower, x_upper]
    if x_lower <= 2.0 <= x_upper:
        candidates.append(2.0)
    return float(max(x * x * np.exp(-x) / distance for x in candidates))


def _alpha_second_derivative_supremum(distance: float, lower: float, upper: float) -> float:
    """Return sup |d^2 exp(-distance/tau) / d tau^2| on an interval."""
    x_lower = distance / upper
    x_upper = distance / lower
    candidates = [x_lower, x_upper]
    for stationary in (3.0 - np.sqrt(3.0), 3.0 + np.sqrt(3.0)):
        if x_lower <= stationary <= x_upper:
            candidates.append(float(stationary))
    values = [np.exp(-x) * x**3 * abs(x - 2.0) / distance**2 for x in candidates]
    return float(max(values))


def gaussian_irregular_relaxation_log_likelihood_derivative(
    model: GaussianIrregularRelaxationEValueModel,
    relaxation_time: float,
) -> float:
    """Evaluate the exact first derivative of the log likelihood kernel in tau."""
    _validated_model(model)
    tau = float(relaxation_time)
    if not (
        model.declared_relaxation_time_lower_bound
        <= tau
        <= model.declared_relaxation_time_upper_bound
    ):
        raise ValueError("relaxation_time lies outside the declared model")

    distance = np.diff(model.sample_times)
    alpha = np.exp(-distance / tau)
    denominator = (1.0 - alpha * alpha) ** 2
    sum_xx = model.transition_sum_xx
    sum_xy = model.transition_sum_xy
    sum_yy = model.transition_sum_yy
    m = float(model.channel_count)

    derivative_alpha = (
        -sum_xx * alpha
        + sum_xy * alpha * alpha
        + sum_xy
        - sum_yy * alpha
        - m * alpha**3
        + m * alpha
    ) / denominator
    alpha_tau_derivative = alpha * distance / tau**2
    return float(np.sum(derivative_alpha * alpha_tau_derivative))


def gaussian_irregular_relaxation_log_likelihood_second_derivative_bound(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    lower_relaxation_time: float | None = None,
    upper_relaxation_time: float | None = None,
) -> float:
    """Bound the absolute second tau derivative of the exact log likelihood.

    The bound is deterministic conditional on the observed calibration record.
    It follows from the exact first and second derivatives with respect to each
    local transition coefficient alpha_i, followed by the chain rule in tau.
    """
    _validated_model(model)
    lower, upper = _validated_interval(
        model,
        lower_relaxation_time,
        upper_relaxation_time,
    )

    total = 0.0
    distances = np.diff(model.sample_times)
    for index, distance_value in enumerate(distances):
        distance = float(distance_value)
        alpha_min = float(np.exp(-distance / lower))
        alpha_max = float(np.exp(-distance / upper))
        variance_min = 1.0 - alpha_max * alpha_max

        sum_xx = float(model.transition_sum_xx[index])
        sum_xy_abs = abs(float(model.transition_sum_xy[index]))
        sum_yy = float(model.transition_sum_yy[index])
        m = float(model.channel_count)

        alpha_one_minus_alpha_squared_sup = max(
            alpha_min * (1.0 - alpha_min * alpha_min),
            alpha_max * (1.0 - alpha_max * alpha_max),
            2.0 / (3.0 * np.sqrt(3.0))
            if alpha_min <= 1.0 / np.sqrt(3.0) <= alpha_max
            else 0.0,
        )

        first_alpha_derivative_bound = (
            sum_xx * alpha_max
            + sum_xy_abs * (alpha_max * alpha_max + 1.0)
            + sum_yy * alpha_max
            + m * alpha_one_minus_alpha_squared_sup
        ) / variance_min**2

        second_alpha_derivative_bound = (
            sum_xx * (3.0 * alpha_max * alpha_max + 1.0)
            + 2.0 * sum_xy_abs * (alpha_max**3 + 3.0 * alpha_max)
            + sum_yy * (3.0 * alpha_max * alpha_max + 1.0)
            + m * (1.0 - alpha_min**4)
        ) / variance_min**3

        alpha_first_bound = _alpha_first_derivative_supremum(distance, lower, upper)
        alpha_second_bound = _alpha_second_derivative_supremum(distance, lower, upper)
        total += (
            second_alpha_derivative_bound * alpha_first_bound**2
            + first_alpha_derivative_bound * alpha_second_bound
        )

    return float(total)


def gaussian_irregular_relaxation_second_order_outer_cover(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    cell_count: int = 200,
) -> GaussianIrregularRelaxationSecondOrderOuterCover:
    """Certify a second-order finite outer cover of the continuum e-value set.

    Taylor's theorem gives, for every tau in a cell centered at c with radius r,

        ell(tau) <= ell(c) + |ell'(c)| r + 0.5 M r^2,

    where M bounds |ell''| on that cell. Therefore log e_tau is bounded below
    by the corresponding center log e-value minus those two terms. A cell is
    excluded only when this deterministic lower bound reaches the rejection
    threshold everywhere in the cell.
    """
    _validated_model(model)
    if model.declared_relaxation_time_lower_bound == model.declared_relaxation_time_upper_bound:
        raise ValueError("outer-cover cells require a nondegenerate relaxation-time interval")
    count = _validated_cell_count(cell_count)
    edges = np.linspace(
        model.declared_relaxation_time_lower_bound,
        model.declared_relaxation_time_upper_bound,
        count + 1,
    )
    centers = 0.5 * (edges[:-1] + edges[1:])
    cell_radius = float(0.5 * (edges[1] - edges[0]))

    center_log_evalues = np.asarray(
        [gaussian_irregular_relaxation_log_evalue(model, float(tau)) for tau in centers],
        dtype=float,
    )
    center_derivatives = np.asarray(
        [
            gaussian_irregular_relaxation_log_likelihood_derivative(model, float(tau))
            for tau in centers
        ],
        dtype=float,
    )
    curvature_bounds = np.asarray(
        [
            gaussian_irregular_relaxation_log_likelihood_second_derivative_bound(
                model,
                lower_relaxation_time=float(edges[index]),
                upper_relaxation_time=float(edges[index + 1]),
            )
            for index in range(count)
        ],
        dtype=float,
    )
    lower_log_evalues = (
        center_log_evalues
        - np.abs(center_derivatives) * cell_radius
        - 0.5 * curvature_bounds * cell_radius**2
    )
    retained = lower_log_evalues < model.log_evalue_threshold
    retained_count = int(np.sum(retained))
    if retained_count:
        retained_indices = np.flatnonzero(retained)
        retained_lower = float(edges[retained_indices[0]])
        retained_upper = float(edges[retained_indices[-1] + 1])
    else:
        retained_lower = np.nan
        retained_upper = np.nan

    return GaussianIrregularRelaxationSecondOrderOuterCover(
        cell_edges=edges,
        cell_centers=centers,
        cell_radius=cell_radius,
        log_evalues_at_centers=center_log_evalues,
        log_likelihood_derivatives_at_centers=center_derivatives,
        cell_log_likelihood_second_derivative_bounds=curvature_bounds,
        cell_log_evalue_lower_bounds=lower_log_evalues,
        retained_mask=retained,
        retained_cell_count=retained_count,
        excluded_cell_count=int(count - retained_count),
        total_cell_count=count,
        retained_relaxation_time_lower_bound=retained_lower,
        retained_relaxation_time_upper_bound=retained_upper,
    )


def gaussian_irregular_relaxation_second_order_target_matrix_chernoff_bound(
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
) -> GaussianIrregularRelaxationSecondOrderTargetBound:
    """Compose the second-order tau cover with an independent target bound."""
    _validated_model(model)
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    target_times = np.asarray(target_sample_times, dtype=float)
    if target_times.ndim != 1 or target_times.size < 2:
        raise ValueError("target_sample_times must be one-dimensional with at least two entries")
    if not np.all(np.isfinite(target_times)) or not np.all(np.diff(target_times) > 0.0):
        raise ValueError("target_sample_times must be finite and strictly increasing")

    design = np.asarray(target_nuisance_design, dtype=float)
    if design.ndim != 2 or design.shape[0] != target_times.size:
        raise ValueError("target_nuisance_design must have one row per target sample time")
    if design.shape[1] < 1 or design.shape[1] >= target_times.size:
        raise ValueError("target_nuisance_design must have rank between one and sample_count-1")
    if not np.all(np.isfinite(design)) or np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("target_nuisance_design must be finite and full column rank")

    outer = gaussian_irregular_relaxation_second_order_outer_cover(
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
        outer.retained_relaxation_time_lower_bound,
        outer.retained_relaxation_time_upper_bound,
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
    return GaussianIrregularRelaxationSecondOrderTargetBound(
        calibration_outer_cover=outer,
        covariance_bound=covariance_bound,
        calibration_confidence=model.confidence,
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(model.confidence * covariance_confidence),
        target_operator_lipschitz_bound=target_lipschitz,
        target_eigenvalue_covering_radius=eigenvalue_radius,
        target_normalization_covering_radius=normalization_radius,
    )
