"""Experiment BH: compare targeted and naive precision-design policies.

This controlled experiment tests the policy logic independently of hardware claims.
Each block has a declared menu of achievable uncertainty radii and a synthetic
full-pipeline evaluator with a decision threshold. The targeted policy chooses
the smallest certified intervention found by P79; baselines use uniform
tightening and largest-radius-first selection.
"""
from __future__ import annotations

import json
from pathlib import Path

from observer_math.minimum_precision_intervention import minimum_radius_on_declared_grid

THRESHOLD = 20.0
BASELINE = {"B0": 0.4, "B1": 0.5, "B2": 0.3}
GRIDS = {
    "B0": (0.3, 0.2, 0.1),
    "B1": (0.4, 0.3, 0.2, 0.1),
    "B2": (0.2, 0.1),
}


def evaluator(block_id: str, radius: float) -> tuple[int, float]:
    # Controlled end-to-end response table. B0 is the binding block even
    # though B1 has the largest baseline radius.
    if block_id == "B0":
        if radius > 0.2:
            return 18, 4.0
        if radius > 0.1:
            return 4, 14.0
        return 1, 24.0
    if block_id == "B1":
        return (18 if radius > 0.2 else 12), (4.0 if radius > 0.2 else 6.0)
    return (18 if radius > 0.1 else 15), (4.0 if radius > 0.1 else 5.0)


def main() -> dict:
    candidates = [
        minimum_radius_on_declared_grid(k, BASELINE[k], GRIDS[k], THRESHOLD, evaluator)
        for k in BASELINE
    ]
    feasible = [x for x in candidates if x.achieved]
    targeted = min(feasible, key=lambda x: x.radius_reduction)

    largest = max(BASELINE, key=BASELINE.get)
    largest_out = minimum_radius_on_declared_grid(
        largest, BASELINE[largest], GRIDS[largest], THRESHOLD, evaluator
    )

    # Uniform policy tightens every block to 25% of its baseline. Its total
    # normalized precision effort is the sum of fractional radius reductions.
    uniform_radii = {k: BASELINE[k] * 0.25 for k in BASELINE}
    uniform_effort = sum((BASELINE[k] - uniform_radii[k]) / BASELINE[k] for k in BASELINE)

    result = {
        "threshold": THRESHOLD,
        "targeted": {
            "block": targeted.block_id,
            "required_radius": targeted.required_radius,
            "absolute_reduction": targeted.radius_reduction,
            "normalized_effort": targeted.radius_reduction / targeted.baseline_radius,
            "robust_evidence": targeted.robust_evidence,
        },
        "largest_uncertainty_first": {
            "block": largest,
            "achieved": largest_out.achieved,
        },
        "uniform_25_percent_radius": {
            "normalized_total_effort": uniform_effort,
        },
        "boundary": "controlled policy experiment; not a hardware or sensor-cost result",
    }
    Path("docs/design_policy_comparison.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
