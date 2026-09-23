"""Experiment BA: finite-sample information to certified boundary workload."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.finite_sample_boundary import finite_sample_boundary_point

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "finite_sample_boundary_workload_audit.json"

def factors():
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
    local, transport, candidates = factors()
    paths = {"W000": (0, 0, 0), "W001": (0, 0, 1), "W011": (0, 1, 1), "W111": (1, 1, 1)}
    rows = []
    for r in (40, 80, 120, 200, 400, 800, 1600, 3200, 6400):
        point = finite_sample_boundary_point(
            r, block_dimension=5, block_count=6, confidence=0.95,
            local_factors=local, transport_factors=transport, candidates=candidates,
            paths=paths, node_count=3, subset_size=2, transport_weight=0.25,
        )
        rows.append({"residual_count": point.residual_count, "covariance_radius": point.covariance_radius, "perturbative_regime": point.perturbative_regime, "retained_count": point.retained_count, "retained_paths": list(point.retained_paths), "p58_unique_recovery_certified": point.recovery_certified})
    record = {"experiment": "BA", "title": "Finite-sample covariance certification to physical-boundary workload", "confidence": 0.95, "block_dimension": 5, "block_count": 6, "innovation_model": "iid Gaussian unit weights after exact whitening", "rows": rows, "scientific_boundary": "Residual counts are innovation degrees of freedom in the controlled exact-whitening model. They are not asserted to equal raw sensor samples in a general measurement system."}
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()
