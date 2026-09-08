"""Derive a first-split screening guarantee from Gaussian concentration."""

import numpy as np

from observer_math import gaussian_safe_near_competitor_screen


def main() -> None:
    time_count = 5
    candidate_count = 12
    node_count = 24
    subset_size = 2
    candidates = tuple((2 * index, 2 * index + 1) for index in range(candidate_count))
    empirical_local = np.zeros((time_count, candidate_count))
    empirical_transport = np.full(
        (time_count - 1, candidate_count, candidate_count), 0.05
    )
    reference_path = (0, 1, 2, 3, 4)
    for time, current in enumerate(reference_path):
        empirical_local[time, current] = 1.00
        if time:
            empirical_transport[time - 1, reference_path[time - 1], current] = 0.95

    # This deliberately large value exposes the conservatism of the current
    # worst-case log-determinant and product-root perturbation chain.
    screening_sample_count = 1_000_000_000_000
    result = gaussian_safe_near_competitor_screen(
        empirical_local,
        empirical_transport,
        candidates,
        screening_sample_count,
        node_count,
        subset_size,
        minimum_block_eigenvalues=np.full((time_count, candidate_count), 0.9),
        maximum_block_eigenvalues=np.full((time_count, candidate_count), 1.4),
        certification_local_score_errors=np.full(
            (time_count, candidate_count), 0.015
        ),
        certification_transport_score_errors=np.full(
            (time_count - 1, candidate_count, candidate_count), 0.02
        ),
        confidence=0.975,
        continuity_weight=0.02,
    )

    complete_state_count = time_count * candidate_count
    complete_edge_count = (time_count - 1) * candidate_count**2
    print(f"Screening sample count: {screening_sample_count:,}")
    print(f"Screening confidence: {result.screening_confidence:.6f}")
    print(
        "Maximum screening covariance radius: "
        f"{result.maximum_covariance_spectral_error:.6f}"
    )
    print(
        "Maximum screening local-score radius: "
        f"{np.max(result.screening_local_score_errors):.6f}"
    )
    print(
        "Maximum screening transport-score radius: "
        f"{np.max(result.screening_transport_score_errors):.6f}"
    )
    print(f"Complete states: {complete_state_count:,}")
    print(f"Retained states: {result.screen.viable_state_count:,}")
    print(f"Complete edges: {complete_edge_count:,}")
    print(f"Retained edges: {result.screen.viable_edge_count:,}")
    print(f"Screen center path: {result.screen.population_path}")
    print(f"All perturbation blocks valid: {result.all_blocks_valid}")
    print(f"Safe-screen guarantee: {result.guarantees_safe_screen}")


if __name__ == "__main__":
    main()
