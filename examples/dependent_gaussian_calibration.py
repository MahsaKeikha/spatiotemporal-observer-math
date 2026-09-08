"""Calibrate the relative covariance theorem under Gaussian AR(1) dependence."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

from observer_math import (
    gaussian_ar1_temporal_correlation_envelope,
    gaussian_dependent_relative_covariance_error_bound,
    gaussian_wishart_relative_covariance_error_bound,
)

if __package__:
    from examples.gaussian_screen_calibration import wilson_interval
else:
    from gaussian_screen_calibration import wilson_interval


def ar1_standardized_observations(sample_count, dimension, autocorrelation, seed):
    """Draw an exactly stationary standardized Gaussian AR(1) sequence."""
    rng = np.random.default_rng(seed)
    innovations = rng.normal(size=(sample_count, dimension))
    initial = rng.normal(size=dimension)
    innovation_scale = np.sqrt(1.0 - autocorrelation**2)
    observations, _ = lfilter(
        [innovation_scale],
        [1.0, -autocorrelation],
        innovations,
        axis=0,
        zi=(autocorrelation * initial)[None, :],
    )
    return observations


def evaluate_trial(task):
    sample_count, dimension, autocorrelation, seed, iid_radius, dependent_radius = task
    observations = ar1_standardized_observations(
        sample_count, dimension, autocorrelation, seed
    )
    covariance = observations.T @ observations / sample_count
    relative_error = float(np.linalg.norm(covariance - np.eye(dimension), ord=2))
    return {
        "relative_error": relative_error,
        "iid_covered": relative_error <= iid_radius,
        "dependent_covered": relative_error <= dependent_radius,
    }


def aggregate(autocorrelation, envelope, iid_radius, dependent_radius, trials):
    errors = np.asarray([trial["relative_error"] for trial in trials])
    record = {
        "autocorrelation": autocorrelation,
        "frobenius_norm_bound": envelope.frobenius_norm_bound,
        "spectral_norm_bound": envelope.spectral_norm_bound,
        "variance_effective_sample_size": envelope.variance_effective_sample_size,
        "operator_effective_sample_size": envelope.operator_effective_sample_size,
        "iid_relative_radius": iid_radius,
        "dependent_relative_radius": dependent_radius,
        "trial_count": len(trials),
        "mean_relative_error": float(np.mean(errors)),
        "standard_error_relative_error": float(
            np.std(errors, ddof=1) / np.sqrt(len(errors))
        ),
        "quantile_95_relative_error": float(np.quantile(errors, 0.95)),
        "maximum_relative_error": float(np.max(errors)),
    }
    for name in ("iid_covered", "dependent_covered"):
        successes = sum(trial[name] for trial in trials)
        record[f"{name}_rate"] = successes / len(trials)
        record[f"{name}_wilson_95"] = wilson_interval(successes, len(trials))
    return record


def plot_results(records, sample_count, output):
    autocorrelation = np.asarray([record["autocorrelation"] for record in records])
    variance_fraction = np.asarray(
        [record["variance_effective_sample_size"] / sample_count for record in records]
    )
    operator_fraction = np.asarray(
        [record["operator_effective_sample_size"] / sample_count for record in records]
    )
    empirical_mean = np.asarray([record["mean_relative_error"] for record in records])
    empirical_95 = np.asarray(
        [record["quantile_95_relative_error"] for record in records]
    )
    iid_radius = np.asarray([record["iid_relative_radius"] for record in records])
    dependent_radius = np.asarray(
        [record["dependent_relative_radius"] for record in records]
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.2), constrained_layout=True)

    axes[0, 0].plot(autocorrelation, variance_fraction, "o-", label=r"$N_F/N$")
    axes[0, 0].plot(autocorrelation, operator_fraction, "s-", label=r"$N_{op}/N$")
    axes[0, 0].set_title("Effective sample fractions")
    axes[0, 0].set_ylabel("fraction of nominal sample count")
    axes[0, 0].legend(frameon=False)

    axes[0, 1].plot(autocorrelation, empirical_mean, "o-", label="mean error")
    axes[0, 1].plot(autocorrelation, empirical_95, "s-", label="95th percentile")
    axes[0, 1].plot(autocorrelation, iid_radius, "--", label="i.i.d. radius")
    axes[0, 1].plot(
        autocorrelation, dependent_radius, "--", label="dependent radius"
    )
    axes[0, 1].set_title("Population-whitened covariance error")
    axes[0, 1].set_ylabel("spectral error")
    axes[0, 1].legend(frameon=False)

    axes[1, 0].plot(
        autocorrelation,
        100 * np.asarray([record["iid_covered_rate"] for record in records]),
        "o-",
        label="i.i.d. formula",
    )
    axes[1, 0].plot(
        autocorrelation,
        100 * np.asarray([record["dependent_covered_rate"] for record in records]),
        "s-",
        label="dependent formula",
    )
    axes[1, 0].set_title("Recorded covariance-event frequency")
    axes[1, 0].set_ylabel("trials covered (%)")
    axes[1, 0].set_ylim(-3, 103)
    axes[1, 0].legend(frameon=False)

    axes[1, 1].plot(
        autocorrelation, iid_radius / empirical_95, "o-", label="i.i.d. radius"
    )
    axes[1, 1].plot(
        autocorrelation,
        dependent_radius / empirical_95,
        "s-",
        label="dependent radius",
    )
    axes[1, 1].axhline(1.0, color="black", ls=":")
    axes[1, 1].set_title("Radius relative to empirical 95th percentile")
    axes[1, 1].set_ylabel("radius / empirical percentile")
    axes[1, 1].legend(frameon=False)

    for axis in axes.flat:
        axis.set_xlabel(r"AR(1) autocorrelation $\phi$")
        axis.grid(alpha=0.25)
    figure.suptitle(
        "Relative covariance concentration under dependent Gaussian samples",
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
    confidence = 0.975
    iid_radius = gaussian_wishart_relative_covariance_error_bound(
        args.dimension, 1, args.sample_count, confidence=confidence
    )
    root_seed = 20260927
    children = np.random.SeedSequence(root_seed).spawn(
        len(autocorrelations) * args.trials
    )
    tasks = []
    envelopes = {}
    dependent_radii = {}
    for index, autocorrelation in enumerate(autocorrelations):
        envelope = gaussian_ar1_temporal_correlation_envelope(
            args.sample_count, autocorrelation
        )
        dependent_radius = gaussian_dependent_relative_covariance_error_bound(
            args.dimension,
            1,
            args.sample_count,
            temporal_correlation_frobenius_norm=envelope.frobenius_norm_bound,
            temporal_correlation_spectral_norm=envelope.spectral_norm_bound,
            confidence=confidence,
        )
        envelopes[autocorrelation] = envelope
        dependent_radii[autocorrelation] = dependent_radius
        for child in children[index * args.trials : (index + 1) * args.trials]:
            seed = int(child.generate_state(1, dtype=np.uint64)[0])
            tasks.append(
                (
                    args.sample_count,
                    args.dimension,
                    autocorrelation,
                    seed,
                    iid_radius,
                    dependent_radius,
                )
            )
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        trial_results = list(executor.map(evaluate_trial, tasks))
    records = []
    for index, autocorrelation in enumerate(autocorrelations):
        trials = trial_results[index * args.trials : (index + 1) * args.trials]
        records.append(
            aggregate(
                autocorrelation,
                envelopes[autocorrelation],
                iid_radius,
                dependent_radii[autocorrelation],
                trials,
            )
        )
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "sampling_model": (
            "known-zero-mean Gaussian observations with temporal correlation "
            "R_ij=phi^abs(i-j) and identity population covariance"
        ),
        "sample_count": args.sample_count,
        "block_dimension": args.dimension,
        "simultaneous_block_count": 1,
        "confidence": confidence,
        "trials_per_autocorrelation": args.trials,
        "records": records,
    }
    json_output = root / "docs" / "dependent_gaussian_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "dependent_gaussian_calibration.png"
    plot_results(records, args.sample_count, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"phi={record['autocorrelation']:.2f}",
            f"Neff={record['variance_effective_sample_size']:.1f}",
            f"error95={record['quantile_95_relative_error']:.4f}",
            f"coverage={record['iid_covered_rate']:.3f}/"
            f"{record['dependent_covered_rate']:.3f}",
        )


if __name__ == "__main__":
    main()
