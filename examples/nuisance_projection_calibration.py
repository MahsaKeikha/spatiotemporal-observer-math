"""Experiment AD: affine temporal nuisance projection under AR(1) dependence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math.nuisance import (
    gaussian_ar1_projected_temporal_envelope,
    gaussian_projected_relative_covariance_error_bound,
    separable_gaussian_projected_covariance,
)


def relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def simulate_ar1(spatial, design, coefficients, phi, rng):
    n, dimension = design.shape[0], spatial.shape[0]
    chol = np.linalg.cholesky(spatial)
    innovations = rng.normal(size=(n, dimension)) @ chol.T
    residual = np.empty_like(innovations)
    residual[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, n):
        residual[index] = phi * residual[index - 1] + scale * innovations[index]
    return design @ coefficients + residual


def wilson_interval(successes, total, z=1.959963984540054):
    if total <= 0:
        return [float("nan"), float("nan")]
    p = successes / total
    denominator = 1.0 + z**2 / total
    center = (p + z**2 / (2.0 * total)) / denominator
    half = z * np.sqrt(
        p * (1.0 - p) / total + z**2 / (4.0 * total**2)
    ) / denominator
    return [float(center - half), float(center + half)]


def run(trials=96, sample_count=800, phi=0.4, seed=20261011):
    rng = np.random.default_rng(seed)
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    spatial = np.array(
        [
            [1.0, 0.28, -0.12, 0.06],
            [0.28, 1.25, 0.18, -0.07],
            [-0.12, 0.18, 0.92, 0.16],
            [0.06, -0.07, 0.16, 1.08],
        ]
    )
    base_slope = np.array([1.0, -0.8, 0.6, -0.5])
    amplitudes = np.array([0.0, 1.0, 3.0, 6.0, 10.0])
    envelope = gaussian_ar1_projected_temporal_envelope(sample_count, phi, design)
    radius = gaussian_projected_relative_covariance_error_bound(
        spatial.shape[0], 1, envelope, confidence=0.975
    )

    records = []
    for amplitude in amplitudes:
        projected_errors = []
        centered_errors = []
        invariance_errors = []
        for _ in range(trials):
            intercept = rng.normal(scale=2.0, size=spatial.shape[0])
            coefficients = np.vstack((intercept, amplitude * base_slope))
            observations = simulate_ar1(spatial, design, coefficients, phi, rng)
            projected = separable_gaussian_projected_covariance(
                observations, design, envelope.projected_degrees_of_freedom
            )
            centered_values = observations - np.mean(
                observations, axis=0, keepdims=True
            )
            centered = centered_values.T @ centered_values / (sample_count - 1)
            projected_errors.append(relative_error(spatial, projected))
            centered_errors.append(relative_error(spatial, centered))

            extra = rng.normal(size=(design.shape[1], spatial.shape[0]))
            shifted = separable_gaussian_projected_covariance(
                observations + design @ extra,
                design,
                envelope.projected_degrees_of_freedom,
            )
            invariance_errors.append(
                float(np.linalg.norm(shifted - projected, ord=2))
            )

        projected_errors = np.asarray(projected_errors)
        centered_errors = np.asarray(centered_errors)
        covered = projected_errors <= radius
        records.append(
            {
                "slope_amplitude": float(amplitude),
                "trial_count": int(trials),
                "mean_projected_relative_error": float(np.mean(projected_errors)),
                "median_projected_relative_error": float(np.median(projected_errors)),
                "q95_projected_relative_error": float(
                    np.quantile(projected_errors, 0.95)
                ),
                "max_projected_relative_error": float(np.max(projected_errors)),
                "mean_constant_centered_relative_error": float(
                    np.mean(centered_errors)
                ),
                "median_constant_centered_relative_error": float(
                    np.median(centered_errors)
                ),
                "q95_constant_centered_relative_error": float(
                    np.quantile(centered_errors, 0.95)
                ),
                "max_constant_centered_relative_error": float(
                    np.max(centered_errors)
                ),
                "projected_coverage_rate": float(np.mean(covered)),
                "projected_coverage_wilson_95": wilson_interval(
                    int(np.sum(covered)), trials
                ),
                "maximum_nuisance_invariance_error": float(
                    np.max(invariance_errors)
                ),
            }
        )

    return {
        "seed": seed,
        "sampling_model": "Gaussian separable spatial covariance with stationary AR(1) temporal dependence and an unknown affine temporal mean",
        "sample_count": sample_count,
        "dimension": int(spatial.shape[0]),
        "autocorrelation": phi,
        "nuisance_design": "intercept + predeclared linear time trend",
        "nuisance_rank": envelope.nuisance_rank,
        "confidence": 0.975,
        "analytical_relative_radius": radius,
        "projected_degrees_of_freedom": envelope.projected_degrees_of_freedom,
        "projected_frobenius_norm": envelope.projected_frobenius_norm,
        "projected_spectral_norm": envelope.projected_spectral_norm,
        "variance_effective_sample_size": envelope.variance_effective_sample_size,
        "operator_effective_sample_size": envelope.operator_effective_sample_size,
        "records": records,
    }


def plot(results, output_path):
    records = results["records"]
    x = np.array([record["slope_amplitude"] for record in records])
    projected = np.array(
        [record["median_projected_relative_error"] for record in records]
    )
    centered = np.array(
        [record["median_constant_centered_relative_error"] for record in records]
    )
    q95_projected = np.array(
        [record["q95_projected_relative_error"] for record in records]
    )
    coverage = np.array([record["projected_coverage_rate"] for record in records])
    invariance = np.array(
        [record["maximum_nuisance_invariance_error"] for record in records]
    )
    radius = results["analytical_relative_radius"]

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))
    ax = axes[0, 0]
    ax.plot(x, projected, marker="o", label="projected estimator")
    ax.plot(x, centered, marker="o", label="constant mean-centering")
    ax.set_yscale("log")
    ax.set_xlabel("linear-trend amplitude")
    ax.set_ylabel("median relative covariance error")
    ax.set_title("Affine nuisance projection removes trend bias")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    ax.plot(x, q95_projected, marker="o", label="95th percentile observed error")
    ax.axhline(radius, linestyle="--", label="97.5% analytical radius")
    ax.set_xlabel("linear-trend amplitude")
    ax.set_ylabel("relative covariance error")
    ax.set_title("The theorem radius is trend-amplitude invariant")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 0]
    ax.plot(x, coverage, marker="o")
    ax.axhline(0.975, linestyle="--")
    ax.set_ylim(0.0, 1.02)
    ax.set_xlabel("linear-trend amplitude")
    ax.set_ylabel("empirical coverage")
    ax.set_title("Recorded coverage of the projected covariance event")
    ax.grid(True, alpha=0.25)

    ax = axes[1, 1]
    ax.plot(x, invariance, marker="o")
    ax.set_yscale("log")
    ax.set_xlabel("linear-trend amplitude")
    ax.set_ylabel("spectral difference after adding H B")
    ax.set_title("Numerical nuisance invariance")
    ax.grid(True, alpha=0.25)

    fig.suptitle(
        "Experiment AD — time-varying mean removal by predeclared temporal projection",
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=96)
    parser.add_argument("--sample-count", type=int, default=800)
    parser.add_argument("--autocorrelation", type=float, default=0.4)
    parser.add_argument("--seed", type=int, default=20261011)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(
        trials=args.trials,
        sample_count=args.sample_count,
        phi=args.autocorrelation,
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "nuisance_projection_calibration.json"
    figure_path = args.output_dir / "nuisance_projection_calibration.png"
    json_path.write_text(json.dumps(results, indent=2) + "\n")
    plot(results, figure_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
