"""Experiment AQ: exact innovation whitening removes the target temporal penalty."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import chi2

from observer_math.compact_temporal_family import (
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)
from observer_math.innovation_whitening import (
    gaussian_innovation_whitened_matrix_chernoff_bound,
    separable_gaussian_innovation_whitened_covariance,
)
from observer_math.physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_markov_factorization,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "innovation_whitened_target.json"


def _target_times() -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _simulate(times: np.ndarray, tau: float, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty(times.size, dtype=float)
    values[0] = rng.standard_normal()
    for index, gap in enumerate(np.diff(times)):
        alpha = np.exp(-gap / tau)
        values[index + 1] = (
            alpha * values[index]
            + np.sqrt(1.0 - alpha * alpha) * rng.standard_normal()
        )
    return values


def build_record() -> dict[str, object]:
    tau = 0.78
    confidence = 0.975
    times = _target_times()
    centered = times - np.mean(times)
    design = np.column_stack((np.ones(times.size), centered))

    raw_temporal = exponential_relaxation_covariance(times, tau)[None, :, :]
    raw_oracle = gaussian_compact_temporal_family_matrix_chernoff_bound(
        block_dimension=1,
        block_count=1,
        temporal_covariance_grid=raw_temporal,
        nuisance_design=design,
        eigenvalue_covering_radius=0.0,
        normalization_covering_radius=0.0,
        confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )
    whitened = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        block_dimension=1,
        block_count=1,
        relaxation_time=tau,
        confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )

    residual_degrees = whitened.residual_degrees_of_freedom
    alpha = 1.0 - confidence
    scalar_lower = float(chi2.ppf(alpha / 2.0, residual_degrees) / residual_degrees)
    scalar_upper = float(chi2.ppf(1.0 - alpha / 2.0, residual_degrees) / residual_degrees)
    scalar_exact_radius = float(max(1.0 - scalar_lower, scalar_upper - 1.0))

    factorization = exponential_relaxation_markov_factorization(times, tau)
    identity_error = float(
        np.linalg.norm(
            factorization.whitening_matrix
            @ exponential_relaxation_covariance(times, tau)
            @ factorization.whitening_matrix.T
            - np.eye(times.size),
            ord=2,
        )
    )

    trial_count = 512
    errors = []
    nuisance = np.array([3.0, -0.7])
    for trial in range(trial_count):
        values = _simulate(times, tau, seed=20263000 + trial) + design @ nuisance
        estimate = separable_gaussian_innovation_whitened_covariance(
            values,
            times,
            design,
            tau,
        )
        errors.append(abs(float(estimate[0, 0]) - 1.0))
    error_array = np.asarray(errors, dtype=float)

    reduction = float(
        1.0 - whitened.covariance_relative_error / raw_oracle.covariance_relative_error
    )
    return {
        "experiment": "AQ",
        "title": "Exact innovation-whitened target covariance concentration",
        "model": {
            "relaxation_time_seconds": tau,
            "target_sample_count": int(times.size),
            "target_nuisance_rank": int(design.shape[1]),
            "residual_degrees_of_freedom": int(residual_degrees),
            "covariance_confidence": confidence,
            "block_dimension": 1,
            "block_count": 1,
        },
        "raw_known_tau_oracle": {
            "covariance_relative_error": raw_oracle.covariance_relative_error,
            "projected_degrees_of_freedom_lower_bound": (
                raw_oracle.projected_degrees_of_freedom_lower_bound
            ),
            "projected_spectral_norm_bound": raw_oracle.projected_spectral_norm_bound,
        },
        "innovation_whitened": {
            "covariance_relative_error": whitened.covariance_relative_error,
            "upper_deviation": whitened.covariance_bound.upper_deviation,
            "lower_deviation": whitened.covariance_bound.lower_deviation,
            "temporal_trace": whitened.covariance_bound.temporal_trace,
            "temporal_frobenius_norm": whitened.covariance_bound.temporal_frobenius_norm,
            "temporal_spectral_norm": whitened.covariance_bound.temporal_spectral_norm,
            "whitening_nonzero_count": whitened.whitening_nonzero_count,
            "precision_nonzero_count": whitened.precision_nonzero_count,
            "whitening_identity_operator_error": identity_error,
            "relative_radius_reduction_fraction": reduction,
            "crosses_relative_radius_one": bool(whitened.covariance_relative_error < 1.0),
        },
        "scalar_exact_reference": {
            "lower_variance_ratio": scalar_lower,
            "upper_variance_ratio": scalar_upper,
            "two_sided_relative_radius": scalar_exact_radius,
            "role": (
                "Scalar chi-square quantiles are reported only as a dimension-one reference. "
                "Proposition 56 uses the matrix-Chernoff route so the theorem remains matrix-valued."
            ),
        },
        "seeded_visibility_check": {
            "trial_count": trial_count,
            "covered_trial_count": int(
                np.sum(error_array <= whitened.covariance_relative_error)
            ),
            "empirical_coverage_fraction": float(
                np.mean(error_array <= whitened.covariance_relative_error)
            ),
            "median_relative_error": float(np.median(error_array)),
            "maximum_relative_error": float(np.max(error_array)),
            "quantile_95_relative_error": float(np.quantile(error_array, 0.95)),
            "quantile_975_relative_error": float(np.quantile(error_array, 0.975)),
        },
        "interpretation": {
            "main_result": (
                "On the exact Experiment AP target schedule, the current known-tau raw-time "
                "oracle radius is above one. Exact innovation whitening changes the estimator "
                "rather than merely tightening the same temporal cover and reduces the matrix "
                "concentration problem to N-q independent Gaussian residual coordinates."
            ),
            "scope": (
                "The result is conditional on the declared one-timescale Gaussian exponential "
                "relaxation model and exact knowledge of tau on the target record. Uncertain tau "
                "requires a separate robustness theorem."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
