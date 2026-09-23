"""P75: exact robust-evidence minimization on a retained layered graph."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class RobustEvidenceDPResult:
    robust_e_value: float
    log_robust_e_value: float
    minimizing_path: tuple[int, ...]


def minimize_factorized_evidence(
    retained_nodes: np.ndarray,
    retained_edges: np.ndarray,
    node_e_factors: np.ndarray,
    edge_e_factors: np.ndarray,
) -> RobustEvidenceDPResult:
    """Minimize a positive factorized path evidence value without path enumeration."""
    nodes = np.asarray(retained_nodes, dtype=bool)
    edges = np.asarray(retained_edges, dtype=bool)
    nf = np.asarray(node_e_factors, dtype=float)
    ef = np.asarray(edge_e_factors, dtype=float)
    if nodes.shape != nf.shape:
        raise ValueError("node arrays must have equal shape")
    t_count, c_count = nodes.shape
    if edges.shape != (t_count - 1, c_count, c_count):
        raise ValueError("retained_edges has incompatible shape")
    if ef.shape != edges.shape:
        raise ValueError("edge arrays must have equal shape")
    if np.any(nf <= 0) or np.any(ef <= 0):
        raise ValueError("evidence factors must be strictly positive")

    cost = np.full((t_count, c_count), np.inf)
    parent = np.full((t_count, c_count), -1, dtype=int)
    cost[0, nodes[0]] = np.log(nf[0, nodes[0]])

    for t in range(1, t_count):
        for j in np.flatnonzero(nodes[t]):
            allowed = np.flatnonzero(nodes[t - 1] & edges[t - 1, :, j])
            if allowed.size == 0:
                continue
            values = cost[t - 1, allowed] + np.log(ef[t - 1, allowed, j])
            k = int(np.argmin(values))
            i = int(allowed[k])
            if np.isfinite(values[k]):
                cost[t, j] = values[k] + np.log(nf[t, j])
                parent[t, j] = i

    j = int(np.argmin(cost[-1]))
    if not np.isfinite(cost[-1, j]):
        raise ValueError("retained graph contains no complete path")
    log_value = float(cost[-1, j])
    path = [j]
    for t in range(t_count - 1, 0, -1):
        j = int(parent[t, j])
        path.append(j)
    path.reverse()
    return RobustEvidenceDPResult(float(np.exp(log_value)), log_value, tuple(path))
