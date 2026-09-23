"""Experiment BB: finite information to robust downstream conclusion."""
from __future__ import annotations

import json
from pathlib import Path

from examples.finite_sample_boundary_workload_audit import factors
from observer_math.finite_sample_boundary import finite_sample_boundary_point
from observer_math.finite_sample_evidence import boundary_point_to_evidence

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "finite_information_to_robust_evidence_audit.json"

def main() -> None:
    local, transport, candidates = factors()
    paths = {"W000": (0, 0, 0), "W001": (0, 0, 1), "W011": (0, 1, 1), "W111": (1, 1, 1)}
    e_values = {"W000": 30.0, "W001": 2.0, "W011": 8.0, "W111": 25.0}
    threshold = 20.0
    rows = []
    for r in (40, 80, 120, 200, 400, 800, 1600, 3200, 6400):
        boundary = finite_sample_boundary_point(
            r, block_dimension=5, block_count=6, confidence=0.95,
            local_factors=local, transport_factors=transport, candidates=candidates,
            paths=paths, node_count=3, subset_size=2, transport_weight=0.25,
        )
        evidence = boundary_point_to_evidence(boundary, e_values, threshold=threshold)
        rows.append({
            "residual_count": r,
            "covariance_radius": boundary.covariance_radius,
            "perturbative_regime": boundary.perturbative_regime,
            "retained_count": boundary.retained_count,
            "retained_paths": list(boundary.retained_paths),
            "robust_e_value": evidence.robust_e_value,
            "crosses_threshold": evidence.crosses_threshold,
            "p58_unique_recovery_certified": boundary.recovery_certified,
        })
    record = {
        "experiment": "BB",
        "title": "Finite information to robust downstream conclusion",
        "confidence": 0.95,
        "e_value_threshold": threshold,
        "path_specific_e_values": e_values,
        "rows": rows,
        "scientific_boundary": "The covariance radius is finite-sample Proposition 47 evidence in a controlled exact-whitening Gaussian innovation model. Path-specific e-values are controlled downstream inputs. BB audits the composition; it is not a biological or general sensor sample-complexity claim.",
    }
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()
