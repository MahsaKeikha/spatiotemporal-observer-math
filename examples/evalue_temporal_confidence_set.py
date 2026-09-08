"""Experiment AK: joint e-value geometry for temporal covariance calibration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from observer_math.calibrated_temporal_family import (
    gaussian_ar1_white_noise_increment_parameter_interval,
)
from observer_math.evalue_temporal_family import (
    gaussian_ar1_white_noise_evalue_grid,
    gaussian_ar1_white_noise_evalue_model,
    gaussian_ar1_white_noise_log_evalue,
)


def temporal_covariance(sample_count, phi, eta):
    indices = np.arange(sample_count)
    ar1 = phi ** np.abs(indices[:, None] - indices[None, :])
    return (1.0 - eta) * ar1 + eta * np.eye(sample_count)


def simulate_calibration(sample_count, channel_count, phi, eta, rng):
    temporal = temporal_covariance(sample_count, phi, eta)
    values = np.linalg.cholesky(temporal) @ rng.normal(
        size=(sample_count, channel_count)
    )
    offsets = rng.normal(scale=4.0, size=channel_count)
    return values + offsets[None, :]


def wilson_interval(successes, total, z=1.959963984540054):
    p = successes / total
    denominator = 1.0 + z**2 / total
    center = (p + z**2 / (2.0 * total)) / denominator
    half = z * np.sqrt(
        p * (1.0 - p) / total + z**2 / (4.0 * total**2)
    ) / denominator
    return [float(center - half), float(center + half)]


def run(seed=20261024):
    true_phi = 0.60
    true_eta = 0.04
    lower_phi = 0.40
    upper_phi = 0.80
    lower_eta = 0.0
    upper_eta = 0.25
    confidence = 0.9875
    sample_count = 100
    channel_counts = (32, 64, 128, 256)
    contrast_dimension = 30
    mixture_phi_count = 7
    mixture_eta_count = 5
    evaluation_phi_count = 33
    evaluation_eta_count = 26

    rng = np.random.default_rng(seed)
    all_values = simulate_calibration(
        sample_count,
        max(channel_counts),
        true_phi,
        true_eta,
        rng,
    )

    records = []
    for channel_count in channel_counts:
        values = all_values[:, :channel_count]
        rectangle = gaussian_ar1_white_noise_increment_parameter_interval(
            values,
            lower_autocorrelation=lower_phi,
            upper_autocorrelation=upper_phi,
            lower_white_noise_fraction=lower_eta,
            upper_white_noise_fraction=upper_eta,
            confidence=confidence,
        )
        model = gaussian_ar1_white_noise_evalue_model(
            values,
            lower_autocorrelation=lower_phi,
            upper_autocorrelation=upper_phi,
            lower_white_noise_fraction=lower_eta,
            upper_white_noise_fraction=upper_eta,
            confidence=confidence,
            contrast_dimension=contrast_dimension,
            mixture_autocorrelation_grid_size=mixture_phi_count,
            mixture_white_noise_fraction_grid_size=mixture_eta_count,
        )
        evaluation = gaussian_ar1_white_noise_evalue_grid(
            model,
            autocorrelation_grid_size=evaluation_phi_count,
            white_noise_fraction_grid_size=evaluation_eta_count,
        )

        rectangle_area = float(
            (rectangle.autocorrelation_upper_bound - rectangle.autocorrelation_lower_bound)
            * (
                rectangle.white_noise_fraction_upper_bound
                - rectangle.white_noise_fraction_lower_bound
            )
        )
        evalue_box_area = float(
            (
                evaluation.accepted_autocorrelation_upper_bound
                - evaluation.accepted_autocorrelation_lower_bound
            )
            * (
                evaluation.accepted_white_noise_fraction_upper_bound
                - evaluation.accepted_white_noise_fraction_lower_bound
            )
        )
        grid_view = {
            "accepted_point_count": evaluation.accepted_point_count,
            "total_point_count": evaluation.total_point_count,
            "accepted_fraction": (
                evaluation.accepted_point_count / evaluation.total_point_count
            ),
            "autocorrelation_lower": evaluation.accepted_autocorrelation_lower_bound,
            "autocorrelation_upper": evaluation.accepted_autocorrelation_upper_bound,
            "white_noise_fraction_lower": (
                evaluation.accepted_white_noise_fraction_lower_bound
            ),
            "white_noise_fraction_upper": (
                evaluation.accepted_white_noise_fraction_upper_bound
            ),
            "bounding_box_area": evalue_box_area,
            "bounding_box_area_ratio_to_proposition_50": (
                evalue_box_area / rectangle_area if rectangle_area > 0.0 else None
            ),
            "true_parameter_log_evalue": gaussian_ar1_white_noise_log_evalue(
                model, true_phi, true_eta
            ),
            "log_evalue_threshold": model.log_evalue_threshold,
        }
        if channel_count == max(channel_counts):
            grid_view["accepted_points"] = [
                [
                    float(evaluation.autocorrelation_grid[phi_index]),
                    float(evaluation.white_noise_fraction_grid[eta_index]),
                ]
                for phi_index, eta_index in zip(
                    *np.where(evaluation.accepted_mask),
                    strict=True,
                )
            ]

        records.append(
            {
                "channel_count": channel_count,
                "proposition_50_rectangle": {
                    "autocorrelation_lower": rectangle.autocorrelation_lower_bound,
                    "autocorrelation_upper": rectangle.autocorrelation_upper_bound,
                    "white_noise_fraction_lower": (
                        rectangle.white_noise_fraction_lower_bound
                    ),
                    "white_noise_fraction_upper": (
                        rectangle.white_noise_fraction_upper_bound
                    ),
                    "bounding_box_area": rectangle_area,
                },
                "proposition_51_grid_view": grid_view,
            }
        )

    coverage_trials = 256
    coverage_successes = 0
    true_log_evalues = []
    for trial in range(coverage_trials):
        trial_rng = np.random.default_rng(20261100 + trial)
        values = simulate_calibration(40, 32, true_phi, true_eta, trial_rng)
        model = gaussian_ar1_white_noise_evalue_model(
            values,
            lower_autocorrelation=lower_phi,
            upper_autocorrelation=upper_phi,
            lower_white_noise_fraction=lower_eta,
            upper_white_noise_fraction=upper_eta,
            confidence=confidence,
            contrast_dimension=10,
            mixture_autocorrelation_grid_size=7,
            mixture_white_noise_fraction_grid_size=5,
        )
        log_evalue = gaussian_ar1_white_noise_log_evalue(model, true_phi, true_eta)
        true_log_evalues.append(log_evalue)
        coverage_successes += int(log_evalue < model.log_evalue_threshold)

    return {
        "experiment": "AK",
        "seed": seed,
        "sampling_model": (
            "independent Gaussian calibration channels with arbitrary constant means "
            "and shared AR(1)-plus-white-noise temporal covariance"
        ),
        "true_autocorrelation": true_phi,
        "true_white_noise_fraction": true_eta,
        "declared_autocorrelation_interval": [lower_phi, upper_phi],
        "declared_white_noise_fraction_interval": [lower_eta, upper_eta],
        "confidence": confidence,
        "sample_count": sample_count,
        "contrast_dimension": contrast_dimension,
        "mixture_grid": [mixture_phi_count, mixture_eta_count],
        "visualization_grid": [evaluation_phi_count, evaluation_eta_count],
        "visualization_warning": (
            "Accepted grid points visualize the exact continuum e-value function. "
            "They are not a certified outer discretization of the continuum confidence set."
        ),
        "records": records,
        "coverage_visibility_check": {
            "sample_count": 40,
            "channel_count": 32,
            "contrast_dimension": 10,
            "trial_count": coverage_trials,
            "success_count": coverage_successes,
            "success_rate": coverage_successes / coverage_trials,
            "wilson_95": wilson_interval(coverage_successes, coverage_trials),
            "median_true_parameter_log_evalue": float(np.median(true_log_evalues)),
            "q95_true_parameter_log_evalue": float(
                np.quantile(true_log_evalues, 0.95)
            ),
            "maximum_true_parameter_log_evalue": float(np.max(true_log_evalues)),
            "log_evalue_threshold": float(np.log(1.0 / (1.0 - confidence))),
            "interpretation": (
                "This repeated-sampling run is a numerical visibility check. "
                "Proposition 51 supplies the coverage proof."
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20261024)
    parser.add_argument("--output-dir", type=Path, default=Path("docs"))
    args = parser.parse_args()

    results = run(seed=args.seed)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    output = args.output_dir / "evalue_temporal_confidence_set.json"
    output.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
