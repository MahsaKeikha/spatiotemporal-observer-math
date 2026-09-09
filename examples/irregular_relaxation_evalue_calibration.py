"""Experiment AN: finite-sample physical relaxation-time calibration.

The experiment uses the exact irregular-time innovation likelihood from the
Proposition 53 continuation. It builds a continuum e-value confidence set for a
physical relaxation time, certifies a finite retained-cell outer cover of that
continuum set, checks time-unit invariance, and composes the retained family with
an independent target covariance theorem.

The simulation is deterministic. Numerical grids are used for visualization and
for the certified geometric cover. The finite-sample confidence statement comes
from the e-value identity, not from Monte Carlo coverage.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_grid,
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_log_evalue,
    gaussian_irregular_relaxation_target_matrix_chernoff_bound,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "irregular_relaxation_evalue_calibration.json"


def _sample_times() -> np.ndarray:
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


def _simulate(
    sample_times: np.ndarray,
    relaxation_time: float,
    channel_count: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty((sample_times.size, channel_count), dtype=float)
    values[0] = rng.standard_normal(channel_count)
    alpha = np.exp(-np.diff(sample_times) / relaxation_time)
    for index, coefficient in enumerate(alpha):
        innovation_scale = np.sqrt(1.0 - coefficient * coefficient)
        values[index + 1] = (
            coefficient * values[index]
            + innovation_scale * rng.standard_normal(channel_count)
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
    calibration_channel_count = 96
    mixture_grid_size = 21
    outer_cell_count = 160

    calibration_times = _sample_times()
    calibration_values = _simulate(
        calibration_times,
        true_tau,
        calibration_channel_count,
        seed=20261110,
    )
    model = gaussian_irregular_relaxation_evalue_model(
        calibration_values,
        calibration_times,
        lower_relaxation_time=lower_tau,
        upper_relaxation_time=upper_tau,
        confidence=confidence,
        mixture_relaxation_time_grid_size=mixture_grid_size,
    )
    diagnostic = gaussian_irregular_relaxation_evalue_grid(
        model,
        relaxation_time_grid_size=2001,
    )
    outer = gaussian_irregular_relaxation_evalue_outer_cover(
        model,
        cell_count=outer_cell_count,
    )

    true_log_evalue = gaussian_irregular_relaxation_log_evalue(model, true_tau)
    maximum_accepted_log_evalue = float(
        np.max(diagnostic.log_evalues[diagnostic.accepted_mask])
    )
    minimum_rejected_log_evalue = float(
        np.min(diagnostic.log_evalues[~diagnostic.accepted_mask])
    )

    scale = 1000.0
    model_ms = gaussian_irregular_relaxation_evalue_model(
        calibration_values,
        scale * calibration_times,
        lower_relaxation_time=scale * lower_tau,
        upper_relaxation_time=scale * upper_tau,
        confidence=confidence,
        mixture_relaxation_time_grid_size=mixture_grid_size,
    )
    unit_check_grid = np.linspace(lower_tau, upper_tau, 101)
    unit_errors = [
        abs(
            gaussian_irregular_relaxation_log_evalue(model, float(tau))
            - gaussian_irregular_relaxation_log_evalue(model_ms, float(scale * tau))
        )
        for tau in unit_check_grid
    ]

    target_times = _target_times()
    centered_target_time = target_times - np.mean(target_times)
    target_design = np.column_stack((np.ones(target_times.size), centered_target_time))
    target = gaussian_irregular_relaxation_target_matrix_chernoff_bound(
        model,
        target_times,
        target_design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=outer_cell_count,
        covariance_confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    channel_scaling = []
    full_values = _simulate(calibration_times, true_tau, 192, seed=20261111)
    for channel_count in (24, 48, 96, 192):
        prefix_model = gaussian_irregular_relaxation_evalue_model(
            full_values[:, :channel_count],
            calibration_times,
            lower_relaxation_time=lower_tau,
            upper_relaxation_time=upper_tau,
            confidence=confidence,
            mixture_relaxation_time_grid_size=mixture_grid_size,
        )
        prefix_grid = gaussian_irregular_relaxation_evalue_grid(
            prefix_model,
            relaxation_time_grid_size=2001,
        )
        prefix_outer = gaussian_irregular_relaxation_evalue_outer_cover(
            prefix_model,
            cell_count=outer_cell_count,
        )
        channel_scaling.append(
            {
                "channel_count": channel_count,
                "diagnostic_accepted_lower_seconds": (
                    prefix_grid.accepted_relaxation_time_lower_bound
                ),
                "diagnostic_accepted_upper_seconds": (
                    prefix_grid.accepted_relaxation_time_upper_bound
                ),
                "diagnostic_accepted_width_seconds": (
                    prefix_grid.accepted_relaxation_time_upper_bound
                    - prefix_grid.accepted_relaxation_time_lower_bound
                ),
                "certified_retained_lower_seconds": (
                    prefix_outer.retained_relaxation_time_lower_bound
                ),
                "certified_retained_upper_seconds": (
                    prefix_outer.retained_relaxation_time_upper_bound
                ),
                "certified_retained_cell_count": prefix_outer.retained_cell_count,
                "certified_excluded_cell_count": prefix_outer.excluded_cell_count,
            }
        )

    return {
        "experiment": "AN",
        "title": "Finite-sample irregular-time relaxation calibration",
        "model": {
            "true_relaxation_time_seconds": true_tau,
            "declared_interval_seconds": [lower_tau, upper_tau],
            "calibration_confidence": confidence,
            "calibration_channel_count": calibration_channel_count,
            "calibration_sample_count": int(calibration_times.size),
            "calibration_sample_times_seconds": calibration_times.tolist(),
            "calibration_gap_min_seconds": float(np.min(np.diff(calibration_times))),
            "calibration_gap_max_seconds": float(np.max(np.diff(calibration_times))),
            "mixture_grid_size": mixture_grid_size,
            "outer_cover_cell_count": outer_cell_count,
        },
        "continuum_evalue": {
            "log_evalue_threshold": model.log_evalue_threshold,
            "true_tau_log_evalue": true_log_evalue,
            "true_tau_accepted": bool(true_log_evalue < model.log_evalue_threshold),
            "diagnostic_grid_size": int(diagnostic.total_point_count),
            "diagnostic_accepted_point_count": int(diagnostic.accepted_point_count),
            "diagnostic_accepted_lower_seconds": (
                diagnostic.accepted_relaxation_time_lower_bound
            ),
            "diagnostic_accepted_upper_seconds": (
                diagnostic.accepted_relaxation_time_upper_bound
            ),
            "maximum_accepted_log_evalue": maximum_accepted_log_evalue,
            "minimum_rejected_log_evalue": minimum_rejected_log_evalue,
            "diagnostic_tau_grid_seconds": diagnostic.relaxation_time_grid.tolist(),
            "diagnostic_log_evalues": diagnostic.log_evalues.tolist(),
            "diagnostic_accepted_mask": diagnostic.accepted_mask.tolist(),
        },
        "certified_outer_cover": {
            "cell_count": outer.total_cell_count,
            "retained_cell_count": outer.retained_cell_count,
            "excluded_cell_count": outer.excluded_cell_count,
            "cell_radius_seconds": outer.cell_radius,
            "retained_lower_seconds": outer.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": outer.retained_relaxation_time_upper_bound,
            "maximum_cell_log_likelihood_lipschitz_per_second": (
                outer.log_likelihood_lipschitz_bound
            ),
            "cell_edges_seconds": outer.cell_edges.tolist(),
            "retained_mask": outer.retained_mask.tolist(),
        },
        "time_unit_invariance": {
            "unit_check_point_count": int(unit_check_grid.size),
            "max_abs_log_evalue_error_seconds_vs_milliseconds": float(max(unit_errors)),
        },
        "independent_target_composition": {
            "target_sample_count": int(target_times.size),
            "target_sample_times_seconds": target_times.tolist(),
            "target_nuisance_rank": 2,
            "covariance_confidence": confidence,
            "combined_confidence": target.combined_confidence,
            "target_eigenvalue_covering_radius": (
                target.target_eigenvalue_covering_radius
            ),
            "target_normalization_covering_radius": (
                target.target_normalization_covering_radius
            ),
            "target_covariance_relative_error": (
                target.covariance_bound.covariance_relative_error
            ),
            "target_projected_degrees_of_freedom_lower_bound": (
                target.covariance_bound.projected_degrees_of_freedom_lower_bound
            ),
            "retained_temporal_cover_point_count": (
                target.covariance_bound.cover_point_count
            ),
        },
        "calibration_information_scaling": channel_scaling,
        "interpretation": {
            "theorem_role": (
                "The confidence set is finite-sample and continuum-valued in physical tau. "
                "The mixture grid defines the numerator density q but does not discretize the "
                "confidence theorem."
            ),
            "outer_cover_role": (
                "A cell is excluded only when a deterministic cell-local likelihood derivative "
                "bound proves every tau in that cell is rejected. A valid weak-data cover may "
                "retain the complete declared interval."
            ),
            "target_role": (
                "The target record is independent of calibration. The retained tau family is "
                "propagated through Proposition 49 on a different irregular timestamp grid."
            ),
            "not_established": (
                "The experiment does not establish that a real system follows one exponential "
                "relaxation law, does not infer an observer boundary, and does not establish "
                "consciousness."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
