import numpy as np

from observer_math import (
    gaussian_factor_aware_near_competitor_screen,
    gaussian_safe_near_competitor_screen,
    optimize_worldtube,
)


def _inputs(sample_count: int = 100_000_000):
    time_count = 4
    candidate_count = 4
    candidates = ((0, 1), (2, 3), (4, 5), (6, 7))
    path = (0, 1, 2, 3)
    local_factors = np.full((time_count, candidate_count, 3), 0.28)
    transport_factors = np.full(
        (time_count - 1, candidate_count, candidate_count, 2), 0.22
    )
    for time, current in enumerate(path):
        local_factors[time, current] = 0.88
        if time:
            transport_factors[time - 1, path[time - 1], current] = 0.90
    arguments = {
        "candidates": candidates,
        "screening_sample_count": sample_count,
        "node_count": 8,
        "subset_size": 2,
        "minimum_block_eigenvalues": np.full((time_count, candidate_count), 0.9),
        "maximum_block_eigenvalues": np.full((time_count, candidate_count), 1.4),
        "certification_local_score_errors": np.full(
            (time_count, candidate_count), 0.015
        ),
        "certification_transport_score_errors": np.full(
            (time_count - 1, candidate_count, candidate_count), 0.02
        ),
        "confidence": 0.975,
        "continuity_weight": 0.03,
    }
    return local_factors, transport_factors, arguments


def test_positive_factor_refinement_is_no_wider_than_zero_safe_bound():
    local_factors, transport_factors, arguments = _inputs()
    refined = gaussian_factor_aware_near_competitor_screen(
        local_factors, transport_factors, **arguments
    )
    baseline = gaussian_safe_near_competitor_screen(
        np.prod(local_factors, axis=2) ** (1.0 / 3.0),
        np.sqrt(np.prod(transport_factors, axis=3)),
        **arguments,
    )

    assert np.all(refined.positive_local_factor_floor_mask)
    assert np.all(refined.positive_transport_factor_floor_mask)
    assert np.all(
        refined.screening_local_score_errors
        <= baseline.screening_local_score_errors
    )
    assert np.all(
        refined.screening_transport_score_errors
        <= baseline.screening_transport_score_errors
    )
    assert refined.screen.viable_state_count <= baseline.screen.viable_state_count
    assert refined.screen.viable_edge_count <= baseline.screen.viable_edge_count


def test_factor_aware_screen_contains_randomized_later_winners():
    local_factors, transport_factors, arguments = _inputs()
    result = gaussian_factor_aware_near_competitor_screen(
        local_factors, transport_factors, **arguments
    )
    rng = np.random.default_rng(7001)

    assert result.guarantees_safe_screen
    for _ in range(200):
        population_local_factors = np.clip(
            local_factors
            + rng.uniform(
                -result.screening_local_factor_errors,
                result.screening_local_factor_errors,
            ),
            0.0,
            1.0,
        )
        population_transport_factors = np.clip(
            transport_factors
            + rng.uniform(
                -result.screening_transport_factor_errors,
                result.screening_transport_factor_errors,
            ),
            0.0,
            1.0,
        )
        population_local = np.prod(population_local_factors, axis=2) ** (1.0 / 3.0)
        population_transport = np.sqrt(np.prod(population_transport_factors, axis=3))
        later_local = population_local + rng.uniform(
            -0.015, 0.015, population_local.shape
        )
        later_transport = population_transport + rng.uniform(
            -0.02, 0.02, population_transport.shape
        )
        winner = optimize_worldtube(
            later_local,
            arguments["candidates"],
            transport_scores=later_transport,
            continuity_weight=arguments["continuity_weight"],
        ).candidate_indices

        assert all(
            winner[time] in result.screen.viable_states[time]
            for time in range(len(winner))
        )
        assert all(
            (winner[time], winner[time + 1]) in result.screen.viable_edges[time]
            for time in range(len(winner) - 1)
        )


def test_zero_factor_uses_zero_safe_fallback():
    local_factors, transport_factors, arguments = _inputs()
    local_factors[0, 0, 0] = 0.0
    refined = gaussian_factor_aware_near_competitor_screen(
        local_factors, transport_factors, **arguments
    )
    baseline = gaussian_safe_near_competitor_screen(
        np.prod(local_factors, axis=2) ** (1.0 / 3.0),
        np.sqrt(np.prod(transport_factors, axis=3)),
        **arguments,
    )

    assert not refined.positive_local_factor_floor_mask[0, 0]
    assert np.isclose(
        refined.screening_local_score_errors[0, 0],
        baseline.screening_local_score_errors[0, 0],
    )


def test_factor_aware_screen_rejects_factors_outside_unit_interval():
    local_factors, transport_factors, arguments = _inputs()
    local_factors[0, 0, 0] = 1.01

    with np.testing.assert_raises_regex(ValueError, "lie in"):
        gaussian_factor_aware_near_competitor_screen(
            local_factors, transport_factors, **arguments
        )
