"""Check the closed-form moving-clique recovery theorem numerically."""

from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

from observer_math import (
    certify_worldtube,
    covariance_preserving_moving_clique_bound,
    covariance_preserving_moving_cliques,
    observer_metrics,
    transport_metrics,
)


def main():
    node_count = 5
    module_size = 2
    transport_weight = 0.02
    continuity_weight = 0.01
    planted, systems = covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    candidates = tuple(combinations(range(node_count), module_size))
    local = np.array(
        [
            [observer_metrics(*system, candidate).observer_score for candidate in candidates]
            for system in systems
        ]
    )
    transport = np.empty((len(systems) - 1, len(candidates), len(candidates)))
    for time, (transition, noise) in enumerate(systems[:-1]):
        for previous, source in enumerate(candidates):
            for current, target in enumerate(candidates):
                transport[time, previous, current] = transport_metrics(
                    np.eye(node_count), transition, noise, source, target
                ).transport_score
    symbolic = covariance_preserving_moving_clique_bound(
        0.2,
        0.3,
        module_size,
        minimum_consecutive_overlap=1,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    numerical = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )

    print("Planted path:", planted)
    print("Recovered path:", numerical.result.path)
    print("Closed-form planted local score:", f"{symbolic.planted_local_score:.6f}")
    print("Symbolic action-margin lower bound:", f"{symbolic.per_mismatch_action_margin:.6f}")
    print("Exact action margin:", f"{numerical.action_margin:.6f}")
    print(
        "Symbolic sufficient condition:",
        "satisfied" if symbolic.guarantees_unique_planted_path else "not satisfied",
    )

    memory_values = np.linspace(0.0, 0.8, 81)
    coupling_values = np.linspace(0.0, 0.45, 91)
    margins = np.full((len(coupling_values), len(memory_values)), np.nan)
    for row, coupling in enumerate(coupling_values):
        for column, memory in enumerate(memory_values):
            try:
                bound = covariance_preserving_moving_clique_bound(
                    float(memory),
                    float(coupling),
                    module_size,
                    minimum_consecutive_overlap=1,
                    transport_weight=transport_weight,
                    continuity_weight=continuity_weight,
                )
            except ValueError:
                continue
            margins[row, column] = bound.per_mismatch_action_margin

    figure, axis = plt.subplots(figsize=(8, 6))
    axis.set_facecolor("0.88")
    image = axis.imshow(
        margins,
        origin="lower",
        aspect="auto",
        extent=(
            memory_values[0],
            memory_values[-1],
            coupling_values[0],
            coupling_values[-1],
        ),
        cmap="coolwarm",
        norm=TwoSlopeNorm(vmin=-0.08, vcenter=0.0, vmax=0.24),
    )
    axis.contour(
        memory_values,
        coupling_values,
        margins,
        levels=[0.0],
        colors="black",
        linewidths=1.5,
    )
    axis.scatter([0.2], [0.3], marker="*", color="gold", edgecolor="black", s=180)
    axis.set_xlabel(r"Self-memory $\alpha$")
    axis.set_ylabel(r"Internal coupling $\beta$")
    axis.set_title("Sufficient moving-clique recovery margin")
    figure.colorbar(image, ax=axis, label="Symbolic action-margin lower bound")
    figure.tight_layout()
    output = Path(__file__).resolve().parents[1] / "docs" / "symbolic_recovery_region.png"
    figure.savefig(output, dpi=180)
    print("Recovery-region figure:", output)


if __name__ == "__main__":
    main()
