"""Compare absolute and covariance-normalized Gaussian screening certificates."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wishart

from observer_math import (
    gaussian_relative_structural_null_near_competitor_screen,
    gaussian_structural_null_near_competitor_screen,
)

if __package__:
    from examples.gaussian_screen_calibration import empirical_factors, wilson_interval
    from examples.multi_regime_coupled_calibration import regime_grid, regime_problem
    from examples.trajectory_coupled_screen_calibration import extract_adjacent_covariances
else:
    from gaussian_screen_calibration import empirical_factors, wilson_interval
    from multi_regime_coupled_calibration import regime_grid, regime_problem
    from trajectory_coupled_screen_calibration import extract_adjacent_covariances


def _relative_error(population, empirical):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (empirical - population) @ inverse_sqrt, ord=2)
    )


def evaluate_trial(sample_count, seed, problem, trajectory, null_mask):
    """Draw one trajectory covariance and evaluate the two paired screens."""
    rng = np.random.default_rng(seed)
    empirical_trajectory = wishart.rvs(
        df=sample_count - 1,
        scale=trajectory / (sample_count - 1),
        random_state=rng,
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    empirical_joints = extract_adjacent_covariances(
        empirical_trajectory, problem["node_count"], time_count
    )
    local_factors, transport_factors = empirical_factors(empirical_joints, problem)
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
    absolute = gaussian_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        problem["candidates"],
        sample_count,
        problem["node_count"],
        3,
        minimum_block_eigenvalues=problem["minimum"],
        maximum_block_eigenvalues=problem["maximum"],
        **common,
    )
    relative = gaussian_relative_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        problem["candidates"],
        sample_count,
        problem["node_count"],
        3,
        **common,
    )

    relative_errors = np.empty((time_count, candidate_count))
    for time, (population, empirical) in enumerate(
        zip(problem["joints"], empirical_joints, strict=True)
    ):
        for current, candidate in enumerate(problem["candidates"]):
            indices = tuple(range(problem["node_count"])) + tuple(
                problem["node_count"] + node for node in candidate
            )
            relative_errors[time, current] = _relative_error(
                population[np.ix_(indices, indices)], empirical[np.ix_(indices, indices)]
            )

    empirical_local = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    population_local = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    empirical_transport = np.sqrt(np.prod(transport_factors, axis=3))
    population_transport = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    score_covered = bool(
        np.all(
            np.abs(empirical_local - population_local)
            <= relative.screening_local_score_errors
        )
        and np.all(
            np.abs(empirical_transport - population_transport)
            <= relative.screening_transport_score_errors
        )
    )
    path = problem["population_path"]
    path_retained = bool(
        all(path[t] in relative.screen.viable_states[t] for t in range(time_count))
        and all(
            (path[t], path[t + 1]) in relative.screen.viable_edges[t]
            for t in range(time_count - 1)
        )
    )
    state_total = time_count * candidate_count
    edge_total = (time_count - 1) * candidate_count**2
    return {
        "relative_covariance_covered": bool(
            np.all(relative_errors <= relative.covariance_relative_errors)
        ),
        "relative_score_covered": score_covered,
        "relative_path_retained": path_retained,
        "relative_blocks_valid": relative.all_blocks_valid,
        "maximum_relative_radius_ratio": float(
            np.max(relative_errors / relative.covariance_relative_errors)
        ),
        "absolute_state_fraction": absolute.screen.viable_state_count / state_total,
        "relative_state_fraction": relative.screen.viable_state_count / state_total,
        "absolute_edge_fraction": absolute.screen.viable_edge_count / edge_total,
        "relative_edge_fraction": relative.screen.viable_edge_count / edge_total,
        "relative_radius": relative.maximum_covariance_relative_error,
        "absolute_radius_to_minimum_ratio": float(
            np.max(absolute.covariance_spectral_errors / problem["minimum"])
        ),
    }


def run_regime(task):
    label, base, active, coupling, condition, sample_count, seeds = task
    problem, trajectory, null_mask, certificate, _ = regime_problem(
        base, active, coupling, condition
    )
    trials = [
        evaluate_trial(sample_count, seed, problem, trajectory, null_mask) for seed in seeds
    ]
    record = {
        "memory_label": label,
        "base_memory": base,
        "active_memory": active,
        "internal_coupling": coupling,
        "noise_condition": condition,
        "sample_count": sample_count,
        "trial_count": len(trials),
        "population_action_margin": certificate.action_margin,
        "relative_radius": trials[0]["relative_radius"],
        "absolute_radius_to_minimum_ratio": trials[0][
            "absolute_radius_to_minimum_ratio"
        ],
    }
    for name in (
        "relative_covariance_covered",
        "relative_score_covered",
        "relative_path_retained",
        "relative_blocks_valid",
    ):
        successes = sum(trial[name] for trial in trials)
        record[f"{name}_rate"] = successes / len(trials)
        record[f"{name}_wilson_95"] = wilson_interval(successes, len(trials))
    for name in (
        "maximum_relative_radius_ratio",
        "absolute_state_fraction",
        "relative_state_fraction",
        "absolute_edge_fraction",
        "relative_edge_fraction",
    ):
        values = np.asarray([trial[name] for trial in trials])
        record[f"mean_{name}"] = float(np.mean(values))
        record[f"standard_error_{name}"] = float(
            np.std(values, ddof=1) / np.sqrt(len(values))
        )
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
        (100 * _matrix(records, "mean_absolute_state_fraction"), "Absolute: states retained"),
        (100 * _matrix(records, "mean_relative_state_fraction"), "Relative: states retained"),
        (100 * _matrix(records, "mean_absolute_edge_fraction"), "Absolute: edges retained"),
        (100 * _matrix(records, "mean_relative_edge_fraction"), "Relative: edges retained"),
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 9.0), constrained_layout=True)
    for axis, (values, title) in zip(axes.flat, panels, strict=True):
        image = axis.imshow(values, cmap="viridis", vmin=0.0, vmax=100.0, aspect="auto")
        axis.set_xticks(range(3), column_labels)
        axis.set_yticks(range(6), row_labels)
        axis.set_title(f"{title} (%)")
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
            "relative_covariance_covered_rate",
            "relative_score_covered_rate",
            "relative_path_retained_rate",
        )
    )
    figure.suptitle("Absolute and covariance-normalized screening on paired trials", fontsize=15)
    figure.supxlabel(
        "64 paired trajectory draws per cell at N=80 billion; "
        f"minimum relative-certificate coverage {minimum_coverage:.1%}",
        fontsize=9,
    )
    figure.savefig(output, dpi=190, bbox_inches="tight")
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--sample-count", type=int, default=80_000_000_000)
    args = parser.parse_args()
    if args.trials < 3 or args.jobs < 1 or args.sample_count < 2:
        raise ValueError("require at least three trials, one job, and two samples")
    grid = regime_grid()
    root_seed = 20260912
    seed_sequence = np.random.SeedSequence(root_seed)
    children = seed_sequence.spawn(len(grid) * args.trials)
    seeds = [
        [
            int(child.generate_state(1, dtype=np.uint64)[0])
            for child in children[index * args.trials : (index + 1) * args.trials]
        ]
        for index in range(len(grid))
    ]
    tasks = [
        (*regime, args.sample_count, regime_seeds)
        for regime, regime_seeds in zip(grid, seeds, strict=True)
    ]
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        records = list(executor.map(run_regime, tasks))
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "trials_per_regime": args.trials,
        "sample_count": args.sample_count,
        "nominal_screening_confidence": 0.975,
        "comparison": "paired absolute-spectral and population-whitened relative screens",
        "records": records,
    }
    json_output = root / "docs" / "relative_covariance_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "relative_covariance_calibration.png"
    plot_results(records, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"memory={record['memory_label']}",
            f"kappaQ={record['noise_condition']:g}",
            f"beta={record['internal_coupling']:.2f}",
            f"coverage={record['relative_score_covered_rate']:.3f}",
            f"states={record['mean_absolute_state_fraction']:.3f}"
            f"->{record['mean_relative_state_fraction']:.3f}",
            f"edges={record['mean_absolute_edge_fraction']:.3f}"
            f"->{record['mean_relative_edge_fraction']:.3f}",
        )


if __name__ == "__main__":
    main()
