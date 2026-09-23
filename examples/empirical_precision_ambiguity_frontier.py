"""Experiment BG: empirical precision-ambiguity-workload Pareto frontier."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from examples.full_benchmark_scalable_certification import population_problem
from observer_math.ambiguity_count import count_retained_paths
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound
from observer_math.research_tradeoff import ResearchTradeoffPoint, pareto_frontier
from observer_math.score_interval_graph import compress_score_interval_graph

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "empirical_precision_ambiguity_frontier.json"

def main() -> None:
    planted, candidates, local_factors, transport_factors = population_problem()
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    continuity = np.zeros((len(candidates), len(candidates)))
    for i, a in enumerate(candidates):
        for j, b in enumerate(candidates):
            continuity[i, j] = 1.0 - len(set(a) & set(b)) / len(set(a) | set(b))
    points, records = [], []
    for delta in (0.05, 0.02, 0.01, 0.005, 0.001, 0.0005, 0.0002, 0.0001):
        bridge = relative_covariance_worldtube_recovery_bound(local_factors, transport_factors, candidates, 7, 3, covariance_relative_errors=np.full(local_scores.shape, delta), transport_weight=0.25, continuity_weight=0.08)
        graph = compress_score_interval_graph(local_scores, bridge.local_score_errors, transport_scores, bridge.transport_score_errors, continuity, transport_weight=0.25, continuity_weight=0.08)
        ambiguity = count_retained_paths(graph.retained_nodes, graph.retained_edges)
        workload = int(np.sum(graph.retained_edges))
        point = ResearchTradeoffPoint(delta, ambiguity.total_paths, 1.0, workload)
        points.append(point)
        records.append({"covariance_relative_radius": delta, "retained_path_count": ambiguity.total_paths, "retained_edge_workload": workload, "p58_unique_recovery_certified": bool(bridge.guarantees_population_path)})
    frontier = pareto_frontier(tuple(points))
    frontier_keys = {(p.precision_radius, p.retained_path_count, p.graph_workload) for p in frontier}
    for row in records:
        row["pareto_nondominated"] = (row["covariance_relative_radius"], row["retained_path_count"], row["retained_edge_workload"]) in frontier_keys
    record = {"experiment": "BG", "title": "Empirical precision-ambiguity-workload Pareto frontier", "benchmark": {"n": 7, "s": 3, "T": len(planted), "C": len(candidates)}, "evidence_coordinate": "held constant at 1.0 to isolate physical geometry", "rows": records, "scientific_boundary": "The frontier is descriptive and uses declared covariance radii. It does not assign utility weights, probabilities to paths, or application preferences."}
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()
