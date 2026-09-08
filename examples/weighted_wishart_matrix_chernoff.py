"""Experiment AG: matrix Chernoff versus sphere-net covariance concentration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math.matrix_chernoff import (
    gaussian_weighted_wishart_matrix_bound,
    projected_temporal_eigenvalues,
)
from observer_math.nuisance import (
    gaussian_ar1_projected_temporal_envelope,
    gaussian_projected_relative_covariance_error_bound,
)


def _ar1_matrix(sample_count, phi):
    index = np.arange(sample_count)
    return phi ** np.abs(index[:, None] - index[None, :])


def _affine_design(sample_count):
    t = np.linspace(-1.0, 1.0, sample_count)
    return np.column_stack((np.ones_like(t), t))


def run(seed=20261022, trial_count=96):
    records = []
    for sample_count in (300, 500, 850):
        design = _affine_design(sample_count)
        for phi in (0.10, 0.40, 0.65, 0.80):
            temporal = _ar1_matrix(sample_count, phi)
            weights = projected_temporal_eigenvalues(temporal, design)
            matrix_bound = gaussian_weighted_wishart_matrix_bound(
                4, 1, weights, confidence=0.975
            )
            envelope = gaussian_ar1_projected_temporal_envelope(
                sample_count, phi, design
            )
            sphere_net = gaussian_projected_relative_covariance_error_bound(
                4, 1, envelope, confidence=0.975
            )
            records.append(
                {
                    "sample_count": sample_count,
                    "autocorrelation": phi,
                    "projected_trace": matrix_bound.temporal_trace,
                    "projected_frobenius_norm": matrix_bound.temporal_frobenius_norm,
                    "projected_spectral_norm": matrix_bound.temporal_spectral_norm,
                    "sphere_net_radius": sphere_net,
                    "matrix_chernoff_radius": matrix_bound.relative_covariance_error,
                    "matrix_upper_deviation": matrix_bound.upper_deviation,
                    "matrix_lower_deviation": matrix_bound.lower_deviation,
                    "fractional_radius_reduction": 1.0
                    - matrix_bound.relative_covariance_error / sphere_net,
                }
            )

    rng = np.random.default_rng(seed)
    sample_count = 300
    phi = 0.65
    design = _affine_design(sample_count)
    weights = projected_temporal_eigenvalues(_ar1_matrix(sample_count, phi), design)
    verification_bound = gaussian_weighted_wishart_matrix_bound(
        4, 1, weights, confidence=0.975
    )
    degrees = np.sum(weights)
    errors = []
    for _ in range(trial_count):
        gaussian = rng.normal(size=(weights.size, 4))
        covariance = gaussian.T @ (weights[:, None] * gaussian) / degrees
        errors.append(float(np.linalg.norm(covariance - np.eye(4), ord=2)))

    return {
        "experiment": "AG",
        "block_dimension": 4,
        "block_count": 1,
        "confidence": 0.975,
        "nuisance_design": "predeclared intercept + linear time trend",
        "records": records,
        "seeded_visibility_check": {
            "seed": seed,
            "trial_count": trial_count,
            "sample_count": sample_count,
            "autocorrelation": phi,
            "matrix_chernoff_radius": verification_bound.relative_covariance_error,
            "median_observed_error": float(np.median(errors)),
            "q95_observed_error": float(np.quantile(errors, 0.95)),
            "maximum_observed_error": float(np.max(errors)),
            "covered_trials": int(np.sum(np.asarray(errors) <= verification_bound.relative_covariance_error)),
        },
    }


def plot(results, output_path):
    fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.2))
    records = results["records"]
    for sample_count in (300, 500, 850):
        rows = [row for row in records if row["sample_count"] == sample_count]
        phi = [row["autocorrelation"] for row in rows]
        axes[0].plot(phi, [row["sphere_net_radius"] for row in rows], marker="o", label=f"N={sample_count}")
        axes[1].plot(phi, [row["matrix_chernoff_radius"] for row in rows], marker="o", label=f"N={sample_count}")
        axes[2].plot(phi, [100.0 * row["fractional_radius_reduction"] for row in rows], marker="o", label=f"N={sample_count}")

    axes[0].set_title("Previous sphere-net radius")
    axes[1].set_title("Proposition 47 matrix radius")
    axes[2].set_title("Radius reduction")
    axes[0].set_ylabel("relative covariance radius")
    axes[1].set_ylabel("relative covariance radius")
    axes[2].set_ylabel("reduction (%)")
    for axis in axes:
        axis.set_xlabel("AR(1) coefficient")
        axis.grid(True, alpha=0.25)
        axis.legend()
    axes[0].axhline(1.0, linestyle="--")
    axes[1].axhline(1.0, linestyle="--")
    fig.suptitle("Experiment AG — exact matrix concentration removes the sphere-net bottleneck")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--trials", type=int, default=96)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(seed=args.seed, trial_count=args.trials)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "weighted_wishart_matrix_chernoff.json"
    figure_path = args.output_dir / "weighted_wishart_matrix_chernoff.svg"
    json_path.write_text(json.dumps(results, indent=2) + "\n")
    plot(results, figure_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
