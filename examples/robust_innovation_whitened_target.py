"""Experiment AR: propagate the Proposition 55 tau interval through whitening."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from observer_math.innovation_whitening import (
    gaussian_innovation_whitened_matrix_chernoff_bound,
)
from observer_math.matrix_chernoff import (
    gaussian_weighted_wishart_matrix_bound,
    projected_temporal_eigenvalues,
)
from observer_math.physical_relaxation import (
    exponential_relaxation_covariance,
    exponential_relaxation_markov_factorization,
)
from observer_math.robust_innovation_whitening import (
    gaussian_robust_innovation_whitened_matrix_chernoff_bound,
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "robust_innovation_whitened_target.json"


def _target_times() -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10], dtype=float),
        119,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _pointwise_radius(
    true_tau: float,
    working_tau: float,
    normalization: float,
    times: np.ndarray,
    design: np.ndarray,
) -> dict[str, float]:
    whitening = exponential_relaxation_markov_factorization(
        times,
        working_tau,
    ).whitening_matrix
    transformed_design = whitening @ design
    transformed_covariance = (
        whitening
        @ exponential_relaxation_covariance(times, true_tau)
        @ whitening.T
    )
    weights = projected_temporal_eigenvalues(
        transformed_covariance,
        transformed_design,
    )
    matrix_bound = gaussian_weighted_wishart_matrix_bound(
        1,
        1,
        weights,
        confidence=0.975,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    trace_ratio = float(np.sum(weights) / normalization)
    upper = float(trace_ratio * (1.0 + matrix_bound.upper_deviation) - 1.0)
    lower = float(max(0.0, 1.0 - trace_ratio * (1.0 - matrix_bound.lower_deviation)))
    return {
        "true_relaxation_time_seconds": float(true_tau),
        "projected_temporal_trace": float(np.sum(weights)),
        "projected_temporal_minimum_eigenvalue": float(np.min(weights)),
        "projected_temporal_maximum_eigenvalue": float(np.max(weights)),
        "normalization_ratio": trace_ratio,
        "upper_relative_deviation": upper,
        "lower_relative_deviation": lower,
        "pointwise_relative_radius": float(max(upper, lower)),
    }


def build_record() -> dict[str, object]:
    lower = 0.686875
    upper = 0.8515625
    true_tau = 0.78
    working = 0.5 * (lower + upper)
    calibration_confidence = 0.975
    covariance_confidence = 0.975
    times = _target_times()
    design = np.column_stack((np.ones(times.size), times - np.mean(times)))

    robust = gaussian_robust_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        block_dimension=1,
        block_count=1,
        lower_relaxation_time=lower,
        upper_relaxation_time=upper,
        working_relaxation_time=working,
        relaxation_time_grid_size=1025,
        confidence=covariance_confidence,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )
    exact = gaussian_innovation_whitened_matrix_chernoff_bound(
        times,
        design,
        block_dimension=1,
        block_count=1,
        relaxation_time=true_tau,
        confidence=covariance_confidence,
        upper_theta_grid_size=256,
        lower_theta_grid_size=256,
    )

    pointwise = [
        _pointwise_radius(tau, working, robust.covariance_normalization, times, design)
        for tau in (lower, working, true_tau, upper)
    ]

    covariance = robust.covariance_bound
    return {
        "experiment": "AR",
        "title": "Finite-sample tau uncertainty propagated through innovation whitening",
        "calibration_input": {
            "source_experiment": "AP",
            "source_proposition": 55,
            "retained_lower_seconds": lower,
            "retained_upper_seconds": upper,
            "retained_width_seconds": upper - lower,
            "calibration_confidence": calibration_confidence,
        },
        "target_model": {
            "true_relaxation_time_seconds_for_visibility": true_tau,
            "working_relaxation_time_seconds": working,
            "target_sample_count": int(times.size),
            "target_nuisance_rank": int(design.shape[1]),
            "residual_degrees_of_freedom": robust.residual_degrees_of_freedom,
            "covariance_confidence": covariance_confidence,
            "combined_calibration_target_confidence": (
                calibration_confidence * covariance_confidence
            ),
            "block_dimension": 1,
            "block_count": 1,
        },
        "certified_transformed_family_cover": {
            "relaxation_time_grid_size": robust.relaxation_time_grid_size,
            "maximum_relaxation_time_spacing_seconds": (
                robust.maximum_relaxation_time_spacing
            ),
            "raw_covariance_operator_lipschitz_bound_per_second": (
                robust.raw_covariance_operator_lipschitz_bound
            ),
            "whitening_operator_norm": robust.whitening_operator_norm,
            "transformed_operator_lipschitz_bound_per_second": (
                robust.transformed_operator_lipschitz_bound
            ),
            "transformed_normalization_lipschitz_bound_per_second": (
                robust.transformed_normalization_lipschitz_bound
            ),
            "transformed_eigenvalue_covering_radius": (
                robust.transformed_eigenvalue_covering_radius
            ),
            "transformed_normalization_covering_radius": (
                robust.transformed_normalization_covering_radius
            ),
        },
        "uniform_target_certificate": {
            "covariance_normalization": robust.covariance_normalization,
            "projected_degrees_of_freedom_lower_bound": (
                covariance.projected_degrees_of_freedom_lower_bound
            ),
            "projected_degrees_of_freedom_upper_bound": (
                covariance.projected_degrees_of_freedom_upper_bound
            ),
            "projected_spectral_norm_bound": covariance.projected_spectral_norm_bound,
            "oracle_upper_deviation": covariance.oracle_upper_deviation,
            "oracle_lower_deviation": covariance.oracle_lower_deviation,
            "final_upper_deviation": covariance.final_upper_deviation,
            "final_lower_deviation": covariance.final_lower_deviation,
            "covariance_relative_error": robust.covariance_relative_error,
            "crosses_relative_radius_one": bool(robust.covariance_relative_error < 1.0),
        },
        "comparison": {
            "proposition_55_raw_time_calibrated_radius": 2.4148799294322116,
            "proposition_55_raw_time_known_tau_oracle_radius": 2.167246895150515,
            "proposition_56_exact_tau_innovation_radius": exact.covariance_relative_error,
            "proposition_57_uncertain_tau_innovation_radius": robust.covariance_relative_error,
            "reduction_from_raw_time_calibrated_fraction": float(
                1.0 - robust.covariance_relative_error / 2.4148799294322116
            ),
        },
        "pointwise_diagnostics": pointwise,
        "interpretation": {
            "main_result": (
                "The full finite-sample Proposition 55 relaxation-time interval can be "
                "propagated through a single midpoint innovation whitener and still yields "
                "a uniform target covariance radius below one on the Experiment AP schedule."
            ),
            "operator_cover": (
                "The transformed eigenvalue cover uses ||W||_2^2 times the raw covariance "
                "operator-Lipschitz bound."
            ),
            "normalization_cover": (
                "Projected-trace uncertainty is certified separately from the operator "
                "cover by differentiating tr(P_G W R_tau W^T) and bounding its derivative "
                "entrywise over the full relaxation-time interval. This is rigorous and "
                "substantially tighter than residual_rank times the operator radius."
            ),
            "scope": (
                "The certificate remains conditional on the declared separable Gaussian "
                "one-timescale exponential relaxation model and on calibration and target "
                "records being separated as required by the finite-sample composition."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
