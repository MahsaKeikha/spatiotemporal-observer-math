"""Experiment BE: count residual complete world-tubes after certified graph compression."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from examples.full_benchmark_scalable_certification import population_problem
from observer_math.ambiguity_count import count_retained_paths
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound
from observer_math.score_interval_graph import compress_score_interval_graph

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "certified_ambiguity_path_count.json"


def main() -> None:
    planted, candidates, local_factors, transport_factors = population_problem()
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    continuity = np.zeros((len(candidates), len(candidates)))
    for i, a in enumerate(candidates):
        for j, b in enumerate(candidates):
            continuity[i, j] = 1.0 - len(set(a) & set(b)) / len(set(a) | set(b))
    full_count = len(candidates) ** len(planted)
    rows = []
    for delta in (0.05, 0.02, 0.01, 0.005, 0.001, 0.0005, 0.0002, 0.0001):
        bridge = relative_covariance_worldtube_recovery_bound(
            local_factors, transport_factors, candidates, 7, 3,
            covariance_relative_errors=np.full(local_scores.shape, delta),
            transport_weight=0.25, continuity_weight=0.08,
        )
        graph = compress_score_interval_graph(
            local_scores, bridge.local_score_errors, transport_scores,
            bridge.transport_score_errors, continuity,
            transport_weight=0.25, continuity_weight=0.08,
        )
        count = count_retained_paths(graph.retained_nodes, graph.retained_edges)
        rows.append({
            "covariance_relative_radius": delta,
            "retained_path_count": count.total_paths,
            "full_path_count": full_count,
            "retained_path_fraction": count.total_paths / full_count,
            "retained_nodes": int(np.sum(graph.retained_nodes)),
            "retained_edges": int(np.sum(graph.retained_edges)),
            "p58_unique_recovery_certified": bool(bridge.guarantees_population_path),
        })
    record = {
        "experiment": "BE",
        "title": "Certified residual world-tube ambiguity count",
        "implicit_full_path_count": full_count,
        "rows": rows,
        "scientific_boundary": "Retained path counts quantify graph-certified ambiguity. They are counts, not probabilities or posterior mass.",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
