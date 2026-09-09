"""Experiment AS: return covariance certification to world-tube recovery."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import numpy as np

from observer_math import (
    adjacent_joint_covariance,
    certify_worldtube,
    moving_module_systems,
    observer_metrics_from_covariances,
    propagate_covariances,
    transport_metrics,
)
from observer_math.gaussian import stationary_covariance
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "observer_bridge_dimension_audit.json"


def _target_times(sample_count: int = 120) -> np.ndarray:
    gaps = np.resize(
        np.array([0.04, 0.07, 0.05, 0.09, 0.06, 0.11, 0.08, 0.05, 0.10]),
        sample_count - 1,
    )
    return np.concatenate(([0.0], np.cumsum(gaps)))


def _log_unit_matrix_mgf_factor(
    dimension: int,
    x: np.ndarray,
    *,
    upper_tail: bool,
) -> np.ndarray:
    if upper_tail:
        log_chi = -0.5 * dimension * np.log1p(-2.0 * x)
        sign_term = -x
    else:
        log_chi = -0.5 * dimension * np.log1p(2.0 * x)
        sign_term = x
    if dimension == 1:
        log_bracket = log_chi
    else:
        log_bracket = (
            np.logaddexp(np.log(float(dimension - 1)), log_chi)
            - np.log(float(dimension))
        )
    return sign_term + log_bracket


def _unit_weight_matrix_radius(
    block_dimension: int,
    block_count: int,
    residual_degrees: int,
    *,
    confidence: float = 0.975,
    theta_grid_size: int = 1024,
) -> float:
    """Evaluate Proposition 47 exactly for repeated unit temporal weights."""
    log_prefactor = float(
        np.log(2.0 * block_count * block_dimension / (1.0 - confidence))
    )
    upper_x = np.geomspace(1e-8, 0.499999, theta_grid_size)
    upper = (
        log_prefactor
        + residual_degrees
        * _log_unit_matrix_mgf_factor(
            block_dimension,
            upper_x,
            upper_tail=True,
        )
    ) / upper_x / residual_degrees
    lower_x = np.geomspace(1e-8, 1e3, theta_grid_size)
    lower = (
        log_prefactor
        + residual_degrees
        * _log_unit_matrix_mgf_factor(
            block_dimension,
            lower_x,
            upper_tail=False,
        )
    ) / lower_x / residual_degrees
    return float(max(np.min(upper), min(1.0, float(np.min(lower)))))


def _minimum_residual_degrees_for_radius(
    threshold: float,
    block_dimension: int,
    block_count: int,
    *,
    confidence: float = 0.975,
    theta_grid_size: int = 1024,
) -> int:
    if not 0.0 < threshold < 2.0:
        raise ValueError("threshold must lie in (0, 2)")
    lower = 2
    upper = 4
    while (
        _unit_weight_matrix_radius(
            block_dimension,
            block_count,
            upper,
            confidence=confidence,
            theta_grid_size=theta_grid_size,
        )
        >= threshold
    ):
        upper *= 2
    while lower < upper:
        midpoint = (lower + upper) // 2
        radius = _unit_weight_matrix_radius(
            block_dimension,
            block_count,
            midpoint,
            confidence=confidence,
            theta_grid_size=theta_grid_size,
        )
        if radius < threshold:
            upper = midpoint
        else:
            lower = midpoint + 1
    return int(lower)


def _population_worldtube() -> dict[str, object]:
    node_count = 7
    subset_size = 3
    planted_path, systems = moving_module_systems(node_count=node_count)
    candidates = tuple(combinations(range(node_count), subset_size))
    covariances = propagate_covariances(
        [system[0] for system in systems[:-1]],
        [system[1] for system in systems[:-1]],
        stationary_covariance(*systems[0]),
    )
    time_count = len(systems)
    candidate_count = len(candidates)
    local_factors = np.zeros((time_count, candidate_count, 3))
    transport_factors = np.zeros(
        (time_count - 1, candidate_count, candidate_count, 2)
    )
    local_scores = np.zeros((time_count, candidate_count))
    transport_scores = np.zeros((time_count - 1, candidate_count, candidate_count))
    joints = []

    for time, (transition, noise) in enumerate(systems):
        joint = adjacent_joint_covariance(covariances[time], transition, noise)
        joints.append(joint)
        for index, candidate in enumerate(candidates):
            metrics = observer_metrics_from_covariances(
                covariances[time],
                joint,
                candidate,
            )
            local_factors[time, index] = (
                metrics.integration_strength,
                metrics.independence,
                metrics.persistence,
            )
            local_scores[time, index] = metrics.observer_score

    for time in range(time_count - 1):
        transition, noise = systems[time]
        for previous, source in enumerate(candidates):
            for current, target in enumerate(candidates):
                metrics = transport_metrics(
                    covariances[time],
                    transition,
                    noise,
                    source,
                    target,
                )
                transport_factors[time, previous, current] = (
                    metrics.independence,
                    metrics.persistence,
                )
                transport_scores[time, previous, current] = metrics.transport_score

    certificate = certify_worldtube(
        local_scores,
        candidates,
        transport_scores=transport_scores,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    structural_nulls = local_factors[:, :, 0] == 0.0
    return {
        "node_count": node_count,
        "subset_size": subset_size,
        "planted_path": planted_path,
        "candidates": candidates,
        "local_factors": local_factors,
        "transport_factors": transport_factors,
        "structural_nulls": structural_nulls,
        "certificate": certificate,
        "time_count": time_count,
        "candidate_count": candidate_count,
    }


def _maximum_path_admissible_radius(population: dict[str, object]) -> float:
    local_factors = population["local_factors"]
    transport_factors = population["transport_factors"]
    candidates = population["candidates"]
    nulls = population["structural_nulls"]
    shape = (population["time_count"], population["candidate_count"])

    lower = 0.0
    upper = 0.01
    for _ in range(60):
        midpoint = 0.5 * (lower + upper)
        bound = relative_covariance_worldtube_recovery_bound(
            local_factors,
            transport_factors,
            candidates,
            population["node_count"],
            population["subset_size"],
            covariance_relative_errors=np.full(shape, midpoint),
            structural_integration_null_mask=nulls,
            transport_weight=0.25,
            continuity_weight=0.08,
        )
        if bound.guarantees_population_path:
            lower = midpoint
        else:
            upper = midpoint
    return float(lower)


def build_record() -> dict[str, object]:
    population = _population_worldtube()
    certificate = population["certificate"]
    time_count = int(population["time_count"])
    candidate_count = int(population["candidate_count"])
    node_count = int(population["node_count"])
    subset_size = int(population["subset_size"])

    block_dimension = node_count + subset_size
    covariance_block_count = time_count * candidate_count
    raw_edge_count = (time_count - 1) * candidate_count**2
    target_sample_count = 120
    nuisance_rank = 2
    residual_degrees = target_sample_count - nuisance_rank
    confidence = 0.975
    theta_grid_size = 1024

    scalar_oracle_radius = _unit_weight_matrix_radius(
        1,
        1,
        residual_degrees,
        confidence=confidence,
        theta_grid_size=theta_grid_size,
    )
    observer_oracle_radius = _unit_weight_matrix_radius(
        block_dimension,
        covariance_block_count,
        residual_degrees,
        confidence=confidence,
        theta_grid_size=theta_grid_size,
    )
    entry_residual_degrees = _minimum_residual_degrees_for_radius(
        1.0,
        block_dimension,
        covariance_block_count,
        confidence=confidence,
        theta_grid_size=theta_grid_size,
    )

    path_radius_threshold = _maximum_path_admissible_radius(population)
    conservative_path_residual_degrees = _minimum_residual_degrees_for_radius(
        path_radius_threshold,
        block_dimension,
        covariance_block_count,
        confidence=confidence,
        theta_grid_size=theta_grid_size,
    )

    return {
        "experiment": "AS",
        "title": "Observer-scale covariance-to-world-tube certification audit",
        "population_worldtube": {
            "node_count": node_count,
            "subset_size": subset_size,
            "time_count": time_count,
            "candidate_count": candidate_count,
            "planted_path": [list(value) for value in population["planted_path"]],
            "recovered_path": [list(value) for value in certificate.result.path],
            "population_action": certificate.result.total_action,
            "runner_up_action": certificate.runner_up_action,
            "population_action_margin": certificate.action_margin,
            "uniform_score_radius": certificate.uniform_score_radius,
            "declared_structural_integration_null_count": int(
                np.sum(population["structural_nulls"])
            ),
        },
        "covariance_geometry": {
            "maximum_required_block_dimension": block_dimension,
            "simultaneous_covariance_block_count": covariance_block_count,
            "raw_candidate_edge_count": raw_edge_count,
            "explanation": (
                "One block containing all current coordinates and one future candidate "
                "supports that candidate's local factors and every incoming transport edge."
            ),
        },
        "exact_tau_innovation_oracle": {
            "target_sample_count": target_sample_count,
            "nuisance_rank": nuisance_rank,
            "residual_innovation_degrees_of_freedom": residual_degrees,
            "covariance_confidence": confidence,
            "theta_grid_size": theta_grid_size,
            "scalar_block_radius": scalar_oracle_radius,
            "observer_scale_radius": observer_oracle_radius,
            "observer_scale_inside_relative_perturbation_regime": bool(
                observer_oracle_radius < 1.0
            ),
        },
        "dimension_entry_threshold": {
            "minimum_residual_innovation_degrees_for_radius_below_one": (
                entry_residual_degrees
            ),
            "corresponding_sample_count_at_nuisance_rank_two": (
                entry_residual_degrees + nuisance_rank
            ),
            "radius_at_threshold": _unit_weight_matrix_radius(
                block_dimension,
                covariance_block_count,
                entry_residual_degrees,
                confidence=confidence,
                theta_grid_size=theta_grid_size,
            ),
            "radius_one_step_below_threshold": _unit_weight_matrix_radius(
                block_dimension,
                covariance_block_count,
                entry_residual_degrees - 1,
                confidence=confidence,
                theta_grid_size=theta_grid_size,
            ),
        },
        "current_end_to_end_bridge": {
            "maximum_uniform_relative_radius_certifying_population_path": (
                path_radius_threshold
            ),
            "current_matrix_chernoff_residual_degrees_at_that_radius": (
                conservative_path_residual_degrees
            ),
            "interpretation": (
                "This is a conservatism diagnostic for the current uniform relative "
                "covariance and factor-perturbation chain, not a fundamental sample "
                "requirement for the physical problem."
            ),
        },
        "interpretation": {
            "main_result": (
                "The scalar Proposition 56 and 57 success does not automatically imply "
                "observer-scale certification. At the actual world-tube block dimension "
                "and simultaneous block count, even the exact-tau innovation oracle is "
                "outside the relative perturbation regime on 118 residual degrees."
            ),
            "next_bottleneck": (
                "The next tightness frontier is dimensional and structural: localized "
                "factor-specific covariance control, screening, and sharper score-margin "
                "propagation, rather than further refinement of physical-time calibration."
            ),
        },
    }


def main() -> None:
    record = build_record()
    OUTPUT.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(record, indent=2))


if __name__ == "__main__":
    main()
