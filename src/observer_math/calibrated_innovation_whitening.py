"""Calibrated innovation-whitened covariance confidence tubes.

Proposition 57 combines the finite-sample relaxation-time outer cover from
Proposition 55 with the exact known-tau innovation-whitened covariance theorem
from Proposition 56. Rather than forcing one estimated relaxation time into the
target analysis, it keeps every relaxation time not excluded by calibration and
associates each candidate with its corresponding exact innovation-whitened
covariance confidence ball.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .innovation_whitening import separable_gaussian_innovation_whitened_covariance
from .irregular_relaxation_evalue import GaussianIrregularRelaxationEValueModel
from .matrix_chernoff import (
    GaussianWeightedWishartMatrixBound,
    gaussian_weighted_wishart_matrix_bound,
)
from .relaxation_curvature import (
    GaussianIrregularRelaxationQuadraticOuterCover,
    gaussian_irregular_relaxation_quadratic_outer_cover,
)


@dataclass(frozen=True)
class GaussianCalibratedInnovationConfidenceTube:
    """Finite-sample confidence tube over relaxation time and spatial covariance."""

    calibration_outer_cover: GaussianIrregularRelaxationQuadraticOuterCover
    calibration_confidence: float
    covariance_confidence: float
    combined_confidence: float
    sample_count: int
    nuisance_rank: int
    residual_degrees_of_freedom: int
    block_dimension: int
    block_count: int
    covariance_bound: GaussianWeightedWishartMatrixBound

    @property
    def covariance_relative_error(self) -> float:
        """Return the common Proposition 56 relative covariance radius."""
        return self.covariance_bound.relative_covariance_error

    @property
    def retained_relaxation_time_lower_bound(self) -> float:
        """Return the lower endpoint of the retained calibration hull."""
        return self.calibration_outer_cover.retained_relaxation_time_lower_bound

    @property
    def retained_relaxation_time_upper_bound(self) -> float:
        """Return the upper endpoint of the retained calibration hull."""
        return self.calibration_outer_cover.retained_relaxation_time_upper_bound


def _validated_times(values: ArrayLike) -> np.ndarray:
    times = np.asarray(values, dtype=float)
    if times.ndim != 1 or times.size < 2:
        raise ValueError("sample_times must be one-dimensional with at least two entries")
    if not np.all(np.isfinite(times)) or not np.all(np.diff(times) > 0.0):
        raise ValueError("sample_times must be finite and strictly increasing")
    return times


def _validated_design(values: ArrayLike, sample_count: int) -> np.ndarray:
    design = np.asarray(values, dtype=float)
    if design.ndim == 1:
        design = design[:, None]
    if design.ndim != 2 or design.shape[0] != sample_count:
        raise ValueError("nuisance_design must have one row per sample time")
    if design.shape[1] < 1 or design.shape[1] >= sample_count:
        raise ValueError("nuisance_design must have rank between one and sample_count-1")
    if not np.all(np.isfinite(design)) or np.linalg.matrix_rank(design) != design.shape[1]:
        raise ValueError("nuisance_design must be finite and full column rank")
    return design


def gaussian_calibrated_innovation_confidence_tube(
    model: GaussianIrregularRelaxationEValueModel,
    target_sample_times: ArrayLike,
    target_nuisance_design: ArrayLike,
    block_dimension: int,
    block_count: int,
    *,
    calibration_cell_count: int = 160,
    covariance_confidence: float = 0.975,
    upper_theta_grid_size: int = 4096,
    lower_theta_grid_size: int = 4096,
) -> GaussianCalibratedInnovationConfidenceTube:
    """Compose calibrated tau uncertainty with exact candidate-wise whitening.

    Let ``O`` be the Proposition 55 deterministic outer cover of the continuum
    e-value confidence set. For every candidate ``tau`` in ``O``, define the
    Proposition 56 covariance estimator obtained by whitening the target record
    with ``W_tau`` and residualizing the transformed nuisance design.

    The target covariance radius is the same for every candidate tau because,
    if that candidate is the true physical relaxation time, exact whitening
    leaves ``N-q`` unit-weight Gaussian residual coordinates. The resulting
    confidence object is therefore a tube indexed by the calibrated tau set,
    not one covariance ball around a plug-in relaxation-time estimate.

    If calibration and target records are independent, the true pair
    ``(tau_*, Gamma_*)`` belongs to this tube with probability at least
    ``calibration_confidence * covariance_confidence``. No multiplicity penalty
    over candidate tau values is required: the proof invokes the target event
    only at the single true tau_*, while the calibration event guarantees that
    tau_* lies in the retained outer cover.
    """
    if not isinstance(model, GaussianIrregularRelaxationEValueModel):
        raise TypeError("model has the wrong type")
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")

    times = _validated_times(target_sample_times)
    design = _validated_design(target_nuisance_design, times.size)
    outer = gaussian_irregular_relaxation_quadratic_outer_cover(
        model,
        cell_count=calibration_cell_count,
    )
    if outer.retained_cell_count < 1:
        raise ValueError("the calibrated relaxation-time outer cover retained no cells")

    residual_degrees = int(times.size - design.shape[1])
    covariance_bound = gaussian_weighted_wishart_matrix_bound(
        block_dimension,
        block_count,
        np.ones(residual_degrees, dtype=float),
        confidence=covariance_confidence,
        upper_theta_grid_size=upper_theta_grid_size,
        lower_theta_grid_size=lower_theta_grid_size,
    )

    return GaussianCalibratedInnovationConfidenceTube(
        calibration_outer_cover=outer,
        calibration_confidence=float(model.confidence),
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(model.confidence * covariance_confidence),
        sample_count=int(times.size),
        nuisance_rank=int(design.shape[1]),
        residual_degrees_of_freedom=residual_degrees,
        block_dimension=int(block_dimension),
        block_count=int(block_count),
        covariance_bound=covariance_bound,
    )


def innovation_whitened_covariance_path(
    values: ArrayLike,
    sample_times: ArrayLike,
    nuisance_design: ArrayLike,
    relaxation_times: ArrayLike,
) -> np.ndarray:
    """Evaluate the Proposition 56 covariance center along candidate tau values."""
    times = _validated_times(sample_times)
    design = _validated_design(nuisance_design, times.size)
    candidates = np.asarray(relaxation_times, dtype=float)
    if candidates.ndim != 1 or candidates.size < 1:
        raise ValueError("relaxation_times must contain at least one candidate")
    if not np.all(np.isfinite(candidates)) or np.any(candidates <= 0.0):
        raise ValueError("relaxation_times must be finite and positive")

    estimates = [
        separable_gaussian_innovation_whitened_covariance(
            values,
            times,
            design,
            float(tau),
        )
        for tau in candidates
    ]
    return np.stack(estimates)


def scalar_relative_covariance_interval(
    covariance_estimate: float,
    relative_radius: float,
) -> tuple[float, float]:
    """Convert a scalar relative covariance ball to an explicit variance interval."""
    estimate = float(covariance_estimate)
    radius = float(relative_radius)
    if not np.isfinite(estimate) or estimate <= 0.0:
        raise ValueError("covariance_estimate must be finite and positive")
    if not np.isfinite(radius) or not 0.0 <= radius < 1.0:
        raise ValueError("relative_radius must lie in [0, 1)")
    return estimate / (1.0 + radius), estimate / (1.0 - radius)
