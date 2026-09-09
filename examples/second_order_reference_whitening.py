"""Experiment AO: second-order tau certification and reference whitening.

The experiment reuses the deterministic Proposition 53B calibration and target
geometry. It compares the original first-derivative outer cover and raw target
covariance certificate against Proposition 54's second-order cell certificate
and calibration-derived reference whitening.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.irregular_relaxation_evalue import (
    gaussian_irregular_relaxation_evalue_grid,
    gaussian_irregular_relaxation_evalue_model,
    gaussian_irregular_relaxation_evalue_outer_cover,
    gaussian_irregular_relaxation_target_matrix_chernoff_bound,
)
from observer_math.physical_relaxation import exponential_relaxation_covariance
from observer_math.second_order_relaxation import (
    gaussian_irregular_relaxation_second_order_outer_cover,
    gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "second_order_reference_whitening.json"


def _calibration_times() -> np.ndarray:
    gaps = np.array(
        [
            0.03,
            0.05,
            0.08,
            0.04,
            0.11,
            0.07,
            0.15,
            0.06,
            0.09,
            0.13,
            0.05,
            0.17,
            0.08,
            0.12,
            0.04,
            0.10,
            0.14,
            0.06,
            0.18,
            0.07,
            0.09,
            0.16,
            0.05,
            0.11,
            0.20,
            0.08,
            0.13,
            0.06,
            0.15,
            0.09,
            0.12,
        ],
        dtype=float,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _simulate(
    sample_times: np.ndarray,
    relaxation_time: float,
    channel_count: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    values = np.empty((sample_times.size, channel_count), dtype=float)
    values[0] = rng.standard_normal(channel_count)
    alpha = np.exp(-np.diff(sample_times) / relaxation_time)
    for index, coefficient in enumerate(alpha):
        values[index + 1] = (
            coefficient * values[index]
            + np.sqrt(1.0 - coefficient * coefficient)
            * rng.standard_normal(channel_count)
        )
    return values


def _target_geometry() -> tuple[np.ndarray, np.ndarray]:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10]),
        119,
    )
    times = np.concatenate(([0.0], np.cumsum(gaps)))
    centered = times - np.mean(times)
    design = np.column_stack((np.ones(times.size), centered))
    return times, design


def _projector(design: np.ndarray) -> np.ndarray:
    basis, _ = np.linalg.qr(design, mode="complete")
    complement = basis[:, design.shape[1] :]
    return complement @ complement.T


def _dense_target_cover_check(
    target_times: np.ndarray,
    result,
) -> dict[str, float]:
    whitening = result.reference_whitening_matrix
    projector = _projector(result.transformed_nuisance_design)
    outer = result.calibration_outer_cover
    maximum_operator_error = 0.0
    maximum_normalization_error = 0.0

    for index in np.flatnonzero(outer.retained_mask):
        lower = float(outer.cell_edges[index])
        upper = float(outer.cell_edges[index + 1])
        center = float(outer.cell_centers[index])
        center_covariance = (
            whitening
            @ exponential_relaxation_covariance(target_times, center)
            @ whitening.T
        )
        center_degrees = float(np.trace(projector @ center_covariance))
        for tau in np.linspace(lower, upper, 21):
            covariance = (
                whitening
                @ exponential_relaxation_covariance(target_times, float(tau))
                @ whitening.T
            )
            maximum_operator_error = max(
                maximum_operator_error,
                float(np.linalg.norm(covariance - center_covariance, ord=2)),
            )
            maximum_normalization_error = max(
                maximum_normalization_error,
                abs(float(np.trace(projector @ covariance)) - center_degrees),
            )

    return {
        "maximum_observed_operator_error": maximum_operator_error,
        "maximum_observed_normalization_error": maximum_normalization_error,
        "operator_error_to_certificate_ratio": (
            maximum_operator_error / result.temporal_covering_radius
        ),
        "normalization_error_to_certificate_ratio": (
            maximum_normalization_error / result.normalization_covering_radius
        ),
    }


def build_record() -> dict[str, object]:
    true_tau = 0.78
    lower_tau = 0.40
    upper_tau = 1.25
    confidence = 0.975
    cell_count = 160

    calibration_times = _calibration_times()
    calibration_values = _simulate(
        calibration_times,
        true_tau,
        96,
        seed=20261110,
    )
    model = gaussian_irregular_relaxation_evalue_model(
        calibration_values,
        calibration_times,
        lower_relaxation_time=lower_tau,
        upper_relaxation_time=upper_tau,
        confidence=confidence,
        mixture_relaxation_time_grid_size=21,
    )
    diagnostic = gaussian_irregular_relaxation_evalue_grid(
        model,
        relaxation_time_grid_size=1001,
    )
    first_order = gaussian_irregular_relaxation_evalue_outer_cover(
        model,
        cell_count=cell_count,
    )
    second_order = gaussian_irregular_relaxation_second_order_outer_cover(
        model,
        cell_count=cell_count,
    )

    target_times, target_design = _target_geometry()
    raw_target = gaussian_irregular_relaxation_target_matrix_chernoff_bound(
        model,
        target_times,
        target_design,
        block_dimension=1,
        block_count=1,
        outer_cover_cell_count=cell_count,
        covariance_confidence=confidence,
        upper_theta_grid_size=1024,
        lower_theta_grid_size=1024,
    )
    whitened_target = (
        gaussian_reference_whitened_irregular_relaxation_target_matrix_chernoff_bound(
            model,
            target_times,
            target_design,
            block_dimension=1,
            block_count=1,
            outer_cover_cell_count=cell_count,
            covariance_confidence=confidence,
            upper_theta_grid_size=1024,
            lower_theta_grid_size=1024,
        )
    )

    whitened_identity = (
        whitened_target.reference_whitening_matrix
        @ exponential_relaxation_covariance(
            target_times,
            whitened_target.reference_relaxation_time,
        )
        @ whitened_target.reference_whitening_matrix.T
    )
    dense_target_check = _dense_target_cover_check(target_times, whitened_target)

    first_width = (
        first_order.retained_relaxation_time_upper_bound
        - first_order.retained_relaxation_time_lower_bound
    )
    second_width = (
        second_order.retained_relaxation_time_upper_bound
        - second_order.retained_relaxation_time_lower_bound
    )

    return {
        "experiment": "AO",
        "title": "Second-order physical-time certification and reference whitening",
        "model": {
            "true_relaxation_time_seconds": true_tau,
            "declared_interval_seconds": [lower_tau, upper_tau],
            "calibration_confidence": confidence,
            "covariance_confidence": confidence,
            "combined_confidence": whitened_target.combined_confidence,
            "calibration_channel_count": 96,
            "calibration_sample_count": int(calibration_times.size),
            "target_sample_count": int(target_times.size),
            "target_nuisance_rank": int(target_design.shape[1]),
            "cell_count": cell_count,
        },
        "diagnostic_continuum": {
            "grid_size": int(diagnostic.total_point_count),
            "accepted_lower_seconds": diagnostic.accepted_relaxation_time_lower_bound,
            "accepted_upper_seconds": diagnostic.accepted_relaxation_time_upper_bound,
            "tau_grid_seconds": diagnostic.relaxation_time_grid.tolist(),
            "log_evalues": diagnostic.log_evalues.tolist(),
            "log_evalue_threshold": model.log_evalue_threshold,
        },
        "first_order_certificate": {
            "retained_cell_count": first_order.retained_cell_count,
            "excluded_cell_count": first_order.excluded_cell_count,
            "retained_lower_seconds": first_order.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": first_order.retained_relaxation_time_upper_bound,
            "retained_width_seconds": first_width,
        },
        "second_order_certificate": {
            "retained_cell_count": second_order.retained_cell_count,
            "excluded_cell_count": second_order.excluded_cell_count,
            "retained_lower_seconds": second_order.retained_relaxation_time_lower_bound,
            "retained_upper_seconds": second_order.retained_relaxation_time_upper_bound,
            "retained_width_seconds": second_width,
            "maximum_log_likelihood_second_derivative_bound": (
                second_order.maximum_log_likelihood_second_derivative_bound
            ),
            "maximum_interpolation_error_bound": (
                second_order.maximum_interpolation_error_bound
            ),
            "width_reduction_factor_vs_first_order": first_width / second_width,
            "retained_cell_reduction_factor_vs_first_order": (
                first_order.retained_cell_count / second_order.retained_cell_count
            ),
            "cell_edges_seconds": second_order.cell_edges.tolist(),
            "retained_mask": second_order.retained_mask.tolist(),
        },
        "raw_target_certificate": {
            "temporal_cover_point_count": raw_target.covariance_bound.cover_point_count,
            "eigenvalue_covering_radius": raw_target.target_eigenvalue_covering_radius,
            "normalization_covering_radius": (
                raw_target.target_normalization_covering_radius
            ),
            "projected_degrees_of_freedom_lower_bound": (
                raw_target.covariance_bound.projected_degrees_of_freedom_lower_bound
            ),
            "projected_spectral_norm_bound": (
                raw_target.covariance_bound.projected_spectral_norm_bound
            ),
            "covariance_relative_error": (
                raw_target.covariance_bound.covariance_relative_error
            ),
        },
        "reference_whitened_target_certificate": {
            "reference_relaxation_time_seconds": (
                whitened_target.reference_relaxation_time
            ),
            "temporal_cover_point_count": (
                whitened_target.covariance_bound.cover_point_count
            ),
            "temporal_covering_radius": whitened_target.temporal_covering_radius,
            "normalization_covering_radius": (
                whitened_target.normalization_covering_radius
            ),
            "maximum_center_temporal_derivative_norm": (
                whitened_target.maximum_center_temporal_derivative_norm
            ),
            "maximum_temporal_second_derivative_bound": (
                whitened_target.maximum_temporal_second_derivative_bound
            ),
            "maximum_center_normalization_derivative": (
                whitened_target.maximum_center_normalization_derivative
            ),
            "maximum_normalization_second_derivative_bound": (
                whitened_target.maximum_normalization_second_derivative_bound
            ),
            "projected_degrees_of_freedom_lower_bound": (
                whitened_target.covariance_bound.projected_degrees_of_freedom_lower_bound
            ),
            "projected_degrees_of_freedom_upper_bound": (
                whitened_target.covariance_bound.projected_degrees_of_freedom_upper_bound
            ),
            "projected_spectral_norm_bound": (
                whitened_target.covariance_bound.projected_spectral_norm_bound
            ),
            "oracle_relative_error": (
                whitened_target.covariance_bound.oracle_relative_error
            ),
            "covariance_relative_error": (
                whitened_target.covariance_bound.covariance_relative_error
            ),
            "reference_whitening_identity_max_abs_error": float(
                np.max(np.abs(whitened_identity - np.eye(target_times.size)))
            ),
        },
        "dense_target_visibility_check": dense_target_check,
        "interpretation": {
            "closed_bottleneck": (
                "On the same controlled target geometry as Experiment AN, the certified "
                "relative covariance radius moves from above one to below one."
            ),
            "why_second_order_helps": (
                "Endpoint interpolation pays a cell-width-squared curvature remainder "
                "instead of a cell-width first-derivative remainder."
            ),
            "why_reference_whitening_helps": (
                "The calibration-derived Proposition 53A whitener makes the target "
                "temporal covariance close to identity over the retained tau cells."
            ),
            "scope": (
                "The result remains conditional on independent standardized Gaussian "
                "calibration channels, one exponential relaxation time, a fixed target "
                "nuisance design, separable Gaussian target fluctuations, and calibration "
                "independence from the target record."
            ),
            "not_established": (
                "The experiment does not establish that a real system has one exponential "
                "timescale, does not identify an observer boundary by itself, and does not "
                "establish consciousness."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
