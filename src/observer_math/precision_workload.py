"""P65 precision-to-ambiguity engineering diagnostics."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from .path_pruning import ActionInterval, prune_inadmissible_paths


@dataclass(frozen=True)
class PrecisionWorkloadPoint:
    precision_scale: float
    retained_count: int
    pruned_count: int
    compression_fraction: float
    retained_paths: tuple[str, ...]


def scale_action_intervals(
    nominal_actions: Mapping[str, float],
    base_radii: Mapping[str, float],
    precision_scale: float,
) -> dict[str, ActionInterval]:
    """Construct intervals when all certified radii scale by a declared factor."""
    if precision_scale < 0:
        raise ValueError("precision_scale must be nonnegative")
    if nominal_actions.keys() != base_radii.keys():
        raise ValueError("nominal_actions and base_radii must have identical keys")
    return {
        key: ActionInterval(value - precision_scale * base_radii[key], value + precision_scale * base_radii[key])
        for key, value in nominal_actions.items()
    }


def precision_workload_curve(
    nominal_actions: Mapping[str, float],
    base_radii: Mapping[str, float],
    precision_scales: tuple[float, ...],
    *,
    tolerance: float = 0.0,
) -> tuple[PrecisionWorkloadPoint, ...]:
    """Map measurement-radius scale to certified downstream path workload."""
    points = []
    total = len(nominal_actions)
    if total == 0:
        raise ValueError("at least one path is required")
    for scale in precision_scales:
        intervals = scale_action_intervals(nominal_actions, base_radii, scale)
        out = prune_inadmissible_paths(intervals, tolerance=tolerance)
        points.append(
            PrecisionWorkloadPoint(
                precision_scale=scale,
                retained_count=len(out.retained),
                pruned_count=len(out.pruned),
                compression_fraction=len(out.pruned) / total,
                retained_paths=out.retained,
            )
        )
    return tuple(points)
