"""P67 finite-sample covariance radius to boundary workload composition."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .action_intervals import path_action_interval
from .matrix_chernoff import gaussian_weighted_wishart_matrix_bound
from .observer_bridge import relative_covariance_worldtube_recovery_bound
from .path_pruning import prune_inadmissible_paths


@dataclass(frozen=True)
class FiniteSampleBoundaryPoint:
    residual_count: int
    covariance_radius: float
    perturbative_regime: bool
    retained_count: int | None
    retained_paths: tuple[str, ...]
    recovery_certified: bool


def iid_unit_weights(residual_count: int) -> np.ndarray:
    if residual_count <= 0:
        raise ValueError("residual_count must be positive")
    return np.ones(residual_count, dtype=float)


def finite_sample_boundary_point(
    residual_count: int,
    *,
    block_dimension: int,
    block_count: int,
    confidence: float,
    local_factors: np.ndarray,
    transport_factors: np.ndarray,
    candidates: tuple[tuple[int, ...], ...],
    paths: dict[str, tuple[int, ...]],
    node_count: int,
    subset_size: int,
    transport_weight: float,
) -> FiniteSampleBoundaryPoint:
    bound = gaussian_weighted_wishart_matrix_bound(
        block_dimension,
        block_count,
        iid_unit_weights(residual_count),
        confidence=confidence,
    )
    delta = float(bound.relative_covariance_error)
    if delta >= 1.0:
        return FiniteSampleBoundaryPoint(residual_count, delta, False, None, (), False)

    bridge = relative_covariance_worldtube_recovery_bound(
        local_factors,
        transport_factors,
        candidates,
        node_count=node_count,
        subset_size=subset_size,
        covariance_relative_errors=np.full(local_factors.shape[:2], delta),
        transport_weight=transport_weight,
        continuity_weight=0.0,
    )
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    continuity = np.zeros((len(candidates), len(candidates)))
    intervals = {}
    for name, path in paths.items():
        intervals[name] = path_action_interval(
            path,
            local_scores,
            bridge.local_score_errors,
            transport_scores,
            bridge.transport_score_errors,
            continuity,
            transport_weight=transport_weight,
            continuity_weight=0.0,
        ).interval
    pruning = prune_inadmissible_paths(intervals)
    return FiniteSampleBoundaryPoint(
        residual_count,
        delta,
        True,
        len(pruning.retained),
        pruning.retained,
        bridge.guarantees_population_path,
    )
