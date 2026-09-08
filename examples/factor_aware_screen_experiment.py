"""Compare zero-safe and positive-factor Gaussian screening radii."""

import numpy as np

from observer_math import (
    gaussian_factor_aware_near_competitor_screen,
    gaussian_safe_near_competitor_screen,
)


def main() -> None:
    time_count = 4
    candidate_count = 4
    node_count = 8
    subset_size = 2
    candidates = ((0, 1), (2, 3), (4, 5), (6, 7))
    reference_path = (0, 1, 2, 3)
    local_factors = np.full((time_count, candidate_count, 3), 0.28)
    transport_factors = np.full(
        (time_count - 1, candidate_count, candidate_count, 2), 0.22
    )
    for time, current in enumerate(reference_path):
        local_factors[time, current] = 0.88
        if time:
            transport_factors[time - 1, reference_path[time - 1], current] = 0.90

    screening_sample_count = 10_000_000
    arguments = {
        "candidates": candidates,
        "screening_sample_count": screening_sample_count,
        "node_count": node_count,
        "subset_size": subset_size,
        "minimum_block_eigenvalues": np.full(
            (time_count, candidate_count), 0.9
        ),
        "maximum_block_eigenvalues": np.full(
            (time_count, candidate_count), 1.4
        ),
        "certification_local_score_errors": np.full(
            (time_count, candidate_count), 0.015
        ),
        "certification_transport_score_errors": np.full(
            (time_count - 1, candidate_count, candidate_count), 0.02
        ),
        "confidence": 0.975,
        "continuity_weight": 0.03,
    }
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    zero_safe = gaussian_safe_near_competitor_screen(
        local_scores, transport_scores, **arguments
    )
    factor_aware = gaussian_factor_aware_near_competitor_screen(
        local_factors, transport_factors, **arguments
    )

    complete_states = time_count * candidate_count
    complete_edges = (time_count - 1) * candidate_count**2
    print(f"Screening sample count: {screening_sample_count:,}")
    print(f"Screening confidence: {factor_aware.screening_confidence:.6f}")
    print(
        "Maximum covariance radius: "
        f"{factor_aware.maximum_covariance_spectral_error:.6f}"
    )
    print(
        "Maximum zero-safe local-score radius: "
        f"{np.max(zero_safe.screening_local_score_errors):.6f}"
    )
    print(
        "Maximum factor-aware local-score radius: "
        f"{np.max(factor_aware.screening_local_score_errors):.6f}"
    )
    print(
        "Maximum zero-safe transport-score radius: "
        f"{np.max(zero_safe.screening_transport_score_errors):.6f}"
    )
    print(
        "Maximum factor-aware transport-score radius: "
        f"{np.max(factor_aware.screening_transport_score_errors):.6f}"
    )
    print(f"Complete states: {complete_states}")
    print(f"Zero-safe retained states: {zero_safe.screen.viable_state_count}")
    print(f"Factor-aware retained states: {factor_aware.screen.viable_state_count}")
    print(f"Complete edges: {complete_edges}")
    print(f"Zero-safe retained edges: {zero_safe.screen.viable_edge_count}")
    print(f"Factor-aware retained edges: {factor_aware.screen.viable_edge_count}")
    print(
        "Positive local factor floors: "
        f"{np.count_nonzero(factor_aware.positive_local_factor_floor_mask)}"
        f"/{complete_states}"
    )
    print(
        "Positive transport factor floors: "
        f"{np.count_nonzero(factor_aware.positive_transport_factor_floor_mask)}"
        f"/{complete_edges}"
    )
    print(f"Safe-screen guarantee: {factor_aware.guarantees_safe_screen}")


if __name__ == "__main__":
    main()
