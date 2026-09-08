"""Calibrate Gaussian screening coverage and graph reduction by Wishart draws."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wishart

from observer_math import (
    adjacent_joint_covariance,
    gaussian_factor_aware_near_competitor_screen,
    moving_module_systems,
    observer_metrics_from_covariances,
    optimize_worldtube,
    propagate_covariances,
    transport_metrics_from_covariances,
)
from observer_math.gaussian import stationary_covariance
from observer_math.metrics import unique_bipartitions


@lru_cache(maxsize=1)
def population_problem():
    """Return one fixed model, candidate family, and exact score arrays."""
    node_count = 7
    planted_path, systems = moving_module_systems(node_count=node_count)
    return screening_problem_from_systems(planted_path, systems)


def screening_problem_from_systems(planted_path, systems):
    """Construct the fixed-candidate screening problem for supplied systems."""
    systems = tuple(systems)
    planted_path = tuple(tuple(candidate) for candidate in planted_path)
    if not systems or len(planted_path) != len(systems):
        raise ValueError("planted_path and systems must have the same positive length")
    node_count = np.asarray(systems[0][0]).shape[0]
    candidates = tuple(dict.fromkeys((*planted_path, (0, 3, 6), (0, 2, 5), (1, 4, 6))))
    covariances = propagate_covariances(
        [system[0] for system in systems[:-1]],
        [system[1] for system in systems[:-1]],
        stationary_covariance(*systems[0]),
    )
    joints = tuple(
        adjacent_joint_covariance(covariances[time], *systems[time]) for time in range(len(systems))
    )
    time_count = len(joints)
    candidate_count = len(candidates)
    local_factors = np.empty((time_count, candidate_count, 3))
    transport_factors = np.empty((time_count - 1, candidate_count, candidate_count, 2))
    minimum = np.empty((time_count, candidate_count))
    maximum = np.empty_like(minimum)
    for time, joint in enumerate(joints):
        for current, candidate in enumerate(candidates):
            metrics = observer_metrics_from_covariances(covariances[time], joint, candidate)
            local_factors[time, current] = (
                metrics.integration_strength,
                metrics.independence,
                metrics.persistence,
            )
            block_indices = tuple(range(node_count)) + tuple(
                node_count + node for node in candidate
            )
            eigenvalues = np.linalg.eigvalsh(joint[np.ix_(block_indices, block_indices)])
            minimum[time, current] = eigenvalues[0]
            maximum[time, current] = eigenvalues[-1]
        if time < time_count - 1:
            for previous, source in enumerate(candidates):
                for current, target in enumerate(candidates):
                    metrics = transport_metrics_from_covariances(
                        covariances[time], joint, source, target
                    )
                    transport_factors[time, previous, current] = (
                        metrics.independence,
                        metrics.persistence,
                    )
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    population_path = optimize_worldtube(
        local_scores,
        candidates,
        transport_scores=transport_scores,
        transport_weight=0.25,
        continuity_weight=0.08,
    ).candidate_indices
    return {
        "node_count": node_count,
        "systems": systems,
        "candidates": candidates,
        "covariances": covariances,
        "joints": joints,
        "local_factors": local_factors,
        "transport_factors": transport_factors,
        "minimum": minimum,
        "maximum": maximum,
        "population_path": population_path,
    }


def empirical_factors(empirical_joints, problem):
    """Compute every empirical primitive factor from sampled covariances."""
    candidates = problem["candidates"]
    node_count = problem["node_count"]
    time_count = len(empirical_joints)
    candidate_count = len(candidates)
    local = np.empty((time_count, candidate_count, 3))
    transport = np.empty((time_count - 1, candidate_count, candidate_count, 2))
    for time, joint in enumerate(empirical_joints):
        present = joint[:node_count, :node_count]
        for current, candidate in enumerate(candidates):
            metrics = observer_metrics_from_covariances(present, joint, candidate)
            local[time, current] = (
                metrics.integration_strength,
                metrics.independence,
                metrics.persistence,
            )
        if time < time_count - 1:
            for previous, source in enumerate(candidates):
                for current, target in enumerate(candidates):
                    metrics = transport_metrics_from_covariances(present, joint, source, target)
                    transport[time, previous, current] = (
                        metrics.independence,
                        metrics.persistence,
                    )
    return local, transport


def structural_integration_null_mask(problem, *, tolerance=1e-12):
    """Return model-fixed nulls verified through conditional cross-covariance.

    The moving-module construction has an exact block-support interpretation.
    This numerical audit separates its algebraic zeros from positive memory
    effects by more than eight orders of magnitude.
    """
    node_count = problem["node_count"]
    mask = np.zeros((len(problem["joints"]), len(problem["candidates"])), dtype=bool)

    def conditional_cross(covariance, x, y, given):
        return covariance[np.ix_(x, y)] - covariance[np.ix_(x, given)] @ np.linalg.solve(
            covariance[np.ix_(given, given)], covariance[np.ix_(given, y)]
        )

    for time, joint in enumerate(problem["joints"]):
        scale = max(1.0, float(np.linalg.norm(joint, ord=2)))
        for index, candidate in enumerate(problem["candidates"]):
            for left, right in unique_bipartitions(candidate):
                future_left = tuple(node_count + node for node in left)
                future_right = tuple(node_count + node for node in right)
                left_error = np.linalg.norm(
                    conditional_cross(joint, future_left, right, left), ord=2
                )
                right_error = np.linalg.norm(
                    conditional_cross(joint, future_right, left, right), ord=2
                )
                if max(left_error, right_error) <= tolerance * scale:
                    mask[time, index] = True
                    break
    return mask


def evaluate_empirical_joints(sample_count, empirical_joints, problem):
    """Evaluate screening coverage and graph size for supplied covariances."""
    empirical_local, empirical_transport = empirical_factors(empirical_joints, problem)
    candidates = problem["candidates"]
    time_count = len(problem["joints"])
    candidate_count = len(candidates)
    result = gaussian_factor_aware_near_competitor_screen(
        empirical_local,
        empirical_transport,
        candidates,
        sample_count,
        problem["node_count"],
        3,
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

    covariance_errors = np.empty((time_count, candidate_count))
    for time, (population, empirical) in enumerate(
        zip(problem["joints"], empirical_joints, strict=True)
    ):
        for current, candidate in enumerate(candidates):
            indices = tuple(range(problem["node_count"])) + tuple(
                problem["node_count"] + node for node in candidate
            )
            covariance_errors[time, current] = np.linalg.norm(
                empirical[np.ix_(indices, indices)] - population[np.ix_(indices, indices)],
                ord=2,
            )
    local_scores = np.prod(empirical_local, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(empirical_transport, axis=3))
    population_local_scores = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    population_transport_scores = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    covariance_covered = bool(np.all(covariance_errors <= result.covariance_spectral_errors))
    factor_covered = bool(
        np.all(
            np.abs(empirical_local - problem["local_factors"])
            <= result.screening_local_factor_errors
        )
        and np.all(
            np.abs(empirical_transport - problem["transport_factors"])
            <= result.screening_transport_factor_errors
        )
    )
    score_covered = bool(
        np.all(
            np.abs(local_scores - population_local_scores) <= result.screening_local_score_errors
        )
        and np.all(
            np.abs(transport_scores - population_transport_scores)
            <= result.screening_transport_score_errors
        )
    )
    path = problem["population_path"]
    path_retained = bool(
        all(path[time] in result.screen.viable_states[time] for time in range(time_count))
        and all(
            (path[time], path[time + 1]) in result.screen.viable_edges[time]
            for time in range(time_count - 1)
        )
    )
    return {
        "covariance_covered": covariance_covered,
        "factor_covered": factor_covered,
        "score_covered": score_covered,
        "population_path_retained": path_retained,
        "valid_perturbation_regime": result.all_blocks_valid,
        "maximum_covariance_radius_ratio": float(
            np.max(covariance_errors / result.covariance_spectral_errors)
        ),
        "retained_state_fraction": (
            result.screen.viable_state_count / (time_count * candidate_count)
        ),
        "retained_edge_fraction": (
            result.screen.viable_edge_count / ((time_count - 1) * candidate_count**2)
        ),
        "positive_local_floor_fraction": float(np.mean(result.positive_local_factor_floor_mask)),
        "positive_transport_floor_fraction": float(
            np.mean(result.positive_transport_factor_floor_mask)
        ),
    }


def run_trial(task):
    """Draw independent timewise Wishart covariances and evaluate one trial."""
    sample_count, seed = task
    problem = population_problem()
    rng = np.random.default_rng(seed)
    empirical_joints = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=rng,
        )
        for joint in problem["joints"]
    )
    return evaluate_empirical_joints(sample_count, empirical_joints, problem)


def wilson_interval(successes, total, z=1.959963984540054):
    proportion = successes / total
    denominator = 1.0 + z**2 / total
    center = (proportion + z**2 / (2.0 * total)) / denominator
    half_width = (
        z * np.sqrt(proportion * (1.0 - proportion) / total + z**2 / (4.0 * total**2)) / denominator
    )
    return [float(center - half_width), float(center + half_width)]


def aggregate(sample_sizes, trial_count, results):
    records = []
    offset = 0
    event_names = (
        "covariance_covered",
        "factor_covered",
        "score_covered",
        "population_path_retained",
        "valid_perturbation_regime",
    )
    mean_names = (
        "maximum_covariance_radius_ratio",
        "retained_state_fraction",
        "retained_edge_fraction",
        "positive_local_floor_fraction",
        "positive_transport_floor_fraction",
    )
    for sample_count in sample_sizes:
        group = results[offset : offset + trial_count]
        offset += trial_count
        record = {"sample_count": sample_count}
        for name in event_names:
            successes = sum(result[name] for result in group)
            record[f"{name}_rate"] = successes / trial_count
            record[f"{name}_wilson_95"] = wilson_interval(successes, trial_count)
        for name in mean_names:
            values = np.array([result[name] for result in group])
            record[f"mean_{name}"] = float(np.mean(values))
            record[f"standard_error_{name}"] = float(np.std(values, ddof=1) / np.sqrt(trial_count))
        records.append(record)
    return records


def plot_results(records, output):
    sample_sizes = [record["sample_count"] for record in records]
    sample_labels = {
        80_000: "80K",
        8_000_000: "8M",
        800_000_000: "800M",
        80_000_000_000: "80B",
        8_000_000_000_000: "8T",
    }
    positions = np.arange(len(sample_sizes))
    figure, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharex=True)
    coverage_series = (
        ("covariance_covered_rate", "Covariance event"),
        ("factor_covered_rate", "Primitive factors"),
        ("score_covered_rate", "Complete scores"),
        ("population_path_retained_rate", "Population path retained"),
    )
    bar_width = 0.19
    for series_index, (key, label) in enumerate(coverage_series):
        axes[0].bar(
            positions + (series_index - 1.5) * bar_width,
            [record[key] for record in records],
            width=bar_width,
            label=label,
        )
    axes[0].axhline(0.975, color="black", linestyle="--", linewidth=1, label="Target")
    reduction_series = (
        ("mean_retained_state_fraction", "Retained states"),
        ("mean_retained_edge_fraction", "Retained edges"),
        ("mean_positive_local_floor_fraction", "Positive local floors"),
        ("mean_positive_transport_floor_fraction", "Positive transport floors"),
    )
    for key, label in reduction_series:
        axes[1].plot(
            positions,
            [record[key] for record in records],
            marker="o",
            label=label,
        )
    for axis in axes:
        axis.set_xticks(
            positions,
            labels=[sample_labels.get(value, f"{value:.1e}") for value in sample_sizes],
        )
        axis.set_ylim(-0.03, 1.03)
        axis.set_xlabel("Screening observations")
        axis.grid(alpha=0.25)
        axis.legend(loc="lower left", fontsize=8)
    axes[0].set_ylabel("Trial fraction")
    axes[1].set_ylabel("Mean graph or factor fraction")
    axes[0].set_title("Simultaneous empirical coverage")
    axes[1].set_title("Screen reduction and certified factor floors")
    figure.suptitle("Gaussian first-split calibration")
    figure.tight_layout()
    figure.savefig(output, dpi=180)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument(
        "--sample-sizes",
        type=int,
        nargs="+",
        default=[
            80_000,
            8_000_000,
            800_000_000,
            80_000_000_000,
            8_000_000_000_000,
        ],
    )
    args = parser.parse_args()
    if args.trials < 2 or args.jobs < 1 or any(value < 2 for value in args.sample_sizes):
        raise ValueError("require at least two trials, one job, and sample sizes above one")
    seed_sequence = np.random.SeedSequence(20260908)
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
        results = list(executor.map(run_trial, tasks))
    records = aggregate(args.sample_sizes, args.trials, results)
    problem = population_problem()
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": 20260908,
        "trials_per_sample_size": args.trials,
        "nominal_screening_confidence": 0.975,
        "sample_sizes": args.sample_sizes,
        "node_count": problem["node_count"],
        "subset_size": 3,
        "candidate_count": len(problem["candidates"]),
        "time_count": len(problem["joints"]),
        "population_path_indices": problem["population_path"],
        "records": records,
    }
    json_output = root / "docs" / "gaussian_screen_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "gaussian_screen_calibration.png"
    plot_results(records, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"N={record['sample_count']:,}",
            f"covariance={record['covariance_covered_rate']:.3f}",
            f"factors={record['factor_covered_rate']:.3f}",
            f"scores={record['score_covered_rate']:.3f}",
            f"path={record['population_path_retained_rate']:.3f}",
            f"states={record['mean_retained_state_fraction']:.3f}",
            f"edges={record['mean_retained_edge_fraction']:.3f}",
        )


if __name__ == "__main__":
    main()
