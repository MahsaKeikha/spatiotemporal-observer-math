"""Generate the first observer world-tube illustration."""

from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math import (
    adjacent_joint_covariance,
    certify_worldtube,
    componentwise_recovery_bound,
    gaussian_path_recovery_bound,
    localized_gaussian_path_recovery_bound,
    minimum_gaussian_sample_size,
    minimum_localized_gaussian_sample_size,
    moving_module_systems,
    observer_metrics_from_covariances,
    optimize_worldtube,
    propagate_covariances,
    transport_metrics,
)
from observer_math.gaussian import stationary_covariance


def main():
    node_count = 7
    planted_path, systems = moving_module_systems(node_count=node_count)
    candidates = tuple(combinations(range(node_count), 3))
    covariances = propagate_covariances(
        [system[0] for system in systems[:-1]],
        [system[1] for system in systems[:-1]],
        stationary_covariance(*systems[0]),
    )
    local_scores = np.zeros((len(systems), len(candidates)))
    local_factors = np.zeros((len(systems), len(candidates), 3))
    minimum_block_eigenvalues = np.zeros((len(systems), len(candidates)))
    maximum_block_eigenvalues = np.zeros((len(systems), len(candidates)))
    joint_covariances = []
    for time, (transition, noise) in enumerate(systems):
        joint = adjacent_joint_covariance(covariances[time], transition, noise)
        joint_covariances.append(joint)
        for index, candidate in enumerate(candidates):
            metrics = observer_metrics_from_covariances(
                covariances[time], joint, candidate
            )
            local_scores[time, index] = metrics.observer_score
            local_factors[time, index] = (
                metrics.integration_strength,
                metrics.independence,
                metrics.persistence,
            )
            block_indices = tuple(range(node_count)) + tuple(
                node_count + node for node in candidate
            )
            block_eigenvalues = np.linalg.eigvalsh(
                joint[np.ix_(block_indices, block_indices)]
            )
            minimum_block_eigenvalues[time, index] = block_eigenvalues[0]
            maximum_block_eigenvalues[time, index] = block_eigenvalues[-1]

    transport = np.zeros((len(systems) - 1, len(candidates), len(candidates)))
    transport_factors = np.zeros(
        (len(systems) - 1, len(candidates), len(candidates), 2)
    )
    for time in range(len(systems) - 1):
        transition, noise = systems[time]
        for previous, source in enumerate(candidates):
            for current, target in enumerate(candidates):
                metrics = transport_metrics(
                    covariances[time], transition, noise, source, target
                )
                transport[time, previous, current] = metrics.transport_score
                transport_factors[time, previous, current] = (
                    metrics.independence,
                    metrics.persistence,
                )

    certificate = certify_worldtube(
        local_scores,
        candidates,
        transport_scores=transport,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    result = certificate.result
    planted_indices = tuple(candidates.index(subset) for subset in planted_path)
    recovery_bound = componentwise_recovery_bound(
        local_scores,
        candidates,
        planted_indices,
        transport_scores=transport,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    print("Planted path:", planted_path)
    print("Recovered path:", result.path)
    print("Total action:", f"{result.total_action:.6f}")
    print("Runner-up action:", f"{certificate.runner_up_action:.6f}")
    print("Optimality margin:", f"{certificate.action_margin:.6f}")
    print("Certified uniform score radius:", f"{certificate.uniform_score_radius:.6f}")
    print(
        "Componentwise sufficient condition:",
        "satisfied" if recovery_bound.guarantees_unique_recovery else "not satisfied",
    )
    print("Minimum componentwise margin:", f"{recovery_bound.minimum_margin:.6f}")
    minimum_joint_eigenvalue = min(
        float(np.linalg.eigvalsh(joint)[0]) for joint in joint_covariances
    )
    maximum_joint_eigenvalue = max(
        float(np.linalg.eigvalsh(joint)[-1]) for joint in joint_covariances
    )
    finite_bound = gaussian_path_recovery_bound(
        certificate.action_margin,
        node_count,
        len(planted_path[0]),
        len(planted_path),
        640,
        minimum_joint_eigenvalue=minimum_joint_eigenvalue,
        maximum_joint_eigenvalue=maximum_joint_eigenvalue,
        confidence=0.95,
        transport_weight=0.25,
    )
    sufficient_sample_count = minimum_gaussian_sample_size(
        certificate.action_margin,
        node_count,
        len(planted_path[0]),
        len(planted_path),
        minimum_joint_eigenvalue=minimum_joint_eigenvalue,
        maximum_joint_eigenvalue=maximum_joint_eigenvalue,
        confidence=0.95,
        transport_weight=0.25,
        maximum_sample_count=10**30,
    )
    localized_bound = localized_gaussian_path_recovery_bound(
        local_factors,
        transport_factors,
        candidates,
        640,
        node_count,
        len(planted_path[0]),
        minimum_block_eigenvalues=minimum_block_eigenvalues,
        maximum_block_eigenvalues=maximum_block_eigenvalues,
        confidence=0.95,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    localized_sample_count = minimum_localized_gaussian_sample_size(
        local_factors,
        transport_factors,
        candidates,
        node_count,
        len(planted_path[0]),
        minimum_block_eigenvalues=minimum_block_eigenvalues,
        maximum_block_eigenvalues=maximum_block_eigenvalues,
        confidence=0.95,
        transport_weight=0.25,
        continuity_weight=0.08,
        maximum_sample_count=10**30,
    )
    localized_threshold_bound = localized_gaussian_path_recovery_bound(
        local_factors,
        transport_factors,
        candidates,
        localized_sample_count,
        node_count,
        len(planted_path[0]),
        minimum_block_eigenvalues=minimum_block_eigenvalues,
        maximum_block_eigenvalues=maximum_block_eigenvalues,
        confidence=0.95,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    print("Joint covariance eigenvalue interval:", f"[{minimum_joint_eigenvalue:.6f}, {maximum_joint_eigenvalue:.6f}]")
    print(
        "640-sample end-to-end guarantee:",
        "certified" if finite_bound.guarantees_population_path else "not certified",
    )
    print(
        "Sufficient sample count from worst-case bound:",
        f"{sufficient_sample_count:.3e}",
    )
    print(
        "640-sample localized guarantee:",
        "certified" if localized_bound.guarantees_population_path else "not certified",
    )
    print(
        "Sufficient sample count from localized bound:",
        f"{localized_sample_count:.3e}",
    )
    print(
        "Near-competitor graph at localized threshold:",
        f"{localized_threshold_bound.viable_state_count}/{len(systems) * len(candidates)} states,",
        f"{localized_threshold_bound.viable_edge_count}/{(len(systems) - 1) * len(candidates) ** 2} edges",
    )

    order = np.argsort(-local_scores.max(axis=0))[:12]
    display = local_scores[:, order].T
    labels = [str(candidates[index]) for index in order]
    figure, axis = plt.subplots(figsize=(9, 6))
    image = axis.imshow(display, aspect="auto", cmap="magma", vmin=0)
    axis.set_xlabel("Time step")
    axis.set_ylabel("Candidate subsystem")
    axis.set_yticks(np.arange(len(labels)), labels=labels)
    axis.set_title("Distributional world-tube through changing physical nodes")
    for time, subset in enumerate(result.path):
        if subset in [candidates[index] for index in order]:
            row = [candidates[index] for index in order].index(subset)
            axis.scatter(time, row, marker="s", facecolors="none", edgecolors="cyan", s=180)
    figure.colorbar(image, ax=axis, label="Local observer score")
    figure.tight_layout()
    output = Path(__file__).resolve().parents[1] / "docs" / "worldtube_baseline.png"
    figure.savefig(output, dpi=180)
    print("Figure:", output)

    transport_weights = np.linspace(0.0, 0.6, 25)
    continuity_weights = np.linspace(0.0, 0.8, 25)
    recovery = np.zeros((len(continuity_weights), len(transport_weights)))
    for row, continuity_weight in enumerate(continuity_weights):
        for column, transport_weight in enumerate(transport_weights):
            trial = optimize_worldtube(
                local_scores,
                candidates,
                transport_scores=transport,
                transport_weight=float(transport_weight),
                continuity_weight=float(continuity_weight),
            )
            recovery[row, column] = np.mean(
                [found == planted for found, planted in zip(trial.path, planted_path)]
            )

    phase_figure, phase_axis = plt.subplots(figsize=(8, 6))
    phase_image = phase_axis.imshow(
        recovery,
        origin="lower",
        aspect="auto",
        extent=(
            transport_weights[0],
            transport_weights[-1],
            continuity_weights[0],
            continuity_weights[-1],
        ),
        cmap="viridis",
        vmin=0,
        vmax=1,
    )
    phase_axis.set_xlabel("Transport weight")
    phase_axis.set_ylabel("Material-continuity weight")
    phase_axis.set_title("Exact planted-boundary recovery across regularization")
    phase_figure.colorbar(phase_image, ax=phase_axis, label="Fraction of boundaries recovered")
    phase_figure.tight_layout()
    phase_output = output.with_name("worldtube_phase_diagram.png")
    phase_figure.savefig(phase_output, dpi=180)
    print("Phase diagram:", phase_output)


if __name__ == "__main__":
    main()
