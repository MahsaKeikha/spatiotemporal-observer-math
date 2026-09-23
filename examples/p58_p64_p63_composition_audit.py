"""Experiment AY: actual P58 covariance radii propagated through P64 and P63."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.action_intervals import path_action_interval
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound
from observer_math.path_pruning import prune_inadmissible_paths

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "p58_p64_p63_composition_audit.json"


def controlled_factors():
    candidates = ((0, 1), (1, 2))
    local = np.array([
        [[0.72, 0.94, 0.82], [0.18, 0.88, 0.45]],
        [[0.70, 0.93, 0.80], [0.16, 0.86, 0.42]],
        [[0.68, 0.92, 0.78], [0.15, 0.85, 0.40]],
    ], dtype=float)
    transport = np.full((2, 2, 2, 2), 0.20, dtype=float)
    transport[:, 0, 0] = (0.94, 0.86)
    transport[:, 1, 1] = (0.75, 0.52)
    transport[:, 0, 1] = (0.50, 0.35)
    transport[:, 1, 0] = (0.48, 0.32)
    return local, transport, candidates


def main() -> None:
    local_factors, transport_factors, candidates = controlled_factors()
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    continuity = np.zeros((2, 2))
    paths = {"W000": (0, 0, 0), "W001": (0, 0, 1), "W011": (0, 1, 1), "W111": (1, 1, 1)}
    rows = []
    for delta in (0.08, 0.04, 0.02, 0.01, 0.005, 0.001):
        bridge = relative_covariance_worldtube_recovery_bound(
            local_factors, transport_factors, candidates,
            node_count=3, subset_size=2,
            covariance_relative_errors=np.full((3, 2), delta),
            transport_weight=0.25, continuity_weight=0.0,
        )
        intervals = {}
        for name, path in paths.items():
            out = path_action_interval(
                path, local_scores, bridge.local_score_errors,
                transport_scores, bridge.transport_score_errors, continuity,
                transport_weight=0.25, continuity_weight=0.0,
            )
            intervals[name] = out.interval
        pruning = prune_inadmissible_paths(intervals)
        rows.append({
            "relative_covariance_radius": delta,
            "max_local_score_radius": float(np.max(bridge.local_score_errors)),
            "max_transport_score_radius": float(np.max(bridge.transport_score_errors)),
            "retained_paths": list(pruning.retained),
            "retained_count": len(pruning.retained),
            "compression_fraction": len(pruning.pruned) / len(paths),
            "p58_population_recovery_certified": bridge.guarantees_population_path,
            "p58_recovery_slack": bridge.recovery_slack,
        })
    record = {
        "experiment": "AY",
        "title": "P58 to P64 to P63 composition audit",
        "rows": rows,
        "scientific_boundary": "This is a controlled factor benchmark driven by actual P58 relative-covariance perturbation formulas. The swept covariance radii are declared inputs, not sample-size or sensor-performance claims.",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
