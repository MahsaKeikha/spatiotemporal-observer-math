"""Compare generic and structural-null screens on one Wishart draw."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from gaussian_screen_calibration import empirical_factors, population_problem
from scipy.stats import wishart

from observer_math import (
    gaussian_factor_aware_near_competitor_screen,
    gaussian_structural_null_near_competitor_screen,
)


def plot_screen_comparison(generic, null_aware, output: Path) -> None:
    """Plot score-radius and retained-graph comparisons."""
    generic_local_radius = float(np.max(generic.screening_local_score_errors))
    mask = null_aware.structural_integration_null_mask
    null_local_radius = float(
        np.max(null_aware.screening_local_score_errors[mask])
    )
    time_count, candidate_count = mask.shape
    complete_states = time_count * candidate_count
    complete_edges = (time_count - 1) * candidate_count**2
    state_fractions = (
        1.0,
        generic.screen.viable_state_count / complete_states,
        null_aware.screen.viable_state_count / complete_states,
    )
    edge_fractions = (
        1.0,
        generic.screen.viable_edge_count / complete_edges,
        null_aware.screen.viable_edge_count / complete_edges,
    )

    figure, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
    colors = ("#506784", "#1f9e89", "#e0a100")
    axes[0].bar(
        ("Generic bound", "Structural-null bound"),
        (generic_local_radius, null_local_radius),
        color=(colors[0], colors[2]),
    )
    axes[0].set_yscale("log")
    axes[0].set_ylabel("Maximum local-score radius")
    axes[0].set_title("Boundary-adaptive score error")
    for index, value in enumerate((generic_local_radius, null_local_radius)):
        axes[0].text(index, value * 1.08, f"{value:.6f}", ha="center")

    positions = np.arange(3)
    width = 0.36
    axes[1].bar(
        positions - width / 2,
        np.asarray(state_fractions) * 100.0,
        width,
        label="States",
        color="#3b82b8",
    )
    axes[1].bar(
        positions + width / 2,
        np.asarray(edge_fractions) * 100.0,
        width,
        label="Edges",
        color="#e07a3f",
    )
    axes[1].set_xticks(positions, ("Complete", "Generic", "Structural null"))
    axes[1].set_ylim(0.0, 108.0)
    axes[1].set_ylabel("Graph retained (%)")
    axes[1].set_title("Safe near-competitor graph")
    axes[1].legend(frameon=False)
    axes[1].grid(axis="y", alpha=0.25)
    for container in axes[1].containers:
        axes[1].bar_label(container, fmt="%.1f%%", padding=3, fontsize=8)

    figure.suptitle(
        "Structural-null screening at 80 billion observations",
        fontsize=13,
    )
    figure.text(
        0.5,
        0.015,
        "The mask is fixed from the model construction before screening; the population path is retained.",
        ha="center",
        fontsize=9,
    )
    figure.tight_layout(rect=(0.0, 0.06, 1.0, 0.94))
    figure.savefig(output, dpi=200, bbox_inches="tight")
    plt.close(figure)


def main() -> None:
    problem = population_problem()
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    sample_count = 80_000_000_000
    rng = np.random.default_rng(20260909)
    empirical_joints = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=rng,
        )
        for joint in problem["joints"]
    )
    local_factors, transport_factors = empirical_factors(
        empirical_joints, problem
    )
    null_mask = np.ones((time_count, candidate_count), dtype=bool)
    for time in range(time_count):
        null_mask[time, time] = False
    arguments = {
        "candidates": problem["candidates"],
        "screening_sample_count": sample_count,
        "node_count": problem["node_count"],
        "subset_size": 3,
        "minimum_block_eigenvalues": problem["minimum"],
        "maximum_block_eigenvalues": problem["maximum"],
        "certification_local_score_errors": np.zeros(
            (time_count, candidate_count)
        ),
        "certification_transport_score_errors": np.zeros(
            (time_count - 1, candidate_count, candidate_count)
        ),
        "confidence": 0.975,
        "transport_weight": 0.25,
        "continuity_weight": 0.08,
    }
    generic = gaussian_factor_aware_near_competitor_screen(
        local_factors, transport_factors, **arguments
    )
    null_aware = gaussian_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        structural_integration_null_mask=null_mask,
        **arguments,
    )

    complete_states = time_count * candidate_count
    complete_edges = (time_count - 1) * candidate_count**2
    print(f"Screening sample count: {sample_count:,}")
    print(f"Screening confidence: {null_aware.screening_confidence:.6f}")
    print(f"Structurally null local states: {np.count_nonzero(null_mask)}")
    print(
        "Maximum generic local-score radius: "
        f"{np.max(generic.screening_local_score_errors):.6f}"
    )
    print(
        "Maximum null-state local-score radius: "
        f"{np.max(null_aware.screening_local_score_errors[null_mask]):.6f}"
    )
    print(f"Complete states: {complete_states}")
    print(f"Generic retained states: {generic.screen.viable_state_count}")
    print(f"Null-aware retained states: {null_aware.screen.viable_state_count}")
    print(f"Complete edges: {complete_edges}")
    print(f"Generic retained edges: {generic.screen.viable_edge_count}")
    print(f"Null-aware retained edges: {null_aware.screen.viable_edge_count}")
    print(f"Population path: {problem['population_path']}")
    print(f"Null-aware center path: {null_aware.screen.population_path}")
    print(f"Safe-screen guarantee: {null_aware.guarantees_safe_screen}")
    output = Path(__file__).resolve().parents[1] / "docs" / "structural_null_screen.png"
    plot_screen_comparison(generic, null_aware, output)
    print(f"Figure: {output}")


if __name__ == "__main__":
    main()
