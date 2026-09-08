"""Experiment AI: compact two-parameter temporal family concentration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math.compact_temporal_family import (
    gaussian_ar1_white_noise_temporal_cover,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)


def _sphere_net_family_radius(
    block_dimension,
    block_count,
    temporal_grid,
    design,
    eigenvalue_covering_radius,
    normalization_covering_radius,
    confidence,
):
    basis, _ = np.linalg.qr(design, mode="complete")
    complement = basis[:, design.shape[1] :]
    frobenius = []
    spectral = []
    degrees = []
    for temporal in temporal_grid:
        compressed = complement.T @ temporal @ complement
        eigenvalues = np.maximum(np.linalg.eigvalsh(compressed), 0.0)
        frobenius.append(float(np.linalg.norm(eigenvalues)))
        spectral.append(float(eigenvalues[-1]))
        degrees.append(float(np.sum(eigenvalues)))

    projected_rank = complement.shape[1]
    f_plus = max(frobenius) + np.sqrt(projected_rank) * eigenvalue_covering_radius
    s_plus = max(spectral) + eigenvalue_covering_radius
    d_lower = min(degrees) - normalization_covering_radius
    d_upper = max(degrees) + normalization_covering_radius
    tail = np.log(
        2.0 * block_count * 9.0**block_dimension / (1.0 - confidence)
    )
    oracle = 4.0 * (f_plus * np.sqrt(tail) + s_plus * tail) / d_lower
    reference = 0.5 * (d_lower + d_upper)
    a = d_lower / reference
    b = d_upper / reference
    return float(
        max(
            abs(a - 1.0) + a * oracle,
            abs(b - 1.0) + b * oracle,
        )
    )


def _simulate_target(spatial, design, coefficients, phi, eta, rng):
    chol = np.linalg.cholesky(spatial)
    ar_innovations = rng.normal(size=(design.shape[0], spatial.shape[0])) @ chol.T
    ar_component = np.empty_like(ar_innovations)
    ar_component[0] = ar_innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, design.shape[0]):
        ar_component[index] = (
            phi * ar_component[index - 1] + scale * ar_innovations[index]
        )
    white_component = rng.normal(size=(design.shape[0], spatial.shape[0])) @ chol.T
    residual = np.sqrt(1.0 - eta) * ar_component + np.sqrt(eta) * white_component
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
    sample_count=400,
    confidence=0.975,
    theta_grid_size=1024,
    trial_count=96,
    seed=20261120,
):
    time = np.linspace(-1.0, 1.0, sample_count)
    design = np.column_stack((np.ones_like(time), time))
    lower_phi, upper_phi = 0.45, 0.72
    lower_eta, upper_eta = 0.0, 0.05
    resolutions = ((5, 3), (9, 5), (17, 9))

    records = []
    final_cover = None
    final_bound = None
    for phi_points, eta_points in resolutions:
        cover = gaussian_ar1_white_noise_temporal_cover(
            design,
            lower_phi,
            upper_phi,
            lower_eta,
            upper_eta,
            autocorrelation_grid_size=phi_points,
            white_noise_fraction_grid_size=eta_points,
        )
        matrix = gaussian_compact_temporal_family_matrix_chernoff_bound(
            4,
            1,
            cover.temporal_covariance_grid,
            design,
            eigenvalue_covering_radius=cover.projected_eigenvalue_covering_radius,
            normalization_covering_radius=cover.projected_normalization_covering_radius,
            confidence=confidence,
            upper_theta_grid_size=theta_grid_size,
            lower_theta_grid_size=theta_grid_size,
        )
        sphere = _sphere_net_family_radius(
            4,
            1,
            cover.temporal_covariance_grid,
            design,
            cover.projected_eigenvalue_covering_radius,
            cover.projected_normalization_covering_radius,
            confidence,
        )
        records.append(
            {
                "autocorrelation_grid_size": phi_points,
                "white_noise_fraction_grid_size": eta_points,
                "cover_point_count": matrix.cover_point_count,
                "raw_operator_covering_radius": cover.raw_operator_covering_radius,
                "projected_eigenvalue_covering_radius": (
                    cover.projected_eigenvalue_covering_radius
                ),
                "projected_normalization_covering_radius": (
                    cover.projected_normalization_covering_radius
                ),
                "matrix_family_radius": matrix.covariance_relative_error,
                "oracle_normalized_matrix_radius": matrix.oracle_relative_error,
                "sphere_net_family_radius": sphere,
                "relative_radius_reduction": 1.0 - matrix.covariance_relative_error / sphere,
                "projected_degrees_lower": (
                    matrix.projected_degrees_of_freedom_lower_bound
                ),
                "projected_degrees_upper": (
                    matrix.projected_degrees_of_freedom_upper_bound
                ),
                "projected_spectral_norm_bound": matrix.projected_spectral_norm_bound,
            }
        )
        final_cover = cover
        final_bound = matrix

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
    target_parameters = ((0.60, 0.02), (0.70, 0.04))
    trial_records = []
    for parameter_index, (phi, eta) in enumerate(target_parameters):
        errors = []
        for trial in range(trial_count):
            rng = np.random.default_rng(seed + 1000 * parameter_index + trial)
            observations = _simulate_target(
                spatial,
                design,
                coefficients,
                phi,
                eta,
                rng,
            )
            estimate = _projected_covariance(
                observations,
                design,
                final_bound.reference_projected_degrees_of_freedom,
            )
            errors.append(_relative_error(spatial, estimate))
        errors = np.asarray(errors)
        covered = errors <= final_bound.covariance_relative_error
        successes = int(np.sum(covered))
        trial_records.append(
            {
                "true_autocorrelation": phi,
                "true_white_noise_fraction": eta,
                "trial_count": trial_count,
                "mean_relative_error": float(np.mean(errors)),
                "median_relative_error": float(np.median(errors)),
                "q95_relative_error": float(np.quantile(errors, 0.95)),
                "max_relative_error": float(np.max(errors)),
                "uniform_family_radius": final_bound.covariance_relative_error,
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
        "theta_grid_size": theta_grid_size,
        "temporal_family": "R(phi, eta) = (1 - eta) R_phi + eta I",
        "autocorrelation_interval": [lower_phi, upper_phi],
        "white_noise_fraction_interval": [lower_eta, upper_eta],
        "cover_refinement": records,
        "finite_sample_checks": trial_records,
        "final_cover": {
            "autocorrelation_grid": final_cover.autocorrelation_grid.tolist(),
            "white_noise_fraction_grid": final_cover.white_noise_fraction_grid.tolist(),
        },
    }


def plot(results, output_path):
    records = results["cover_refinement"]
    points = np.array([record["cover_point_count"] for record in records])
    matrix = np.array([record["matrix_family_radius"] for record in records])
    sphere = np.array([record["sphere_net_family_radius"] for record in records])
    cover_radius = np.array(
        [record["projected_eigenvalue_covering_radius"] for record in records]
    )
    reduction = 100.0 * np.array(
        [record["relative_radius_reduction"] for record in records]
    )

    fig, axes = plt.subplots(2, 2, figsize=(11.8, 8.4))

    ax = axes[0, 0]
    ax.plot(points, sphere, marker="o", label="sphere-net family certificate")
    ax.plot(points, matrix, marker="o", label="Proposition 49 matrix certificate")
    ax.axhline(1.0, linestyle="--", label="relative error = 1")
    ax.set_xscale("log")
    ax.set_xlabel("temporal cover points")
    ax.set_ylabel("certified relative covariance radius")
    ax.set_title("A two-parameter family crosses into the usable regime")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    ax.plot(points, cover_radius, marker="o", label="operator covering radius")
    ax2 = ax.twinx()
    ax2.plot(points, reduction, marker="s", label="matrix reduction")
    ax.set_xscale("log")
    ax.set_xlabel("temporal cover points")
    ax.set_ylabel("projected operator covering radius")
    ax2.set_ylabel("radius reduction vs sphere-net (%)")
    ax.set_title("Refining geometry tightens the continuum certificate")
    ax.grid(True, alpha=0.25)

    checks = results["finite_sample_checks"]
    labels = [
        f"phi={record['true_autocorrelation']:.2f}\neta={record['true_white_noise_fraction']:.2f}"
        for record in checks
    ]
    q95 = np.array([record["q95_relative_error"] for record in checks])
    maximum = np.array([record["max_relative_error"] for record in checks])
    theorem = np.array([record["uniform_family_radius"] for record in checks])
    x = np.arange(len(checks))
    ax = axes[1, 0]
    ax.plot(x, q95, marker="o", label="95th percentile observed error")
    ax.plot(x, maximum, marker="o", label="maximum observed error")
    ax.plot(x, theorem, marker="o", label="Proposition 49 radius")
    ax.set_xticks(x, labels)
    ax.set_ylabel("relative covariance error")
    ax.set_title("Seeded target-record visibility check")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 1]
    phi_grid = np.asarray(results["final_cover"]["autocorrelation_grid"])
    eta_grid = np.asarray(results["final_cover"]["white_noise_fraction_grid"])
    for eta in eta_grid:
        ax.scatter(phi_grid, np.full_like(phi_grid, eta), s=16, alpha=0.55)
    for record in checks:
        ax.scatter(
            [record["true_autocorrelation"]],
            [record["true_white_noise_fraction"]],
            marker="*",
            s=180,
            label=(
                f"tested ({record['true_autocorrelation']:.2f}, "
                f"{record['true_white_noise_fraction']:.2f})"
            ),
        )
    ax.set_xlabel("AR(1) coefficient phi")
    ax.set_ylabel("white-noise fraction eta")
    ax.set_title("Final 17 x 9 deterministic cover of the full parameter rectangle")
    ax.grid(True, alpha=0.25)
    ax.legend(loc="best", fontsize=8)

    fig.suptitle(
        "Experiment AI: matrix concentration over a compact two-parameter temporal family",
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sample-count", type=int, default=400)
    parser.add_argument("--confidence", type=float, default=0.975)
    parser.add_argument("--theta-grid-size", type=int, default=1024)
    parser.add_argument("--trials", type=int, default=96)
    parser.add_argument("--seed", type=int, default=20261120)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(
        sample_count=args.sample_count,
        confidence=args.confidence,
        theta_grid_size=args.theta_grid_size,
        trial_count=args.trials,
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "compact_temporal_family.json"
    figure_path = args.output_dir / "compact_temporal_family.svg"
    json_path.write_text(json.dumps(results, indent=2) + "\n")
    plot(results, figure_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
