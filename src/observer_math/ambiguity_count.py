"""Count complete paths in a certified retained layered graph without enumeration."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CertifiedPathCount:
    total_paths: int
    forward_counts: tuple[tuple[int, ...], ...]


def count_retained_paths(
    retained_nodes: np.ndarray,
    retained_edges: np.ndarray,
) -> CertifiedPathCount:
    """Count paths using only retained nodes and retained transitions."""
    nodes = np.asarray(retained_nodes, dtype=bool)
    edges = np.asarray(retained_edges, dtype=bool)
    if nodes.ndim != 2:
        raise ValueError("retained_nodes must have shape (T,C)")
    t_count, c_count = nodes.shape
    if edges.shape != (t_count - 1, c_count, c_count):
        raise ValueError("retained_edges must have shape (T-1,C,C)")

    counts = [[0 for _ in range(c_count)] for _ in range(t_count)]
    for j in range(c_count):
        counts[0][j] = int(nodes[0, j])
    for t in range(1, t_count):
        for j in range(c_count):
            if not nodes[t, j]:
                continue
            counts[t][j] = sum(
                counts[t - 1][i]
                for i in range(c_count)
                if nodes[t - 1, i] and edges[t - 1, i, j]
            )
    frozen = tuple(tuple(row) for row in counts)
    return CertifiedPathCount(sum(frozen[-1]), frozen)
