"""Experiment AV: usable consequence of boundary-robust evidence.

This controlled experiment shows why propagating subsystem ambiguity matters.
It is not empirical evidence about consciousness or any biological system.
"""
from __future__ import annotations

import json
from pathlib import Path

from observer_math.boundary_confidence_set import BoundaryEvidenceEnvelope

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "boundary_robust_evidence_audit.json"


def build_record() -> dict[str, object]:
    scenarios = {
        "single_selected_path": {"winner": 100.0},
        "one_plausible_weak_competitor": {"winner": 100.0, "competitor": 1.2},
        "all_admissible_paths_strong": {"winner": 100.0, "competitor_a": 30.0, "competitor_b": 24.0},
    }
    rows = []
    for name, evidence in scenarios.items():
        env = BoundaryEvidenceEnvelope(evidence, delta=0.05, alpha=0.05)
        rows.append({
            "scenario": name,
            "evidence_by_worldtube": evidence,
            "robust_evidence": env.robust_evidence,
            "threshold": 20.0,
            "robust_reject": env.robust_reject,
            "weakest_worldtubes": list(env.weakest_worldtubes),
            "end_to_end_error_budget": env.end_to_end_error_budget,
        })
    return {
        "experiment": "AV",
        "title": "Boundary ambiguity changes downstream conclusions",
        "rows": rows,
        "interpretation": "A strong selected path cannot support a boundary-robust conclusion while a physically admissible competitor remains weak. The conclusion becomes strong only when every retained boundary crosses the declared downstream evidence threshold.",
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
