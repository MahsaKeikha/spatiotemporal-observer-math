"""Numerically check the robust moving-clique recovery theorem."""

from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

from observer_math import (
    a_priori_support_moving_clique_recovery_bound,
    adjacent_joint_covariance,
    certify_worldtube,
    covariance_preserving_moving_cliques,
    observer_metrics_from_covariances,
    perturbed_covariance_preserving_moving_cliques,
    perturbed_moving_clique_recovery_bound,
    propagate_covariances,
    support_resolved_moving_clique_recovery_bound,
    transport_metrics_from_covariances,
)


def main():
    node_count = 5
    module_size = 2
    time_count = 3
    transition_radius = 1e-5
    noise_radius = 1e-6
    transport_weight = 0.02
    continuity_weight = 0.01

    planted, systems = perturbed_covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=time_count,
        self_memory=0.2,
        internal_coupling=0.3,
        external_coupling_norm=transition_radius,
        noise_perturbation_norm=noise_radius,
    )
    _, base_systems = covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=time_count,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    transitions = tuple(system[0] for system in systems)
    noises = tuple(system[1] for system in systems)
    covariances = propagate_covariances(transitions, noises, np.eye(node_count))
    joints = tuple(
        adjacent_joint_covariance(covariances[time], *systems[time])
        for time in range(time_count)
    )
    candidates = tuple(combinations(range(node_count), module_size))
    metrics = tuple(
        tuple(
            observer_metrics_from_covariances(covariances[time], joints[time], candidate)
            for candidate in candidates
        )
        for time in range(time_count)
    )
    local = np.array([[entry.observer_score for entry in row] for row in metrics])
    transport = np.array(
        [
            [
                [
                    transport_metrics_from_covariances(
                        covariances[time], joints[time], source, target
                    ).transport_score
                    for target in candidates
                ]
                for source in candidates
            ]
            for time in range(time_count - 1)
        ]
    )
    bound = perturbed_moving_clique_recovery_bound(
        0.2,
        0.3,
        module_size,
        node_count,
        time_count,
        transition_perturbation=transition_radius,
        noise_perturbation=noise_radius,
        minimum_consecutive_overlap=1,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    certificate = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    support_bound = support_resolved_moving_clique_recovery_bound(
        transitions,
        noises,
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    transition_errors = tuple(
        system[0] - base[0]
        for system, base in zip(systems, base_systems, strict=True)
    )
    noise_errors = tuple(
        system[1] - base[1]
        for system, base in zip(systems, base_systems, strict=True)
    )
    a_priori_bound = a_priori_support_moving_clique_recovery_bound(
        transition_errors,
        noise_errors,
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )

    transition_norms = [
        np.linalg.norm(system[0] - base[0], ord=2)
        for system, base in zip(systems, base_systems, strict=True)
    ]
    noise_norms = [
        np.linalg.norm(system[1] - base[1], ord=2)
        for system, base in zip(systems, base_systems, strict=True)
    ]
    incorrect_scores = [
        entry.observer_score
        for time, row in enumerate(metrics)
        for entry in row
        if entry.subset != planted[time]
    ]
    incorrect_integration = [
        entry.integration_strength
        for time, row in enumerate(metrics)
        for entry in row
        if entry.subset != planted[time]
    ]

    print("Planted path:", planted)
    print("Recovered path:", certificate.result.path)
    print("Maximum transition perturbation norm:", f"{max(transition_norms):.3e}")
    print("Maximum noise perturbation norm:", f"{max(noise_norms):.3e}")
    print("Largest incorrect integration factor:", f"{max(incorrect_integration):.3e}")
    print("Largest incorrect local score:", f"{max(incorrect_scores):.6f}")
    print("Theoretical incorrect-score upper bound:", f"{bound.incorrect_score_upper_bound:.6f}")
    print("Symbolic action-margin lower bound:", f"{bound.per_mismatch_action_margin:.6f}")
    print(
        "Support-resolved incorrect-score upper bound:",
        f"{support_bound.maximum_incorrect_score_upper_bound:.6f}",
    )
    print(
        "Support-resolved action-margin lower bound:",
        f"{support_bound.per_mismatch_action_margin:.6f}",
    )
    print(
        "A priori support-aware incorrect-score upper bound:",
        f"{max(a_priori_bound.maximum_incorrect_score_upper_bounds):.6f}",
    )
    print(
        "A priori support-aware action-margin lower bound:",
        f"{a_priori_bound.per_mismatch_action_margin:.6f}",
    )
    print("Exact action margin:", f"{certificate.action_margin:.6f}")
    print(
        "Symbolic sufficient condition:",
        "satisfied" if bound.guarantees_unique_planted_path else "not satisfied",
    )

    transition_values = np.geomspace(1e-8, 1e-3, 110)
    noise_values = np.geomspace(1e-8, 1e-3, 110)
    margins = np.empty((len(noise_values), len(transition_values)))
    for row, noise_perturbation in enumerate(noise_values):
        for column, transition_perturbation in enumerate(transition_values):
            candidate_bound = perturbed_moving_clique_recovery_bound(
                0.2,
                0.3,
                module_size,
                node_count,
                time_count,
                transition_perturbation=float(transition_perturbation),
                noise_perturbation=float(noise_perturbation),
                minimum_consecutive_overlap=1,
                transport_weight=transport_weight,
                continuity_weight=continuity_weight,
            )
            margins[row, column] = candidate_bound.per_mismatch_action_margin

    figure, axis = plt.subplots(figsize=(8, 6))
    image = axis.pcolormesh(
        transition_values,
        noise_values,
        margins,
        shading="auto",
        cmap="coolwarm",
        norm=TwoSlopeNorm(vmin=-0.12, vcenter=0.0, vmax=0.13),
    )
    axis.contour(
        transition_values,
        noise_values,
        margins,
        levels=[0.0],
        colors="black",
        linewidths=1.5,
    )
    axis.scatter(
        [transition_radius],
        [noise_radius],
        marker="*",
        color="gold",
        edgecolor="black",
        s=180,
        zorder=3,
    )
    axis.set_xscale("log")
    axis.set_yscale("log")
    axis.set_xlabel(r"Transition perturbation bound $\gamma$")
    axis.set_ylabel(r"Noise perturbation bound $\nu$")
    axis.set_title("Robust moving-clique recovery certificate")
    figure.colorbar(image, ax=axis, label="Action-margin lower bound")
    figure.tight_layout()
    output = Path(__file__).resolve().parents[1] / "docs" / "perturbed_recovery_region.png"
    figure.savefig(output, dpi=180)
    print("Perturbation-region figure:", output)


if __name__ == "__main__":
    main()
