"""Calibrate mean-centered covariance under separable Gaussian dependence."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math import (
    gaussian_ar1_centered_temporal_correlation_envelope,
    gaussian_ar1_temporal_correlation_envelope,
    gaussian_dependent_centered_relative_covariance_error_bound,
    gaussian_dependent_relative_covariance_error_bound,
    separable_gaussian_centered_covariance,
)

if __package__:
    from examples.dependent_gaussian_calibration import ar1_standardized_observations
    from examples.gaussian_screen_calibration import wilson_interval
else:
    from dependent_gaussian_calibration import ar1_standardized_observations
    from gaussian_screen_calibration import wilson_interval


def evaluate_trial(task):
    (
        sample_count,
        dimension,
        autocorrelation,
        degrees,
        seed,
        known_mean_radius,
        centered_radius,
    ) = task
    residuals = ar1_standardized_observations(
        sample_count, dimension, autocorrelation, seed
    )
    mean = np.linspace(-2.5, 3.5, dimension)
    observations = residuals + mean
    known_mean = residuals.T @ residuals / sample_count
    corrected = separable_gaussian_centered_covariance(observations, degrees)
    ordinary = np.cov(observations, rowvar=False, ddof=1)
    translated_back = separable_gaussian_centered_covariance(residuals, degrees)
    identity = np.eye(dimension)
    known_error = float(np.linalg.norm(known_mean - identity, ord=2))
    centered_error = float(np.linalg.norm(corrected - identity, ord=2))
    ordinary_error = float(np.linalg.norm(ordinary - identity, ord=2))
    return {
        "known_mean_error": known_error,
        "centered_error": centered_error,
        "ordinary_centered_error": ordinary_error,
        "translation_discrepancy": float(
            np.linalg.norm(corrected - translated_back, ord=2)
        ),
        "known_mean_covered": known_error <= known_mean_radius,
        "centered_covered": centered_error <= centered_radius,
    }


def aggregate(autocorrelation, centered, known_radius, centered_radius, trials):
    record = {
        "autocorrelation": autocorrelation,
        "centering_degrees_of_freedom": centered.centering_degrees_of_freedom,
        "normalizer_relative_to_n_minus_one": (
            centered.centering_degrees_of_freedom / (centered.sample_count - 1)
        ),
        "variance_effective_sample_size": centered.variance_effective_sample_size,
        "operator_effective_sample_size": centered.operator_effective_sample_size,
        "known_mean_relative_radius": known_radius,
        "centered_relative_radius": centered_radius,
        "trial_count": len(trials),
    }
    for field in ("known_mean_error", "centered_error", "ordinary_centered_error"):
        values = np.asarray([trial[field] for trial in trials])
        record[f"mean_{field}"] = float(np.mean(values))
        record[f"quantile_95_{field}"] = float(np.quantile(values, 0.95))
        record[f"maximum_{field}"] = float(np.max(values))
    record["maximum_translation_discrepancy"] = max(
        trial["translation_discrepancy"] for trial in trials
    )
    for field in ("known_mean_covered", "centered_covered"):
        successes = sum(trial[field] for trial in trials)
        record[f"{field}_rate"] = successes / len(trials)
        record[f"{field}_wilson_95"] = wilson_interval(successes, len(trials))
    return record


def plot_results(records, output):
    phi = np.asarray([record["autocorrelation"] for record in records])
    normalizer = np.asarray(
        [record["normalizer_relative_to_n_minus_one"] for record in records]
    )
    known_q95 = np.asarray(
        [record["quantile_95_known_mean_error"] for record in records]
    )
    centered_q95 = np.asarray(
        [record["quantile_95_centered_error"] for record in records]
    )
    ordinary_q95 = np.asarray(
        [record["quantile_95_ordinary_centered_error"] for record in records]
    )
    known_radius = np.asarray(
        [record["known_mean_relative_radius"] for record in records]
    )
    centered_radius = np.asarray(
        [record["centered_relative_radius"] for record in records]
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.2), constrained_layout=True)

    axes[0, 0].plot(phi, normalizer, "o-")
    axes[0, 0].axhline(1.0, color="black", ls=":")
    axes[0, 0].set_title("Correct centering normalization")
    axes[0, 0].set_ylabel(r"$d_R/(N-1)$")

    axes[0, 1].plot(phi, known_q95, "o-", label="known mean")
    axes[0, 1].plot(phi, centered_q95, "s-", label="estimated mean, corrected")
    axes[0, 1].plot(phi, ordinary_q95, "^-", label="ordinary N-1")
    axes[0, 1].set_title("Empirical 95th-percentile covariance error")
    axes[0, 1].set_ylabel("population-whitened spectral error")
    axes[0, 1].legend(frameon=False)

    axes[1, 0].plot(
        phi,
        100 * np.asarray([record["known_mean_covered_rate"] for record in records]),
        "o-",
        label="known-mean theorem",
    )
    axes[1, 0].plot(
        phi,
        100 * np.asarray([record["centered_covered_rate"] for record in records]),
        "s-",
        label="centered theorem",
    )
    axes[1, 0].set_title("Recorded covariance-event frequency")
    axes[1, 0].set_ylabel("trials covered (%)")
    axes[1, 0].set_ylim(-3, 103)
    axes[1, 0].legend(frameon=False)

    axes[1, 1].plot(phi, known_radius / known_q95, "o-", label="known mean")
    axes[1, 1].plot(
        phi, centered_radius / centered_q95, "s-", label="estimated mean"
    )
    axes[1, 1].axhline(1.0, color="black", ls=":")
    axes[1, 1].set_title("Radius relative to empirical 95th percentile")
    axes[1, 1].set_ylabel("radius / empirical percentile")
    axes[1, 1].legend(frameon=False)

    for axis in axes.flat:
        axis.set_xlabel(r"AR(1) autocorrelation $\phi$")
        axis.grid(alpha=0.25)
    figure.suptitle(
        "Mean-centered covariance under dependent Gaussian sampling", fontsize=14
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=128)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--sample-count", type=int, default=50_000)
    parser.add_argument("--dimension", type=int, default=10)
    args = parser.parse_args()
    if args.trials < 2 or args.jobs < 1:
        raise ValueError("require at least two trials and one worker")
    autocorrelations = (0.0, 0.25, 0.50, 0.70, 0.85, 0.93, 0.97)
    confidence = 0.975
    root_seed = 20260930
    children = np.random.SeedSequence(root_seed).spawn(
        len(autocorrelations) * args.trials
    )
    tasks = []
    envelopes = {}
    radii = {}
    for index, autocorrelation in enumerate(autocorrelations):
        known = gaussian_ar1_temporal_correlation_envelope(
            args.sample_count, autocorrelation
        )
        centered = gaussian_ar1_centered_temporal_correlation_envelope(
            args.sample_count, autocorrelation
        )
        known_radius = gaussian_dependent_relative_covariance_error_bound(
            args.dimension,
            1,
            args.sample_count,
            temporal_correlation_frobenius_norm=known.frobenius_norm_bound,
            temporal_correlation_spectral_norm=known.spectral_norm_bound,
            confidence=confidence,
        )
        centered_radius = gaussian_dependent_centered_relative_covariance_error_bound(
            args.dimension,
            1,
            centering_degrees_of_freedom=centered.centering_degrees_of_freedom,
            projected_temporal_frobenius_norm=(
                centered.projected_frobenius_norm_bound
            ),
            projected_temporal_spectral_norm=(
                centered.projected_spectral_norm_bound
            ),
            confidence=confidence,
        )
        envelopes[autocorrelation] = centered
        radii[autocorrelation] = (known_radius, centered_radius)
        for child in children[index * args.trials : (index + 1) * args.trials]:
            tasks.append(
                (
                    args.sample_count,
                    args.dimension,
                    autocorrelation,
                    centered.centering_degrees_of_freedom,
                    int(child.generate_state(1, dtype=np.uint64)[0]),
                    known_radius,
                    centered_radius,
                )
            )
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        trial_results = list(executor.map(evaluate_trial, tasks))
    records = []
    for index, autocorrelation in enumerate(autocorrelations):
        trials = trial_results[index * args.trials : (index + 1) * args.trials]
        known_radius, centered_radius = radii[autocorrelation]
        records.append(
            aggregate(
                autocorrelation,
                envelopes[autocorrelation],
                known_radius,
                centered_radius,
                trials,
            )
        )
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "sampling_model": (
            "Gaussian observations with unknown constant spatial mean, temporal "
            "correlation R_ij=phi^abs(i-j), and identity spatial covariance"
        ),
        "sample_count": args.sample_count,
        "block_dimension": args.dimension,
        "simultaneous_block_count": 1,
        "confidence": confidence,
        "trials_per_autocorrelation": args.trials,
        "records": records,
    }
    json_output = root / "docs" / "dependent_centered_gaussian_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "dependent_centered_gaussian_calibration.png"
    plot_results(records, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"phi={record['autocorrelation']:.2f}",
            f"dR={record['centering_degrees_of_freedom']:.3f}",
            f"error95={record['quantile_95_centered_error']:.4f}",
            f"coverage={record['centered_covered_rate']:.3f}",
        )


if __name__ == "__main__":
    main()
