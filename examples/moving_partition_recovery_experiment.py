"""Propagate layered covariance radii into a path-recovery certificate."""

from itertools import pairwise

import numpy as np

from observer_math import (
    moving_block_covariance_error_envelope,
    moving_partition_localized_recovery_bound,
)


def main() -> None:
    candidates = ((0, 1), (2, 3))
    planted = (0, 1, 0)
    local_factors = np.full((3, 2, 3), 0.05)
    transport_factors = np.full((2, 2, 2, 2), 0.05)
    for time, current in enumerate(planted):
        local_factors[time, current] = 0.9
    for time, (previous, current) in enumerate(pairwise(planted)):
        transport_factors[time, previous, current] = 0.9

    block_counts = (2, 3, 4, 2)
    transitions = tuple(
        np.zeros((block_counts[time + 1], block_counts[time]))
        for time in range(3)
    )
    forcings = tuple(np.eye(count) * 1e-10 for count in block_counts[1:])
    perturbations = tuple(np.zeros_like(matrix) for matrix in transitions)
    envelope = moving_block_covariance_error_envelope(
        transitions,
        forcings,
        perturbations,
    )

    future_candidate_blocks = (
        ((0, 1), (2,)),
        ((0, 1), (2, 3)),
        ((0,), (1,)),
    )
    result = moving_partition_localized_recovery_bound(
        envelope,
        future_candidate_blocks,
        local_factors,
        transport_factors,
        candidates,
        node_count=4,
        subset_size=2,
        minimum_block_eigenvalues=np.ones((3, 2)),
        maximum_block_eigenvalues=np.full((3, 2), 2.0),
        transport_weight=0.1,
        continuity_weight=0.0,
    )

    print(f"Partition block counts: {block_counts}")
    print(f"Population path: {result.population_path}")
    print(f"Adversarial competitor: {result.adversarial_competitor}")
    print(f"Population action margin: {result.population_action_margin:.6f}")
    print(f"Maximum covariance radius: {np.max(result.covariance_spectral_errors):.3e}")
    print(f"Maximum local-score error: {np.max(result.local_score_errors):.3e}")
    print(
        "Maximum transport-score error: "
        f"{np.max(result.transport_score_errors):.3e}"
    )
    print(f"Recovery slack: {result.recovery_slack:.6f}")
    print(f"Sufficient condition: {result.guarantees_population_path}")


if __name__ == "__main__":
    main()
