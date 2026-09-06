"""Generate the first observer world-tube illustration."""

from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from observer_math import observer_metrics, optimize_worldtube, structural_transport


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
    candidate_index = {candidate: index for index, candidate in enumerate(candidates)}

    systems = [active_system(node_count, active) for active in planted_path]
    local_scores = np.zeros((len(systems), len(candidates)))
    for time, (transition, noise) in enumerate(systems):
        for index, candidate in enumerate(candidates):
            local_scores[time, index] = observer_metrics(
                transition, noise, candidate
            ).observer_score

    transport = np.zeros((len(systems) - 1, len(candidates), len(candidates)))
    for time in range(len(systems) - 1):
        next_transition = systems[time + 1][0]
        for previous, source in enumerate(candidates):
            for current, target in enumerate(candidates):
                transport[time, previous, current] = structural_transport(
                    next_transition, source, target
                )

    result = optimize_worldtube(
        local_scores,
        candidates,
        transport_scores=transport,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    print("Planted path:", planted_path)
    print("Recovered path:", result.path)
    print("Total action:", f"{result.total_action:.6f}")

    order = np.argsort(-local_scores.max(axis=0))[:12]
    display = local_scores[:, order].T
    labels = [str(candidates[index]) for index in order]
    figure, axis = plt.subplots(figsize=(9, 6))
    image = axis.imshow(display, aspect="auto", cmap="magma", vmin=0)
    axis.set_xlabel("Time step")
    axis.set_ylabel("Candidate subsystem")
    axis.set_yticks(np.arange(len(labels)), labels=labels)
    axis.set_title("A persistent organization moving through physical nodes")
    for time, subset in enumerate(result.path):
        if subset in [candidates[index] for index in order]:
            row = [candidates[index] for index in order].index(subset)
            axis.scatter(time, row, marker="s", facecolors="none", edgecolors="cyan", s=180)
    figure.colorbar(image, ax=axis, label="Fixed-boundary observer score")
    figure.tight_layout()
    output = Path(__file__).resolve().parents[1] / "docs" / "worldtube_baseline.png"
    figure.savefig(output, dpi=180)
    print("Figure:", output)


if __name__ == "__main__":
    main()
