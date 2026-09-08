"""Calibrate drift-robust pilot normalization under structure-preserving drift."""

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
    gaussian_drift_robust_relative_near_competitor_screen,
)

if __package__:
    from examples.cross_fitted_relative_calibration import (
        _candidate_relative_errors,
    )
    from examples.gaussian_screen_calibration import empirical_factors, wilson_interval
    from examples.multi_regime_coupled_calibration import regime_problem
    from examples.trajectory_coupled_screen_calibration import extract_adjacent_covariances
else:
    from cross_fitted_relative_calibration import _candidate_relative_errors
    from gaussian_screen_calibration import empirical_factors, wilson_interval
    from multi_regime_coupled_calibration import regime_problem
    from trajectory_coupled_screen_calibration import extract_adjacent_covariances


def _drifted_population(trajectory, node_count, time_count, amplitude):
    """Apply a fixed invertible coordinate rescaling to a full trajectory."""
    signs = np.fromfunction(
        lambda time, node: (-1.0) ** (time + node),
        (time_count + 1, node_count),
    )
    scales = np.exp(amplitude * signs).reshape(-1)
    drifted = scales[:, None] * trajectory * scales[None, :]
    return drifted, extract_adjacent_covariances(drifted, node_count, time_count)


def _candidate_drift_errors(reference_joints, drifted_joints, problem):
    return _candidate_relative_errors(reference_joints, drifted_joints, problem)


