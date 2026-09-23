"""P64 converts score uncertainty into auditable world-tube action intervals."""
from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .path_pruning import ActionInterval


@dataclass(frozen=True)
class PathActionInterval:
    candidate_indices: tuple[int, ...]
    interval: ActionInterval
    nominal_action: float
    uncertainty_radius: float


def path_action_interval(
    candidate_indices: Sequence[int],
    local_scores: ArrayLike,
    local_score_errors: ArrayLike,
    transport_scores: ArrayLike,
    transport_score_errors: ArrayLike,
    continuity_costs: ArrayLike,
    *,
    transport_weight: float,
    continuity_weight: float,
) -> PathActionInterval:
    """Propagate candidate-local score radii to one path action interval."""
    path = tuple(int(i) for i in candidate_indices)
    local = np.asarray(local_scores, dtype=float)
    local_err = np.asarray(local_score_errors, dtype=float)
    transport = np.asarray(transport_scores, dtype=float)
    transport_err = np.asarray(transport_score_errors, dtype=float)
    continuity = np.asarray(continuity_costs, dtype=float)
    time_count, candidate_count = local.shape
    if len(path) != time_count or any(i < 0 or i >= candidate_count for i in path):
        raise ValueError("candidate_indices must define one valid candidate per time")
    if local_err.shape != local.shape:
        raise ValueError("local_score_errors must match local_scores")
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    if transport.shape != edge_shape or transport_err.shape != edge_shape:
        raise ValueError("transport arrays have incompatible shape")
    if continuity.shape != (candidate_count, candidate_count):
        raise ValueError("continuity_costs has incompatible shape")
    nominal = float(sum(local[t, path[t]] for t in range(time_count)))
    nominal += float(transport_weight * sum(transport[t, path[t], path[t + 1]] for t in range(time_count - 1)))
    nominal -= float(continuity_weight * sum(continuity[path[t], path[t + 1]] for t in range(time_count - 1)))
    radius = float(sum(local_err[t, path[t]] for t in range(time_count)))
    radius += float(abs(transport_weight) * sum(transport_err[t, path[t], path[t + 1]] for t in range(time_count - 1)))
    return PathActionInterval(path, ActionInterval(nominal - radius, nominal + radius), nominal, radius)
