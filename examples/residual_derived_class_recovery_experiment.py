"""Derive class factor intervals from covariance residual radii."""

from math import comb

import numpy as np

from observer_math import residual_class_covariance_path_recovery_bound


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

    representative_local = np.empty((time_count, class_count, 3))
    for overlap in range(class_count):
        representative_local[:, overlap] = 0.05 + 0.08 * overlap
    representative_local[:, planted_class] = 0.9
    representative_transport = np.full(
        (time_count - 1, class_count, class_count, 2),
        0.1,
    )
    representative_transport[:, planted_class, planted_class] = 0.85

    local_residuals = np.empty((time_count, class_count))
    for overlap in range(class_count):
        local_residuals[:, overlap] = (7 - overlap) * 1e-6
    transport_residuals = np.full(
        (time_count - 1, class_count, class_count),
        4e-6,
    )
    feasible_edges = np.ones(transport_residuals.shape, dtype=bool)
    continuity_lower = np.zeros(transport_residuals.shape)
    planted_distances = np.full(time_count - 1, 1.0 / 3.0)

    result = residual_class_covariance_path_recovery_bound(
        representative_local,
        representative_transport,
        multiplicities,
        (planted_class,) * time_count,
        feasible_edges,
        continuity_lower,
        planted_distances,
        node_count,
        subset_size,
        local_covariance_residual_bounds=local_residuals,
        representative_minimum_block_eigenvalues=np.ones(local_residuals.shape),
        representative_maximum_block_eigenvalues=np.full(
            local_residuals.shape, 2.0
        ),
        transport_covariance_residual_bounds=transport_residuals,
        representative_minimum_transport_eigenvalues=np.ones(
            transport_residuals.shape
        ),
        representative_maximum_transport_eigenvalues=np.full(
            transport_residuals.shape, 2.0
        ),
        covariance_spectral_errors=np.full(local_residuals.shape, 1e-9),
        transport_covariance_spectral_errors=np.full(
            transport_residuals.shape, 1e-9
        ),
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    certificate = result.recovery
    maximum_local_width = np.max(
        result.local_factor_upper_bounds - result.local_factor_lower_bounds
    )
    maximum_transport_width = np.max(
        result.transport_factor_upper_bounds
        - result.transport_factor_lower_bounds
    )

    print(f"Candidates per time: {comb(node_count, subset_size):,}")
    print(f"Maximum local covariance residual: {np.max(local_residuals):.3e}")
    print(f"Maximum transport covariance residual: {np.max(transport_residuals):.3e}")
    print(f"Maximum derived local factor width: {maximum_local_width:.6f}")
    print(f"Maximum derived transport factor width: {maximum_transport_width:.6f}")
    print(f"Adversarial class path: {certificate.adversarial_class_path}")
    print(f"Planted action lower bound: {certificate.planted_action_lower:.6f}")
    print(f"Competitor action upper bound: {certificate.competitor_action_upper:.6f}")
    print(f"Recovery slack: {certificate.recovery_slack:.6f}")
    print(f"Sufficient condition: {certificate.guarantees_population_path}")


if __name__ == "__main__":
    main()
