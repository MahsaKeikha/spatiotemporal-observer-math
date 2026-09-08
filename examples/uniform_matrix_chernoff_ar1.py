"""Experiment AH: interval-uniform matrix concentration for AR(1) covariance."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math.design_interval import gaussian_ar1_design_uniform_envelope
from observer_math.matrix_chernoff import gaussian_projected_weighted_wishart_matrix_bound
from observer_math.uniform_matrix_chernoff import gaussian_ar1_uniform_matrix_chernoff_bound


def _ar1_matrix(sample_count, phi):
    indices = np.arange(sample_count)
    return phi ** np.abs(indices[:, None] - indices[None, :])


def _sphere_net_radius(dimension, block_count, design, lower, upper, confidence, grid_size):
    envelope = gaussian_ar1_design_uniform_envelope(
        design,
        lower,
        upper,
        grid_size=grid_size,
    )
    tail = np.log(2.0 * block_count * 9.0**dimension / (1.0 - confidence))
    oracle = 4.0 * (
        envelope.projected_frobenius_norm_bound * np.sqrt(tail)
        + envelope.projected_spectral_norm_bound * tail
    ) / envelope.projected_degrees_of_freedom_lower_bound
    d_lower = envelope.projected_degrees_of_freedom_lower_bound
    d_upper = envelope.projected_degrees_of_freedom_upper_bound
    d_star = 0.5 * (d_lower + d_upper)
    a = d_lower / d_star
    b = d_upper / d_star
    return float(
        max(
            abs(a - 1.0) + a * oracle,
            abs(b - 1.0) + b * oracle,
        )
    )


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


def _projected_covariance(observations, design, normalization):
    coefficients, _, _, _ = np.linalg.lstsq(design, observations, rcond=None)
    residuals = observations - design @ coefficients
    return residuals.T @ residuals / normalization


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def _wilson_interval(successes, total, z=1.959963984540054):
    p = successes / total
    denominator = 1.0 + z**2 / total
    center = (p + z**2 / (2.0 * total)) / denominator
    half = z * np.sqrt(
        p * (1.0 - p) / total + z**2 / (4.0 * total**2)
    ) / denominator
    return [float(center - half), float(center + half)]


def run(
    sample_count=500,
    confidence=0.975,
    phi_grid_size=17,
    theta_grid_size=1024,
    trial_count=96,
    seed=20261030,
):
    t = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(t), t))
    intervals = [(0.05, 0.15), (0.35, 0.45), (0.60, 0.70), (0.70, 0.80)]
    records = []

    for lower, upper in intervals:
        matrix = gaussian_ar1_uniform_matrix_chernoff_bound(
            4,
            1,
            design,
            lower,
            upper,
            confidence=confidence,
            phi_grid_size=phi_grid_size,
            upper_theta_grid_size=theta_grid_size,
            lower_theta_grid_size=theta_grid_size,
        )
        sphere = _sphere_net_radius(
            4,
            1,
            design,
            lower,
            upper,
            confidence,
            phi_grid_size,
        )
        midpoint = 0.5 * (lower + upper)
        oracle = gaussian_projected_weighted_wishart_matrix_bound(
            4,
            1,
            _ar1_matrix(sample_count, midpoint),
            design,
            confidence=confidence,
            upper_theta_grid_size=theta_grid_size,
            lower_theta_grid_size=theta_grid_size,
        )
        envelope = matrix.design_envelope
        records.append(
            {
                "lower_autocorrelation": lower,
                "upper_autocorrelation": upper,
                "midpoint_autocorrelation": midpoint,
                "sphere_net_interval_radius": sphere,
                "uniform_matrix_radius": matrix.covariance_relative_error,
                "uniform_oracle_normalized_radius": matrix.oracle_relative_error,
                "known_midpoint_oracle_matrix_radius": oracle.relative_covariance_error,
                "relative_radius_reduction": 1.0 - matrix.covariance_relative_error / sphere,
                "projected_degrees_lower": envelope.projected_degrees_of_freedom_lower_bound,
                "projected_degrees_upper": envelope.projected_degrees_of_freedom_upper_bound,
                "projected_spectral_norm_bound": envelope.projected_spectral_norm_bound,
                "eigenvalue_covering_radius": matrix.eigenvalue_covering_radius,
            }
        )

    spatial = np.array(
        [
            [1.0, 0.25, -0.08, 0.05],
            [0.25, 1.2, 0.16, -0.06],
            [-0.08, 0.16, 0.9, 0.14],
            [0.05, -0.06, 0.14, 1.05],
        ]
    )
    coefficients = np.array(
        [[2.0, -1.0, 0.5, 2.5], [7.0, -5.0, 4.0, -6.0]]
    )
    trial_records = []
    for phi, lower, upper in ((0.65, 0.60, 0.70), (0.75, 0.70, 0.80)):
        matrix = gaussian_ar1_uniform_matrix_chernoff_bound(
            4,
            1,
            design,
            lower,
            upper,
            confidence=confidence,
            phi_grid_size=phi_grid_size,
            upper_theta_grid_size=theta_grid_size,
            lower_theta_grid_size=theta_grid_size,
        )
        errors = []
        for trial in range(trial_count):
            rng = np.random.default_rng(seed + 1000 * int(phi * 100) + trial)
            observations = _simulate_target(spatial, design, coefficients, phi, rng)
            estimate = _projected_covariance(
                observations,
                design,
                matrix.reference_projected_degrees_of_freedom,
            )
            errors.append(_relative_error(spatial, estimate))
        errors = np.asarray(errors)
        covered = errors <= matrix.covariance_relative_error
        successes = int(np.sum(covered))
        trial_records.append(
            {
                "true_autocorrelation": phi,
                "declared_interval": [lower, upper],
                "trial_count": trial_count,
                "mean_relative_error": float(np.mean(errors)),
                "median_relative_error": float(np.median(errors)),
                "q95_relative_error": float(np.quantile(errors, 0.95)),
                "max_relative_error": float(np.max(errors)),
                "uniform_matrix_radius": matrix.covariance_relative_error,
                "coverage_rate": float(np.mean(covered)),
                "coverage_wilson_95": _wilson_interval(successes, trial_count),
            }
        )

    return {
        "seed": seed,
        "sample_count": sample_count,
        "dimension": 4,
        "block_count": 1,
        "nuisance_design": "intercept + predeclared linear trend",
        "confidence": confidence,
        "phi_grid_size": phi_grid_size,
        "theta_grid_size": theta_grid_size,
        "interval_comparison": records,
        "finite_sample_checks": trial_records,
    }


def plot(results, output_path):
    records = results["interval_comparison"]
    midpoint = np.array([record["midpoint_autocorrelation"] for record in records])
    sphere = np.array([record["sphere_net_interval_radius"] for record in records])
    matrix = np.array([record["uniform_matrix_radius"] for record in records])
    oracle = np.array([record["known_midpoint_oracle_matrix_radius"] for record in records])
    reduction = 100.0 * np.array([record["relative_radius_reduction"] for record in records])

    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.0))

    ax = axes[0, 0]
    ax.plot(midpoint, sphere, marker="o", label="design sphere-net interval")
    ax.plot(midpoint, matrix, marker="o", label="uniform matrix interval")
    ax.plot(midpoint, oracle, marker="o", label="known midpoint oracle")
    ax.axhline(1.0, linestyle="--", label="relative error = 1")
    ax.set_xlabel("AR(1) interval midpoint")
    ax.set_ylabel("certified relative covariance radius")
    ax.set_title("Unknown phi no longer forces the matrix bound above one")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    ax.plot(midpoint, reduction, marker="o")
    ax.set_xlabel("AR(1) interval midpoint")
    ax.set_ylabel("radius reduction (%)")
    ax.set_title("Reduction relative to Proposition 46")
    ax.grid(True, alpha=0.25)

    checks = results["finite_sample_checks"]
    true_phi = np.array([record["true_autocorrelation"] for record in checks])
    q95 = np.array([record["q95_relative_error"] for record in checks])
    radius = np.array([record["uniform_matrix_radius"] for record in checks])
    ax = axes[1, 0]
    ax.plot(true_phi, q95, marker="o", label="95th percentile observed error")
    ax.plot(true_phi, radius, marker="o", label="uniform theorem radius")
    ax.set_xlabel("true AR(1) coefficient")
    ax.set_ylabel("relative covariance error")
    ax.set_title("Seeded target-record visibility check")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 1]
    coverage = np.array([record["coverage_rate"] for record in checks])
    ax.plot(true_phi, coverage, marker="o")
    ax.axhline(results["confidence"], linestyle="--")
    ax.set_ylim(0.0, 1.02)
    ax.set_xlabel("true AR(1) coefficient")
    ax.set_ylabel("empirical coverage")
    ax.set_title("All recorded target errors remained inside the bound")
    ax.grid(True, alpha=0.25)

    fig.suptitle(
        "Experiment AH: interval-uniform matrix concentration with an affine nuisance mean",
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-count", type=int, default=500)
    parser.add_argument("--confidence", type=float, default=0.975)
    parser.add_argument("--phi-grid-size", type=int, default=17)
    parser.add_argument("--theta-grid-size", type=int, default=1024)
    parser.add_argument("--trials", type=int, default=96)
    parser.add_argument("--seed", type=int, default=20261030)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(
        sample_count=args.sample_count,
        confidence=args.confidence,
        phi_grid_size=args.phi_grid_size,
        theta_grid_size=args.theta_grid_size,
        trial_count=args.trials,
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "uniform_matrix_chernoff_ar1.json"
    figure_path = args.output_dir / "uniform_matrix_chernoff_ar1.png"
    json_path.write_text(json.dumps(results, indent=2) + "\n")
    plot(results, figure_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
