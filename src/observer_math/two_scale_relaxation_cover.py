"""Two-scale target covers after finite-sample irregular-time tau calibration.

Proposition 54 separates the numerical resolution used to certify the calibration
confidence set from the resolution used in the independent target covariance
bound. A fine calibration grid can therefore tighten the retained physical-time
span without forcing Proposition 49 to union over every fine calibration cell.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .compact_temporal_family import (
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from .irregular_relaxation_evalue import (
    GaussianIrregularRelaxationEValueModel,
    GaussianIrregularRelaxationEValueOuterCover,
    gaussian_irregular_relaxation_evalue_outer_cover,
)
from .physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_operator_lipschitz_bound,
)


@dataclass(frozen=True)
class GaussianIrregularRelaxationTwoScaleTargetBound:
    """Certified target bound using distinct calibration and target resolutions."""

    calibration_outer_cover: GaussianIrregularRelaxationEValueOuterCover
    covariance_bound: GaussianCompactTemporalFamilyMatrixChernoffBound
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence: float
    retained_relaxation_time_lower_bound: float
    retained_relaxation_time_upper_bound: float
    retained_relaxation_time_width: float
    target_cover_relaxation_times: np.ndarray
    target_cover_point_count: int
    target_parameter_covering_radius: float
    target_operator_lipschitz_bound: float
    target_eigenvalue_covering_radius: float
    target_normalization_covering_radius: float
    calibration_cell_count: int
    retained_calibration_cell_count: int
    cover_compression_ratio: float


@dataclass(frozen=True)
class GaussianOptimizedIrregularRelaxationTwoScaleTargetBound:
    """Best valid two-scale bound among calibration-only cover-size choices."""

    selected: GaussianIrregularRelaxationTwoScaleTargetBound
    candidate_cover_point_counts: np.ndarray
    candidate_covariance_relative_errors: np.ndarray
    selected_index: int


def _validated_times(sample_times: ArrayLike) -> np.ndarray:
    times = np.asarray(sample_times, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("target_sample_times must be one-dimensional with at least two entries")
    if not np.all(np.isfinite(times)) or not np.all(np.diff(times) > 0.0):
        raise ValueError("target_sample_times must be finite and strictly increasing")
    return times


def _validated_design(nuisance_design: ArrayLike, sample_count: int) -> np.ndarray:
    design = np.asarray(nuisance_design, dtype=float)
    if design.ndim != 2 or design.shape[0] != sample_count:
        raise ValueError("target_nuisance_design must have one row per target sample time")
    if design.shape[1] < 1 or design.shape[1] >= sample_count:
        raise ValueError("target_nuisance_design has an invalid nuisance rank")
    if not np.all(np.isfinite(design)) or np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("target_nuisance_design must be finite and full column rank")
    return design


def _validated_cover_point_count(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, np.integer)):
        raise TypeError("target_cover_point_count must be an integer")
    if value < 2:
        raise ValueError("target_cover_point_count must be at least two")
    return int(value)


def gaussian_irregular_relaxation_two_scale_target_bound(
    model: GaussianIrregularRelaxationEValueModel,
    target_sample_times: ArrayLike,
    target_nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    calibration_outer_cover_cell_count: int = 1600,
    target_cover_point_count: int = 25,
    covariance_confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianIrregularRelaxationTwoScaleTargetBound:
    """Compose a fine calibration certificate with a coarser target cover.

    The e-value theorem remains continuum-valued. The fine calibration cells are
    used only to produce a deterministic outer cover of that continuum set. The
    retained cells are then enclosed by their smallest containing interval
    ``[tau_lower, tau_upper]``. A separate equally spaced target grid covers this
    interval. If its spacing is ``h``, every retained tau lies within ``h / 2``
    of a target representative.

    The target covariance family obeys the operator-Lipschitz bound on the
    retained interval itself, so the Proposition 49 covering radii are
    ``L * h / 2`` for projected eigenvalues and ``q * L * h / 2`` for the
    nuisance-projected normalization.

    The calibration record and target record must be independent. The target
    cover size may be chosen as any deterministic function of calibration data
    because the target concentration statement is conditional on that record.
    """
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    target_times = _validated_times(target_sample_times)
    design = _validated_design(target_nuisance_design, target_times.size)
    cover_count = _validated_cover_point_count(target_cover_point_count)

    outer = gaussian_irregular_relaxation_evalue_outer_cover(
        model,
        cell_count=calibration_outer_cover_cell_count,
    )
    if outer.retained_cell_count < 1:
        raise ValueError("the certified calibration outer cover retained no cells")

    lower = float(outer.retained_relaxation_time_lower_bound)
    upper = float(outer.retained_relaxation_time_upper_bound)
    width = float(upper - lower)
    if not np.isfinite(width) or width <= 0.0:
        raise ValueError("the retained relaxation-time span must be nondegenerate")

    tau_grid = np.linspace(lower, upper, cover_count)
    spacing = width / (cover_count - 1)
    tau_radius = float(0.5 * spacing)
    temporal_grid = np.stack(
        [exponential_relaxation_covariance(target_times, float(tau)) for tau in tau_grid]
    )

    target_lipschitz = exponential_relaxation_operator_lipschitz_bound(
        target_times,
        lower,
        upper,
    )
    eigenvalue_radius = float(target_lipschitz * tau_radius)
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

    compression_ratio = float(outer.retained_cell_count / cover_count)
    return GaussianIrregularRelaxationTwoScaleTargetBound(
        calibration_outer_cover=outer,
        covariance_bound=covariance_bound,
        calibration_confidence=model.confidence,
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(model.confidence * covariance_confidence),
        retained_relaxation_time_lower_bound=lower,
        retained_relaxation_time_upper_bound=upper,
        retained_relaxation_time_width=width,
        target_cover_relaxation_times=tau_grid,
        target_cover_point_count=cover_count,
        target_parameter_covering_radius=tau_radius,
        target_operator_lipschitz_bound=float(target_lipschitz),
        target_eigenvalue_covering_radius=eigenvalue_radius,
        target_normalization_covering_radius=normalization_radius,
        calibration_cell_count=outer.total_cell_count,
        retained_calibration_cell_count=outer.retained_cell_count,
        cover_compression_ratio=compression_ratio,
    )


def gaussian_optimized_irregular_relaxation_two_scale_target_bound(
    model: GaussianIrregularRelaxationEValueModel,
    target_sample_times: ArrayLike,
    target_nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    calibration_outer_cover_cell_count: int = 1600,
    candidate_target_cover_point_counts: Iterable[int] = (5, 7, 9, 13, 17, 25, 33, 49),
    covariance_confidence: float = 0.975,
    upper_theta_grid_size: int = 1024,
    lower_theta_grid_size: int = 1024,
) -> GaussianOptimizedIrregularRelaxationTwoScaleTargetBound:
    """Choose the tightest valid target cover using calibration-side information.

    Every candidate is already a valid conditional Proposition 49 certificate.
    The selection uses only the calibration-derived temporal family and declared
    target timestamps/design, never target observations. Therefore choosing the
    smallest resulting deterministic radius does not spend additional target
    probability budget.
    """
    raw_counts = list(candidate_target_cover_point_counts)
    if not raw_counts:
        raise ValueError("candidate_target_cover_point_counts must be nonempty")
    counts = np.asarray([_validated_cover_point_count(value) for value in raw_counts], dtype=int)
    if np.unique(counts).size != counts.size:
        raise ValueError("candidate_target_cover_point_counts must be unique")

    bounds = [
        gaussian_irregular_relaxation_two_scale_target_bound(
            model,
            target_sample_times,
            target_nuisance_design,
            block_dimension,
            block_count,
            calibration_outer_cover_cell_count=calibration_outer_cover_cell_count,
            target_cover_point_count=int(count),
            covariance_confidence=covariance_confidence,
            upper_theta_grid_size=upper_theta_grid_size,
            lower_theta_grid_size=lower_theta_grid_size,
        )
        for count in counts
    ]
    errors = np.asarray(
        [bound.covariance_bound.covariance_relative_error for bound in bounds],
        dtype=float,
    )
    index = int(np.argmin(errors))
    return GaussianOptimizedIrregularRelaxationTwoScaleTargetBound(
        selected=bounds[index],
        candidate_cover_point_counts=counts,
        candidate_covariance_relative_errors=errors,
        selected_index=index,
    )
