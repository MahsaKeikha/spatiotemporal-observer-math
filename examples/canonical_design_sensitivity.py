"""Experiment BI: canonical benchmark precision-design sensitivity.

Uses the same population problem and certificate pipeline as Experiment BD.
The intervention variable is the simultaneous covariance-radius scale assigned
to one candidate-time block at a time. No sensor-cost or hardware claim is made.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from examples.full_benchmark_scalable_certification import population_problem
from observer_math.ambiguity_count import count_retained_paths
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound
from observer_math.score_interval_graph import compress_score_interval_graph

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "canonical_design_sensitivity.json"


def continuity_matrix(candidates):
    out = np.zeros((len(candidates), len(candidates)))
    for i, a in enumerate(candidates):
        for j, b in enumerate(candidates):
            out[i, j] = 1.0 - len(set(a) & set(b)) / len(set(a) | set(b))
    return out


def evaluate(local_factors, transport_factors, candidates, delta_map):
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    errors = np.full(local_scores.shape, 0.0005)
    for (t, j), radius in delta_map.items():
        errors[t, j] = radius
    bridge = relative_covariance_worldtube_recovery_bound(
        local_factors, transport_factors, candidates, 7, 3,
        covariance_relative_errors=errors,
        transport_weight=0.25, continuity_weight=0.08,
    )
    graph = compress_score_interval_graph(
        local_scores, bridge.local_score_errors, transport_scores,
        bridge.transport_score_errors, continuity_matrix(candidates),
        transport_weight=0.25, continuity_weight=0.08,
    )
    return {
        "retained_paths": int(count_retained_paths(graph.retained_nodes, graph.retained_edges).total_paths),
        "retained_nodes": int(np.sum(graph.retained_nodes)),
        "retained_edges": int(np.sum(graph.retained_edges)),
        "unique_recovery": bool(bridge.guarantees_population_path),
    }


def main():
    planted, candidates, local_factors, transport_factors = population_problem()
    baseline = evaluate(local_factors, transport_factors, candidates, {})
    candidate_radii = (0.0002, 0.0001)
    rows = []
    for t in range(len(planted)):
        for j, candidate in enumerate(candidates):
            for radius in candidate_radii:
                out = evaluate(local_factors, transport_factors, candidates, {(t, j): radius})
                rows.append({
                    "time": t,
                    "candidate_index": j,
                    "candidate": list(candidate),
                    "radius": radius,
                    **out,
                })
    best = min(rows, key=lambda r: (r["retained_paths"], r["retained_edges"], r["radius"]))
    record = {
        "experiment": "BI",
        "title": "Canonical moving-module single-block precision sensitivity",
        "baseline_radius": 0.0005,
        "baseline": baseline,
        "candidate_radii": list(candidate_radii),
        "interventions_evaluated": len(rows),
        "best_by_ambiguity_then_edges": best,
        "rows": rows,
        "scientific_boundary": (
            "BI is an in-silico certificate-design audit on the canonical population benchmark. "
            "A candidate-time covariance radius is a mathematical uncertainty block, not a physical "
            "sensor cost. The experiment tests whether localized precision can change the certified "
            "ambiguity graph before any hardware interpretation is made."
        ),
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
