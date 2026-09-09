"""Experiment AP: second-order irregular-time tau calibration and oracle floor."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.compact_temporal_family import (
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
)
from observer_math.physical_relaxation import exponential_relaxation_covariance
from observer_math.quadratic_relaxation_target import (
    gaussian_irregular_relaxation_quadratic_target_bound,
)
from observer_math.relaxation_curvature import (
    gaussian_irregular_relaxation_quadratic_outer_cover,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "quadratic_relaxation_calibration.json"


def _calibration_times() -> np.ndarray:
    gaps = np.array(
        [
            0.03, 0.05, 0.08, 0.04, 0.11, 0.07, 0.15, 0.06,
            0.09, 0.13, 0.05, 0.17, 0.08, 0.12, 0.04, 0.10,
            0.14, 0.06, 0.18, 0.07, 0.09, 0.16, 0.05, 0.11,
            0.20, 0.08, 0.13, 0.06, 0.15, 0.09, 0.12,
        ],
        dtype=float,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _simulate(times: np.ndarray, tau: float, channels: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty((times.size, channels), dtype=float)
    values[0] = rng.standard_normal(channels)
    for index, gap in enumerate(np.diff(times)):
        alpha = np.exp(-gap / tau)
        values[index + 1] = (
            alpha * values[index]
            + np.sqrt(1.0 - alpha * alpha) * rng.standard_normal(channels)
        )
    return values


def _target_times() -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def build_record() -> dict[str, object]:
    true_tau = 0.78
    confidence = 0.975
    calibration_times = _calibration_times()
    values = _simulate(calibration_times, true_tau, 96, seed=20261110)
    model = gaussian_irregular_relaxation_evalue_model(
        values,
        calibration_times,
        lower_relaxation_time=0.40,
        upper_relaxation_time=1.25,
        confidence=confidence,
        mixture_relaxation_time_grid_size=21,
    )

    target_times = _target_times()
    centered = target_times - np.mean(target_times)
    design = np.column_stack((np.ones(target_times.size), centered))

    cover_comparison = []
    for cells in (40, 80, 160, 320, 640):
        first = gaussian_irregular_relaxation_evalue_outer_cover(model, cell_count=cells)
        quadratic = gaussian_irregular_relaxation_quadratic_outer_cover(model, cell_count=cells)
        cover_comparison.append(
            {
                "cell_count": cells,
                "first_order_retained_cells": first.retained_cell_count,
                "first_order_lower_seconds": first.retained_relaxation_time_lower_bound,
                "first_order_upper_seconds": first.retained_relaxation_time_upper_bound,
                "first_order_width_seconds": (
                    first.retained_relaxation_time_upper_bound
                    - first.retained_relaxation_time_lower_bound
                ),
                "quadratic_retained_cells": quadratic.retained_cell_count,
                "quadratic_lower_seconds": quadratic.retained_relaxation_time_lower_bound,
                "quadratic_upper_seconds": quadratic.retained_relaxation_time_upper_bound,
                "quadratic_width_seconds": (
                    quadratic.retained_relaxation_time_upper_bound
                    - quadratic.retained_relaxation_time_lower_bound
                ),
            }
        )

    candidate_rows = []
    candidates = (5, 7, 9, 13, 17, 25, 33, 49, 65)
    for count in candidates:
        bound = gaussian_irregular_relaxation_quadratic_target_bound(
            model,
            target_times,
            design,
            block_dimension=1,
            block_count=1,
            calibration_cell_count=160,
            target_cover_point_count=count,
            covariance_confidence=confidence,
            upper_theta_grid_size=256,
            lower_theta_grid_size=256,
        )
        candidate_rows.append(
            {
                "target_cover_point_count": count,
                "approximate_covariance_relative_error": (
                    bound.covariance_bound.covariance_relative_error
                ),
            }
        )
    selected_k = min(
        candidate_rows,
        key=lambda row: row["approximate_covariance_relative_error"],
    )["target_cover_point_count"]

    final = gaussian_irregular_relaxation_quadratic_target_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        calibration_cell_count=160,
        target_cover_point_count=int(selected_k),
        covariance_confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    oracle_temporal = exponential_relaxation_covariance(target_times, true_tau)[None, :, :]
    oracle = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension=1,
        block_count=1,
        temporal_covariance_grid=oracle_temporal,
        nuisance_design=design,
        eigenvalue_covering_radius=0.0,
        normalization_covering_radius=0.0,
        confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    return {
        "experiment": "AP",
        "title": "Quadratic irregular-time relaxation calibration and oracle target floor",
        "model": {
            "true_relaxation_time_seconds": true_tau,
            "declared_interval_seconds": [0.40, 1.25],
            "calibration_confidence": confidence,
            "covariance_confidence": confidence,
            "combined_confidence": confidence**2,
            "calibration_channel_count": 96,
            "calibration_sample_count": int(calibration_times.size),
            "target_sample_count": int(target_times.size),
            "target_nuisance_rank": int(design.shape[1]),
        },
        "outer_cover_comparison": cover_comparison,
        "quadratic_target_search": {
            "calibration_cell_count": 160,
            "candidate_results": candidate_rows,
            "selected_target_cover_point_count": int(selected_k),
        },
        "quadratic_target_final": {
            "retained_calibration_cell_count": final.calibration_outer_cover.retained_cell_count,
            "retained_lower_seconds": final.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": final.retained_relaxation_time_upper_bound,
            "retained_width_seconds": final.retained_relaxation_time_width,
            "target_cover_point_count": final.target_cover_point_count,
            "target_eigenvalue_covering_radius": final.target_eigenvalue_covering_radius,
            "target_normalization_covering_radius": final.target_normalization_covering_radius,
            "target_covariance_relative_error": final.covariance_bound.covariance_relative_error,
        },
        "oracle_known_tau_target": {
            "temporal_cover_point_count": oracle.cover_point_count,
            "eigenvalue_covering_radius": 0.0,
            "normalization_covering_radius": 0.0,
            "covariance_confidence": confidence,
            "target_covariance_relative_error": oracle.covariance_relative_error,
            "projected_degrees_of_freedom_lower_bound": (
                oracle.projected_degrees_of_freedom_lower_bound
            ),
        },
        "reference_radii": {
            "proposition_53b": 3.155489544511118,
            "proposition_54": 2.572074694777741,
        },
        "interpretation": {
            "quadratic_role": (
                "The quadratic cover changes only deterministic containment of the already valid "
                "continuum e-value set. It spends no additional probability budget."
            ),
            "oracle_role": (
                "The known-tau target bound is not an implementable calibration procedure. It is "
                "a diagnostic floor showing how much of the current radius remains even if temporal "
                "parameter uncertainty is removed completely."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
