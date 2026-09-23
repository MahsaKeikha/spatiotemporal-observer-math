"""Experiment BC: graph compression versus explicit path enumeration."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.graph_pruning import certified_graph_compression

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "certified_graph_compression_audit.json"

def main() -> None:
    t_count, c_count = 8, 12
    node_nominal = np.full((t_count, c_count), 0.25)
    node_nominal[:, 0] = 1.0
    node_radius = np.full_like(node_nominal, 0.08)
    edge_nominal = np.zeros((t_count - 1, c_count, c_count))
    edge_nominal[:, 0, 0] = 0.20
    edge_radius = np.full_like(edge_nominal, 0.04)
    result = certified_graph_compression(node_nominal - node_radius, node_nominal + node_radius, edge_nominal - edge_radius, edge_nominal + edge_radius)
    retained_nodes = int(np.sum(result.retained_nodes))
    retained_edges = int(np.sum(result.retained_edges))
    record = {"experiment": "BC", "title": "Polynomial-time certified graph compression", "time_layers": t_count, "candidates_per_layer": c_count, "explicit_path_count": int(c_count**t_count), "best_certified_lower_action": result.best_lower_action, "total_nodes": int(t_count * c_count), "retained_nodes": retained_nodes, "total_edges": int((t_count - 1) * c_count * c_count), "retained_edges": retained_edges, "node_compression_fraction": 1.0 - retained_nodes / (t_count * c_count), "edge_compression_fraction": 1.0 - retained_edges / ((t_count - 1) * c_count * c_count), "algorithmic_complexity": "O(T*C^2)", "scientific_boundary": "BC is a controlled interval-graph scalability audit. It demonstrates certified graph compression without enumerating paths; it is not a timing benchmark or a sensor-data experiment."}
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()
