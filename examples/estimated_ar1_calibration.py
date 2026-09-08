"""Calibrate covariance recovery when a shared AR(1) coefficient is estimated."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math import (
    gaussian_ar1_centered_temporal_correlation_envelope,
    gaussian_ar1_increment_autocorrelation_interval,
    gaussian_dependent_centered_relative_covariance_error_bound,
    gaussian_estimated_ar1_centered_covariance_bound,
    separable_gaussian_centered_covariance,
)

if __package__:
    from examples.dependent_gaussian_calibration import ar1_standardized_observations
    from examples.gaussian_screen_calibration import wilson_interval
else:
    from dependent_gaussian_calibration import ar1_standardized_observations
    from gaussian_screen_calibration import wilson_interval


def evaluate_trial(task):
    sample_count, dimension, autocorrelation, upper_prior, seed, oracle_radius = task
    residuals = ar1_standardized_observations(
        sample_count, dimension, autocorrelation, seed
    )
    observations = residuals + np.linspace(-3.0, 4.0, dimension)
    interval = gaussian_ar1_increment_autocorrelation_interval(
        observations,
        declared_upper_bound=upper_prior,
        confidence=0.9875,
    )
    bound = gaussian_estimated_ar1_centered_covariance_bound(
        dimension,
        1,
        sample_count,
        interval,
        covariance_confidence=0.9875,
    )
    estimate = separable_gaussian_centered_covariance(
        observations, bound.reference_centering_degrees_of_freedom
    )
    error = float(np.linalg.norm(estimate - np.eye(dimension), ord=2))
    phi_covered = interval.lower_bound <= autocorrelation <= interval.upper_bound
    covariance_covered = error <= bound.covariance_relative_error
    return {
        "autocorrelation_estimate": interval.estimate,
        "autocorrelation_lower_bound": interval.lower_bound,
        "autocorrelation_upper_bound": interval.upper_bound,
        "autocorrelation_error_radius": interval.error_radius,
        "interval_intersects_declared_model": interval.interval_intersects_declared_model,
        "phi_covered": phi_covered,
        "covariance_error": error,
        "covariance_relative_radius": bound.covariance_relative_error,
        "oracle_relative_radius": oracle_radius,
        "normalization_error": bound.normalization_error,
        "covariance_covered": covariance_covered,
        "joint_event_covered": phi_covered and covariance_covered,
    }


def aggregate(autocorrelation, trials):
    record = {
        "autocorrelation": autocorrelation,
        "trial_count": len(trials),
        "all_intervals_compatible_with_declared_model": all(
            trial["interval_intersects_declared_model"] for trial in trials
        ),
    }
    for field in (
        "autocorrelation_estimate",
        "autocorrelation_lower_bound",
        "autocorrelation_upper_bound",
        "autocorrelation_error_radius",
        "covariance_error",
        "covariance_relative_radius",
        "oracle_relative_radius",
        "normalization_error",
    ):
        values = np.asarray([trial[field] for trial in trials])
        record[f"mean_{field}"] = float(np.mean(values))
        record[f"quantile_05_{field}"] = float(np.quantile(values, 0.05))
        record[f"quantile_95_{field}"] = float(np.quantile(values, 0.95))
        record[f"maximum_{field}"] = float(np.max(values))
    for field in ("phi_covered", "covariance_covered", "joint_event_covered"):
        successes = sum(trial[field] for trial in trials)
        record[f"{field}_rate"] = successes / len(trials)
        record[f"{field}_wilson_95"] = wilson_interval(successes, len(trials))
    return record


def plot_results(records, output):
    phi = np.asarray([record["autocorrelation"] for record in records])
    mean_estimate = np.asarray(
        [record["mean_autocorrelation_estimate"] for record in records]
    )
    lower = np.asarray(
        [record["mean_autocorrelation_lower_bound"] for record in records]
    )
    upper = np.asarray(
        [record["mean_autocorrelation_upper_bound"] for record in records]
    )
    empirical_q95 = np.asarray(
        [record["quantile_95_covariance_error"] for record in records]
    )
    estimated_radius = np.asarray(
        [record["mean_covariance_relative_radius"] for record in records]
    )
    oracle_radius = np.asarray(
        [record["mean_oracle_relative_radius"] for record in records]
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.2), constrained_layout=True)

    axes[0, 0].fill_between(phi, lower, upper, alpha=0.22, label="mean confidence interval")
    axes[0, 0].plot(phi, mean_estimate, "o-", label="mean estimate")
    axes[0, 0].plot(phi, phi, "k:", label="true coefficient")
    axes[0, 0].set_title("Increment-based AR(1) estimation")
    axes[0, 0].set_ylabel("estimated correlation")
    axes[0, 0].legend(frameon=False)

    axes[0, 1].plot(
        phi,
        100 * np.asarray([record["phi_covered_rate"] for record in records]),
        "o-",
        label="correlation interval",
    )
    axes[0, 1].plot(
        phi,
        100 * np.asarray([record["joint_event_covered_rate"] for record in records]),
        "s-",
        label="joint correlation + covariance",
    )
    axes[0, 1].axhline(97.5, color="black", ls=":", label="joint guarantee")
    axes[0, 1].set_ylim(90, 101)
    axes[0, 1].set_title("Recorded event frequency")
    axes[0, 1].set_ylabel("trials covered (%)")
    axes[0, 1].legend(frameon=False)

    axes[1, 0].plot(phi, empirical_q95, "o-", label="empirical 95th percentile")
    axes[1, 0].plot(phi, oracle_radius, "s--", label="known-correlation radius")
    axes[1, 0].plot(phi, estimated_radius, "^--", label="estimated-correlation radius")
    axes[1, 0].set_title("Centered covariance error")
    axes[1, 0].set_ylabel("population-whitened spectral error")
    axes[1, 0].legend(frameon=False)

    axes[1, 1].plot(phi, estimated_radius / oracle_radius, "o-", label="radius inflation")
    axes[1, 1].plot(
        phi,
        np.asarray([record["mean_normalization_error"] for record in records]),
        "s-",
        label="normalization uncertainty",
    )
    axes[1, 1].axhline(1.0, color="black", ls=":")
    axes[1, 1].set_title("Cost of estimating temporal dependence")
    axes[1, 1].set_ylabel("ratio or absolute error")
    axes[1, 1].legend(frameon=False)

    for axis in axes.flat:
        axis.set_xlabel(r"AR(1) autocorrelation $\phi$")
        axis.grid(alpha=0.25)
    figure.suptitle(
        "Same-record temporal calibration and centered covariance recovery",
        fontsize=14,
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
    upper_prior = 0.98
    root_seed = 20261004
    children = np.random.SeedSequence(root_seed).spawn(
        len(autocorrelations) * args.trials
    )
    tasks = []
    for index, autocorrelation in enumerate(autocorrelations):
        oracle = gaussian_ar1_centered_temporal_correlation_envelope(
            args.sample_count, autocorrelation
        )
        oracle_radius = gaussian_dependent_centered_relative_covariance_error_bound(
            args.dimension,
            1,
            centering_degrees_of_freedom=oracle.centering_degrees_of_freedom,
            projected_temporal_frobenius_norm=oracle.projected_frobenius_norm_bound,
            projected_temporal_spectral_norm=oracle.projected_spectral_norm_bound,
            confidence=0.9875,
        )
        for child in children[index * args.trials : (index + 1) * args.trials]:
            tasks.append(
                (
                    args.sample_count,
                    args.dimension,
                    autocorrelation,
                    upper_prior,
                    int(child.generate_state(1, dtype=np.uint64)[0]),
                    oracle_radius,
                )
            )
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        trial_results = list(executor.map(evaluate_trial, tasks))
    records = []
    for index, autocorrelation in enumerate(autocorrelations):
        trials = trial_results[index * args.trials : (index + 1) * args.trials]
        records.append(aggregate(autocorrelation, trials))

    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "sampling_model": (
            "Independent unit-variance Gaussian spatial channels with arbitrary "
            "constant means and a shared stationary nonnegative AR(1) coefficient"
        ),
        "sample_count": args.sample_count,
        "calibration_channel_count": args.dimension,
        "declared_autocorrelation_range": [0.0, upper_prior],
        "autocorrelation_confidence": 0.9875,
        "covariance_confidence": 0.9875,
        "union_bound_joint_confidence": 0.975,
        "trials_per_autocorrelation": args.trials,
        "same_record_used_for_both_events": True,
        "records": records,
    }
    json_output = root / "docs" / "estimated_ar1_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "estimated_ar1_calibration.png"
    plot_results(records, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"phi={record['autocorrelation']:.2f}",
            f"estimate={record['mean_autocorrelation_estimate']:.4f}",
            f"joint={record['joint_event_covered_rate']:.3f}",
            f"radius={record['mean_covariance_relative_radius']:.4f}",
        )


if __name__ == "__main__":
    main()
