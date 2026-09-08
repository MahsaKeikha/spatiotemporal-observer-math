"""Experiment AJ: data-calibrated two-parameter temporal covariance family."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math.calibrated_temporal_family import (
    gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound,
    separable_gaussian_calibrated_ar1_white_noise_projected_covariance,
)
from observer_math.compact_temporal_family import (
    gaussian_ar1_white_noise_temporal_cover,
    gaussian_compact_temporal_family_matrix_chernoff_bound,
)


def _affine_design(sample_count):
    time = np.linspace(-1.0, 1.0, sample_count)
    return np.column_stack((np.ones_like(time), time))


def _simulate_standardized_calibration(sample_count, channel_count, phi, eta, rng):
    innovations = rng.normal(size=(sample_count, channel_count))
    ar = np.empty_like(innovations)
    ar[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, sample_count):
        ar[index] = phi * ar[index - 1] + scale * innovations[index]
    white = rng.normal(size=(sample_count, channel_count))
    values = np.sqrt(1.0 - eta) * ar + np.sqrt(eta) * white
    offsets = np.linspace(-12.0, 18.0, channel_count)
    return values + offsets[None, :]


def _simulate_target(spatial, design, coefficients, phi, eta, rng):
    chol = np.linalg.cholesky(spatial)
    innovations = rng.normal(size=(design.shape[0], spatial.shape[0])) @ chol.T
    ar = np.empty_like(innovations)
    ar[0] = innovations[0]
    scale = np.sqrt(1.0 - phi**2)
    for index in range(1, design.shape[0]):
        ar[index] = phi * ar[index - 1] + scale * innovations[index]
    white = rng.normal(size=innovations.shape) @ chol.T
    residual = np.sqrt(1.0 - eta) * ar + np.sqrt(eta) * white
    return design @ coefficients + residual


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def _generic_increment_error(
    sample_count,
    channel_count,
    lag,
    lower_phi,
    upper_phi,
    lower_eta,
    upper_eta,
    confidence,
):
    pair_count = sample_count - lag
    minimum_correlation = (1.0 - upper_eta) * lower_phi**lag
    trace_bound = 2.0 * pair_count * (1.0 - minimum_correlation)
    raw_temporal_spectral = (
        (1.0 - lower_eta) * (1.0 + upper_phi) / (1.0 - upper_phi)
        + lower_eta
    )
    spectral_bound = 4.0 * raw_temporal_spectral
    frobenius_bound = np.sqrt(trace_bound * spectral_bound)
    tail = np.log(4.0 / (1.0 - confidence))
    return float(
        frobenius_bound * np.sqrt(tail) / (np.sqrt(channel_count) * pair_count)
        + spectral_bound * tail / (channel_count * pair_count)
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
    target_sample_count=400,
    calibration_sample_count=400,
    calibration_confidence=0.9875,
    covariance_confidence=0.9875,
    theta_grid_size=1024,
    trial_count=96,
    seed=20261201,
):
    lower_phi, upper_phi = 0.45, 0.75
    lower_eta, upper_eta = 0.0, 0.05
    true_phi, true_eta = 0.60, 0.02
    calibration_channel_counts = (16, 32, 64, 128, 256)
    maximum_channels = max(calibration_channel_counts)

    design = _affine_design(target_sample_count)
    full_cover = gaussian_ar1_white_noise_temporal_cover(
        design,
        lower_phi,
        upper_phi,
        lower_eta,
        upper_eta,
        autocorrelation_grid_size=9,
        white_noise_fraction_grid_size=5,
    )
    full_bound = gaussian_compact_temporal_family_matrix_chernoff_bound(
        4,
        1,
        full_cover.temporal_covariance_grid,
        design,
        eigenvalue_covering_radius=full_cover.projected_eigenvalue_covering_radius,
        normalization_covering_radius=full_cover.projected_normalization_covering_radius,
        confidence=covariance_confidence,
        upper_theta_grid_size=theta_grid_size,
        lower_theta_grid_size=theta_grid_size,
    )

    calibration_rng = np.random.default_rng(seed)
    calibration = _simulate_standardized_calibration(
        calibration_sample_count,
        maximum_channels,
        true_phi,
        true_eta,
        calibration_rng,
    )

    records = []
    bounds = {}
    for channel_count in calibration_channel_counts:
        bound = gaussian_calibrated_ar1_white_noise_matrix_chernoff_bound(
            calibration[:, :channel_count],
            4,
            1,
            design,
            lower_autocorrelation=lower_phi,
            upper_autocorrelation=upper_phi,
            lower_white_noise_fraction=lower_eta,
            upper_white_noise_fraction=upper_eta,
            calibration_confidence=calibration_confidence,
            covariance_confidence=covariance_confidence,
            autocorrelation_grid_size=9,
            white_noise_fraction_grid_size=5,
            upper_theta_grid_size=theta_grid_size,
            lower_theta_grid_size=theta_grid_size,
        )
        interval = bound.parameter_interval
        records.append(
            {
                "channel_count": channel_count,
                "lag_one_estimate": interval.lag_one.estimate,
                "lag_one_error_radius": interval.lag_one.error_radius,
                "lag_two_estimate": interval.lag_two.estimate,
                "lag_two_error_radius": interval.lag_two.error_radius,
                "autocorrelation_lower": interval.autocorrelation_lower_bound,
                "autocorrelation_upper": interval.autocorrelation_upper_bound,
                "white_noise_fraction_lower": interval.white_noise_fraction_lower_bound,
                "white_noise_fraction_upper": interval.white_noise_fraction_upper_bound,
                "matrix_radius": bound.covariance_bound.covariance_relative_error,
                "full_prior_matrix_radius": full_bound.covariance_relative_error,
                "combined_confidence_lower_bound": bound.combined_confidence_lower_bound,
                "cover_point_count": bound.covariance_bound.cover_point_count,
                "lag_one_generic_error_radius": _generic_increment_error(
                    calibration_sample_count,
                    channel_count,
                    1,
                    lower_phi,
                    upper_phi,
                    lower_eta,
                    upper_eta,
                    calibration_confidence,
                ),
                "lag_two_generic_error_radius": _generic_increment_error(
                    calibration_sample_count,
                    channel_count,
                    2,
                    lower_phi,
                    upper_phi,
                    lower_eta,
                    upper_eta,
                    calibration_confidence,
                ),
            }
        )
        bounds[channel_count] = bound

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
    finite_sample_checks = []
    for channel_count in (64, 256):
        bound = bounds[channel_count]
        errors = []
        for trial in range(trial_count):
            target_rng = np.random.default_rng(seed + 10000 + 1000 * channel_count + trial)
            target = _simulate_target(
                spatial,
                design,
                coefficients,
                true_phi,
                true_eta,
                target_rng,
            )
            estimated = separable_gaussian_calibrated_ar1_white_noise_projected_covariance(
                target,
                design,
                bound,
            )
            errors.append(_relative_error(spatial, estimated))
        errors = np.asarray(errors)
        radius = bound.covariance_bound.covariance_relative_error
        covered = errors <= radius
        successes = int(np.sum(covered))
        finite_sample_checks.append(
            {
                "calibration_channel_count": channel_count,
                "trial_count": trial_count,
                "median_relative_error": float(np.median(errors)),
                "q95_relative_error": float(np.quantile(errors, 0.95)),
                "max_relative_error": float(np.max(errors)),
                "theorem_radius": radius,
                "coverage_rate": float(np.mean(covered)),
                "coverage_wilson_95": _wilson_interval(successes, trial_count),
            }
        )

    return {
        "seed": seed,
        "target_sample_count": target_sample_count,
        "calibration_sample_count": calibration_sample_count,
        "dimension": 4,
        "nuisance_design": "intercept + predeclared linear trend",
        "calibration_confidence": calibration_confidence,
        "covariance_confidence": covariance_confidence,
        "combined_confidence_lower_bound": calibration_confidence * covariance_confidence,
        "theta_grid_size": theta_grid_size,
        "temporal_family": "R(phi, eta) = (1 - eta) R_phi + eta I",
        "declared_autocorrelation_interval": [lower_phi, upper_phi],
        "declared_white_noise_fraction_interval": [lower_eta, upper_eta],
        "true_autocorrelation": true_phi,
        "true_white_noise_fraction": true_eta,
        "full_prior_matrix_radius": full_bound.covariance_relative_error,
        "calibration_refinement": records,
        "finite_sample_checks": finite_sample_checks,
        "interpretation": (
            "The calibration channels are independent of every target record. "
            "The simulations are visibility checks; Proposition 50 is proved analytically."
        ),
    }


def plot(results, output_path):
    records = results["calibration_refinement"]
    channels = np.array([record["channel_count"] for record in records])
    radii = np.array([record["matrix_radius"] for record in records])
    full_radius = results["full_prior_matrix_radius"]

    fig, axes = plt.subplots(2, 2, figsize=(11.8, 8.4))

    ax = axes[0, 0]
    ax.plot(channels, radii, marker="o", label="Proposition 50 calibrated radius")
    ax.axhline(full_radius, linestyle="--", label="full declared family")
    ax.axhline(1.0, linestyle=":", label="relative error = 1")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("independent calibration channels")
    ax.set_ylabel("certified relative covariance radius")
    ax.set_title("Learning temporal uncertainty changes theorem usability")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[0, 1]
    phi_lower = np.array([record["autocorrelation_lower"] for record in records])
    phi_upper = np.array([record["autocorrelation_upper"] for record in records])
    phi_true = results["true_autocorrelation"]
    ax.fill_between(channels, phi_lower, phi_upper, alpha=0.25, label="certified phi interval")
    ax.plot(channels, phi_lower, marker="o")
    ax.plot(channels, phi_upper, marker="o")
    ax.axhline(phi_true, linestyle="--", label="true phi in controlled study")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("independent calibration channels")
    ax.set_ylabel("AR(1) coefficient")
    ax.set_title("Lag-1 and lag-2 energies contract the parameter region")
    ax.grid(True, alpha=0.25)
    ax.legend()

    ax = axes[1, 0]
    lag_one_specific = np.array([record["lag_one_error_radius"] for record in records])
    lag_one_generic = np.array(
        [record["lag_one_generic_error_radius"] for record in records]
    )
    lag_two_specific = np.array([record["lag_two_error_radius"] for record in records])
    lag_two_generic = np.array(
        [record["lag_two_generic_error_radius"] for record in records]
    )
    ax.plot(channels, lag_one_generic, marker="o", label="lag 1 generic spectral product")
    ax.plot(channels, lag_one_specific, marker="o", label="lag 1 increment-specific")
    ax.plot(channels, lag_two_generic, marker="s", label="lag 2 generic spectral product")
    ax.plot(channels, lag_two_specific, marker="s", label="lag 2 increment-specific")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlabel("independent calibration channels")
    ax.set_ylabel("correlation error radius")
    ax.set_title("The increment filter removes most of the dependence penalty")
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8)

    checks = results["finite_sample_checks"]
    x = np.arange(len(checks))
    q95 = np.array([record["q95_relative_error"] for record in checks])
    maximum = np.array([record["max_relative_error"] for record in checks])
    theorem = np.array([record["theorem_radius"] for record in checks])
    labels = [f"{record['calibration_channel_count']} channels" for record in checks]
    ax = axes[1, 1]
    ax.plot(x, q95, marker="o", label="95th percentile observed error")
    ax.plot(x, maximum, marker="o", label="maximum observed error")
    ax.plot(x, theorem, marker="o", label="Proposition 50 radius")
    ax.set_xticks(x, labels)
    ax.set_ylabel("relative covariance error")
    ax.set_title("Independent target-record visibility checks")
    ax.grid(True, alpha=0.25)
    ax.legend()

    fig.suptitle(
        "Experiment AJ: observable calibration of a two-parameter temporal family",
        fontsize=14,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-sample-count", type=int, default=400)
    parser.add_argument("--calibration-sample-count", type=int, default=400)
    parser.add_argument("--calibration-confidence", type=float, default=0.9875)
    parser.add_argument("--covariance-confidence", type=float, default=0.9875)
    parser.add_argument("--theta-grid-size", type=int, default=1024)
    parser.add_argument("--trials", type=int, default=96)
    parser.add_argument("--seed", type=int, default=20261201)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(
        target_sample_count=args.target_sample_count,
        calibration_sample_count=args.calibration_sample_count,
        calibration_confidence=args.calibration_confidence,
        covariance_confidence=args.covariance_confidence,
        theta_grid_size=args.theta_grid_size,
        trial_count=args.trials,
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    json_path = args.output_dir / "calibrated_temporal_family.json"
    figure_path = args.output_dir / "calibrated_temporal_family.svg"
    json_path.write_text(json.dumps(results, indent=2) + "\n")
    plot(results, figure_path)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
