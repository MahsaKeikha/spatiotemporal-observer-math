"""P68 composes finite-sample retained boundary sets with robust downstream evidence."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .finite_sample_boundary import FiniteSampleBoundaryPoint
from .robust_boundary_evidence import robust_e_value


@dataclass(frozen=True)
class FiniteSampleEvidencePoint:
    residual_count: int
    covariance_radius: float
    retained_count: int | None
    robust_e_value: float | None
    crosses_threshold: bool | None


def boundary_point_to_evidence(
    point: FiniteSampleBoundaryPoint,
    e_values: Mapping[str, float],
    *,
    threshold: float,
) -> FiniteSampleEvidencePoint:
    """Carry one P67 boundary record into the P62/P66 robust evidence envelope."""
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    if not point.perturbative_regime or point.retained_count is None:
        return FiniteSampleEvidencePoint(
            point.residual_count, point.covariance_radius, None, None, None
        )
    value = robust_e_value(e_values, point.retained_paths)
    return FiniteSampleEvidencePoint(
        point.residual_count,
        point.covariance_radius,
        point.retained_count,
        value,
        value >= threshold,
    )
