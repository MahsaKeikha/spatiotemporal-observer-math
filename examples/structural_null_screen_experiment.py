"""Compare generic and structural-null screens on one Wishart draw."""

import numpy as np
from gaussian_screen_calibration import empirical_factors, population_problem
from scipy.stats import wishart

from observer_math import (
    gaussian_factor_aware_near_competitor_screen,
    gaussian_structural_null_near_competitor_screen,
)


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


if __name__ == "__main__":
    main()