def evaluate_draw(task):
    (
        amplitude,
        seed,
        problem,
        drifted_trajectory,
        drifted_joints,
        drift_errors,
        null_mask,
        pilot_joints,
        pilot_sample_count,
        screening_sample_count,
    ) = task
    rng = np.random.default_rng(seed)
    empirical_trajectory = wishart.rvs(
        df=screening_sample_count - 1,
        scale=drifted_trajectory / (screening_sample_count - 1),
        random_state=rng,
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    screening_joints = extract_adjacent_covariances(
        empirical_trajectory, problem["node_count"], time_count
    )
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
    stationary = gaussian_cross_fitted_relative_near_competitor_screen(
        pilot_joints,
        screening_joints,
        problem["candidates"],
        pilot_sample_count,
        problem["node_count"],
        3,
        **common,
    )
    robust = gaussian_drift_robust_relative_near_competitor_screen(
        pilot_joints,
        screening_joints,
        problem["candidates"],
        pilot_sample_count,
        problem["node_count"],
        3,
        population_drift_relative_errors=drift_errors,
        **common,
    )
    actual = _candidate_relative_errors(drifted_joints, screening_joints, problem)
    local_factors, transport_factors = empirical_factors(screening_joints, problem)
    empirical_local = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    population_local = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    empirical_transport = np.sqrt(np.prod(transport_factors, axis=3))
    population_transport = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    score_covered = bool(
        np.all(
            np.abs(empirical_local - population_local)
            <= robust.screening_local_score_errors
        )
        and np.all(
            np.abs(empirical_transport - population_transport)
            <= robust.screening_transport_score_errors
        )
    )
    path = problem["population_path"]
    path_retained = bool(
        all(path[t] in robust.screen.viable_states[t] for t in range(time_count))
        and all(
            (path[t], path[t + 1]) in robust.screen.viable_edges[t]
            for t in range(time_count - 1)
        )
    )
    state_total = time_count * candidate_count
    edge_total = (time_count - 1) * candidate_count**2
    return {
        "amplitude": amplitude,
        "covariance_covered": bool(np.all(actual <= robust.covariance_relative_errors)),
        "score_covered": score_covered,
        "path_retained": path_retained,
        "all_blocks_valid": robust.all_blocks_valid,
        "maximum_actual_relative_error": float(np.max(actual)),
        "maximum_stationary_radius": stationary.maximum_covariance_relative_error,
        "maximum_robust_radius": robust.maximum_covariance_relative_error,
        "robust_to_stationary_radius_ratio": (
            robust.maximum_covariance_relative_error
            / stationary.maximum_covariance_relative_error
        ),
        "stationary_state_fraction": stationary.screen.viable_state_count / state_total,
        "robust_state_fraction": robust.screen.viable_state_count / state_total,
        "stationary_edge_fraction": stationary.screen.viable_edge_count / edge_total,
        "robust_edge_fraction": robust.screen.viable_edge_count / edge_total,
    }


def _aggregate(amplitude, drift_errors, population_factor_change, trials):
    record = {
        "log_scale_amplitude": amplitude,
        "maximum_population_drift_relative_error": float(np.max(drift_errors)),
        "minimum_population_drift_relative_error": float(np.min(drift_errors)),
        "maximum_population_factor_change": population_factor_change,
        "trial_count": len(trials),
    }
    for name in (
        "covariance_covered",
        "score_covered",
        "path_retained",
        "all_blocks_valid",
    ):
        successes = sum(trial[name] for trial in trials)
        record[f"{name}_rate"] = successes / len(trials)
        record[f"{name}_wilson_95"] = wilson_interval(successes, len(trials))
    for name in (
        "maximum_actual_relative_error",
        "maximum_stationary_radius",
        "maximum_robust_radius",
        "robust_to_stationary_radius_ratio",
        "stationary_state_fraction",
        "robust_state_fraction",
        "stationary_edge_fraction",
        "robust_edge_fraction",
    ):
        values = np.asarray([trial[name] for trial in trials])
        record[f"mean_{name}"] = float(np.mean(values))
        record[f"standard_error_{name}"] = float(
            np.std(values, ddof=1) / np.sqrt(len(values))
        )
    return record


def plot_results(records, output):
    drift = 100 * np.asarray(
        [record["maximum_population_drift_relative_error"] for record in records]
    )
    stationary_radius = np.asarray(
        [record["mean_maximum_stationary_radius"] for record in records]
    )
    robust_radius = np.asarray(
        [record["mean_maximum_robust_radius"] for record in records]
    )
    figure, axes = plt.subplots(2, 2, figsize=(11.8, 8.2), constrained_layout=True)

    axes[0, 0].plot(drift, stationary_radius, "o-", label="stationary formula")
    axes[0, 0].plot(drift, robust_radius, "o-", label="drift-robust formula")
    axes[0, 0].set_title("Maximum candidate covariance radius")
    axes[0, 0].set_ylabel("relative radius")
    axes[0, 0].legend(frameon=False)

    axes[0, 1].plot(
        drift,
        100 * np.asarray([record["mean_robust_state_fraction"] for record in records]),
        "o-",
        label="states",
    )
    axes[0, 1].plot(
        drift,
        100 * np.asarray([record["mean_robust_edge_fraction"] for record in records]),
        "s-",
        label="edges",
    )
    axes[0, 1].set_title("Drift-robust graph retained")
    axes[0, 1].set_ylabel("retained (%)")
    axes[0, 1].legend(frameon=False)

    coverage_names = (
        ("covariance_covered_rate", "covariance"),
        ("score_covered_rate", "complete score"),
        ("path_retained_rate", "population path"),
    )
    for name, label in coverage_names:
        axes[1, 0].plot(
            drift,
            100 * np.asarray([record[name] for record in records]),
            "o-",
            label=label,
        )
    axes[1, 0].set_title("Recorded event frequency (64 trials per point)")
    axes[1, 0].set_ylabel("trials satisfying event (%)")
    axes[1, 0].set_ylim(90, 100.5)
    axes[1, 0].legend(frameon=False)

    radius_increment = robust_radius - stationary_radius
    declared_radius = drift / 100
    axes[1, 1].plot(
        drift, radius_increment, "o-", label="added certificate radius"
    )
    axes[1, 1].plot(drift, declared_radius, "--", label=r"declared $\rho$")
    axes[1, 1].set_title("Additive price of the drift guarantee")
    axes[1, 1].set_ylabel("relative radius")
    axes[1, 1].legend(frameon=False)

    for axis in axes.flat:
        axis.set_xlabel(r"maximum declared drift $100\rho$ (%)")
        axis.grid(alpha=0.25)
    figure.suptitle(
        "Pilot-normalized screening under structure-preserving covariance drift",
        fontsize=14,
    )
    figure.savefig(output, dpi=180)
    plt.close(figure)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=64)
    parser.add_argument("--jobs", type=int, default=6)
    parser.add_argument("--pilot-sample-count", type=int, default=8_000_000_000_000)
    parser.add_argument("--screening-sample-count", type=int, default=300_000_000)
    args = parser.parse_args()
    if args.trials < 2 or args.jobs < 1:
        raise ValueError("require at least two trials and one worker")

    problem, trajectory, null_mask, _, _ = regime_problem(
        0.32, 0.46, 0.18, 1.0
    )
    time_count = len(problem["joints"])
    amplitudes = (0.0, 0.00005, 0.00010, 0.00020, 0.00035, 0.00050, 0.00075)
    root_seed = 20260918
    children = np.random.SeedSequence(root_seed).spawn(
        1 + len(amplitudes) * args.trials
    )
    pilot_rng = np.random.default_rng(
        int(children[0].generate_state(1, dtype=np.uint64)[0])
    )
    pilot_trajectory = wishart.rvs(
        df=args.pilot_sample_count - 1,
        scale=trajectory / (args.pilot_sample_count - 1),
        random_state=pilot_rng,
    )
    pilot_joints = extract_adjacent_covariances(
        pilot_trajectory, problem["node_count"], time_count
    )
    tasks = []
    drift_by_amplitude = {}
    factor_change_by_amplitude = {}
    offset = 1
    for amplitude in amplitudes:
        drifted_trajectory, drifted_joints = _drifted_population(
            trajectory, problem["node_count"], time_count, amplitude
        )
        drift_errors = _candidate_drift_errors(
            problem["joints"], drifted_joints, problem
        )
        drift_by_amplitude[amplitude] = drift_errors
        drifted_local, drifted_transport = empirical_factors(drifted_joints, problem)
        factor_change = max(
            float(np.max(np.abs(drifted_local - problem["local_factors"]))),
            float(np.max(np.abs(drifted_transport - problem["transport_factors"]))),
        )
        if factor_change > 1e-10:
            raise RuntimeError("coordinate drift changed a population factor")
        factor_change_by_amplitude[amplitude] = factor_change
        for child in children[offset : offset + args.trials]:
            seed = int(child.generate_state(1, dtype=np.uint64)[0])
            tasks.append(
                (
                    amplitude,
                    seed,
                    problem,
                    drifted_trajectory,
                    drifted_joints,
                    drift_errors,
                    null_mask,
                    pilot_joints,
                    args.pilot_sample_count,
                    args.screening_sample_count,
                )
            )
        offset += args.trials
    with ProcessPoolExecutor(max_workers=args.jobs) as executor:
        trial_results = list(executor.map(evaluate_draw, tasks))
    records = []
    for amplitude in amplitudes:
        trials = [
            trial for trial in trial_results if trial["amplitude"] == amplitude
        ]
        records.append(
            _aggregate(
                amplitude,
                drift_by_amplitude[amplitude],
                factor_change_by_amplitude[amplitude],
                trials,
            )
        )

    root = Path(__file__).resolve().parents[1]
    payload = {
        "seed": root_seed,
        "construction": (
            "checkerboard diagonal congruence with scale exp(amplitude*(-1)^(t+j)); "
            "population information factors and path are invariant"
        ),
        "trials_per_drift_level": args.trials,
        "pilot_sample_count": args.pilot_sample_count,
        "screening_sample_count": args.screening_sample_count,
        "nominal_pilot_confidence": 0.975,
        "records": records,
    }
    json_output = root / "docs" / "drift_robust_relative_calibration.json"
    json_output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    figure_output = root / "docs" / "drift_robust_relative_calibration.png"
    plot_results(records, figure_output)
    print("Results:", json_output)
    print("Figure:", figure_output)
    for record in records:
        print(
            f"rho={record['maximum_population_drift_relative_error']:.6f}",
            f"radius={record['mean_maximum_robust_radius']:.6f}",
            f"states={record['mean_robust_state_fraction']:.3f}",
            f"edges={record['mean_robust_edge_fraction']:.3f}",
            f"coverage={record['score_covered_rate']:.3f}",
        )


if __name__ == "__main__":
    main()
