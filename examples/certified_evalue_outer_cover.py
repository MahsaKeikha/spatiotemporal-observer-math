"""Experiment AL: certify a Proposition 51 continuum set for target covariance use."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.evalue_outer_cover import (
    gaussian_evalue_outer_cover_matrix_chernoff_bound,
    separable_gaussian_evalue_outer_cover_projected_covariance,
)
from observer_math.evalue_temporal_family import (
    gaussian_ar1_white_noise_evalue_grid,
    gaussian_ar1_white_noise_evalue_model,
    gaussian_ar1_white_noise_log_evalue,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = REPO_ROOT / "docs" / "certified_evalue_outer_cover.json"


def temporal_covariance(sample_count: int, phi: float, eta: float) -> np.ndarray:
    indices = np.arange(sample_count)
    ar1 = phi ** np.abs(indices[:, None] - indices[None, :])
    return (1.0 - eta) * ar1 + eta * np.eye(sample_count)


def simulate_calibration(
    sample_count: int,
    channel_count: int,
    phi: float,
    eta: float,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    temporal = temporal_covariance(sample_count, phi, eta)
    return np.linalg.cholesky(temporal) @ rng.normal(
        size=(sample_count, channel_count)
    )


def main() -> None:
    calibration_sample_count = 48
    calibration_channel_count = 256
    true_phi = 0.50
    true_eta = 0.01
    calibration_seed = 20261122
    target_seed = 20261123

    calibration = simulate_calibration(
        calibration_sample_count,
        calibration_channel_count,
        true_phi,
        true_eta,
        calibration_seed,
    )
    model = gaussian_ar1_white_noise_evalue_model(
        calibration,
        lower_autocorrelation=0.30,
        upper_autocorrelation=0.70,
        lower_white_noise_fraction=0.0,
        upper_white_noise_fraction=0.05,
        confidence=0.975,
        contrast_dimension=6,
        mixture_autocorrelation_grid_size=9,
        mixture_white_noise_fraction_grid_size=7,
    )

    pointwise = gaussian_ar1_white_noise_evalue_grid(
        model,
        autocorrelation_grid_size=121,
        white_noise_fraction_grid_size=61,
    )

    target_sample_count = 120
    target_time = np.linspace(-1.0, 1.0, target_sample_count)
    nuisance_design = np.column_stack((np.ones_like(target_time), target_time))
    bound = gaussian_evalue_outer_cover_matrix_chernoff_bound(
        model,
        block_dimension=1,
        block_count=1,
        nuisance_design=nuisance_design,
        outer_autocorrelation_grid_size=121,
        outer_white_noise_fraction_grid_size=61,
        covariance_confidence=0.975,
        upper_theta_grid_size=96,
        lower_theta_grid_size=96,
    )

    outer = bound.outer_cover
    covariance = bound.covariance_bound
    retained = outer.retained_parameter_centers

    rng = np.random.default_rng(target_seed)
    target_temporal = temporal_covariance(target_sample_count, true_phi, true_eta)
    target_factor = np.linalg.cholesky(target_temporal)
    nuisance_coefficients = np.array([[8.0], [-5.0]])

    empirical_errors = []
    nuisance_invariance_errors = []
    for _ in range(128):
        target = target_factor @ rng.normal(size=(target_sample_count, 1))
        shifted = target + nuisance_design @ nuisance_coefficients
        estimate = separable_gaussian_evalue_outer_cover_projected_covariance(
            target,
            nuisance_design,
            bound,
        )
        shifted_estimate = separable_gaussian_evalue_outer_cover_projected_covariance(
            shifted,
            nuisance_design,
            bound,
        )
        empirical_errors.append(abs(float(estimate[0, 0]) - 1.0))
        nuisance_invariance_errors.append(
            abs(float(shifted_estimate[0, 0] - estimate[0, 0]))
        )

    empirical = np.asarray(empirical_errors)
    nuisance_errors = np.asarray(nuisance_invariance_errors)
    theorem_radius = covariance.covariance_relative_error

    result = {
        "experiment": "AL",
        "proposition": 52,
        "calibration_seed": calibration_seed,
        "target_seed": target_seed,
        "calibration_sample_count": calibration_sample_count,
        "calibration_channel_count": calibration_channel_count,
        "contrast_dimension": model.contrast_dimension,
        "true_autocorrelation": true_phi,
        "true_white_noise_fraction": true_eta,
        "declared_autocorrelation_lower_bound": 0.30,
        "declared_autocorrelation_upper_bound": 0.70,
        "declared_white_noise_fraction_lower_bound": 0.0,
        "declared_white_noise_fraction_upper_bound": 0.05,
        "calibration_confidence": bound.calibration_confidence,
        "covariance_confidence": bound.covariance_confidence,
        "combined_confidence_lower_bound": bound.combined_confidence_lower_bound,
        "true_log_evalue": gaussian_ar1_white_noise_log_evalue(
            model,
            true_phi,
            true_eta,
        ),
        "log_evalue_threshold": model.log_evalue_threshold,
        "pointwise_visualization_grid_size": pointwise.total_point_count,
        "pointwise_accepted_grid_points": pointwise.accepted_point_count,
        "pointwise_accepted_autocorrelation_lower_bound": (
            pointwise.accepted_autocorrelation_lower_bound
        ),
        "pointwise_accepted_autocorrelation_upper_bound": (
            pointwise.accepted_autocorrelation_upper_bound
        ),
        "pointwise_accepted_white_noise_fraction_lower_bound": (
            pointwise.accepted_white_noise_fraction_lower_bound
        ),
        "pointwise_accepted_white_noise_fraction_upper_bound": (
            pointwise.accepted_white_noise_fraction_upper_bound
        ),
        "outer_cover_total_cells": outer.total_cell_count,
        "outer_cover_retained_cells": outer.retained_cell_count,
        "outer_cover_excluded_cells": outer.excluded_cell_count,
        "outer_cover_retained_fraction": (
            outer.retained_cell_count / outer.total_cell_count
        ),
        "outer_cover_autocorrelation_lower_bound": float(retained[:, 0].min()),
        "outer_cover_autocorrelation_upper_bound": float(retained[:, 0].max()),
        "outer_cover_white_noise_fraction_lower_bound": float(retained[:, 1].min()),
        "outer_cover_white_noise_fraction_upper_bound": float(retained[:, 1].max()),
        "maximum_calibration_compressed_cell_radius": (
            outer.calibration_operator_cell_radius
        ),
        "target_sample_count": target_sample_count,
        "target_nuisance_rank": nuisance_design.shape[1],
        "block_dimension": covariance.block_dimension,
        "block_count": covariance.block_count,
        "target_eigenvalue_covering_radius": bound.target_eigenvalue_covering_radius,
        "target_normalization_covering_radius": (
            bound.target_normalization_covering_radius
        ),
        "projected_degrees_of_freedom_lower_bound": (
            covariance.projected_degrees_of_freedom_lower_bound
        ),
        "projected_degrees_of_freedom_upper_bound": (
            covariance.projected_degrees_of_freedom_upper_bound
        ),
        "reference_projected_degrees_of_freedom": (
            covariance.reference_projected_degrees_of_freedom
        ),
        "projected_spectral_norm_bound": covariance.projected_spectral_norm_bound,
        "oracle_upper_deviation": covariance.oracle_upper_deviation,
        "oracle_lower_deviation": covariance.oracle_lower_deviation,
        "covariance_relative_error": theorem_radius,
        "empirical_target_trials": int(empirical.size),
        "empirical_target_covered_trials": int(np.sum(empirical <= theorem_radius)),
        "empirical_median_relative_error": float(np.median(empirical)),
        "empirical_q95_relative_error": float(np.quantile(empirical, 0.95)),
        "empirical_max_relative_error": float(np.max(empirical)),
        "maximum_nuisance_invariance_error": float(np.max(nuisance_errors)),
        "scope_note": (
            "The outer cover is certified for the complete Proposition 51 continuum set. "
            "The pointwise grid is only a visualization. The target record is independent "
            "of the calibration record and shares the same controlled temporal parameters."
        ),
    }

    OUTPUT_PATH.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
