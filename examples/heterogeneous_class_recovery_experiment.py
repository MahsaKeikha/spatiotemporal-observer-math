"""Certify overlap classes with bounded within-class heterogeneity."""

from math import comb

import numpy as np

from observer_math import interval_class_covariance_path_recovery_bound


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

    local_center = np.empty((time_count, class_count, 3))
    for overlap in range(class_count):
        local_center[:, overlap] = 0.05 + 0.08 * overlap
    local_center[:, planted_class] = 0.9
    local_width = np.empty_like(local_center)
    for overlap in range(class_count):
        local_width[:, overlap] = 0.008 + 0.001 * (subset_size - overlap)
    local_lower = np.clip(local_center - local_width, 0.0, 1.0)
    local_upper = np.clip(local_center + local_width, 0.0, 1.0)

    transport_center = np.full(
        (time_count - 1, class_count, class_count, 2),
        0.1,
    )
    transport_center[:, planted_class, planted_class] = 0.85
    transport_width = np.full_like(transport_center, 0.01)
    transport_lower = np.clip(transport_center - transport_width, 0.0, 1.0)
    transport_upper = np.clip(transport_center + transport_width, 0.0, 1.0)

    feasible_edges = np.ones(
        (time_count - 1, class_count, class_count),
        dtype=bool,
    )
    continuity_lower = np.zeros_like(feasible_edges, dtype=float)
    planted_distances = np.full(time_count - 1, 1.0 / 3.0)
    local_covariance_errors = np.tile(
        np.arange(1, class_count + 1, dtype=float) * 1e-9,
        (time_count, 1),
    )
    edge_covariance_errors = np.full(feasible_edges.shape, 6e-9)

    result = interval_class_covariance_path_recovery_bound(
        local_lower,
        local_upper,
        transport_lower,
        transport_upper,
        multiplicities,
        (planted_class,) * time_count,
        feasible_edges,
        continuity_lower,
        planted_distances,
        node_count,
        subset_size,
        covariance_spectral_errors=local_covariance_errors,
        minimum_block_eigenvalues=np.ones((time_count, class_count)),
        maximum_block_eigenvalues=np.full((time_count, class_count), 2.0),
        transport_covariance_spectral_errors=edge_covariance_errors,
        minimum_transport_block_eigenvalues=np.ones(feasible_edges.shape),
        maximum_transport_block_eigenvalues=np.full(feasible_edges.shape, 2.0),
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    print(f"Candidates per time: {comb(node_count, subset_size):,}")
    print(f"Maximum local factor interval width: {2 * np.max(local_width):.3f}")
    print(f"Maximum transport factor interval width: {2 * np.max(transport_width):.3f}")
    print(f"Adversarial class path: {result.adversarial_class_path}")
    print(f"Planted action lower bound: {result.planted_action_lower:.6f}")
    print(f"Competitor action upper bound: {result.competitor_action_upper:.6f}")
    print(f"Recovery slack: {result.recovery_slack:.6f}")
    print(f"Sufficient condition: {result.guarantees_population_path}")


if __name__ == "__main__":
    main()
