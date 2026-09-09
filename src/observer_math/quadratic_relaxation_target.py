"""Target covariance propagation after Proposition 55 quadratic calibration."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .compact_temporal_family import (
    GaussianCompactTemporalFamilyMatrixChernoffBound,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from .irregular_relaxation_evalue import GaussianIrregularRelaxationEValueModel
from .physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_operator_lipschitz_bound,
)
from .relaxation_curvature import (
    GaussianIrregularRelaxationQuadraticOuterCover,
    gaussian_irregular_relaxation_quadratic_outer_cover,
)


@dataclass(frozen=True)
class GaussianIrregularRelaxationQuadraticTargetBound:
    """Independent target certificate after quadratic tau calibration."""

    calibration_outer_cover: GaussianIrregularRelaxationQuadraticOuterCover
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


def _validated_times(values: ArrayLike) -> np.ndarray:
    times = np.asarray(values, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("target_sample_times must be one-dimensional with at least two entries")
    if not np.all(np.isfinite(times)) or not np.all(np.diff(times) > 0.0):
        raise ValueError("target_sample_times must be finite and strictly increasing")
    return times


def _validated_design(values: ArrayLike, sample_count: int) -> np.ndarray:
    design = np.asarray(values, dtype=float)
    if design.ndim != 2 or design.shape[0] != sample_count:
        raise ValueError("target_nuisance_design must have one row per target sample time")
    if design.shape[1] < 1 or design.shape[1] >= sample_count:
        raise ValueError("target_nuisance_design has an invalid nuisance rank")
    if not np.all(np.isfinite(design)) or np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("target_nuisance_design must be finite and full column rank")
    return design


def gaussian_irregular_relaxation_quadratic_target_bound(
    model: GaussianIrregularRelaxationEValueModel,
    target_sample_times: ArrayLike,
    target_nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    calibration_cell_count: int = 160,
    target_cover_point_count: int = 25,
    covariance_confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianIrregularRelaxationQuadraticTargetBound:
    """Propagate the quadratic calibration cover to an independent target record."""
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")
    if isinstance(target_cover_point_count, bool) or not isinstance(
        target_cover_point_count, (int, np.integer)
    ):
        raise TypeError("target_cover_point_count must be an integer")
    if target_cover_point_count < 2:
        raise ValueError("target_cover_point_count must be at least two")

    target_times = _validated_times(target_sample_times)
    design = _validated_design(target_nuisance_design, target_times.size)
    outer = gaussian_irregular_relaxation_quadratic_outer_cover(
        model,
        cell_count=calibration_cell_count,
    )
    if outer.retained_cell_count < 1:
        raise ValueError("the quadratic calibration outer cover retained no cells")

    lower = float(outer.retained_relaxation_time_lower_bound)
    upper = float(outer.retained_relaxation_time_upper_bound)
    width = float(upper - lower)
    if not np.isfinite(width) or width <= 0.0:
        raise ValueError("the retained relaxation-time span must be nondegenerate")

    cover_count = int(target_cover_point_count)
    tau_grid = np.linspace(lower, upper, cover_count)
    tau_radius = float(width / (2.0 * (cover_count - 1)))
    target_lipschitz = exponential_relaxation_operator_lipschitz_bound(
        target_times,
        lower,
        upper,
    )
    eigenvalue_radius = float(target_lipschitz * tau_radius)
    normalization_radius = float(design.shape[1] * eigenvalue_radius)
    temporal_grid = np.stack(
        [exponential_relaxation_covariance(target_times, float(tau)) for tau in tau_grid]
    )

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

    return GaussianIrregularRelaxationQuadraticTargetBound(
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
    )
