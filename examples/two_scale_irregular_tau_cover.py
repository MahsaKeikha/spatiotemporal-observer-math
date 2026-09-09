"""Experiment AO: decouple calibration resolution from target cover resolution.

This experiment reuses the deterministic Experiment AN physical-time problem.
It first tightens the certified e-value outer cover by increasing only the
calibration cell resolution. It then compresses the retained tau span into a
separate target covariance cover and searches that cover size using calibration
information only.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_target_matrix_chernoff_bound,
)
from observer_math.two_scale_relaxation_cover import (
    gaussian_irregular_relaxation_two_scale_target_bound,
    gaussian_optimized_irregular_relaxation_two_scale_target_bound,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "two_scale_irregular_tau_cover.json"


def _calibration_times() -> np.ndarray:
    gaps = np.array(
        [
            0.03,
            0.05,
            0.08,
            0.04,
            0.11,
            0.07,
            0.15,
            0.06,
            0.09,
            0.13,
            0.05,
            0.17,
            0.08,
            0.12,
            0.04,
            0.10,
            0.14,
            0.06,
            0.18,
            0.07,
            0.09,
            0.16,
            0.05,
            0.11,
            0.20,
            0.08,
            0.13,
            0.06,
            0.15,
            0.09,
            0.12,
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
    lower_tau = 0.40
    upper_tau = 1.25
    confidence = 0.975
    calibration_times = _calibration_times()
    calibration_values = _simulate(calibration_times, true_tau, 96, seed=20261110)
    model = gaussian_irregular_relaxation_evalue_model(
        calibration_values,
        calibration_times,
        lower_relaxation_time=lower_tau,
        upper_relaxation_time=upper_tau,
        confidence=confidence,
        mixture_relaxation_time_grid_size=21,
    )

    target_times = _target_times()
    centered = target_times - np.mean(target_times)
    design = np.column_stack((np.ones(target_times.size), centered))

    calibration_resolution = []
    for cell_count in (160, 320, 640, 1280, 2560):
        outer = gaussian_irregular_relaxation_evalue_outer_cover(model, cell_count=cell_count)
        calibration_resolution.append(
            {
                "cell_count": cell_count,
                "retained_cell_count": outer.retained_cell_count,
                "excluded_cell_count": outer.excluded_cell_count,
                "retained_lower_seconds": outer.retained_relaxation_time_lower_bound,
                "retained_upper_seconds": outer.retained_relaxation_time_upper_bound,
                "retained_width_seconds": (
                    outer.retained_relaxation_time_upper_bound
                    - outer.retained_relaxation_time_lower_bound
                ),
                "cell_radius_seconds": outer.cell_radius,
            }
        )

    legacy = gaussian_irregular_relaxation_target_matrix_chernoff_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=160,
        covariance_confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    candidates = (5, 7, 9, 13, 17, 25, 33, 49, 65)
    optimized = gaussian_optimized_irregular_relaxation_two_scale_target_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        calibration_outer_cover_cell_count=1280,
        candidate_target_cover_point_counts=candidates,
        covariance_confidence=confidence,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    selected_k = int(optimized.selected.target_cover_point_count)
    final = gaussian_irregular_relaxation_two_scale_target_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        calibration_outer_cover_cell_count=1280,
        target_cover_point_count=selected_k,
        covariance_confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    candidate_rows = []
    for count, error in zip(
        optimized.candidate_cover_point_counts,
        optimized.candidate_covariance_relative_errors,
        strict=True,
    ):
        candidate_rows.append(
            {
                "target_cover_point_count": int(count),
                "approximate_covariance_relative_error": float(error),
            }
        )

    legacy_error = float(legacy.covariance_bound.covariance_relative_error)
    final_error = float(final.covariance_bound.covariance_relative_error)
    return {
        "experiment": "AO",
        "title": "Two-scale certified irregular-time relaxation cover",
        "model": {
            "true_relaxation_time_seconds": true_tau,
            "declared_interval_seconds": [lower_tau, upper_tau],
            "calibration_confidence": confidence,
            "covariance_confidence": confidence,
            "combined_confidence": confidence**2,
            "calibration_channel_count": 96,
            "calibration_sample_count": int(calibration_times.size),
            "target_sample_count": int(target_times.size),
            "target_nuisance_rank": int(design.shape[1]),
        },
        "calibration_resolution": calibration_resolution,
        "target_cover_search": {
            "calibration_outer_cover_cell_count": 1280,
            "candidate_results": candidate_rows,
            "selected_target_cover_point_count": selected_k,
        },
        "legacy_proposition_53b": {
            "calibration_outer_cover_cell_count": 160,
            "retained_temporal_cover_point_count": legacy.covariance_bound.cover_point_count,
            "target_eigenvalue_covering_radius": legacy.target_eigenvalue_covering_radius,
            "target_normalization_covering_radius": legacy.target_normalization_covering_radius,
            "target_covariance_relative_error": legacy_error,
        },
        "proposition_54_two_scale": {
            "calibration_outer_cover_cell_count": final.calibration_cell_count,
            "retained_calibration_cell_count": final.retained_calibration_cell_count,
            "retained_lower_seconds": final.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": final.retained_relaxation_time_upper_bound,
            "retained_width_seconds": final.retained_relaxation_time_width,
            "target_cover_point_count": final.target_cover_point_count,
            "cover_compression_ratio": final.cover_compression_ratio,
            "target_parameter_covering_radius_seconds": final.target_parameter_covering_radius,
            "target_operator_lipschitz_bound_per_second": (
                final.target_operator_lipschitz_bound
            ),
            "target_eigenvalue_covering_radius": final.target_eigenvalue_covering_radius,
            "target_normalization_covering_radius": final.target_normalization_covering_radius,
            "target_covariance_relative_error": final_error,
            "projected_degrees_of_freedom_lower_bound": (
                final.covariance_bound.projected_degrees_of_freedom_lower_bound
            ),
        },
        "comparison": {
            "absolute_radius_reduction": legacy_error - final_error,
            "relative_radius_reduction_fraction": 1.0 - final_error / legacy_error,
            "epsilon_below_one": bool(final_error < 1.0),
        },
        "interpretation": {
            "validity": (
                "The calibration confidence set remains continuum-valued. Fine calibration cells "
                "certify containment, while a separate target grid covers only the resulting "
                "retained physical-time interval."
            ),
            "selection": (
                "Target cover size is selected from calibration-derived geometry and declared "
                "target timestamps/design only. No target observations are used in the selection."
            ),
            "next_step_if_needed": (
                "If the final radius remains above one, the remaining bottleneck is no longer "
                "forced coupling of calibration and target resolutions. The next theorem should "
                "tighten the calibration outer cover or the temporal operator envelope itself."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
