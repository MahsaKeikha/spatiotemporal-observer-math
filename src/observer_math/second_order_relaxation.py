"""Second-order calibration geometry and reference whitening for physical time.

Proposition 54 strengthens Proposition 53B in two places. First, it certifies
continuum e-value cells with a second-derivative interpolation remainder instead
of a first-derivative Lipschitz remainder. Second, it uses the exact Proposition
53A innovation whitener at a calibration-derived reference relaxation time and
certifies the residual target temporal family with a local Taylor cover.

The calibration record and target record remain independent. The reference
relaxation time and every retained target cover cell are functions of calibration
data only, so target concentration can be conditioned on the complete calibration
record.
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
    exponential_relaxation_markov_factorization,
)


@dataclass(frozen=True)
class GaussianIrregularRelaxationSecondOrderOuterCover:
    """Certified cell cover using endpoint interpolation and curvature bounds."""

    cell_edges: np.ndarray
    cell_centers: np.ndarray
    cell_radius: float
    log_evalues_at_left_edges: np.ndarray
    log_evalues_at_right_edges: np.ndarray
    cell_log_likelihood_second_derivative_bounds: np.ndarray
    cell_interpolation_error_bounds: np.ndarray
    retained_mask: np.ndarray
    retained_cell_count: int
    excluded_cell_count: int
    total_cell_count: int
    retained_relaxation_time_lower_bound: float
    retained_relaxation_time_upper_bound: float
    maximum_log_likelihood_second_derivative_bound: float
    maximum_interpolation_error_bound: float


@dataclass(frozen=True)
class GaussianReferenceWhitenedRelaxationTargetBound:
    """Independent target covariance bound after calibrated reference whitening."""

    calibration_outer_cover: GaussianIrregularRelaxationSecondOrderOuterCover
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence: float
    reference_relaxation_time: float
    reference_whitening_matrix: np.ndarray
    transformed_nuisance_design: np.ndarray
    temporal_covering_radius: float
    normalization_covering_radius: float
    maximum_center_temporal_derivative_norm: float
    maximum_temporal_second_derivative_bound: float
    maximum_center_normalization_derivative: float
    maximum_normalization_second_derivative_bound: float


def _validated_subinterval(
    model: GaussianIrregularRelaxationEValueModel,
    lower_relaxation_time: float | None,
    upper_relaxation_time: float | None,
) -> tuple[float, float]:
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
        raise ValueError("requested interval lies outside the declared calibration model")
    return lower, upper


def _alpha_derivative_supremum(distance: float, lower: float, upper: float) -> float:
    candidate = float(np.clip(0.5 * distance, lower, upper))
    return float(distance * np.exp(-distance / candidate) / candidate**2)


def _alpha_second_derivative_supremum(
    distance: float,
    lower: float,
    upper: float,
) -> float:
    if distance <= 0.0:
        return 0.0
    lower_x = distance / upper
    upper_x = distance / lower
    candidates = [lower_x, upper_x]
    for value in (2.0, 3.0 - np.sqrt(3.0), 3.0 + np.sqrt(3.0)):
        if lower_x <= value <= upper_x:
            candidates.append(float(value))
    return float(
        max(
            np.exp(-value) * value**3 * abs(value - 2.0) / distance**2
            for value in candidates
        )
    )


def _transition_log_likelihood_derivatives_in_alpha(
    channel_count: int,
    sum_xx: float,
    sum_xy: float,
    sum_yy: float,
    alpha: float,
) -> tuple[float, float]:
    variance = 1.0 - alpha * alpha
    residual = sum_yy - 2.0 * alpha * sum_xy + alpha * alpha * sum_xx
    numerator = alpha * (channel_count - sum_xx) + sum_xy
    first = numerator / variance - alpha * residual / variance**2
    second = (
        (channel_count - sum_xx) / variance
        + 2.0 * alpha * numerator / variance**2
        - (
            residual
            + 2.0 * alpha * (alpha * sum_xx - sum_xy)
        )
        / variance**2
        - 4.0 * alpha * alpha * residual / variance**3
    )
    return float(first), float(second)


def gaussian_irregular_relaxation_log_likelihood_second_derivative(
    model: GaussianIrregularRelaxationEValueModel,
    relaxation_time: float,
) -> float:
    """Evaluate the exact second derivative of the calibration log likelihood."""
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    tau = float(relaxation_time)
    if not (
        model.declared_relaxation_time_lower_bound
        <= tau
        <= model.declared_relaxation_time_upper_bound
    ):
        raise ValueError("relaxation_time lies outside the declared calibration model")

    total = 0.0
    for index, distance in enumerate(np.diff(model.sample_times)):
        alpha = float(np.exp(-distance / tau))
        first_alpha, second_alpha = _transition_log_likelihood_derivatives_in_alpha(
            model.channel_count,
            float(model.transition_sum_xx[index]),
            float(model.transition_sum_xy[index]),
            float(model.transition_sum_yy[index]),
            alpha,
        )
        first_tau = float(distance * alpha / tau**2)
        second_tau = float(
            alpha * distance / tau**3 * (distance / tau - 2.0)
        )
        total += second_alpha * first_tau**2 + first_alpha * second_tau
    return float(total)


def gaussian_irregular_relaxation_log_likelihood_second_derivative_bound(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    lower_relaxation_time: float | None = None,
    upper_relaxation_time: float | None = None,
) -> float:
    """Bound the absolute second derivative on a declared tau subinterval.

    The bound is deterministic conditional on the observed calibration record.
    It uses exact suprema of the first two derivatives of
    ``alpha(tau)=exp(-distance/tau)`` and data-dependent bounds on the first two
    alpha derivatives of each local Gaussian innovation likelihood term.
    """
    lower, upper = _validated_subinterval(
        model,
        lower_relaxation_time,
        upper_relaxation_time,
    )

    total = 0.0
    for index, distance in enumerate(np.diff(model.sample_times)):
        alpha_max = float(np.exp(-distance / upper))
        variance_min = 1.0 - alpha_max * alpha_max
        sum_xx = float(model.transition_sum_xx[index])
        sum_xy_abs = abs(float(model.transition_sum_xy[index]))
        sum_yy = float(model.transition_sum_yy[index])

        residual_upper = (
            sum_yy
            + 2.0 * alpha_max * sum_xy_abs
            + alpha_max * alpha_max * sum_xx
        )
        numerator_upper = (
            alpha_max * abs(model.channel_count - sum_xx) + sum_xy_abs
        )
        first_alpha_bound = (
            numerator_upper / variance_min
            + alpha_max * residual_upper / variance_min**2
        )
        residual_derivative_bound = 2.0 * (
            alpha_max * sum_xx + sum_xy_abs
        )
        second_alpha_bound = (
            abs(model.channel_count - sum_xx) / variance_min
            + 2.0 * alpha_max * numerator_upper / variance_min**2
            + (
                residual_upper
                + alpha_max * residual_derivative_bound
            )
            / variance_min**2
            + 4.0 * alpha_max**2 * residual_upper / variance_min**3
        )

        first_tau_bound = _alpha_derivative_supremum(
            float(distance),
            lower,
            upper,
        )
        second_tau_bound = _alpha_second_derivative_supremum(
            float(distance),
            lower,
            upper,
        )
        total += (
            second_alpha_bound * first_tau_bound**2
            + first_alpha_bound * second_tau_bound
        )
    return float(total)


def gaussian_irregular_relaxation_second_order_outer_cover(
    model: GaussianIrregularRelaxationEValueModel,
    *,
    cell_count: int = 200,
) -> GaussianIrregularRelaxationSecondOrderOuterCover:
    """Certify an outer cover of the continuum e-value confidence set.

    On each cell ``[a,b]``, let ``f(tau)=log e_tau``. Linear interpolation of
    the two endpoint values has the standard remainder

        |f(tau)-L(tau)| <= M (b-a)^2 / 8,

    whenever ``|f''| <= M`` on the cell. Since ``f''=-ell''``, the likelihood
    curvature bound above applies directly. A cell is excluded only when the
    endpoint interpolation lower bound is at least the e-value threshold.
    """
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    if (
        model.declared_relaxation_time_lower_bound
        == model.declared_relaxation_time_upper_bound
    ):
        raise ValueError("second-order cover requires a nondegenerate interval")
    if isinstance(cell_count, bool) or not isinstance(cell_count, (int, np.integer)):
        raise TypeError("cell_count must be an integer")
    if cell_count < 2:
        raise ValueError("cell_count must be at least two")

    edges = np.linspace(
        model.declared_relaxation_time_lower_bound,
        model.declared_relaxation_time_upper_bound,
        int(cell_count) + 1,
    )
    centers = 0.5 * (edges[:-1] + edges[1:])
    width = float(edges[1] - edges[0])
    radius = 0.5 * width
    edge_log_evalues = np.asarray(
        [gaussian_irregular_relaxation_log_evalue(model, float(tau)) for tau in edges],
        dtype=float,
    )
    second_bounds = np.asarray(
        [
            gaussian_irregular_relaxation_log_likelihood_second_derivative_bound(
                model,
                lower_relaxation_time=float(edges[index]),
                upper_relaxation_time=float(edges[index + 1]),
            )
            for index in range(int(cell_count))
        ],
        dtype=float,
    )
    interpolation_error = second_bounds * width * width / 8.0
    lower_log_evalue = (
        np.minimum(edge_log_evalues[:-1], edge_log_evalues[1:])
        - interpolation_error
    )
    retained = lower_log_evalue < model.log_evalue_threshold
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
        cell_radius=float(radius),
        log_evalues_at_left_edges=edge_log_evalues[:-1],
        log_evalues_at_right_edges=edge_log_evalues[1:],
        cell_log_likelihood_second_derivative_bounds=second_bounds,
        cell_interpolation_error_bounds=interpolation_error,
        retained_mask=retained,
        retained_cell_count=retained_count,
        excluded_cell_count=int(cell_count - retained_count),
        total_cell_count=int(cell_count),
        retained_relaxation_time_lower_bound=retained_lower,
        retained_relaxation_time_upper_bound=retained_upper,
        maximum_log_likelihood_second_derivative_bound=float(np.max(second_bounds)),
        maximum_interpolation_error_bound=float(np.max(interpolation_error)),
    )


def _validated_target_inputs(
    target_sample_times: ArrayLike,
    target_nuisance_design: ArrayLike,
) -> tuple[np.ndarray, np.ndarray]:
    times = np.asarray(target_sample_times, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("target_sample_times must contain at least two entries")
    if not np.all(np.isfinite(times)) or not np.all(np.diff(times) > 0.0):
        raise ValueError("target_sample_times must be finite and strictly increasing")

    design = np.asarray(target_nuisance_design, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] != times.size:
        raise ValueError("target_nuisance_design must have one row per target sample")
    if design.shape[1] < 1 or design.shape[1] >= times.size:
        raise ValueError("target nuisance rank must lie between one and sample_count-1")
    if not np.all(np.isfinite(design)):
        raise ValueError("target_nuisance_design must be finite")
    if np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("target_nuisance_design must have full column rank")
    return times, design


def _exponential_covariance_derivative(
    sample_times: np.ndarray,
    relaxation_time: float,
) -> np.ndarray:
    distances = np.abs(sample_times[:, None] - sample_times[None, :])
    derivative = np.zeros_like(distances)
    positive = distances > 0.0
    derivative[positive] = (
        distances[positive]
        * np.exp(-distances[positive] / relaxation_time)
        / relaxation_time**2
    )
    return derivative


def _exponential_covariance_second_derivative_suprema(
    sample_times: np.ndarray,
    lower_relaxation_time: float,
    upper_relaxation_time: float,
) -> np.ndarray:
    distances = np.abs(sample_times[:, None] - sample_times[None, :])
    bounds = np.zeros_like(distances)
    for row in range(sample_times.size):
        for column in range(sample_times.size):
            bounds[row, column] = _alpha_second_derivative_supremum(
                float(distances[row, column]),
                lower_relaxation_time,
                upper_relaxation_time,
            )
    return bounds


def _nuisance_projector(design: np.ndarray) -> np.ndarray:
    basis, _ = np.linalg.qr(design, mode="complete")
    complement = basis[:, design.shape[1] :]
    return complement @ complement.T


def gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound(
    model: GaussianIrregularRelaxationEValueModel,
    target_sample_times: ArrayLike,
    target_nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    outer_cover_cell_count: int = 200,
    covariance_confidence: float = 0.975,
    reference_relaxation_time: float | None = None,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianReferenceWhitenedRelaxationTargetBound:
    """Compose second-order tau calibration with reference-whitened target data.

    The target record must be independent of the calibration record. A reference
    ``tau_ref`` is chosen from the calibration outer cover before target data are
    inspected. The exact Proposition 53A whitener ``W_ref`` is then fixed and the
    target nuisance design becomes ``W_ref H``.

    For every retained calibration cell, the transformed temporal family

        S_tau = W_ref K_tau W_ref.T

    is covered around the cell center by an exact first derivative plus a
    deterministic second-order remainder. The projected normalization receives a
    separate scalar Taylor certificate. These two radii satisfy Proposition 49's
    cover assumptions and therefore yield a uniform target covariance bound.
    """
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")
    times, design = _validated_target_inputs(
        target_sample_times,
        target_nuisance_design,
    )
    outer = gaussian_irregular_relaxation_second_order_outer_cover(
        model,
        cell_count=outer_cover_cell_count,
    )
    if outer.retained_cell_count < 1:
        raise ValueError("the second-order calibration cover retained no cells")

    if reference_relaxation_time is None:
        reference_tau = 0.5 * (
            outer.retained_relaxation_time_lower_bound
            + outer.retained_relaxation_time_upper_bound
        )
    else:
        reference_tau = float(reference_relaxation_time)
        if not (
            outer.retained_relaxation_time_lower_bound
            <= reference_tau
            <= outer.retained_relaxation_time_upper_bound
        ):
            raise ValueError("reference_relaxation_time must lie inside retained extremes")

    factorization = exponential_relaxation_markov_factorization(times, reference_tau)
    whitening = factorization.whitening_matrix
    transformed_design = whitening @ design
    projector = _nuisance_projector(transformed_design)
    normalization_kernel = whitening.T @ projector @ whitening
    abs_whitening = np.abs(whitening)

    temporal_cover = []
    temporal_radii = []
    normalization_radii = []
    first_derivative_norms = []
    temporal_second_bounds = []
    normalization_first_derivatives = []
    normalization_second_bounds = []

    retained_indices = np.flatnonzero(outer.retained_mask)
    for index in retained_indices:
        lower = float(outer.cell_edges[index])
        upper = float(outer.cell_edges[index + 1])
        center = float(outer.cell_centers[index])
        radius = 0.5 * (upper - lower)

        covariance = exponential_relaxation_covariance(times, center)
        transformed_covariance = whitening @ covariance @ whitening.T
        transformed_covariance = 0.5 * (
            transformed_covariance + transformed_covariance.T
        )
        temporal_cover.append(transformed_covariance)

        covariance_derivative = _exponential_covariance_derivative(times, center)
        transformed_derivative = whitening @ covariance_derivative @ whitening.T
        transformed_derivative = 0.5 * (
            transformed_derivative + transformed_derivative.T
        )
        first_norm = float(np.linalg.norm(transformed_derivative, ord=2))

        second_entry_bounds = _exponential_covariance_second_derivative_suprema(
            times,
            lower,
            upper,
        )
        transformed_second_entry_bounds = (
            abs_whitening @ second_entry_bounds @ abs_whitening.T
        )
        second_operator_bound = float(
            np.max(np.sum(transformed_second_entry_bounds, axis=1))
        )
        temporal_radius = float(
            radius * first_norm
            + 0.5 * radius * radius * second_operator_bound
        )

        normalization_first = abs(
            float(np.sum(normalization_kernel * covariance_derivative))
        )
        normalization_second = float(
            np.sum(np.abs(normalization_kernel) * second_entry_bounds)
        )
        normalization_radius = float(
            radius * normalization_first
            + 0.5 * radius * radius * normalization_second
        )

        temporal_radii.append(temporal_radius)
        normalization_radii.append(normalization_radius)
        first_derivative_norms.append(first_norm)
        temporal_second_bounds.append(second_operator_bound)
        normalization_first_derivatives.append(normalization_first)
        normalization_second_bounds.append(normalization_second)

    eigenvalue_radius = float(max(temporal_radii))
    normalization_radius = float(max(normalization_radii))
    covariance_bound = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension=block_dimension,
        block_count=block_count,
        temporal_covariance_grid=np.asarray(temporal_cover),
        nuisance_design=transformed_design,
        eigenvalue_covering_radius=eigenvalue_radius,
        normalization_covering_radius=normalization_radius,
        confidence=covariance_confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )

    return GaussianReferenceWhitenedRelaxationTargetBound(
        calibration_outer_cover=outer,
        covariance_bound=covariance_bound,
        calibration_confidence=float(model.confidence),
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(model.confidence * covariance_confidence),
        reference_relaxation_time=float(reference_tau),
        reference_whitening_matrix=whitening,
        transformed_nuisance_design=transformed_design,
        temporal_covering_radius=eigenvalue_radius,
        normalization_covering_radius=normalization_radius,
        maximum_center_temporal_derivative_norm=float(max(first_derivative_norms)),
        maximum_temporal_second_derivative_bound=float(max(temporal_second_bounds)),
        maximum_center_normalization_derivative=float(
            max(normalization_first_derivatives)
        ),
        maximum_normalization_second_derivative_bound=float(
            max(normalization_second_bounds)
        ),
    )
