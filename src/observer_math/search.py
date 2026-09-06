"""Exhaustive subsystem search for small research examples."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from numpy.typing import ArrayLike

from .metrics import ObserverMetrics, observer_metrics


@dataclass(frozen=True)
class Candidate:
    rank: int
    metrics: ObserverMetrics


def rank_subsystems(
    transition: ArrayLike,
    noise_covariance: ArrayLike,
    *,
    min_size: int = 2,
    max_size: int | None = None,
    lag: int = 1,
) -> list[Candidate]:
    """Rank all candidate subsets. Intended for small systems only."""
    node_count = len(transition)
    max_size = node_count - 1 if max_size is None else max_size
    if min_size < 2 or max_size >= node_count or min_size > max_size:
        raise ValueError("require 2 <= min_size <= max_size < node_count")
    results = []
    for size in range(min_size, max_size + 1):
        for subset in combinations(range(node_count), size):
            results.append(
                observer_metrics(transition, noise_covariance, subset, lag=lag)
            )
    ordered = sorted(results, key=lambda item: item.observer_score, reverse=True)
    return [Candidate(rank=index + 1, metrics=value) for index, value in enumerate(ordered)]
