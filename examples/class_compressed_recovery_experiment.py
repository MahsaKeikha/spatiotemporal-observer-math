"""Evaluate a robust recovery certificate over implicit overlap classes."""

from math import comb

import numpy as np

from observer_math import class_compressed_covariance_path_recovery_bound


def main() -> None:
    node_count = 1_000
    subset_size = 5
    time_count = 5
    class_count = subset_size + 1
    planted_class = subset_size

    multiplicity_row = np.array(
        [
            comb(subset_size, overlap)
            * comb(node_count - subset_size, subset_size - overlap)
            for overlap in range(class_count)
        ],
        dtype=object,
    )
    multiplicities = np.tile(multiplicity_row, (time_count, 1))
    local_factors = np.empty((time_count, class_count, 3))
    for overlap in range(class_count):
        value = 0.05 + 0.08 * overlap
        local_factors[:, overlap] = value
    local_factors[:, planted_class] = 0.9

    transport_factors = np.full(
        (time_count - 1, class_count, class_count, 2),
        0.1,
    )
    transport_factors[:, planted_class, planted_class] = 0.85
    feasible_edges = np.ones(
        (time_count - 1, class_count, class_count),
        dtype=bool,
    )
    continuity_lower = np.zeros_like(feasible_edges, dtype=float)
    planted_distances = np.full(time_count - 1, 1.0 / 3.0)
    covariance_errors = np.tile(
        np.arange(1, class_count + 1, dtype=float) * 1e-9,
        (time_count, 1),
    )

    result = class_compressed_covariance_path_recovery_bound(
        local_factors,
        transport_factors,
        multiplicities,
        (planted_class,) * time_count,
        feasible_edges,
        continuity_lower,
        planted_distances,
        node_count,
        subset_size,
        covariance_spectral_errors=covariance_errors,
        minimum_block_eigenvalues=np.ones((time_count, class_count)),
        maximum_block_eigenvalues=np.full((time_count, class_count), 2.0),
        transport_covariance_spectral_errors=np.full(feasible_edges.shape, 6e-9),
        minimum_transport_block_eigenvalues=np.ones(feasible_edges.shape),
        maximum_transport_block_eigenvalues=np.full(feasible_edges.shape, 2.0),
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    candidate_count = comb(node_count, subset_size)
    print(f"Candidates per time: {candidate_count:,}")
    print(f"Overlap classes per time: {result.class_count}")
    print(f"Implicit paths: {result.implicit_path_count:,}")
    print(f"Adversarial class path: {result.adversarial_class_path}")
    print(f"Planted action lower bound: {result.planted_action_lower:.6f}")
    print(f"Competitor action upper bound: {result.competitor_action_upper:.6f}")
    print(f"Recovery slack: {result.recovery_slack:.6f}")
    print(f"Sufficient condition: {result.guarantees_population_path}")


if __name__ == "__main__":
    main()
