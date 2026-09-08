"""Stress-test trajectory-coupled screening across a fixed parameter grid."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from functools import cache
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm

from observer_math import certify_worldtube, full_trajectory_covariance
from observer_math.gaussian import stationary_covariance

if __package__:
    from examples.gaussian_screen_calibration import (
        screening_problem_from_systems,
        structural_integration_null_mask,
        wilson_interval,
    )
    from examples.trajectory_coupled_screen_calibration import evaluate_coupled_trial
else:
    from gaussian_screen_calibration import (
        screening_problem_from_systems,
        structural_integration_null_mask,
        wilson_interval,
    )
    from trajectory_coupled_screen_calibration import evaluate_coupled_trial


MEMORY_LEVELS = (
    ("short", 0.12, 0.28),
    ("baseline", 0.32, 0.46),
    ("long", 0.52, 0.66),
)
COUPLING_LEVELS = (0.10, 0.18, 0.26)
NOISE_CONDITIONS = (1.0, 9.0)


def parameterized_moving_module_systems(
    *,
    base_memory,
    active_memory,
    internal_coupling,
    noise_condition,
    node_count=7,
    module_size=3,
    step_count=5,
    target_radius=0.84,
):
    """Build a moving module with declared memory, coupling, and noise condition."""
    if not 0.0 <= base_memory < active_memory:
        raise ValueError("require 0 <= base_memory < active_memory")
    if internal_coupling < 0.0 or noise_condition < 1.0:
        raise ValueError("coupling must be nonnegative and noise condition at least one")
    planted = tuple(tuple(range(start, start + module_size)) for start in range(step_count))
    base_noise = 0.18 * np.geomspace(
        1.0 / np.sqrt(noise_condition),
        np.sqrt(noise_condition),
        node_count,
    )
    systems = []
    for time, active in enumerate(planted):
        transition = np.eye(node_count) * base_memory
        for target in active:
            transition[target, target] = active_memory
            for source in active:
                if source != target:
                    transition[target, source] = internal_coupling
        spectral_radius = float(np.max(np.abs(np.linalg.eigvals(transition))))
        transition *= target_radius / spectral_radius
        noise = np.diag(np.roll(base_noise, time))
        systems.append((transition, noise))
    return planted, tuple(systems)


@cache
def regime_problem(base_memory, active_memory, coupling, noise_condition):
    """Return one population problem and its complete trajectory covariance."""
    planted, systems = parameterized_moving_module_systems(
        base_memory=base_memory,
        active_memory=active_memory,
        internal_coupling=coupling,
        noise_condition=noise_condition,
    )
    problem = screening_problem_from_systems(planted, systems)
    trajectory = full_trajectory_covariance(
        [transition for transition, _ in systems],
        [noise for _, noise in systems],
        stationary_covariance(*systems[0]),
    )
    null_mask = structural_integration_null_mask(problem)
    local_scores = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    certificate = certify_worldtube(
        local_scores,
        problem["candidates"],
        transport_scores=transport_scores,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    declared_indices = tuple(problem["candidates"].index(candidate) for candidate in planted)
    return problem, trajectory, null_mask, certificate, declared_indices


def regime_grid():
    """Return the fixed Cartesian parameter grid in plotting order."""
    return tuple(
        (label, base, active, coupling, condition)
        for label, base, active in MEMORY_LEVELS
        for condition in NOISE_CONDITIONS
        for coupling in COUPLING_LEVELS
    )


def run_regime(task):
    """Run all seeded coupled trials for one parameter regime."""
    label, base, active, coupling, condition, sample_count, seeds = task
    problem, trajectory, null_mask, certificate, declared = regime_problem(
        base, active, coupling, condition
    )
    trials = [
        evaluate_coupled_trial(sample_count, seed, problem, trajectory, null_mask) for seed in seeds
    ]
    event_names = (
        "covariance_covered",
        "score_covered",
        "null_score_covered",
        "null_population_path_retained",
    )
    record = {
        "memory_label": label,
        "base_memory": base,
        "active_memory": active,
        "internal_coupling": coupling,
        "noise_condition": condition,
        "sample_count": sample_count,
        "trial_count": len(trials),
        "population_action_margin": certificate.action_margin,
        "declared_path_is_population_optimum": problem["population_path"] == declared,
        "structural_null_state_count": int(np.count_nonzero(null_mask)),
        "minimum_joint_eigenvalue": float(np.min(problem["minimum"])),
        "maximum_joint_eigenvalue": float(np.max(problem["maximum"])),
    }
    for name in event_names:
        successes = sum(trial[name] for trial in trials)
        record[f"{name}_rate"] = successes / len(trials)
        record[f"{name}_wilson_95"] = wilson_interval(successes, len(trials))
    for name in (
        "retained_state_fraction",
        "retained_edge_fraction",
        "null_retained_state_fraction",
        "null_retained_edge_fraction",
        "maximum_covariance_radius_ratio",
    ):
        values = np.asarray([trial[name] for trial in trials])
        record[f"mean_{name}"] = float(np.mean(values))
        record[f"standard_error_{name}"] = float(np.std(values, ddof=1) / np.sqrt(len(values)))
    return record


def _matrix(records, key):
    rows = len(MEMORY_LEVELS) * len(NOISE_CONDITIONS)
    columns = len(COUPLING_LEVELS)
    return np.asarray([record[key] for record in records]).reshape(rows, columns)


def plot_results(records, output):
    """Plot population separation and certified graph size across the grid."""
    margins = _matrix(records, "population_action_margin")
    states = 100.0 * _matrix(records, "mean_null_retained_state_fraction")
    edges = 100.0 * _matrix(records, "mean_null_retained_edge_fraction")
    row_labels = [
        f"{label} memory | κ(Q)={condition:g}"
        for label, _, _ in MEMORY_LEVELS
        for condition in NOISE_CONDITIONS
    ]
    column_labels = [f"β={coupling:.2f}" for coupling in COUPLING_LEVELS]
    figure, axes = plt.subplots(1, 3, figsize=(14.8, 6.0), constrained_layout=True)
    panels = (
        (margins, "Population action margin", "viridis", LogNorm(), ".3g"),
        (states, "Null-aware states retained (%)", "Blues", None, ".1f"),
        (edges, "Null-aware edges retained (%)", "Oranges", None, ".1f"),
    )
    for axis, (values, title, cmap, norm, number_format) in zip(axes, panels, strict=True):
        image = axis.imshow(values, cmap=cmap, norm=norm, aspect="auto")
        axis.set_xticks(range(len(column_labels)), column_labels)
        axis.set_yticks(range(len(row_labels)), row_labels)
        axis.set_title(title)
        figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
        midpoint = (float(np.min(values)) + float(np.max(values))) / 2.0
        for row in range(values.shape[0]):
            for column in range(values.shape[1]):
                value = values[row, column]
                color = "white" if value > midpoint else "black"
                axis.text(
                    column,
                    row,
                    format(value, number_format),
                    ha="center",
                    va="center",
                    color=color,
                    fontsize=8,
                )
    minimum_coverage = min(
        record[key]
        for record in records
        for key in (
            "covariance_covered_rate",
            "score_covered_rate",
            "null_score_covered_rate",
            "null_population_path_retained_rate",
        )
    )
    declared_count = sum(record["declared_path_is_population_optimum"] for record in records)
    figure.suptitle("Trajectory-coupled screening across 18 declared regimes", fontsize=15)
    figure.supxlabel(
        f"64 coupled trials per cell at N=80 billion; minimum recorded coverage "
        f"{minimum_coverage:.1%}; declared path optimal in {declared_count}/18 regimes",
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
    root_seed = 20260911
    seed_sequence = np.random.SeedSequence(root_seed)
    child_seeds = seed_sequence.spawn(len(grid) * args.trials)
    regime_seeds = [
        [
            int(child.generate_state(1, dtype=np.uint64)[0])
            for child in child_seeds[index * args.trials : (index + 1) * args.trials]
        ]
        for index in range(len(grid))
    ]
    tasks = [
        (*regime, args.sample_count, seeds)
        for regime, seeds in zip(grid, regime_seeds, strict=True)
    ]
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        records = list(executor.map(run_regime, tasks))
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "trials_per_regime": args.trials,
        "sample_count": args.sample_count,
        "nominal_screening_confidence": 0.975,
        "memory_levels": MEMORY_LEVELS,
        "coupling_levels": COUPLING_LEVELS,
        "noise_conditions": NOISE_CONDITIONS,
        "records": records,
    }
    data_output = root / "docs" / "multi_regime_coupled_calibration.json"
    data_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "multi_regime_coupled_calibration.png"
    plot_results(records, figure_output)
    print("Results:", data_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"memory={record['memory_label']}",
            f"kappaQ={record['noise_condition']:g}",
            f"beta={record['internal_coupling']:.2f}",
            f"margin={record['population_action_margin']:.6f}",
            f"coverage={record['null_score_covered_rate']:.3f}",
            f"states={record['mean_null_retained_state_fraction']:.3f}",
            f"edges={record['mean_null_retained_edge_fraction']:.3f}",
        )


if __name__ == "__main__":
    main()
