"""Experiment AO: second-order certification of irregular-time tau calibration.

The experiment reuses the exact deterministic calibration and target geometry
from Experiment AN. It compares the Proposition 53B first-order cell certificate
with the Proposition 54 second-order Taylor certificate, then propagates both
covers through the same Proposition 49 target covariance theorem.

The final oracle calculation fixes tau to its true value and removes all cover
uncertainty. It is included to diagnose whether the remaining target radius is
caused by calibration uncertainty or by temporal dependence in the target record.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.compact_temporal_family import (
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_grid,
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_target_matrix_chernoff_bound,
)
from observer_math.physical_relaxation import exponential_relaxation_covariance
from observer_math.second_order_relaxation_cover import (
    gaussian_irregular_relaxation_second_order_outer_cover,
    gaussian_irregular_relaxation_second_order_target_matrix_chernoff_bound,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "second_order_irregular_tau_cover.json"


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
        values[index + 1] = (
            coefficient * values[index]
            + np.sqrt(1.0 - coefficient * coefficient) * rng.standard_normal(channel_count)
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
    cell_count = 160
    theta_grid_size = 1024

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
    diagnostic = gaussian_irregular_relaxation_evalue_grid(
        model,
        relaxation_time_grid_size=2001,
    )
    first_order = gaussian_irregular_relaxation_evalue_outer_cover(
        model,
        cell_count=cell_count,
    )
    second_order = gaussian_irregular_relaxation_second_order_outer_cover(
        model,
        cell_count=cell_count,
    )

    target_times = _target_times()
    centered = target_times - np.mean(target_times)
    design = np.column_stack((np.ones(target_times.size), centered))

    first_target = gaussian_irregular_relaxation_target_matrix_chernoff_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=cell_count,
        covariance_confidence=confidence,
        upper_theta_grid_size=theta_grid_size,
        lower_theta_grid_size=theta_grid_size,
    )
    second_target = gaussian_irregular_relaxation_second_order_target_matrix_chernoff_bound(
        model,
        target_times,
        design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=cell_count,
        covariance_confidence=confidence,
        upper_theta_grid_size=theta_grid_size,
        lower_theta_grid_size=theta_grid_size,
    )

    oracle_temporal = exponential_relaxation_covariance(target_times, true_tau)
    oracle = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension=1,
        block_count=1,
        temporal_covariance_grid=oracle_temporal,
        nuisance_design=design,
        eigenvalue_covering_radius=0.0,
        normalization_covering_radius=0.0,
        confidence=confidence,
        upper_theta_grid_size=theta_grid_size,
        lower_theta_grid_size=theta_grid_size,
    )

    first_width = (
        first_order.retained_relaxation_time_upper_bound
        - first_order.retained_relaxation_time_lower_bound
    )
    second_width = (
        second_order.retained_relaxation_time_upper_bound
        - second_order.retained_relaxation_time_lower_bound
    )
    diagnostic_width = (
        diagnostic.accepted_relaxation_time_upper_bound
        - diagnostic.accepted_relaxation_time_lower_bound
    )
    first_radius = first_target.covariance_bound.covariance_relative_error
    second_radius = second_target.covariance_bound.covariance_relative_error

    return {
        "experiment": "AO",
        "title": "Second-order certified irregular-time relaxation cover",
        "model": {
            "true_relaxation_time_seconds": true_tau,
            "declared_interval_seconds": [lower_tau, upper_tau],
            "calibration_confidence": confidence,
            "covariance_confidence": confidence,
            "combined_confidence": second_target.combined_confidence,
            "calibration_channel_count": 96,
            "calibration_sample_count": int(calibration_times.size),
            "target_sample_count": int(target_times.size),
            "target_nuisance_rank": 2,
            "cell_count": cell_count,
            "theta_grid_size": theta_grid_size,
        },
        "diagnostic_continuum": {
            "accepted_lower_seconds": diagnostic.accepted_relaxation_time_lower_bound,
            "accepted_upper_seconds": diagnostic.accepted_relaxation_time_upper_bound,
            "accepted_width_seconds": diagnostic_width,
        },
        "first_order_certificate": {
            "retained_cell_count": first_order.retained_cell_count,
            "excluded_cell_count": first_order.excluded_cell_count,
            "retained_lower_seconds": first_order.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": first_order.retained_relaxation_time_upper_bound,
            "retained_width_seconds": first_width,
            "target_covariance_relative_error": first_radius,
            "target_eigenvalue_covering_radius": first_target.target_eigenvalue_covering_radius,
            "target_normalization_covering_radius": (
                first_target.target_normalization_covering_radius
            ),
        },
        "second_order_certificate": {
            "retained_cell_count": second_order.retained_cell_count,
            "excluded_cell_count": second_order.excluded_cell_count,
            "retained_lower_seconds": second_order.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": second_order.retained_relaxation_time_upper_bound,
            "retained_width_seconds": second_width,
            "cover_width_reduction_fraction": 1.0 - second_width / first_width,
            "target_covariance_relative_error": second_radius,
            "target_radius_reduction_fraction": 1.0 - second_radius / first_radius,
            "target_eigenvalue_covering_radius": second_target.target_eigenvalue_covering_radius,
            "target_normalization_covering_radius": (
                second_target.target_normalization_covering_radius
            ),
            "target_projected_degrees_of_freedom_lower_bound": (
                second_target.covariance_bound.projected_degrees_of_freedom_lower_bound
            ),
            "target_projected_degrees_of_freedom_upper_bound": (
                second_target.covariance_bound.projected_degrees_of_freedom_upper_bound
            ),
        },
        "oracle_known_tau": {
            "target_covariance_relative_error": oracle.covariance_relative_error,
            "projected_degrees_of_freedom": oracle.reference_projected_degrees_of_freedom,
            "projected_spectral_norm": oracle.projected_spectral_norm_bound,
            "interpretation": (
                "This removes all tau-cover uncertainty. A radius above one here proves that "
                "cover tightening alone cannot reach the downstream perturbative regime for "
                "this target record."
            ),
        },
        "interpretation": {
            "what_closed": (
                "A cell-local Taylor certificate makes the finite outer cover track the exact "
                "continuum e-value geometry closely without changing the finite-sample coverage "
                "theorem."
            ),
            "remaining_bottleneck": (
                "The target record is strongly temporally dependent. Even oracle knowledge of "
                "tau leaves the Proposition 49 covariance radius above one. The next theorem "
                "must exploit the exact irregular-time innovation whitener rather than only "
                "tighten tau uncertainty."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
