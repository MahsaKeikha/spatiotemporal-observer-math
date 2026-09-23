"""Experiment AT: factor-specific covariance dimension audit."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.factor_geometry import observer_factor_block_geometry

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "factor_specific_covariance_audit.json"


def _log_unit_matrix_mgf_factor(dimension: int, x: np.ndarray, *, upper_tail: bool) -> np.ndarray:
    if upper_tail:
        log_chi = -0.5 * dimension * np.log1p(-2.0 * x)
        sign_term = -x
    else:
        log_chi = -0.5 * dimension * np.log1p(2.0 * x)
        sign_term = x
    if dimension == 1:
        log_bracket = log_chi
    else:
        log_bracket = np.logaddexp(np.log(float(dimension - 1)), log_chi) - np.log(float(dimension))
    return sign_term + log_bracket


def unit_weight_radius(dimension: int, block_count: int, residual_degrees: int, *, confidence: float = 0.975, grid_size: int = 1024) -> float:
    log_prefactor = float(np.log(2.0 * block_count * dimension / (1.0 - confidence)))
    upper_x = np.geomspace(1e-8, 0.499999, grid_size)
    upper = (log_prefactor + residual_degrees * _log_unit_matrix_mgf_factor(dimension, upper_x, upper_tail=True)) / upper_x / residual_degrees
    lower_x = np.geomspace(1e-8, 1e3, grid_size)
    lower = (log_prefactor + residual_degrees * _log_unit_matrix_mgf_factor(dimension, lower_x, upper_tail=False)) / lower_x / residual_degrees
    return float(max(np.min(upper), min(1.0, float(np.min(lower)))))


def minimum_residual_degrees(dimension: int, block_count: int, *, threshold: float = 1.0) -> int:
    lower, upper = 2, 4
    while unit_weight_radius(dimension, block_count, upper) >= threshold:
        upper *= 2
    while lower < upper:
        midpoint = (lower + upper) // 2
        if unit_weight_radius(dimension, block_count, midpoint) < threshold:
            upper = midpoint
        else:
            lower = midpoint + 1
    return int(lower)


def build_record() -> dict[str, object]:
    n, s, time_count, candidate_count = 7, 3, 5, 35
    blocks = time_count * candidate_count
    residual = 118
    geometry = observer_factor_block_geometry(n, s)
    small = geometry.integration_dimension
    full = geometry.local_independence_dimension
    small_entry = minimum_residual_degrees(small, blocks)
    full_entry = minimum_residual_degrees(full, blocks)
    return {
        "experiment": "AT",
        "title": "Factor-specific covariance geometry audit",
        "benchmark": {"node_count": n, "subset_size": s, "time_count": time_count, "candidate_count": candidate_count, "simultaneous_time_candidate_blocks": blocks},
        "factor_dimensions": {
            "integration": geometry.integration_dimension,
            "local_persistence": geometry.local_persistence_dimension,
            "transport_persistence": geometry.transport_persistence_dimension,
            "local_environmental_independence": geometry.local_independence_dimension,
            "transport_environmental_independence": geometry.transport_independence_dimension,
        },
        "exact_tau_unit_weight_diagnostic": {
            "residual_innovation_degrees": residual,
            "confidence": 0.975,
            "dimension_6_radius": unit_weight_radius(small, blocks, residual),
            "dimension_10_radius": unit_weight_radius(full, blocks, residual),
            "dimension_6_first_residual_degrees_below_one": small_entry,
            "dimension_6_radius_at_entry": unit_weight_radius(small, blocks, small_entry),
            "dimension_10_first_residual_degrees_below_one": full_entry,
            "dimension_10_radius_at_entry": unit_weight_radius(full, blocks, full_entry),
        },
        "conclusion": "Integration and persistence admit smaller sufficient covariance blocks, but environmental leakage retains the full n+s block. Factor-specific geometry tightens the certificate without by itself resolving the observer-scale bottleneck.",
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
