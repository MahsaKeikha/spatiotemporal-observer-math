"""P63 safe path pruning from deterministic action intervals."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass


@dataclass(frozen=True)
class ActionInterval:
    lower: float
    upper: float

    def __post_init__(self) -> None:
        if self.lower > self.upper:
            raise ValueError("lower action bound cannot exceed upper bound")


@dataclass(frozen=True)
class PruningResult:
    retained: tuple[str, ...]
    pruned: tuple[str, ...]
    best_certified_lower_bound: float


def prune_inadmissible_paths(intervals: Mapping[str, ActionInterval], *, tolerance: float = 0.0) -> PruningResult:
    """Safely remove paths whose upper bound cannot approach the best lower bound."""
    if not intervals:
        raise ValueError("at least one path interval is required")
    if tolerance < 0:
        raise ValueError("tolerance must be nonnegative")
    best_lower = max(v.lower for v in intervals.values())
    threshold = best_lower - tolerance
    retained = tuple(k for k, v in intervals.items() if v.upper >= threshold)
    pruned = tuple(k for k, v in intervals.items() if v.upper < threshold)
    return PruningResult(retained, pruned, best_lower)
