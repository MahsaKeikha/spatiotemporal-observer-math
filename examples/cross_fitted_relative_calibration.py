"""Calibrate a pilot-normalized adaptive screen across the fixed regime grid."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wishart

from observer_math import (
    gaussian_cross_fitted_relative_near_competitor_screen,
    gaussian_relative_structural_null_near_competitor_screen,
    gaussian_wishart_relative_covariance_error_bound,
)

if __package__:
    from examples.gaussian_screen_calibration import empirical_factors, wilson_interval
    from examples.multi_regime_coupled_calibration import regime_grid, regime_problem
    from examples.trajectory_coupled_screen_calibration import extract_adjacent_covariances
else:
    from gaussian_screen_calibration import empirical_factors, wilson_interval
    from multi_regime_coupled_calibration import regime_grid, regime_problem
    from trajectory_coupled_screen_calibration import extract_adjacent_covariances


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def _candidate_relative_errors(population_joints, empirical_joints, problem):
    errors = np.empty((len(population_joints), len(problem["candidates"])))
    for time, (population, empirical) in enumerate(
        zip(population_joints, empirical_joints, strict=True)
    ):
        for current, candidate in enumerate(problem["candidates"]):
            indices = tuple(range(problem["node_count"])) + tuple(
                problem["node_count"] + node for node in candidate
            )
            errors[time, current] = _relative_error(
                population[np.ix_(indices, indices)], empirical[np.ix_(indices, indices)]
            )
    return errors


def evaluate_screening_draw(
    screening_sample_count,
    seed,
    problem,
    trajectory,
    null_mask,
    pilot_joints,
    pilot_sample_count,
):
    """Evaluate fixed and pilot-adaptive relative screens on one screening draw."""
    rng = np.random.default_rng(seed)
    empirical_trajectory = wishart.rvs(
        df=screening_sample_count - 1,
        scale=trajectory / (screening_sample_count - 1),
        random_state=rng,
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    screening_joints = extract_adjacent_covariances(
        empirical_trajectory, problem["node_count"], time_count
    )
    local_factors, transport_factors = empirical_factors(screening_joints, problem)
    local_zeros = np.zeros((time_count, candidate_count))
    transport_zeros = np.zeros((time_count - 1, candidate_count, candidate_count))
    common = {
        "structural_integration_null_mask": null_mask,
        "certification_local_score_errors": local_zeros,
        "certification_transport_score_errors": transport_zeros,
        "confidence": 0.975,
        "transport_weight": 0.25,
        "continuity_weight": 0.08,
    }
    fixed = gaussian_relative_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        problem["candidates"],
        screening_sample_count,
        problem["node_count"],
        3,
        **common,
    )
    adaptive = gaussian_cross_fitted_relative_near_competitor_screen(
        pilot_joints,
        screening_joints,
        problem["candidates"],
        pilot_sample_count,
        problem["node_count"],
        3,
        **common,
    )
    actual_relative = _candidate_relative_errors(
        problem["joints"], screening_joints, problem
    )
    empirical_local = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    population_local = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    empirical_transport = np.sqrt(np.prod(transport_factors, axis=3))
    population_transport = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    score_covered = bool(
        np.all(
            np.abs(empirical_local - population_local)
            <= adaptive.screening_local_score_errors
        )
        and np.all(
            np.abs(empirical_transport - population_transport)
            <= adaptive.screening_transport_score_errors
        )
    )
    path = problem["population_path"]
    path_retained = bool(
        all(path[t] in adaptive.screen.viable_states[t] for t in range(time_count))
        and all(
            (path[t], path[t + 1]) in adaptive.screen.viable_edges[t]
            for t in range(time_count - 1)
        )
    )
    state_total = time_count * candidate_count
    edge_total = (time_count - 1) * candidate_count**2
    return {
        "adaptive_covariance_covered": bool(
            np.all(actual_relative <= adaptive.covariance_relative_errors)
        ),
        "adaptive_score_covered": score_covered,
        "adaptive_path_retained": path_retained,
        "adaptive_blocks_valid": adaptive.all_blocks_valid,
        "fixed_state_fraction": fixed.screen.viable_state_count / state_total,
        "adaptive_state_fraction": adaptive.screen.viable_state_count / state_total,
        "fixed_edge_fraction": fixed.screen.viable_edge_count / edge_total,
        "adaptive_edge_fraction": adaptive.screen.viable_edge_count / edge_total,
        "fixed_relative_radius": fixed.maximum_covariance_relative_error,
        "maximum_adaptive_relative_radius": adaptive.maximum_covariance_relative_error,
        "maximum_adaptive_to_fixed_radius_ratio": (
            adaptive.maximum_covariance_relative_error
            / fixed.maximum_covariance_relative_error
        ),
        "maximum_actual_to_adaptive_radius_ratio": float(
            np.max(actual_relative / adaptive.covariance_relative_errors)
        ),
    }


def run_regime(task):
    (
        label,
        base,
        active,
        coupling,
        condition,
        pilot_sample_count,
        screening_sample_count,
        pilot_seed,
        screening_seeds,
    ) = task
    problem, trajectory, null_mask, certificate, _ = regime_problem(
        base, active, coupling, condition
    )
    pilot_rng = np.random.default_rng(pilot_seed)
    pilot_trajectory = wishart.rvs(
        df=pilot_sample_count - 1,
        scale=trajectory / (pilot_sample_count - 1),
        random_state=pilot_rng,
    )
    pilot_joints = extract_adjacent_covariances(
        pilot_trajectory, problem["node_count"], len(problem["joints"])
    )
    pilot_actual = _candidate_relative_errors(problem["joints"], pilot_joints, problem)
    trials = [
        evaluate_screening_draw(
            screening_sample_count,
            seed,
            problem,
            trajectory,
            null_mask,
            pilot_joints,
            pilot_sample_count,
        )
        for seed in screening_seeds
    ]
    pilot_radius = gaussian_wishart_relative_covariance_error_bound(
        problem["node_count"] + 3,
        len(problem["joints"]) * len(problem["candidates"]),
        pilot_sample_count,
        confidence=0.975,
    )
    record = {
        "memory_label": label,
        "base_memory": base,
        "active_memory": active,
        "internal_coupling": coupling,
        "noise_condition": condition,
        "population_action_margin": certificate.action_margin,
        "pilot_sample_count": pilot_sample_count,
        "screening_sample_count": screening_sample_count,
        "screening_trial_count": len(trials),
        "pilot_relative_radius": pilot_radius,
        "maximum_pilot_relative_error": float(np.max(pilot_actual)),
        "pilot_covariance_covered": bool(np.all(pilot_actual <= pilot_radius)),
    }
    for name in (
        "adaptive_covariance_covered",
        "adaptive_score_covered",
        "adaptive_path_retained",
        "adaptive_blocks_valid",
    ):
        successes = sum(trial[name] for trial in trials)
        record[f"{name}_rate"] = successes / len(trials)
        record[f"{name}_wilson_95"] = wilson_interval(successes, len(trials))
    for name in (
        "fixed_state_fraction",
        "adaptive_state_fraction",
        "fixed_edge_fraction",
        "adaptive_edge_fraction",
        "maximum_adaptive_relative_radius",
        "maximum_adaptive_to_fixed_radius_ratio",
        "maximum_actual_to_adaptive_radius_ratio",
    ):
        values = np.asarray([trial[name] for trial in trials])
        record[f"mean_{name}"] = float(np.mean(values))
        record[f"standard_error_{name}"] = float(
            np.std(values, ddof=1) / np.sqrt(len(values))
        )
    record["fixed_relative_radius"] = trials[0]["fixed_relative_radius"]
    return record


def _matrix(records, key):
    return np.asarray([record[key] for record in records]).reshape(6, 3)


def plot_results(records, output):
    row_labels = [
        f"{label} memory | κ(Q)={condition:g}"
        for label in ("short", "baseline", "long")
        for condition in (1.0, 9.0)
    ]
    column_labels = ["β=0.10", "β=0.18", "β=0.26"]
    panels = (
        (100 * _matrix(records, "mean_fixed_state_fraction"), "Fixed-radius states"),
        (100 * _matrix(records, "mean_adaptive_state_fraction"), "Pilot-adaptive states"),
        (100 * _matrix(records, "mean_fixed_edge_fraction"), "Fixed-radius edges"),
        (100 * _matrix(records, "mean_adaptive_edge_fraction"), "Pilot-adaptive edges"),
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 9.0), constrained_layout=True)
    for axis, (values, title) in zip(axes.flat, panels, strict=True):
        image = axis.imshow(values, cmap="viridis", vmin=0.0, vmax=100.0, aspect="auto")
        axis.set_xticks(range(3), column_labels)
        axis.set_yticks(range(6), row_labels)
        axis.set_title(f"{title} retained (%)")
        figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
        for row in range(6):
            for column in range(3):
                value = values[row, column]
                axis.text(
                    column,
                    row,
                    f"{value:.1f}",
                    ha="center",
                    va="center",
                    color="white" if value < 35 or value > 75 else "black",
                    fontsize=8,
                )
    minimum_coverage = min(
        record[key]
        for record in records
        for key in (
            "adaptive_covariance_covered_rate",
            "adaptive_score_covered_rate",
            "adaptive_path_retained_rate",
        )
    )
    radius_ratio = np.mean(
        [record["mean_maximum_adaptive_to_fixed_radius_ratio"] for record in records]
    )
    figure.suptitle("Reusable pilot geometry and adaptive Gaussian screening", fontsize=15)
    figure.supxlabel(
        "One 8-trillion-trajectory pilot per regime; 64 screening draws at N=300 million; "
        f"mean adaptive/fixed radius {radius_ratio:.3f}; minimum coverage {minimum_coverage:.1%}",
        fontsize=9,
    )
    figure.savefig(output, dpi=190, bbox_inches="tight")
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--pilot-sample-count", type=int, default=8_000_000_000_000)
    parser.add_argument("--screening-sample-count", type=int, default=300_000_000)
    args = parser.parse_args()
    if (
        args.trials < 3
        or args.jobs < 1
        or args.pilot_sample_count < 2
        or args.screening_sample_count < 2
    ):
        raise ValueError("require at least three trials, one job, and sample counts above one")
    grid = regime_grid()
    root_seed = 20260915
    children = np.random.SeedSequence(root_seed).spawn(len(grid) * (args.trials + 1))
    tasks = []
    for index, regime in enumerate(grid):
        offset = index * (args.trials + 1)
        pilot_seed = int(children[offset].generate_state(1, dtype=np.uint64)[0])
        screening_seeds = [
            int(child.generate_state(1, dtype=np.uint64)[0])
            for child in children[offset + 1 : offset + 1 + args.trials]
        ]
        tasks.append(
            (
                *regime,
                args.pilot_sample_count,
                args.screening_sample_count,
                pilot_seed,
                screening_seeds,
            )
        )
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        records = list(executor.map(run_regime, tasks))
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "trials_per_regime": args.trials,
        "pilot_sample_count": args.pilot_sample_count,
        "screening_sample_count": args.screening_sample_count,
        "nominal_pilot_confidence": 0.975,
        "pilot_reuse": "one pilot covariance per regime, reused across screening draws",
        "records": records,
    }
    json_output = root / "docs" / "cross_fitted_relative_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "cross_fitted_relative_calibration.png"
    plot_results(records, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"memory={record['memory_label']}",
            f"kappaQ={record['noise_condition']:g}",
            f"beta={record['internal_coupling']:.2f}",
            f"coverage={record['adaptive_score_covered_rate']:.3f}",
            f"states={record['mean_fixed_state_fraction']:.3f}"
            f"->{record['mean_adaptive_state_fraction']:.3f}",
            f"edges={record['mean_fixed_edge_fraction']:.3f}"
            f"->{record['mean_adaptive_edge_fraction']:.3f}",
        )


if __name__ == "__main__":
    main()
