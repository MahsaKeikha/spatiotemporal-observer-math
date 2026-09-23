"""Certified graph compression without enumerating world-tube paths."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GraphCompression:
    best_lower_action: float
    node_upper_max_marginals: np.ndarray
    edge_upper_max_marginals: np.ndarray
    retained_nodes: np.ndarray
    retained_edges: np.ndarray


def certified_graph_compression(
    node_lower: np.ndarray,
    node_upper: np.ndarray,
    edge_lower: np.ndarray,
    edge_upper: np.ndarray,
    *,
    tolerance: float = 0.0,
) -> GraphCompression:
    """Safely prune nodes/edges that cannot occur on an eta-near-optimal path."""
    nl = np.asarray(node_lower, dtype=float)
    nu = np.asarray(node_upper, dtype=float)
    el = np.asarray(edge_lower, dtype=float)
    eu = np.asarray(edge_upper, dtype=float)
    if nl.shape != nu.shape or nl.ndim != 2:
        raise ValueError("node arrays must have equal (T,C) shape")
    t_count, c_count = nl.shape
    if el.shape != (t_count - 1, c_count, c_count) or eu.shape != el.shape:
        raise ValueError("edge arrays must have shape (T-1,C,C)")
    if tolerance < 0:
        raise ValueError("tolerance must be nonnegative")
    if np.any(nl > nu) or np.any(el > eu):
        raise ValueError("lower endpoints cannot exceed upper endpoints")

    lower_forward = np.empty_like(nl)
    lower_forward[0] = nl[0]
    for t in range(1, t_count):
        lower_forward[t] = nl[t] + np.max(
            lower_forward[t - 1][:, None] + el[t - 1], axis=0
        )
    best_lower = float(np.max(lower_forward[-1]))

    upper_forward = np.empty_like(nu)
    upper_forward[0] = nu[0]
    for t in range(1, t_count):
        upper_forward[t] = nu[t] + np.max(
            upper_forward[t - 1][:, None] + eu[t - 1], axis=0
        )

    upper_backward = np.empty_like(nu)
    upper_backward[-1] = nu[-1]
    for t in range(t_count - 2, -1, -1):
        upper_backward[t] = nu[t] + np.max(
            eu[t] + upper_backward[t + 1][None, :], axis=1
        )

    node_mm = upper_forward + upper_backward - nu
    edge_mm = np.empty_like(eu)
    for t in range(t_count - 1):
        edge_mm[t] = (
            upper_forward[t][:, None]
            + eu[t]
            + upper_backward[t + 1][None, :]
        )
    cutoff = best_lower - tolerance
    return GraphCompression(
        best_lower,
        node_mm,
        edge_mm,
        node_mm >= cutoff,
        edge_mm >= cutoff,
    )
