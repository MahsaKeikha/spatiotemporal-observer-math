"""Evaluate the direct block-sparse recovery certificate at large n."""

import numpy as np

from observer_math import block_sparse_moving_clique_recovery_bound


def main():
    node_count = 1000
    module_size = 5
    time_count = 3
    planted = tuple(
        tuple(range(time, time + module_size)) for time in range(time_count)
    )
    transition_entries = np.full((time_count, 2, 2), 1e-8)
    transition_degrees = np.full((time_count, 2, 2), 2, dtype=int)
    noise_entries = np.full((time_count, 2, 2), 1e-9)
    noise_degrees = np.full((time_count, 2, 2), 2, dtype=int)

    bound = block_sparse_moving_clique_recovery_bound(
        node_count,
        planted,
        self_memory=0.2,
        internal_coupling=0.1,
        transition_entry_bounds=transition_entries,
        transition_row_degrees=transition_degrees,
        transition_column_degrees=transition_degrees,
        noise_entry_bounds=noise_entries,
        noise_row_degrees=noise_degrees,
        noise_column_degrees=noise_degrees,
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    print("Population size:", node_count)
    print("Implicit candidate count:", bound.recovery.candidate_count)
    print("Overlap classes evaluated:", bound.recovery.overlap_class_count)
    print(
        "Global transition perturbation bound:",
        f"{max(bound.budgets.global_transition_bounds):.3e}",
    )
    print(
        "Maximum incorrect-score upper bound:",
        f"{max(bound.recovery.maximum_incorrect_score_upper_bounds):.6f}",
    )
    print(
        "Action-margin lower bound:",
        f"{bound.recovery.per_mismatch_action_margin:.6f}",
    )
    print(
        "Sufficient condition:",
        "satisfied"
        if bound.recovery.guarantees_unique_planted_path
        else "not satisfied",
    )


if __name__ == "__main__":
    main()
