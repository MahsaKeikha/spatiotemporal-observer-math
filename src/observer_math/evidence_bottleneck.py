"""P76: localize the factors responsible for a limiting robust-evidence path."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class EvidenceBottleneck:
    kind: str
    time: int
    source: int
    target: int | None
    log_contribution: float
    factor: float


def localize_path_evidence_bottlenecks(
    path: tuple[int, ...],
    node_e_factors: np.ndarray,
    edge_e_factors: np.ndarray,
) -> tuple[EvidenceBottleneck, ...]:
    """Rank multiplicative path factors by their log contribution, weakest first."""
    nf = np.asarray(node_e_factors, dtype=float)
    ef = np.asarray(edge_e_factors, dtype=float)
    if len(path) != nf.shape[0]:
        raise ValueError("path length must match node time dimension")
    if np.any(nf <= 0) or np.any(ef <= 0):
        raise ValueError("evidence factors must be strictly positive")
    items: list[EvidenceBottleneck] = []
    for t, j in enumerate(path):
        value = float(nf[t, j])
        items.append(EvidenceBottleneck("node", t, j, None, float(np.log(value)), value))
        if t + 1 < len(path):
            k = path[t + 1]
            value = float(ef[t, j, k])
            items.append(EvidenceBottleneck("edge", t, j, k, float(np.log(value)), value))
    return tuple(sorted(items, key=lambda item: item.log_contribution))


def required_single_factor_multiplier(
    current_robust_e_value: float,
    threshold: float,
) -> float:
    """Minimum multiplicative increase if exactly one binding factor is changed."""
    if current_robust_e_value <= 0 or threshold <= 0:
        raise ValueError("values must be positive")
    return max(1.0, float(threshold / current_robust_e_value))
