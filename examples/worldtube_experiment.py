"""Generate the first observer world-tube illustration."""

from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math import (
    adjacent_joint_covariance,
    certify_worldtube,
    observer_metrics_from_covariances,
    optimize_worldtube,
    propagate_covariances,
    transport_metrics,
)
from observer_math.gaussian import stationary_covariance


def active_system(node_count, active):
    transition = np.eye(node_count) * 0.32
    for target in active:
        transition[target, target] = 0.46
        for source in active:
            if source != target:
                transition[target, source] = 0.18
    radius = np.max(np.abs(np.linalg.eigvals(transition)))
    transition *= 0.84 / radius
    return transition, np.eye(node_count) * 0.18


def main():
    node_count = 7
    planted_path = tuple(tuple(range(start, start + 3)) for start in range(5))
    candidates = tuple(combinations(range(node_count), 3))

    systems = [active_system(node_count, active) for active in planted_path]
    covariances = propagate_covariances(
        [system[0] for system in systems[1:]],
        [system[1] for system in systems[1:]],
        stationary_covariance(*systems[0]),
    )
    local_scores = np.zeros((len(systems), len(candidates)))
    for time, (transition, noise) in enumerate(systems):
        joint = adjacent_joint_covariance(covariances[time], transition, noise)
        for index, candidate in enumerate(candidates):
            local_scores[time, index] = observer_metrics_from_covariances(
                covariances[time], joint, candidate
            ).observer_score

    transport = np.zeros((len(systems) - 1, len(candidates), len(candidates)))
    for time in range(len(systems) - 1):
        next_transition, next_noise = systems[time + 1]
        for previous, source in enumerate(candidates):
            for current, target in enumerate(candidates):
                transport[time, previous, current] = transport_metrics(
                    covariances[time], next_transition, next_noise, source, target
                ).transport_score

    certificate = certify_worldtube(
        local_scores,
        candidates,
        transport_scores=transport,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    result = certificate.result
    print("Planted path:", planted_path)
    print("Recovered path:", result.path)
    print("Total action:", f"{result.total_action:.6f}")
    print("Runner-up action:", f"{certificate.runner_up_action:.6f}")
    print("Optimality margin:", f"{certificate.action_margin:.6f}")
    print("Certified uniform score radius:", f"{certificate.uniform_score_radius:.6f}")

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
