"""Compare oracle, calibrated-drift, and refreshed-reference certificates."""

from __future__ import annotations

import argparse
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wishart

from observer_math import (
    gaussian_calibrated_drift_relative_near_competitor_screen,
    gaussian_cross_fitted_relative_near_competitor_screen,
    gaussian_drift_robust_relative_near_competitor_screen,
)

if __package__:
    from examples.cross_fitted_relative_calibration import (
        _candidate_relative_errors,
    )
    from examples.drift_robust_relative_calibration import (
        _candidate_drift_errors,
        _drifted_population,
    )
    from examples.gaussian_screen_calibration import empirical_factors, wilson_interval
    from examples.multi_regime_coupled_calibration import regime_problem
    from examples.trajectory_coupled_screen_calibration import extract_adjacent_covariances
else:
    from cross_fitted_relative_calibration import _candidate_relative_errors
    from drift_robust_relative_calibration import (
        _candidate_drift_errors,
        _drifted_population,
    )
    from gaussian_screen_calibration import empirical_factors, wilson_interval
    from multi_regime_coupled_calibration import regime_problem
    from trajectory_coupled_screen_calibration import extract_adjacent_covariances


def evaluate_trial(task):
    (
        calibration_sample_count,
        calibration_seed,
        screening_seed,
        problem,
        current_trajectory,
        current_joints,
        exact_drift,
        null_mask,
        reference_joints,
        reference_sample_count,
        screening_sample_count,
    ) = task
    calibration_rng = np.random.default_rng(calibration_seed)
    screening_rng = np.random.default_rng(screening_seed)
    calibration_trajectory = wishart.rvs(
        df=calibration_sample_count - 1,
        scale=current_trajectory / (calibration_sample_count - 1),
        random_state=calibration_rng,
    )
    screening_trajectory = wishart.rvs(
        df=screening_sample_count - 1,
        scale=current_trajectory / (screening_sample_count - 1),
        random_state=screening_rng,
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    calibration_joints = extract_adjacent_covariances(
        calibration_trajectory, problem["node_count"], time_count
    )
    screening_joints = extract_adjacent_covariances(
        screening_trajectory, problem["node_count"], time_count
    )
    zeros_local = np.zeros((time_count, candidate_count))
    zeros_transport = np.zeros((time_count - 1, candidate_count, candidate_count))
    common = {
        "structural_integration_null_mask": null_mask,
        "certification_local_score_errors": zeros_local,
        "certification_transport_score_errors": zeros_transport,
        "transport_weight": 0.25,
        "continuity_weight": 0.08,
    }
    oracle = gaussian_drift_robust_relative_near_competitor_screen(
        reference_joints,
        screening_joints,
        problem["candidates"],
        reference_sample_count,
        problem["node_count"],
        3,
        population_drift_relative_errors=exact_drift,
        confidence=0.975,
        **common,
    )
    calibrated = gaussian_calibrated_drift_relative_near_competitor_screen(
        reference_joints,
        calibration_joints,
        screening_joints,
        problem["candidates"],
        reference_sample_count,
        calibration_sample_count,
        problem["node_count"],
        3,
        confidence=0.975,
        **common,
    )
    refreshed = gaussian_cross_fitted_relative_near_competitor_screen(
        calibration_joints,
        screening_joints,
        problem["candidates"],
        calibration_sample_count,
        problem["node_count"],
        3,
        confidence=0.975,
        **common,
    )
    actual = _candidate_relative_errors(current_joints, screening_joints, problem)
    local_factors, transport_factors = empirical_factors(screening_joints, problem)
    empirical_local = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    population_local = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    empirical_transport = np.sqrt(np.prod(transport_factors, axis=3))
    population_transport = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    calibrated_screen = calibrated.screening
    score_covered = bool(
        np.all(
            np.abs(empirical_local - population_local)
            <= calibrated_screen.screening_local_score_errors
        )
        and np.all(
            np.abs(empirical_transport - population_transport)
            <= calibrated_screen.screening_transport_score_errors
        )
    )
    path = problem["population_path"]
    path_retained = bool(
        all(
            path[time] in calibrated_screen.screen.viable_states[time]
            for time in range(time_count)
        )
        and all(
            (path[time], path[time + 1])
            in calibrated_screen.screen.viable_edges[time]
            for time in range(time_count - 1)
        )
    )
    state_total = time_count * candidate_count
    edge_total = (time_count - 1) * candidate_count**2
    result = {
        "calibration_sample_count": calibration_sample_count,
        "drift_envelope_covered": bool(
            np.all(exact_drift <= calibrated.drift_calibration.population_drift_relative_errors)
        ),
        "covariance_covered": bool(
            np.all(actual <= calibrated_screen.covariance_relative_errors)
        ),
        "score_covered": score_covered,
        "path_retained": path_retained,
        "all_bounds_valid": calibrated.guarantees_safe_screen,
        "maximum_estimated_drift": (
            calibrated.drift_calibration.maximum_population_drift_relative_error
        ),
    }
    for label, screen in (
        ("oracle", oracle),
        ("calibrated", calibrated_screen),
        ("refreshed", refreshed),
    ):
        result[f"{label}_maximum_radius"] = screen.maximum_covariance_relative_error
        result[f"{label}_state_fraction"] = (
            screen.screen.viable_state_count / state_total
        )
        result[f"{label}_edge_fraction"] = (
            screen.screen.viable_edge_count / edge_total
        )
    return result


def aggregate(sample_count, trials):
    record = {
        "current_calibration_sample_count": sample_count,
        "trial_count": len(trials),
    }
    for name in (
        "drift_envelope_covered",
        "covariance_covered",
        "score_covered",
        "path_retained",
        "all_bounds_valid",
    ):
        successes = sum(trial[name] for trial in trials)
        record[f"{name}_rate"] = successes / len(trials)
        record[f"{name}_wilson_95"] = wilson_interval(successes, len(trials))
    for name in (
        "maximum_estimated_drift",
        "oracle_maximum_radius",
        "calibrated_maximum_radius",
        "refreshed_maximum_radius",
        "oracle_state_fraction",
        "calibrated_state_fraction",
        "refreshed_state_fraction",
        "oracle_edge_fraction",
        "calibrated_edge_fraction",
        "refreshed_edge_fraction",
    ):
        values = np.asarray([trial[name] for trial in trials])
        record[f"mean_{name}"] = float(np.mean(values))
        record[f"standard_error_{name}"] = float(
            np.std(values, ddof=1) / np.sqrt(len(values))
        )
    return record


def plot_results(records, exact_maximum_drift, output):
    samples = np.asarray(
        [record["current_calibration_sample_count"] for record in records]
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.2), constrained_layout=True)
    estimated = np.asarray(
        [record["mean_maximum_estimated_drift"] for record in records]
    )
    axes[0, 0].plot(samples, estimated, "o-", label="calibrated upper bound")
    axes[0, 0].axhline(exact_maximum_drift, ls="--", color="black", label="exact drift")
    axes[0, 0].set_title("Population-drift envelope")
    axes[0, 0].set_ylabel("maximum relative drift")
    axes[0, 0].legend(frameon=False)

    styles = (("oracle", "oracle envelope"), ("calibrated", "estimated envelope"),
              ("refreshed", "current reference"))
    for key, label in styles:
        axes[0, 1].plot(
            samples,
            [record[f"mean_{key}_maximum_radius"] for record in records],
            "o-",
            label=label,
        )
        axes[1, 0].plot(
            samples,
            100 * np.asarray([record[f"mean_{key}_state_fraction"] for record in records]),
            "o-",
            label=label,
        )
        axes[1, 1].plot(
            samples,
            100 * np.asarray([record[f"mean_{key}_edge_fraction"] for record in records]),
            "o-",
            label=label,
        )
    axes[0, 1].set_title("Maximum current-population radius")
    axes[0, 1].set_ylabel("relative radius")
    axes[1, 0].set_title("States retained")
    axes[1, 0].set_ylabel("retained (%)")
    axes[1, 1].set_title("Edges retained")
    axes[1, 1].set_ylabel("retained (%)")
    for axis in axes.flat:
        axis.set_xscale("log")
        axis.set_xlabel("current calibration trajectories")
        axis.grid(alpha=0.25)
    for axis in axes.flat[1:]:
        axis.legend(frameon=False)
    figure.suptitle(
        "Estimating drift versus refreshing the covariance reference",
        fontsize=14,
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--reference-sample-count", type=int, default=8_000_000_000_000)
    parser.add_argument("--screening-sample-count", type=int, default=300_000_000)
    args = parser.parse_args()
    if args.trials < 2 or args.jobs < 1:
        raise ValueError("require at least two trials and one worker")
    problem, trajectory, null_mask, _, _ = regime_problem(0.32, 0.46, 0.18, 1.0)
    time_count = len(problem["joints"])
    current_trajectory, current_joints = _drifted_population(
        trajectory, problem["node_count"], time_count, 0.00010
    )
    exact_drift = _candidate_drift_errors(problem["joints"], current_joints, problem)
    sample_counts = (
        300_000_000,
        1_000_000_000,
        3_000_000_000,
        10_000_000_000,
        30_000_000_000,
        100_000_000_000,
        300_000_000_000,
        1_000_000_000_000,
        3_000_000_000_000,
        8_000_000_000_000,
    )
    root_seed = 20260924
    children = np.random.SeedSequence(root_seed).spawn(
        1 + 2 * len(sample_counts) * args.trials
    )
    reference_rng = np.random.default_rng(
        int(children[0].generate_state(1, dtype=np.uint64)[0])
    )
    reference_trajectory = wishart.rvs(
        df=args.reference_sample_count - 1,
        scale=trajectory / (args.reference_sample_count - 1),
        random_state=reference_rng,
    )
    reference_joints = extract_adjacent_covariances(
        reference_trajectory, problem["node_count"], time_count
    )
    tasks = []
    offset = 1
    for sample_count in sample_counts:
        for trial in range(args.trials):
            calibration_seed = int(
                children[offset + 2 * trial].generate_state(1, dtype=np.uint64)[0]
            )
            screening_seed = int(
                children[offset + 2 * trial + 1].generate_state(1, dtype=np.uint64)[0]
            )
            tasks.append(
                (
                    sample_count,
                    calibration_seed,
                    screening_seed,
                    problem,
                    current_trajectory,
                    current_joints,
                    exact_drift,
                    null_mask,
                    reference_joints,
                    args.reference_sample_count,
                    args.screening_sample_count,
                )
            )
        offset += 2 * args.trials
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        trial_results = list(executor.map(evaluate_trial, tasks))
    records = [
        aggregate(
            sample_count,
            [
                trial
                for trial in trial_results
                if trial["calibration_sample_count"] == sample_count
            ],
        )
        for sample_count in sample_counts
    ]
    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "requested_overall_confidence": 0.975,
        "component_confidence": 0.9875,
        "reference_sample_count": args.reference_sample_count,
        "screening_sample_count": args.screening_sample_count,
        "log_scale_amplitude": 0.00010,
        "maximum_exact_population_drift": float(np.max(exact_drift)),
        "trials_per_calibration_size": args.trials,
        "records": records,
    }
    json_output = root / "docs" / "calibrated_drift_comparison.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "calibrated_drift_comparison.png"
    plot_results(records, float(np.max(exact_drift)), figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"Ncal={record['current_calibration_sample_count']}",
            f"rho={record['mean_maximum_estimated_drift']:.6f}",
            f"radii={record['mean_oracle_maximum_radius']:.6f}/"
            f"{record['mean_calibrated_maximum_radius']:.6f}/"
            f"{record['mean_refreshed_maximum_radius']:.6f}",
            f"states={record['mean_oracle_state_fraction']:.3f}/"
            f"{record['mean_calibrated_state_fraction']:.3f}/"
            f"{record['mean_refreshed_state_fraction']:.3f}",
        )


if __name__ == "__main__":
    main()
