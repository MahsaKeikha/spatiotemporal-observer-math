"""Experiment AM: sampling-consistent physical relaxation time.

This experiment is deterministic. It illustrates Proposition 53 by showing that
one physical relaxation time generates different discrete AR(1) coefficients at
different sampling rates, while the recovered relaxation time remains invariant.
It also records irregular-sampling covariance geometry and the certified operator
covering radius for a declared relaxation-time interval.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_operator_lipschitz_bound,
    relaxation_autocorrelation,
    relaxation_time_from_autocorrelation,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "physical_relaxation_sampling.json"


def _dense_cover_error(
    sample_times: np.ndarray,
    lower_tau: float,
    upper_tau: float,
    grid_size: int,
    dense_count: int,
) -> float:
    tau_grid = np.linspace(lower_tau, upper_tau, grid_size)
    dense_grid = np.linspace(lower_tau, upper_tau, dense_count)
    center_covariances = [
        exponential_relaxation_covariance(sample_times, tau) for tau in tau_grid
    ]
    maximum_error = 0.0
    for tau in dense_grid:
        nearest_index = int(np.argmin(np.abs(tau_grid - tau)))
        exact = exponential_relaxation_covariance(sample_times, tau)
        error = float(
            np.linalg.norm(exact - center_covariances[nearest_index], ord=2)
        )
        maximum_error = max(maximum_error, error)
    return maximum_error


def build_record() -> dict[str, object]:
    true_tau = 0.8
    sample_intervals = [0.025, 0.05, 0.1, 0.2, 0.4]

    uniform_sampling = []
    for sample_interval in sample_intervals:
        phi = relaxation_autocorrelation(sample_interval, true_tau)
        recovered_tau = relaxation_time_from_autocorrelation(phi, sample_interval)
        uniform_sampling.append(
            {
                "sample_interval_seconds": sample_interval,
                "sample_rate_hz": 1.0 / sample_interval,
                "phi": phi,
                "recovered_tau_seconds": recovered_tau,
            }
        )

    base_interval = sample_intervals[0]
    base_phi = relaxation_autocorrelation(base_interval, true_tau)
    subsampling = []
    for factor in (1, 2, 4, 8, 16):
        interval = factor * base_interval
        direct_phi = relaxation_autocorrelation(interval, true_tau)
        power_phi = base_phi**factor
        subsampling.append(
            {
                "factor": factor,
                "interval_seconds": interval,
                "direct_phi": direct_phi,
                "power_phi": power_phi,
                "absolute_error": abs(direct_phi - power_phi),
            }
        )

    irregular_times = np.array(
        [0.0, 0.04, 0.11, 0.19, 0.33, 0.52, 0.76, 1.01, 1.29, 1.58, 1.92, 2.31, 2.75],
        dtype=float,
    )
    covariance_seconds = exponential_relaxation_covariance(irregular_times, true_tau)
    covariance_milliseconds = exponential_relaxation_covariance(
        1000.0 * irregular_times,
        1000.0 * true_tau,
    )
    eigenvalues = np.linalg.eigvalsh(covariance_seconds)

    lower_tau = 0.55
    upper_tau = 1.05
    dense_count = 2001
    lipschitz = exponential_relaxation_operator_lipschitz_bound(
        irregular_times,
        lower_tau,
        upper_tau,
    )
    grid_results = []
    for grid_size in (5, 9, 17, 33, 65):
        spacing = (upper_tau - lower_tau) / (grid_size - 1)
        certified_radius = 0.5 * spacing * lipschitz
        dense_error = _dense_cover_error(
            irregular_times,
            lower_tau,
            upper_tau,
            grid_size,
            dense_count,
        )
        grid_results.append(
            {
                "grid_size": grid_size,
                "certified_operator_radius": certified_radius,
                "dense_max_observed_operator_error": dense_error,
                "ratio_observed_to_certified": dense_error / certified_radius,
            }
        )

    return {
        "experiment": "AM",
        "title": "Sampling-consistent physical relaxation time",
        "true_relaxation_time_seconds": true_tau,
        "uniform_sampling": uniform_sampling,
        "subsampling_semigroup_check": subsampling,
        "irregular_sampling": {
            "sample_times_seconds": irregular_times.tolist(),
            "minimum_covariance_eigenvalue": float(eigenvalues[0]),
            "maximum_covariance_eigenvalue": float(eigenvalues[-1]),
            "time_unit_invariance_max_abs_error": float(
                np.max(np.abs(covariance_seconds - covariance_milliseconds))
            ),
        },
        "relaxation_time_cover": {
            "interval_seconds": [lower_tau, upper_tau],
            "operator_lipschitz_bound_per_second": lipschitz,
            "grid_results": grid_results,
            "dense_evaluation_count": dense_count,
        },
        "interpretation": {
            "theorem_role": (
                "The physical parameter is tau. The discrete coefficient phi changes with the "
                "sampling interval, while tau remains invariant under the declared exponential model."
            ),
            "diagnostic_role": (
                "Dense grid evaluation checks numerical scale only. The continuum guarantee comes "
                "from the analytic operator Lipschitz bound in Proposition 53."
            ),
            "not_established": (
                "The experiment does not establish that a real system has one exponential "
                "relaxation time or that the temporal model is universally valid."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
