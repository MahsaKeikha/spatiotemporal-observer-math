import numpy as np
import pytest

from observer_math import gaussian_safe_near_competitor_screen, optimize_worldtube


def _screen(sample_count: int = 2_000_000):
    local = np.array(
        [
            [0.82, 0.48, 0.31],
            [0.37, 0.86, 0.42],
            [0.29, 0.44, 0.84],
        ]
    )
    transport = np.full((2, 3, 3), 0.18)
    transport[0, 0, 1] = 0.91
    transport[1, 1, 2] = 0.89
    candidates = ((0, 1), (2, 3), (4, 5))
    result = gaussian_safe_near_competitor_screen(
        local,
        transport,
        candidates,
        sample_count,
        6,
        2,
        minimum_block_eigenvalues=np.full((3, 3), 0.9),
        maximum_block_eigenvalues=np.full((3, 3), 1.4),
        certification_local_score_errors=np.full((3, 3), 0.015),
        certification_transport_score_errors=np.full((2, 3, 3), 0.02),
        confidence=0.975,
        continuity_weight=0.04,
    )
    return result, local, transport, candidates


def test_safe_screen_contains_every_sampled_second_split_winner():
    result, local, transport, candidates = _screen()
    rng = np.random.default_rng(2917)
    deviation = (
        np.sqrt(8) + np.sqrt(2.0 * np.log(2.0 * 9 / 0.025))
    ) / np.sqrt(2_000_000 - 1)
    expected_covariance_error = 1.4 * (2.0 * deviation + deviation**2)

    assert result.guarantees_safe_screen
    assert np.isclose(
        result.maximum_covariance_spectral_error, expected_covariance_error
    )
    for _ in range(200):
        population_local = local + rng.uniform(
            -result.screening_local_score_errors,
            result.screening_local_score_errors,
        )
        population_transport = transport + rng.uniform(
            -result.screening_transport_score_errors,
            result.screening_transport_score_errors,
        )
        certification_local = population_local + rng.uniform(-0.015, 0.015, local.shape)
        certification_transport = population_transport + rng.uniform(
            -0.02, 0.02, transport.shape
        )
        winner = optimize_worldtube(
            certification_local,
            candidates,
            transport_scores=certification_transport,
            continuity_weight=0.04,
        ).candidate_indices

        assert all(
            winner[time] in result.screen.viable_states[time]
            for time in range(len(winner))
        )
        assert all(
            (winner[time], winner[time + 1]) in result.screen.viable_edges[time]
            for time in range(len(winner) - 1)
        )


def test_more_screening_samples_tighten_errors_and_cannot_expand_screen():
    smaller, *_ = _screen(sample_count=2_000_000)
    larger, *_ = _screen(sample_count=8_000_000)

    assert larger.maximum_covariance_spectral_error < (
        smaller.maximum_covariance_spectral_error
    )
    assert np.all(
        larger.screening_local_score_errors < smaller.screening_local_score_errors
    )
    assert np.all(
        larger.screening_transport_score_errors
        < smaller.screening_transport_score_errors
    )
    assert all(
        set(larger.screen.viable_states[time])
        <= set(smaller.screen.viable_states[time])
        for time in range(3)
    )
    assert all(
        set(larger.screen.viable_edges[time])
        <= set(smaller.screen.viable_edges[time])
        for time in range(2)
    )


def test_invalid_perturbation_regime_is_reported_without_false_guarantee():
    result, *_ = _screen(sample_count=2)

    assert not result.all_blocks_valid
    assert not result.guarantees_safe_screen
    assert np.all(result.screening_local_score_errors == 1.0)
    assert np.all(result.screening_transport_score_errors == 1.0)


def test_safe_screen_rejects_malformed_certification_budget():
    with pytest.raises(ValueError, match="certification local errors"):
        gaussian_safe_near_competitor_screen(
            np.ones((2, 2)),
            np.ones((1, 2, 2)),
            ((0,), (1,)),
            100,
            2,
            1,
            minimum_block_eigenvalues=np.ones((2, 2)),
            maximum_block_eigenvalues=np.ones((2, 2)),
            certification_local_score_errors=np.ones((2, 1)),
            certification_transport_score_errors=np.ones((1, 2, 2)),
        )
