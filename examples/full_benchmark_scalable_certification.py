"""Experiment BD: scalable certification on the full 7-node moving-module benchmark."""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

from observer_math import (
    adjacent_joint_covariance,
    moving_module_systems,
    observer_metrics_from_covariances,
    propagate_covariances,
    transport_metrics,
)
from observer_math.gaussian import stationary_covariance
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound
from observer_math.score_interval_graph import compress_score_interval_graph

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "full_benchmark_scalable_certification.json"
FIGURE = ROOT / "docs" / "full_benchmark_scalable_certification.svg"

def population_problem():
    node_count = 7
    planted, systems = moving_module_systems(node_count=node_count)
    candidates = tuple(combinations(range(node_count), 3))
    covariances = propagate_covariances(
        [system[0] for system in systems[:-1]],
        [system[1] for system in systems[:-1]],
        stationary_covariance(*systems[0]),
    )
    local_factors = np.zeros((len(systems), len(candidates), 3))
    transport_factors = np.zeros((len(systems) - 1, len(candidates), len(candidates), 2))
    for t, (transition, noise) in enumerate(systems):
        joint = adjacent_joint_covariance(covariances[t], transition, noise)
        for j, candidate in enumerate(candidates):
            m = observer_metrics_from_covariances(covariances[t], joint, candidate)
            local_factors[t, j] = (m.integration_strength, m.independence, m.persistence)
    for t in range(len(systems) - 1):
        transition, noise = systems[t]
        for i, source in enumerate(candidates):
            for j, target in enumerate(candidates):
                m = transport_metrics(covariances[t], transition, noise, source, target)
                transport_factors[t, i, j] = (m.independence, m.persistence)
    return planted, candidates, local_factors, transport_factors

def render_figure(rows) -> None:
    import matplotlib.pyplot as plt

    x = np.array([row["covariance_relative_radius"] for row in rows])
    node_fraction = np.array([
        row["retained_nodes"] / row["total_nodes"] for row in rows
    ])
    edge_fraction = np.array([
        row["retained_edges"] / row["total_edges"] for row in rows
    ])
    order = np.argsort(x)
    figure, axis = plt.subplots(figsize=(7.4, 4.8))
    axis.plot(x[order], node_fraction[order], marker="o", label="Retained nodes")
    axis.plot(x[order], edge_fraction[order], marker="s", label="Retained edges")
    axis.set_xscale("log")
    axis.set_xlabel("Simultaneous relative covariance radius")
    axis.set_ylabel("Retained fraction")
    axis.set_ylim(-0.03, 1.03)
    axis.set_title("Certified ambiguity in the full moving-module graph")
    axis.grid(alpha=0.25)
    axis.legend()
    figure.tight_layout()
    figure.savefig(FIGURE)
    plt.close(figure)


def main() -> None:
    planted, candidates, local_factors, transport_factors = population_problem()
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    continuity = np.zeros((len(candidates), len(candidates)))
    for i, a in enumerate(candidates):
        for j, b in enumerate(candidates):
            continuity[i, j] = 1.0 - len(set(a) & set(b)) / len(set(a) | set(b))
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
        rows.append({
            "covariance_relative_radius": delta,
            "retained_nodes": int(np.sum(graph.retained_nodes)),
            "total_nodes": int(graph.retained_nodes.size),
            "retained_edges": int(np.sum(graph.retained_edges)),
            "total_edges": int(graph.retained_edges.size),
            "p58_unique_recovery_certified": bool(bridge.guarantees_population_path),
            "p58_recovery_slack": float(bridge.recovery_slack),
        })
    record = {
        "experiment": "BD",
        "title": "Full moving-module scalable certification",
        "node_count": 7, "subset_size": 3, "time_layers": len(planted),
        "candidates_per_layer": len(candidates),
        "implicit_path_count": int(len(candidates) ** len(planted)),
        "planted_path": [list(x) for x in planted],
        "rows": rows,
        "scientific_boundary": "BD uses the population moving-module benchmark and declared simultaneous relative covariance radii. It audits P58 to P70 to P69 scalability; the radii are not asserted to arise from a particular raw sensor sample count.",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    render_figure(rows)
    print(json.dumps(record, indent=2))
    print("Figure:", FIGURE)

if __name__ == "__main__":
    main()
