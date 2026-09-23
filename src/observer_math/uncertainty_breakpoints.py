"""P74 computes exact uncertainty breakpoints for affine interval graphs."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np


@dataclass(frozen=True)
class AffineBreakpoint:
    radius: float
    source: str


def positive_affine_crossing(a0: float, a1: float, b0: float, b1: float) -> float | None:
    """Solve a0 + r*a1 = b0 + r*b1 for a positive finite r."""
    denominator = a1 - b1
    if abs(denominator) <= 1e-15:
        return None
    radius = (b0 - a0) / denominator
    if radius <= 0 or not np.isfinite(radius):
        return None
    return float(radius)


def pairwise_affine_breakpoints(intercepts: np.ndarray, slopes: np.ndarray) -> tuple[float, ...]:
    """Return sorted positive crossings among affine functions."""
    a = np.asarray(intercepts, dtype=float).ravel()
    b = np.asarray(slopes, dtype=float).ravel()
    if a.shape != b.shape:
        raise ValueError("intercepts and slopes must have equal shape")
    roots = set()
    for i, j in combinations(range(a.size), 2):
        root = positive_affine_crossing(a[i], b[i], a[j], b[j])
        if root is not None:
            roots.add(root)
    return tuple(sorted(roots))
