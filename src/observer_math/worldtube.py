"""Variational inference for observer world-tubes in discrete systems."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatArray = NDArray[np.float64]


@dataclass(frozen=True)
class WorldTubeResult:
    """Maximizing path and its decomposition into local and transition terms."""

    path: tuple[tuple[int, ...], ...]
    candidate_indices: tuple[int, ...]
    total_action: float
    local_score: float
    transport_reward: float
    continuity_cost: float


def jaccard_distance(left: Sequence[int], right: Sequence[int]) -> float:
    """Distance between material memberships, bounded in [0, 1]."""
    left_set, right_set = set(left), set(right)
    union = left_set | right_set
    if not union:
        return 0.0
    return 1.0 - len(left_set & right_set) / len(union)


def structural_transport(
    transition: ArrayLike,
    source: Sequence[int],
    target: Sequence[int],
    *,
    floor: float = 1e-15,
) -> float:
    """Fraction of target transition energy arriving from a source subsystem.

    This is a first classical transport proxy. It is coordinate-dependent and
    will be replaced by a gauge-invariant quantity in the quantum formulation.
    """
    transition = np.asarray(transition, dtype=float)
    source = np.asarray(tuple(source), dtype=int)
    target = np.asarray(tuple(target), dtype=int)
    incoming_from_source = transition[np.ix_(target, source)]
    all_incoming = transition[target, :]
    numerator = float(np.sum(incoming_from_source**2))
    denominator = float(np.sum(all_incoming**2))
    return float(np.clip(numerator / max(denominator, floor), 0.0, 1.0))


def optimize_worldtube(
    local_scores: ArrayLike,
    candidates: Sequence[Sequence[int]],
    *,
    transport_scores: ArrayLike | None = None,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> WorldTubeResult:
    """Maximize a discrete world-tube action by dynamic programming.

    local_scores[t, j] measures observer-like organization for candidate j at
    time t. transport_scores[t, i, j] measures organizational transport from
    candidate i at t to candidate j at t+1. The material continuity penalty
    prevents arbitrary jumps without requiring permanent physical membership.
    """
    local_scores = np.asarray(local_scores, dtype=float)
    candidates = tuple(tuple(candidate) for candidate in candidates)
    if local_scores.ndim != 2:
        raise ValueError("local_scores must have shape (time, candidates)")
    time_count, candidate_count = local_scores.shape
    if time_count < 1 or candidate_count != len(candidates):
        raise ValueError("local_scores and candidates have incompatible shapes")

    if transport_scores is None:
        transport = np.zeros((max(0, time_count - 1), candidate_count, candidate_count))
    else:
        transport = np.asarray(transport_scores, dtype=float)
        expected = (time_count - 1, candidate_count, candidate_count)
        if transport.shape != expected:
            raise ValueError(f"transport_scores must have shape {expected}")

    continuity = np.empty((candidate_count, candidate_count), dtype=float)
    for previous in range(candidate_count):
        for current in range(candidate_count):
            continuity[previous, current] = jaccard_distance(
                candidates[previous], candidates[current]
            )

    value = np.full((time_count, candidate_count), -np.inf)
    parent = np.full((time_count, candidate_count), -1, dtype=int)
    value[0] = local_scores[0]
    for time in range(1, time_count):
        transition_value = (
            value[time - 1, :, None]
            + transport_weight * transport[time - 1]
            - continuity_weight * continuity
        )
        parent[time] = np.argmax(transition_value, axis=0)
        value[time] = local_scores[time] + transition_value[parent[time], np.arange(candidate_count)]

    final = int(np.argmax(value[-1]))
    indices = [final]
    for time in range(time_count - 1, 0, -1):
        indices.append(int(parent[time, indices[-1]]))
    indices.reverse()

    local_total = float(sum(local_scores[t, index] for t, index in enumerate(indices)))
    transport_total = float(
        transport_weight
        * sum(transport[t, indices[t], indices[t + 1]] for t in range(time_count - 1))
    )
    continuity_total = float(
        continuity_weight
        * sum(continuity[indices[t], indices[t + 1]] for t in range(time_count - 1))
    )
    return WorldTubeResult(
        path=tuple(candidates[index] for index in indices),
        candidate_indices=tuple(indices),
        total_action=float(value[-1, final]),
        local_score=local_total,
        transport_reward=transport_total,
        continuity_cost=continuity_total,
    )
