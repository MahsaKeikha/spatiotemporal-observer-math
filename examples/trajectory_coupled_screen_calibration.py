"""Calibrate screening from one joint Wishart draw over complete trajectories."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm
from scipy.stats import wishart

from observer_math import (
    full_trajectory_covariance,
    gaussian_structural_null_near_competitor_screen,
)
from observer_math.gaussian import stationary_covariance

if __package__:
    from examples.gaussian_screen_calibration import (
        aggregate,
        empirical_factors,
        evaluate_empirical_joints,
        population_problem,
        structural_integration_null_mask,
        wilson_interval,
    )
else:
    from gaussian_screen_calibration import (
        aggregate,
        empirical_factors,
        evaluate_empirical_joints,
        population_problem,
        structural_integration_null_mask,
        wilson_interval,
    )


@lru_cache(maxsize=1)
def coupled_problem():
    """Add the complete trajectory covariance and structural null mask."""
    problem = population_problem()
    systems = problem["systems"]
    trajectory = full_trajectory_covariance(
        [transition for transition, _ in systems],
        [noise for _, noise in systems],
        stationary_covariance(*systems[0]),
    )
    null_mask = structural_integration_null_mask(problem)
    return problem, trajectory, null_mask


def extract_adjacent_covariances(trajectory_covariance, node_count, time_count):
    """Extract adjacent blocks ordered as ``[X_t, X_(t+1)]``."""
    return tuple(
        trajectory_covariance[
            time * node_count : (time + 2) * node_count,
            time * node_count : (time + 2) * node_count,
        ]
        for time in range(time_count)
    )


def run_coupled_trial(task):
    """Draw one full-trajectory Wishart covariance and evaluate both screens."""
    sample_count, seed = task
    problem, trajectory, null_mask = coupled_problem()
    return evaluate_coupled_trial(sample_count, seed, problem, trajectory, null_mask)


def evaluate_coupled_trial(sample_count, seed, problem, trajectory, null_mask):
    """Evaluate one coupled draw for an explicitly supplied population model."""
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
    result = evaluate_empirical_joints(sample_count, empirical_joints, problem)
    local_factors, transport_factors = empirical_factors(empirical_joints, problem)
    null_aware = gaussian_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        problem["candidates"],
        sample_count,
        problem["node_count"],
        3,
        structural_integration_null_mask=null_mask,
        minimum_block_eigenvalues=problem["minimum"],
        maximum_block_eigenvalues=problem["maximum"],
        certification_local_score_errors=np.zeros((time_count, candidate_count)),
        certification_transport_score_errors=np.zeros(
            (time_count - 1, candidate_count, candidate_count)
        ),
        confidence=0.975,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    empirical_local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    population_local_scores = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    empirical_transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    population_transport_scores = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    path = problem["population_path"]
    complete_states = time_count * candidate_count
    complete_edges = (time_count - 1) * candidate_count**2
    result.update(
        {
            "null_score_covered": bool(
                np.all(
                    np.abs(empirical_local_scores - population_local_scores)
                    <= null_aware.screening_local_score_errors
                )
                and np.all(
                    np.abs(empirical_transport_scores - population_transport_scores)
                    <= null_aware.screening_transport_score_errors
                )
            ),
            "null_population_path_retained": bool(
                all(
                    path[time] in null_aware.screen.viable_states[time]
                    for time in range(time_count)
                )
                and all(
                    (path[time], path[time + 1]) in null_aware.screen.viable_edges[time]
                    for time in range(time_count - 1)
                )
            ),
            "null_retained_state_fraction": (
                null_aware.screen.viable_state_count / complete_states
            ),
            "null_retained_edge_fraction": (null_aware.screen.viable_edge_count / complete_edges),
            "node_zero_variance_errors": [
                float(
                    empirical_trajectory[time * problem["node_count"], time * problem["node_count"]]
                    - trajectory[time * problem["node_count"], time * problem["node_count"]]
                )
                for time in range(time_count + 1)
            ],
        }
    )
    return result


def theoretical_variance_error_correlation(trajectory, node_count, time_count):
    """Return the Gaussian correlation of sample-variance errors for node zero."""
    indices = np.arange(time_count + 1) * node_count
    covariance = trajectory[np.ix_(indices, indices)]
    scale = np.sqrt(np.diag(covariance))
    correlations = covariance / np.outer(scale, scale)
    return correlations**2


def aggregate_coupled(sample_sizes, trial_count, results):
    """Aggregate coverage, graph size, and cross-time dependence diagnostics."""
    records = aggregate(sample_sizes, trial_count, results)
    _, trajectory, _ = coupled_problem()
    time_count = len(population_problem()["joints"])
    theoretical = theoretical_variance_error_correlation(
        trajectory, population_problem()["node_count"], time_count
    )
    offset = 0
    for record in records:
        group = results[offset : offset + trial_count]
        offset += trial_count
        for name in ("null_score_covered", "null_population_path_retained"):
            successes = sum(result[name] for result in group)
            record[f"{name}_rate"] = successes / trial_count
            record[f"{name}_wilson_95"] = wilson_interval(successes, trial_count)
        for name in ("null_retained_state_fraction", "null_retained_edge_fraction"):
            values = np.asarray([result[name] for result in group])
            record[f"mean_{name}"] = float(np.mean(values))
            record[f"standard_error_{name}"] = float(np.std(values, ddof=1) / np.sqrt(trial_count))
        variance_errors = np.asarray([result["node_zero_variance_errors"] for result in group])
        empirical = np.corrcoef(variance_errors, rowvar=False)
        record["empirical_variance_error_correlation"] = empirical.tolist()
        record["mean_absolute_correlation_error"] = float(np.mean(np.abs(empirical - theoretical)))
    return records, theoretical


def plot_results(records, theoretical, output):
    """Plot coupled coverage, graph reduction, and temporal dependence."""
    labels = {
        80_000: "80K",
        8_000_000: "8M",
        800_000_000: "800M",
        80_000_000_000: "80B",
        8_000_000_000_000: "8T",
    }
    x_labels = [
        labels.get(record["sample_count"], f"{record['sample_count']:.1e}") for record in records
    ]
    positions = np.arange(len(records))
    figure, axes = plt.subplots(1, 3, figsize=(15.5, 4.8))
    coverage = (
        ("covariance_covered_rate", "Covariance"),
        ("score_covered_rate", "Generic score"),
        ("null_score_covered_rate", "Null-aware score"),
        ("null_population_path_retained_rate", "Path retained"),
    )
    for key, label in coverage:
        axes[0].plot(positions, [record[key] for record in records], marker="o", label=label)
    axes[0].axhline(0.975, color="black", linestyle="--", linewidth=1, label="Nominal")
    axes[0].set_ylim(0.94, 1.003)
    axes[0].set_xticks(positions, x_labels)
    axes[0].set_xlabel("Independent trajectories")
    axes[0].set_ylabel("Covered trial fraction")
    axes[0].set_title("Coupled empirical coverage")
    axes[0].legend(fontsize=8, loc="lower right")
    axes[0].grid(alpha=0.25)

    graph_series = (
        ("mean_retained_state_fraction", "Generic states"),
        ("mean_retained_edge_fraction", "Generic edges"),
        ("mean_null_retained_state_fraction", "Null-aware states"),
        ("mean_null_retained_edge_fraction", "Null-aware edges"),
    )
    for key, label in graph_series:
        axes[1].plot(
            positions,
            [100.0 * record[key] for record in records],
            marker="o",
            label=label,
        )
    axes[1].set_ylim(-2.0, 102.0)
    axes[1].set_xticks(positions, x_labels)
    axes[1].set_xlabel("Independent trajectories")
    axes[1].set_ylabel("Graph retained (%)")
    axes[1].set_title("Screen usefulness")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.25)

    empirical = np.asarray(records[-1]["empirical_variance_error_correlation"])
    comparison = np.tril(theoretical) + np.triu(empirical, k=1)
    image = axes[2].imshow(
        comparison,
        norm=TwoSlopeNorm(vmin=-0.2, vcenter=0.0, vmax=1.0),
        cmap="coolwarm",
    )
    axes[2].set_xticks(range(comparison.shape[0]))
    axes[2].set_yticks(range(comparison.shape[0]))
    axes[2].set_xlabel("Time of node-0 variance estimate")
    axes[2].set_ylabel("Time of node-0 variance estimate")
    axes[2].set_title("Error correlation: empirical above, theory below")
    figure.colorbar(image, ax=axes[2], fraction=0.046, pad=0.04)
    for row in range(comparison.shape[0]):
        for column in range(comparison.shape[1]):
            value = comparison[row, column]
            color = "white" if value < -0.05 or value > 0.75 else "black"
            axes[2].text(
                column,
                row,
                f"{value:.2f}",
                ha="center",
                va="center",
                color=color,
                fontsize=7,
            )

    discrepancy = records[-1]["mean_absolute_correlation_error"]
    theoretical_adjacent = float(np.mean(np.diag(theoretical, k=1)))
    figure.suptitle("Trajectory-coupled Gaussian screening calibration", fontsize=14)
    figure.text(
        0.5,
        0.015,
        "One full-trajectory Wishart draw preserves temporal dependence. "
        f"Mean theoretical adjacent variance-error correlation: {theoretical_adjacent:.3f}; "
        f"8T matrix mean absolute error: {discrepancy:.3f}.",
        ha="center",
        fontsize=8.5,
    )
    figure.tight_layout(rect=(0.0, 0.065, 1.0, 0.94))
    figure.savefig(output, dpi=190, bbox_inches="tight")
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=128)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument(
        "--sample-sizes",
        type=int,
        nargs="+",
        default=[80_000, 8_000_000, 800_000_000, 80_000_000_000, 8_000_000_000_000],
    )
    args = parser.parse_args()
    if args.trials < 3 or args.jobs < 1 or any(value < 2 for value in args.sample_sizes):
        raise ValueError("require at least three trials, one job, and sample sizes above one")
    root_seed = 20260910
    seed_sequence = np.random.SeedSequence(root_seed)
    seeds = [
        int(child.generate_state(1, dtype=np.uint64)[0])
        for child in seed_sequence.spawn(len(args.sample_sizes) * args.trials)
    ]
    tasks = [
        (sample_count, seeds[index * args.trials + trial])
        for index, sample_count in enumerate(args.sample_sizes)
        for trial in range(args.trials)
    ]
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        results = list(executor.map(run_coupled_trial, tasks))
    records, theoretical = aggregate_coupled(args.sample_sizes, args.trials, results)
    problem, trajectory, null_mask = coupled_problem()
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "trials_per_sample_size": args.trials,
        "nominal_screening_confidence": 0.975,
        "sample_sizes": args.sample_sizes,
        "node_count": problem["node_count"],
        "trajectory_dimension": int(trajectory.shape[0]),
        "candidate_count": len(problem["candidates"]),
        "time_count": len(problem["joints"]),
        "structural_null_state_count": int(np.count_nonzero(null_mask)),
        "theoretical_variance_error_correlation": theoretical.tolist(),
        "records": records,
    }
    json_output = root / "docs" / "trajectory_coupled_screen_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "trajectory_coupled_screen_calibration.png"
    plot_results(records, theoretical, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"N={record['sample_count']:,}",
            f"covariance={record['covariance_covered_rate']:.3f}",
            f"generic-score={record['score_covered_rate']:.3f}",
            f"null-score={record['null_score_covered_rate']:.3f}",
            f"path={record['null_population_path_retained_rate']:.3f}",
            f"null-states={record['mean_null_retained_state_fraction']:.3f}",
            f"null-edges={record['mean_null_retained_edge_fraction']:.3f}",
            f"correlation-mae={record['mean_absolute_correlation_error']:.3f}",
        )


if __name__ == "__main__":
    main()
