"""Estimate path recovery from sampled, rather than analytical, covariances."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math import (
    adjacent_sample_covariances,
    best_fixed_boundary,
    independent_local_path,
    moving_module_systems,
    observer_metrics_from_covariances,
    optimize_worldtube,
    simulate_gaussian_ensemble,
    structural_transport,
    transport_metrics_from_covariances,
)
from observer_math.gaussian import stationary_covariance

METHODS = (
    "world_tube",
    "independent_local",
    "continuity_only",
    "coefficient_transport",
    "fixed_boundary",
)


def score_empirical_covariances(states, candidates, *, ridge):
    time_count = len(states) - 1
    candidate_count = len(candidates)
    local = np.zeros((time_count, candidate_count))
    transport = np.zeros((time_count - 1, candidate_count, candidate_count))
    structural = np.zeros_like(transport)

    for time in range(time_count):
        present, joint = adjacent_sample_covariances(
            states[time], states[time + 1], ridge=ridge
        )
        for index, candidate in enumerate(candidates):
            local[time, index] = observer_metrics_from_covariances(
                present, joint, candidate
            ).observer_score

        if time < time_count - 1:
            dimension = present.shape[0]
            cross = joint[dimension:, :dimension]
            estimated_transition = cross @ np.linalg.pinv(present)
            for source_index, source in enumerate(candidates):
                for target_index, target in enumerate(candidates):
                    transport[time, source_index, target_index] = (
                        transport_metrics_from_covariances(
                            present, joint, source, target
                        ).transport_score
                    )
                    structural[time, source_index, target_index] = structural_transport(
                        estimated_transition, source, target
                    )
    return local, transport, structural


def evaluate_path(path, planted):
    accuracy = float(np.mean([found == expected for found, expected in zip(path, planted)]))
    return accuracy, float(accuracy == 1.0)


def run_trial(task):
    sample_count, seed, ridge = task
    planted, systems = moving_module_systems()
    transitions = [system[0] for system in systems]
    noises = [system[1] for system in systems]
    initial = stationary_covariance(*systems[0])
    rng = np.random.default_rng(seed)
    states = simulate_gaussian_ensemble(
        transitions, noises, initial, sample_count, rng=rng
    )
    candidates = tuple(combinations(range(transitions[0].shape[0]), len(planted[0])))
    local, transport, structural = score_empirical_covariances(
        states, candidates, ridge=ridge
    )

    paths = {
        "world_tube": optimize_worldtube(
            local,
            candidates,
            transport_scores=transport,
            transport_weight=0.25,
            continuity_weight=0.08,
        ).path,
        "independent_local": independent_local_path(local, candidates).path,
        "continuity_only": optimize_worldtube(
            local,
            candidates,
            transport_weight=0.0,
            continuity_weight=0.08,
        ).path,
        "coefficient_transport": optimize_worldtube(
            local,
            candidates,
            transport_scores=structural,
            transport_weight=0.25,
            continuity_weight=0.08,
        ).path,
        "fixed_boundary": best_fixed_boundary(local, candidates).path,
    }
    return {
        method: evaluate_path(path, planted)
        for method, path in paths.items()
    }


def wilson_interval(successes, total, z=1.959963984540054):
    proportion = successes / total
    denominator = 1.0 + z**2 / total
    center = (proportion + z**2 / (2.0 * total)) / denominator
    half_width = (
        z
        * np.sqrt(proportion * (1.0 - proportion) / total + z**2 / (4.0 * total**2))
        / denominator
    )
    return float(center - half_width), float(center + half_width)


def aggregate(sample_sizes, trial_count, trial_results):
    records = []
    offset = 0
    for sample_count in sample_sizes:
        group = trial_results[offset : offset + trial_count]
        offset += trial_count
        for method in METHODS:
            accuracies = np.array([result[method][0] for result in group])
            exact = np.array([result[method][1] for result in group])
            lower, upper = wilson_interval(int(exact.sum()), trial_count)
            records.append(
                {
                    "sample_count": sample_count,
                    "method": method,
                    "mean_boundary_accuracy": float(accuracies.mean()),
                    "standard_error_boundary_accuracy": float(
                        accuracies.std(ddof=1) / np.sqrt(trial_count)
                    ),
                    "exact_recovery_rate": float(exact.mean()),
                    "exact_recovery_wilson_95": [lower, upper],
                }
            )
    return records


def plot_results(records, output):
    labels = {
        "world_tube": "Distributional world-tube",
        "independent_local": "Independent local choices",
        "continuity_only": "Local + continuity",
        "coefficient_transport": "Coefficient transport",
        "fixed_boundary": "Best fixed boundary",
    }
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharex=True)
    sample_sizes = sorted({record["sample_count"] for record in records})
    for method in METHODS:
        subset = [record for record in records if record["method"] == method]
        x = np.array([record["sample_count"] for record in subset])
        boundary = np.array([record["mean_boundary_accuracy"] for record in subset])
        boundary_error = np.array(
            [record["standard_error_boundary_accuracy"] for record in subset]
        )
        exact = np.array([record["exact_recovery_rate"] for record in subset])
        interval = np.array([record["exact_recovery_wilson_95"] for record in subset])
        axes[0].errorbar(x, boundary, yerr=boundary_error, marker="o", label=labels[method])
        axes[1].plot(x, exact, marker="o", label=labels[method])
        axes[1].fill_between(x, interval[:, 0], interval[:, 1], alpha=0.10)

    for axis in axes:
        axis.set_xscale("log", base=2)
        axis.set_xticks(sample_sizes, labels=[str(value) for value in sample_sizes])
        axis.set_ylim(-0.03, 1.03)
        axis.set_xlabel("Independent sampled trajectories")
        axis.grid(alpha=0.25)
    axes[0].set_ylabel("Mean fraction of boundaries recovered")
    axes[1].set_ylabel("Exact path recovery rate")
    axes[0].set_title("Boundary accuracy")
    axes[1].set_title("Whole-path recovery")
    handles, legend_labels = axes[0].get_legend_handles_labels()
    figure.legend(handles, legend_labels, loc="outside lower center", ncol=3)
    figure.suptitle("Finite-sample moving-module benchmark")
    figure.tight_layout(rect=(0, 0.13, 1, 0.94))
    figure.savefig(output, dpi=180)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=8)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--ridge", type=float, default=1e-5)
    parser.add_argument(
        "--sample-sizes",
        type=int,
        nargs="+",
        default=[20, 40, 80, 160, 320, 640],
    )
    args = parser.parse_args()
    seed_sequence = np.random.SeedSequence(20260907)
    seeds = [
        int(child.generate_state(1, dtype=np.uint64)[0])
        for child in seed_sequence.spawn(len(args.sample_sizes) * args.trials)
    ]
    tasks = [
        (sample_count, seeds[index * args.trials + trial], args.ridge)
        for index, sample_count in enumerate(args.sample_sizes)
        for trial in range(args.trials)
    ]
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        trial_results = list(executor.map(run_trial, tasks))
    records = aggregate(args.sample_sizes, args.trials, trial_results)

    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": 20260907,
        "trials_per_sample_size": args.trials,
        "ridge": args.ridge,
        "sample_sizes": args.sample_sizes,
        "records": records,
    }
    json_output = root / "docs" / "finite_sample_results.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "finite_sample_benchmark.png"
    plot_results(records, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        if record["method"] == "world_tube":
            print(
                record["sample_count"],
                f"boundary={record['mean_boundary_accuracy']:.3f}",
                f"exact={record['exact_recovery_rate']:.3f}",
            )


if __name__ == "__main__":
    main()
