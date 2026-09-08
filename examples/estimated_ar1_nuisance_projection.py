"""Experiment AE: estimated AR(1) calibration plus affine nuisance projection."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math.estimated_nuisance import (
    gaussian_calibrated_ar1_projected_covariance_bound,
    separable_gaussian_estimated_ar1_projected_covariance,
)
from observer_math.nuisance import separable_gaussian_projected_covariance


def _simulate_ar1_channels(sample_count, channel_count, phi, rng):
    innovations = rng.normal(size=(sample_count, channel_count))
    values = np.empty_like(innovations)
    values[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, sample_count):
        values[index] = phi * values[index - 1] + scale * innovations[index]
    return values


def _simulate_target(spatial, design, coefficients, phi, rng):
    innovations = rng.normal(size=(design.shape[0], spatial.shape[0])) @ np.linalg.cholesky(
        spatial
    ).T
    residual = np.empty_like(innovations)
    residual[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, design.shape[0]):
        residual[index] = phi * residual[index - 1] + scale * innovations[index]
    return design @ coefficients + residual


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def _exact_projected_degrees(sample_count, phi, design):
    indices = np.arange(sample_count)
    temporal = phi ** np.abs(indices[:, None] - indices[None, :])
    gram = design.T @ design
    removed_trace = np.trace(np.linalg.solve(gram, design.T @ temporal @ design))
    return float(sample_count - removed_trace)


def _wilson_interval(successes, total, z=1.959963984540054):
    p = successes / total
    denominator = 1.0 + z**2 / total
    center = (p + z**2 / (2.0 * total)) / denominator
    half = z * np.sqrt(
        p * (1.0 - p) / total + z**2 / (4.0 * total**2)
    ) / denominator
    return [float(center - half), float(center + half)]


def run(trials=64, calibration_count=700, channel_count=20, target_count=850, seed=20261020):
    spatial = np.array(
        [
            [1.0, 0.25, -0.08, 0.05],
            [0.25, 1.2, 0.16, -0.06],
            [-0.08, 0.16, 0.9, 0.14],
            [0.05, -0.06, 0.14, 1.05],
        ]
    )
    t = np.linspace(-1.0, 1.0, target_count)
    design = np.column_stack((np.ones_like(t), t))
    coefficients = np.array([[2.0, -1.0, 0.5, 2.5], [7.0, -5.0, 4.0, -6.0]])
    true_phis = (0.10, 0.40, 0.65)
    records = []

    for phi_index, phi in enumerate(true_phis):
        oracle_degrees = _exact_projected_degrees(target_count, phi, design)
        interval_estimates = []
        interval_lowers = []
        interval_uppers = []
        interval_covered = []
        radii = []
        calibrated_errors = []
        oracle_errors = []
        constant_centered_errors = []
        covariance_covered = []
        reference_degrees = []

        for trial in range(trials):
            rng = np.random.default_rng(seed + 10000 * phi_index + trial)
            calibration = _simulate_ar1_channels(
                calibration_count, channel_count, phi, rng
            )
            bound = gaussian_calibrated_ar1_projected_covariance_bound(
                spatial.shape[0],
                1,
                target_count,
                design.shape[1],
                calibration,
                declared_upper_bound=0.85,
                calibration_confidence=0.975,
                covariance_confidence=0.975,
            )
            observations = _simulate_target(
                spatial, design, coefficients, phi, rng
            )
            calibrated = separable_gaussian_estimated_ar1_projected_covariance(
                observations, design, bound
            )
            oracle = separable_gaussian_projected_covariance(
                observations, design, oracle_degrees
            )
            centered_values = observations - np.mean(
                observations, axis=0, keepdims=True
            )
            constant_centered = centered_values.T @ centered_values / (target_count - 1)

            interval = bound.autocorrelation_interval
            calibrated_error = _relative_error(spatial, calibrated)
            interval_estimates.append(interval.estimate)
            interval_lowers.append(interval.lower_bound)
            interval_uppers.append(interval.upper_bound)
            interval_covered.append(interval.lower_bound <= phi <= interval.upper_bound)
            radii.append(bound.covariance_relative_error)
            calibrated_errors.append(calibrated_error)
            oracle_errors.append(_relative_error(spatial, oracle))
            constant_centered_errors.append(_relative_error(spatial, constant_centered))
            covariance_covered.append(calibrated_error <= bound.covariance_relative_error)
            reference_degrees.append(bound.reference_projected_degrees_of_freedom)

        interval_successes = int(np.sum(interval_covered))
        covariance_successes = int(np.sum(covariance_covered))
        records.append(
            {
                "true_autocorrelation": phi,
                "trial_count": trials,
                "mean_interval_estimate": float(np.mean(interval_estimates)),
                "mean_interval_lower": float(np.mean(interval_lowers)),
                "mean_interval_upper": float(np.mean(interval_uppers)),
                "autocorrelation_interval_coverage": float(np.mean(interval_covered)),
                "autocorrelation_interval_coverage_wilson_95": _wilson_interval(
                    interval_successes, trials
                ),
                "mean_relative_radius": float(np.mean(radii)),
                "median_relative_radius": float(np.median(radii)),
                "median_calibrated_projected_error": float(
                    np.median(calibrated_errors)
                ),
                "q95_calibrated_projected_error": float(
                    np.quantile(calibrated_errors, 0.95)
                ),
                "max_calibrated_projected_error": float(np.max(calibrated_errors)),
                "median_oracle_projected_error": float(np.median(oracle_errors)),
                "median_constant_centered_error": float(
                    np.median(constant_centered_errors)
                ),
                "calibrated_covariance_coverage": float(np.mean(covariance_covered)),
                "calibrated_covariance_coverage_wilson_95": _wilson_interval(
                    covariance_successes, trials
                ),
                "exact_oracle_projected_degrees": oracle_degrees,
                "mean_reference_projected_degrees": float(np.mean(reference_degrees)),
            }
        )

    return {
        "seed": seed,
        "trial_count_per_autocorrelation": trials,
        "calibration_sample_count": calibration_count,
        "calibration_channel_count": channel_count,
        "target_sample_count": target_count,
        "dimension": int(spatial.shape[0]),
        "nuisance_design": "intercept + predeclared linear time trend",
        "nuisance_rank": int(design.shape[1]),
        "declared_autocorrelation_upper_bound": 0.85,
        "calibration_confidence": 0.975,
        "covariance_confidence": 0.975,
        "combined_confidence_lower_bound": 0.95,
        "records": records,
    }


def plot(results, output_path):
    records = results["records"]
    phi = np.array([record["true_autocorrelation"] for record in records])
    calibrated = np.array(
        [record["median_calibrated_projected_error"] for record in records]
    )
    oracle = np.array([record["median_oracle_projected_error"] for record in records])
    naive = np.array([record["median_constant_centered_error"] for record in records])
    radius = np.array([record["median_relative_radius"] for record in records])
    upper = np.array([record["mean_interval_upper"] for record in records])

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))
    ax = axes[0, 0]
    ax.plot(phi, calibrated, marker="o", label="calibrated projected")
    ax.plot(phi, oracle, marker="o", label="oracle projected")
    ax.set_xlabel("true AR(1) coefficient")
    ax.set_ylabel("median relative covariance error")
    ax.set_title("Observable calibration tracks the oracle")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    ax.plot(phi, calibrated, marker="o", label="observed median error")
    ax.plot(phi, radius, marker="o", label="Proposition 45 radius")
    ax.set_xlabel("true AR(1) coefficient")
    ax.set_ylabel("relative covariance error")
    ax.set_title("Finite-sample radius remains conservative")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 0]
    ax.plot(phi, upper, marker="o", label="mean calibrated upper bound")
    ax.plot(phi, phi, linestyle="--", label="true coefficient")
    ax.set_xlabel("true AR(1) coefficient")
    ax.set_ylabel("coefficient")
    ax.set_title("Increment-energy calibration")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 1]
    ax.plot(phi, naive, marker="o")
    ax.set_xlabel("true AR(1) coefficient")
    ax.set_ylabel("median constant-centered relative error")
    ax.set_title("Ignoring affine drift fails catastrophically")
    ax.grid(True, alpha=0.25)

    fig.suptitle(
        "Experiment AE — estimated AR(1) dependence with affine nuisance projection",
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--calibration-count", type=int, default=700)
    parser.add_argument("--channel-count", type=int, default=20)
    parser.add_argument("--target-count", type=int, default=850)
    parser.add_argument("--seed", type=int, default=20261020)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(
        trials=args.trials,
        calibration_count=args.calibration_count,
        channel_count=args.channel_count,
        target_count=args.target_count,
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "estimated_ar1_nuisance_projection.json"
    figure_path = args.output_dir / "estimated_ar1_nuisance_projection.png"
    json_path.write_text(json.dumps(results, indent=2) + "\n")
    plot(results, figure_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
