"""Derive a class recovery certificate from block comparison structure."""

from math import comb

import numpy as np

from observer_math import (
    moving_block_covariance_error_envelope,
    structured_residual_class_path_recovery_bound,
)


def main() -> None:
    node_count = 1_000
    subset_size = 5
    time_count = 5
    class_count = 2
    candidate_count = comb(node_count, subset_size)

    transition_comparisons = tuple(
        np.array([[0.20, 0.01], [0.01, 0.20]]) for _ in range(time_count)
    )
    forcing_comparisons = tuple(
        np.array([[2e-7, 5e-8], [5e-8, 1e-7]]) for _ in range(time_count)
    )
    perturbation_comparisons = tuple(
        np.full((2, 2), 1e-8) for _ in range(time_count)
    )
    envelope = moving_block_covariance_error_envelope(
        transition_comparisons,
        forcing_comparisons,
        perturbation_comparisons,
    )

    representative_local = np.full((time_count, class_count, 3), 0.1)
    representative_local[:, 1] = 0.9
    representative_transport = np.full(
        (time_count - 1, class_count, class_count, 2),
        0.1,
    )
    representative_transport[:, 1, 1] = 0.85
    multiplicities = np.tile(
        np.array([candidate_count - 1, 1], dtype=object),
        (time_count, 1),
    )
    future_class_blocks = (((0,), (1,)),) * time_count
    edge_shape = (time_count - 1, class_count, class_count)

    result = structured_residual_class_path_recovery_bound(
        envelope,
        future_class_blocks,
        representative_local,
        representative_transport,
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
        covariance_spectral_errors=np.full((time_count, class_count), 1e-9),
        transport_covariance_spectral_errors=np.full(edge_shape, 1e-9),
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    certificate = result.recovery.recovery

    print(f"Candidates per time: {candidate_count:,}")
    print(
        "Maximum derived local covariance residual: "
        f"{np.max(result.local_covariance_residual_bounds):.3e}"
    )
    print(
        "Maximum derived transport covariance residual: "
        f"{np.max(result.transport_covariance_residual_bounds):.3e}"
    )
    print(f"Adversarial class path: {certificate.adversarial_class_path}")
    print(f"Planted action lower bound: {certificate.planted_action_lower:.6f}")
    print(f"Competitor action upper bound: {certificate.competitor_action_upper:.6f}")
    print(f"Recovery slack: {certificate.recovery_slack:.6f}")
    print(f"Sufficient condition: {certificate.guarantees_population_path}")


if __name__ == "__main__":
    main()
