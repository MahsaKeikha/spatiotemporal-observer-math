"""Experiment AW: certified compression and downstream workload."""
from __future__ import annotations

import json
from pathlib import Path

from observer_math.path_pruning import ActionInterval, prune_inadmissible_paths

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "certified_path_compression_audit.json"


def build_record() -> dict[str, object]:
    intervals = {
        "W0": ActionInterval(10.0, 10.6),
        "W1": ActionInterval(9.7, 10.2),
        "W2": ActionInterval(8.9, 9.3),
        "W3": ActionInterval(8.0, 8.6),
        "W4": ActionInterval(6.0, 7.0),
        "W5": ActionInterval(4.0, 5.0),
    }
    out = prune_inadmissible_paths(intervals, tolerance=0.2)
    return {
        "experiment": "AW",
        "title": "Certified path-space compression and downstream workload",
        "path_count_before": len(intervals),
        "retained_paths": list(out.retained),
        "pruned_paths": list(out.pruned),
        "path_count_after": len(out.retained),
        "compression_fraction": 1.0 - len(out.retained) / len(intervals),
        "downstream_evaluations_avoided": len(out.pruned),
        "tolerance": 0.2,
        "best_certified_lower_bound": out.best_certified_lower_bound,
        "interpretation": "Only paths whose upper action bounds cannot approach the best certified lower bound are removed. Overlapping competitors remain for P62 robust evidence.",
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
