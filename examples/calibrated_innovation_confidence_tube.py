"""Experiment AR: calibrated tau uncertainty propagated through innovation whitening."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.calibrated_innovation_whitening import (
    gaussian_calibrated_innovation_confidence_tube,
    innovation_whitened_covariance_path,
    scalar_relative_covariance_interval,
)
from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_model,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "calibrated_innovation_confidence_tube.json"


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


def _simulate_channels(times: np.ndarray, tau: float, channels: int, seed: int) -> np.ndarray:
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


def _design(times: np.ndarray) -> np.ndarray:
    centered = times - np.mean(times)
    return np.column_stack((np.ones(times.size), centered))


def _retained_visibility_grid(outer, points_per_cell: int = 17) -> np.ndarray:
    pieces = []
    for index in np.flatnonzero(outer.retained_mask):
        pieces.append(
            np.linspace(
                float(outer.cell_edges[index]),
                float(outer.cell_edges[index + 1]),
                points_per_cell,
            )
        )
    return np.unique(np.concatenate(pieces))


def build_record() -> dict[str, object]:
    true_tau = 0.78
    calibration_confidence = 0.975
    covariance_confidence = 0.975

    calibration_times = _calibration_times()
    calibration_values = _simulate_channels(
        calibration_times,
        true_tau,
        96,
        seed=20261110,
    )
    model = gaussian_irregular_relaxation_evalue_model(
        calibration_values,
        calibration_times,
        lower_relaxation_time=0.40,
        upper_relaxation_time=1.25,
        confidence=calibration_confidence,
        mixture_relaxation_time_grid_size=21,
    )

    target_times = _target_times()
    design = _design(target_times)
    tube = gaussian_calibrated_innovation_confidence_tube(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        calibration_cell_count=160,
        covariance_confidence=covariance_confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    outer = tube.calibration_outer_cover
    candidate_tau = _retained_visibility_grid(outer)
    display_noise = _simulate_channels(
        target_times,
        true_tau,
        1,
        seed=20264000,
    )[:, 0]
    display_values = display_noise + design @ np.array([3.0, -0.7])
    covariance_path = innovation_whitened_covariance_path(
        display_values,
        target_times,
        design,
        candidate_tau,
    )[:, 0, 0]
    true_tau_estimate = float(
        innovation_whitened_covariance_path(
            display_values,
            target_times,
            design,
            np.array([true_tau]),
        )[0, 0, 0]
    )

    radius = float(tube.covariance_relative_error)
    lower_path = covariance_path / (1.0 + radius)
    upper_path = covariance_path / (1.0 - radius)
    true_tau_interval = scalar_relative_covariance_interval(true_tau_estimate, radius)

    trial_count = 512
    relative_errors = []
    for trial in range(trial_count):
        noise = _simulate_channels(
            target_times,
            true_tau,
            1,
            seed=20265000 + trial,
        )[:, 0]
        values = noise + design @ np.array([3.0, -0.7])
        estimate = float(
            innovation_whitened_covariance_path(
                values,
                target_times,
                design,
                np.array([true_tau]),
            )[0, 0, 0]
        )
        relative_errors.append(abs(estimate - 1.0))
    error_array = np.asarray(relative_errors, dtype=float)

    return {
        "experiment": "AR",
        "title": "Calibrated innovation-whitened covariance confidence tube",
        "model": {
            "true_relaxation_time_seconds": true_tau,
            "declared_relaxation_interval_seconds": [0.40, 1.25],
            "calibration_confidence": calibration_confidence,
            "covariance_confidence": covariance_confidence,
            "combined_confidence": tube.combined_confidence,
            "calibration_channel_count": 96,
            "calibration_sample_count": int(calibration_times.size),
            "target_sample_count": int(target_times.size),
            "target_nuisance_rank": int(design.shape[1]),
            "residual_innovation_degrees_of_freedom": tube.residual_degrees_of_freedom,
            "block_dimension": 1,
            "block_count": 1,
        },
        "calibrated_relaxation_outer_cover": {
            "cell_count": outer.total_cell_count,
            "retained_cell_count": outer.retained_cell_count,
            "excluded_cell_count": outer.excluded_cell_count,
            "retained_lower_seconds": outer.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": outer.retained_relaxation_time_upper_bound,
            "retained_hull_width_seconds": (
                outer.retained_relaxation_time_upper_bound
                - outer.retained_relaxation_time_lower_bound
            ),
            "true_tau_inside_retained_hull": bool(
                outer.retained_relaxation_time_lower_bound
                <= true_tau
                <= outer.retained_relaxation_time_upper_bound
            ),
        },
        "candidate_wise_target_certificate": {
            "common_matrix_relative_radius": radius,
            "crosses_relative_radius_one": bool(radius < 1.0),
            "role": (
                "For each candidate tau, this is the Proposition 56 radius that would apply if "
                "that candidate were the true physical relaxation time. Proposition 57 takes the "
                "union of those candidate-wise confidence balls over the calibrated tau set."
            ),
        },
        "display_target_visibility": {
            "seed": 20264000,
            "evaluated_candidate_count": int(candidate_tau.size),
            "candidate_relaxation_times_seconds": candidate_tau.tolist(),
            "candidate_covariance_centers": covariance_path.tolist(),
            "candidate_scalar_interval_lower": lower_path.tolist(),
            "candidate_scalar_interval_upper": upper_path.tolist(),
            "true_tau_covariance_estimate": true_tau_estimate,
            "true_tau_scalar_interval": [float(true_tau_interval[0]), float(true_tau_interval[1])],
            "candidate_center_minimum": float(np.min(covariance_path)),
            "candidate_center_maximum": float(np.max(covariance_path)),
            "candidate_center_span": float(np.ptp(covariance_path)),
            "dense_grid_projected_hull": [
                float(np.min(lower_path)),
                float(np.max(upper_path)),
            ],
            "true_spatial_variance": 1.0,
            "visibility_only": (
                "The displayed candidate grid visualizes the continuum confidence tube. The "
                "finite-sample theorem is the set-valued union over the complete retained cells, "
                "not a claim that this numerical grid exhausts the continuum."
            ),
        },
        "seeded_visibility_check": {
            "trial_count": trial_count,
            "covered_trial_count_at_true_tau": int(np.sum(error_array <= radius)),
            "empirical_coverage_fraction_at_true_tau": float(np.mean(error_array <= radius)),
            "median_relative_error": float(np.median(error_array)),
            "maximum_relative_error": float(np.max(error_array)),
            "quantile_95_relative_error": float(np.quantile(error_array, 0.95)),
            "quantile_975_relative_error": float(np.quantile(error_array, 0.975)),
        },
        "reference_radii": {
            "proposition_55_raw_time_target": 2.4148799294322116,
            "proposition_56_known_tau_innovation_whitened": 0.4364443814,
        },
        "interpretation": {
            "main_result": (
                "Finite-sample calibration uncertainty is carried into the target analysis as a "
                "family of exact candidate-wise innovation-whitened covariance confidence balls. "
                "The matrix concentration radius remains the Proposition 56 unit-weight radius; "
                "uncertainty in tau appears through which covariance center is physically admissible."
            ),
            "multiplicity": (
                "No Bonferroni penalty over candidate tau values is used. Coverage requires the "
                "target covariance event only at the one true tau, while the independent calibration "
                "event places that true tau inside the retained outer cover."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
