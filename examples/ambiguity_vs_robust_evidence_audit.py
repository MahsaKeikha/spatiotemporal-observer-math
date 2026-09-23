"""Experiment BF: ambiguity reduction versus robust-evidence bottleneck."""
from __future__ import annotations

import json
from pathlib import Path

from observer_math.ambiguity_evidence import ambiguity_evidence_point

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "ambiguity_vs_robust_evidence_audit.json"


def main() -> None:
    e_values = {"W0": 30.0, "W1": 2.0, "W2": 8.0, "W3": 25.0}
    stages = (
        ("broad", ("W0", "W1", "W2", "W3")),
        ("nonbinding_pruned", ("W0", "W1", "W3")),
        ("more_nonbinding_pruned", ("W0", "W1")),
        ("binding_competitor_removed", ("W0",)),
    )
    rows = []
    for name, paths in stages:
        point = ambiguity_evidence_point(name, paths, e_values, threshold=20.0)
        rows.append({
            "stage": point.stage,
            "retained_path_count": point.retained_path_count,
            "robust_e_value": point.robust_e_value,
            "crosses_threshold": point.crosses_threshold,
            "retained_paths": list(paths),
        })
    record = {
        "experiment": "BF",
        "title": "Ambiguity reduction versus robust-evidence bottleneck",
        "threshold": 20.0,
        "path_specific_e_values": e_values,
        "rows": rows,
        "scientific_boundary": "Path cardinality is reported as ambiguity, not probability. Robust evidence changes only when the evidence bottleneck changes.",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
