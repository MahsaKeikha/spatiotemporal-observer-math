"""Recover a class path with certified screened environmental neighborhoods."""

from math import comb

import numpy as np

from observer_math import (
    moving_block_covariance_error_envelope,
    moving_block_joint_covariance_error_bound,
    screened_structural_class_path_recovery_bound,
)


def main() -> None:
    node_count = 1_000
    subset_size = 5
    time_count = 5
    class_count = 2
    candidate_count = comb(node_count, subset_size)
    transition_comparisons = tuple(
        np.array(
            [
                [0.20, 0.01, 0.00],
                [0.01, 0.20, 0.00],
                [0.00, 0.00, 0.20],
            ]
        )
        for _ in range(time_count)
    )
    forcing_comparisons = tuple(
        np.diag([1e-8, 2e-8, 5e-5]) for _ in range(time_count)
    )
    envelope = moving_block_covariance_error_envelope(
        transition_comparisons,
        forcing_comparisons,
        tuple(np.zeros((3, 3)) for _ in range(time_count)),
    )

    local = np.full((time_count, class_count, 3), 0.1)
    local[:, 1] = 0.9
    transport = np.full((time_count - 1, class_count, class_count, 2), 0.1)
    transport[:, 1, 1] = 0.85
    local_present = (((0,), (1,)),) * time_count
    local_future = (((0,), (1,)),) * time_count
    edge_present_layer = (((0,), (0,)), ((1,), (1,)))
    edge_future_layer = (((0,), (1,)), ((0,), (1,)))
    edge_shape = (time_count - 1, class_count, class_count)
    multiplicities = np.tile(
        np.array([candidate_count - 1, 1], dtype=object),
        (time_count, 1),
    )

    result = screened_structural_class_path_recovery_bound(
        envelope,
        local_present,
        local_future,
        (edge_present_layer,) * (time_count - 1),
        (edge_future_layer,) * (time_count - 1),
        local,
        transport,
        np.full((time_count, class_count), 0.002),
        np.full(edge_shape, 0.002),
        multiplicities,
        (1,) * time_count,
        np.ones(edge_shape, dtype=bool),
        np.zeros(edge_shape),
        np.full(time_count - 1, 1.0 / 3.0),
        node_count,
        subset_size,
        representative_minimum_block_eigenvalues=np.ones(
            (time_count, class_count)
        ),
        representative_maximum_block_eigenvalues=np.full(
            (time_count, class_count), 2.0
        ),
        representative_minimum_transport_eigenvalues=np.ones(edge_shape),
        representative_maximum_transport_eigenvalues=np.full(edge_shape, 2.0),
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    full_radius = moving_block_joint_covariance_error_bound(
        envelope,
        time_count - 1,
        (0, 1, 2),
        (0, 1, 2),
    )
    certificate = result.recovery

    print(f"Candidates per time: {candidate_count:,}")
    print(f"Full-environment residual radius: {full_radius:.3e}")
    print(
        "Maximum screened local residual radius: "
        f"{np.max(result.local_covariance_residual_bounds):.3e}"
    )
    print("Omitted leakage bound: 0.002 bits/node")
    print(f"Adversarial class path: {certificate.adversarial_class_path}")
    print(f"Planted action lower bound: {certificate.planted_action_lower:.6f}")
    print(f"Competitor action upper bound: {certificate.competitor_action_upper:.6f}")
    print(f"Recovery slack: {certificate.recovery_slack:.6f}")
    print(f"Sufficient condition: {certificate.guarantees_population_path}")


if __name__ == "__main__":
    main()
