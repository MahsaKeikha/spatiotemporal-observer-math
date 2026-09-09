"""Experiment AQ: exact temporal whitening restores target innovation degrees of freedom."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.compact_temporal_family import (
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from observer_math.physical_relaxation import exponential_relaxation_covariance
from observer_math.whitened_target_covariance import (
    exponential_relaxation_whitened_projected_covariance,
    gaussian_whitened_projected_covariance_bound,
    gaussian_whitened_scalar_chi_square_bound,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "innovation_whitened_target_covariance.json"


def _target_times() -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _target_design(times: np.ndarray) -> np.ndarray:
    centered = times - np.mean(times)
    return np.column_stack((np.ones(times.size), centered))


def _simulate_scalar_target(
    times: np.ndarray,
    tau: float,
    nuisance_design: np.ndarray,
    coefficients: np.ndarray,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty((times.size, 1), dtype=float)
    values[0, 0] = rng.standard_normal()
    for index, gap in enumerate(np.diff(times)):
        alpha = np.exp(-gap / tau)
        values[index + 1, 0] = (
            alpha * values[index, 0]
            + np.sqrt(1.0 - alpha * alpha) * rng.standard_normal()
        )
    return values + nuisance_design @ coefficients[:, None]


def build_record() -> dict[str, object]:
    tau = 0.78
    confidence = 0.975
    times = _target_times()
    design = _target_design(times)
    residual_degrees = int(times.size - design.shape[1])

    temporal = exponential_relaxation_covariance(times, tau)[None, :, :]
    raw_oracle = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension=1,
        block_count=1,
        temporal_covariance_grid=temporal,
        nuisance_design=design,
        eigenvalue_covering_radius=0.0,
        normalization_covering_radius=0.0,
        confidence=confidence,
        upper_theta_grid_size=4096,
        lower_theta_grid_size=4096,
    )
    whitened_matrix = gaussian_whitened_projected_covariance_bound(
        design,
        block_dimension=1,
        block_count=1,
        confidence=confidence,
        upper_theta_grid_size=4096,
        lower_theta_grid_size=4096,
    )
    exact_scalar = gaussian_whitened_scalar_chi_square_bound(
        design,
        block_count=1,
        confidence=confidence,
    )

    coefficients = np.array([6.0, -4.0])
    trial_errors: list[float] = []
    exact_interval_covered = 0
    nuisance_invariance_errors: list[float] = []
    for trial in range(256):
        seed = 20261130 + trial
        shifted = _simulate_scalar_target(times, tau, design, coefficients, seed)
        unshifted = shifted - design @ coefficients[:, None]
        shifted_estimate = float(
            exponential_relaxation_whitened_projected_covariance(
                shifted,
                times,
                tau,
                design,
            )[0, 0]
        )
        unshifted_estimate = float(
            exponential_relaxation_whitened_projected_covariance(
                unshifted,
                times,
                tau,
                design,
            )[0, 0]
        )
        trial_errors.append(abs(shifted_estimate - 1.0))
        nuisance_invariance_errors.append(abs(shifted_estimate - unshifted_estimate))
        if (
            exact_scalar.lower_variance_ratio
            <= shifted_estimate
            <= exact_scalar.upper_variance_ratio
        ):
            exact_interval_covered += 1

    errors = np.asarray(trial_errors)
    invariance = np.asarray(nuisance_invariance_errors)
    matrix_radius = whitened_matrix.covariance_bound.relative_covariance_error
    exact_radius = exact_scalar.relative_covariance_error
    raw_radius = raw_oracle.covariance_relative_error

    return {
        "experiment": "AQ",
        "title": "Innovation-whitened target covariance and restored Gaussian degrees of freedom",
        "model": {
            "relaxation_time_seconds": tau,
            "target_sample_count": int(times.size),
            "target_nuisance_rank": int(design.shape[1]),
            "residual_degrees_of_freedom": residual_degrees,
            "covariance_confidence": confidence,
            "block_dimension": 1,
            "block_count": 1,
        },
        "certificate_comparison": {
            "raw_space_known_tau_oracle_relative_error": raw_radius,
            "raw_space_projected_degrees_lower_bound": (
                raw_oracle.projected_degrees_of_freedom_lower_bound
            ),
            "innovation_whitened_matrix_relative_error": matrix_radius,
            "innovation_whitened_residual_degrees": residual_degrees,
            "innovation_whitened_exact_scalar_relative_error": exact_radius,
            "exact_scalar_lower_variance_ratio": exact_scalar.lower_variance_ratio,
            "exact_scalar_upper_variance_ratio": exact_scalar.upper_variance_ratio,
            "matrix_reduction_fraction_vs_raw_oracle": 1.0 - matrix_radius / raw_radius,
            "scalar_reduction_fraction_vs_raw_oracle": 1.0 - exact_radius / raw_radius,
        },
        "visibility_trials": {
            "trial_count": int(errors.size),
            "median_absolute_relative_error": float(np.median(errors)),
            "q95_absolute_relative_error": float(np.quantile(errors, 0.95)),
            "maximum_absolute_relative_error": float(np.max(errors)),
            "exact_interval_covered_count": int(exact_interval_covered),
            "exact_interval_coverage_fraction": float(exact_interval_covered / errors.size),
            "maximum_nuisance_invariance_error": float(np.max(invariance)),
        },
        "interpretation": {
            "whitening_role": (
                "Exact temporal whitening exposes the independent innovation coordinates already "
                "implied by the declared temporal model. It does not create additional observations."
            ),
            "nuisance_role": (
                "The nuisance design is transformed by the same whitener before projection, so only "
                "its declared rank is removed from the independent innovation coordinates."
            ),
            "scope": (
                "This experiment assumes the target temporal covariance is known exactly. Robust use "
                "under an estimated relaxation time requires an additional uncertainty theorem."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
