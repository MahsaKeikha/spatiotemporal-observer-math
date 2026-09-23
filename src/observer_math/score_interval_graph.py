"""P70 maps P58 score radii directly to a layered interval graph."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .graph_pruning import GraphCompression, certified_graph_compression


@dataclass(frozen=True)
class ScoreIntervalGraph:
    node_lower: np.ndarray
    node_upper: np.ndarray
    edge_lower: np.ndarray
    edge_upper: np.ndarray


def score_intervals_to_graph(
    local_scores: np.ndarray,
    local_errors: np.ndarray,
    transport_scores: np.ndarray,
    transport_errors: np.ndarray,
    continuity_costs: np.ndarray,
    *,
    transport_weight: float,
    continuity_weight: float,
) -> ScoreIntervalGraph:
    local = np.asarray(local_scores, dtype=float)
    le = np.asarray(local_errors, dtype=float)
    trans = np.asarray(transport_scores, dtype=float)
    te = np.asarray(transport_errors, dtype=float)
    cont = np.asarray(continuity_costs, dtype=float)
    if local.shape != le.shape or local.ndim != 2:
        raise ValueError("local score and error arrays must share (T,C) shape")
    t_count, c_count = local.shape
    if trans.shape != (t_count - 1, c_count, c_count) or te.shape != trans.shape:
        raise ValueError("transport arrays must have shape (T-1,C,C)")
    if cont.shape != (c_count, c_count):
        raise ValueError("continuity_costs must have shape (C,C)")
    if np.any(le < 0) or np.any(te < 0):
        raise ValueError("score errors must be nonnegative")

    node_lower = local - le
    node_upper = local + le
    edge_nominal = transport_weight * trans - continuity_weight * cont[None, :, :]
    edge_radius = abs(transport_weight) * te
    return ScoreIntervalGraph(
        node_lower,
        node_upper,
        edge_nominal - edge_radius,
        edge_nominal + edge_radius,
    )


def compress_score_interval_graph(
    local_scores: np.ndarray,
    local_errors: np.ndarray,
    transport_scores: np.ndarray,
    transport_errors: np.ndarray,
    continuity_costs: np.ndarray,
    *,
    transport_weight: float,
    continuity_weight: float,
    tolerance: float = 0.0,
) -> GraphCompression:
    graph = score_intervals_to_graph(
        local_scores, local_errors, transport_scores, transport_errors,
        continuity_costs, transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return certified_graph_compression(
        graph.node_lower, graph.node_upper, graph.edge_lower, graph.edge_upper,
        tolerance=tolerance,
    )
