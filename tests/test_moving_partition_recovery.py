from itertools import pairwise

import numpy as np

from observer_math import (
    covariance_radius_path_recovery_bound,
    moving_block_covariance_error_envelope,
    moving_block_joint_covariance_error_bound,
    moving_partition_localized_recovery_bound,
)


def _separated_factor_problem():
    candidates = ((0, 1), (2, 3))
    planted = (0, 1, 0)
    local = np.full((3, 2, 3), 0.05)
    transport = np.full((2, 2, 2, 2), 0.05)
    for time, current in enumerate(planted):
        local[time, current] = 0.9
    for time, (previous, current) in enumerate(pairwise(planted)):
        transport[time, previous, current] = 0.9
    return candidates, planted, local, transport


def test_covariance_radius_certificate_recovers_separated_path():
    candidates, planted, local, transport = _separated_factor_problem()
    covariance_errors = np.full((3, 2), 1e-10)
    minimum = np.ones((3, 2))
    maximum = np.full((3, 2), 2.0)

    result = covariance_radius_path_recovery_bound(
        local,
        transport,
        candidates,
        node_count=4,
        subset_size=2,
        covariance_spectral_errors=covariance_errors,
        minimum_block_eigenvalues=minimum,
        maximum_block_eigenvalues=maximum,
        transport_weight=0.1,
        continuity_weight=0.0,
    )

    assert result.population_path == planted
    assert result.all_blocks_valid
    assert result.recovery_slack > 0.0
    assert result.guarantees_population_path


def test_moving_envelope_propagates_through_scores_and_path_certificate():
    candidates, planted, local, transport = _separated_factor_problem()
    transitions = tuple(np.zeros((2, 2)) for _ in range(3))
    forcings = tuple(np.eye(2) * 1e-10 for _ in range(3))
    perturbations = tuple(np.zeros((2, 2)) for _ in range(3))
    envelope = moving_block_covariance_error_envelope(
        transitions,
        forcings,
        perturbations,
    )
    selections = tuple((((0,), (1,))) for _ in range(3))
    minimum = np.ones((3, 2))
    maximum = np.full((3, 2), 2.0)

    result = moving_partition_localized_recovery_bound(
        envelope,
        selections,
        local,
        transport,
        candidates,
        node_count=4,
        subset_size=2,
        minimum_block_eigenvalues=minimum,
        maximum_block_eigenvalues=maximum,
        transport_weight=0.1,
        continuity_weight=0.0,
    )

    expected = np.array(
        [
            [
                moving_block_joint_covariance_error_bound(
                    envelope,
                    time,
                    tuple(range(envelope.block_counts[time])),
                    selection,
                )
                for selection in selections[time]
            ]
            for time in range(3)
        ]
    )
    np.testing.assert_allclose(result.covariance_spectral_errors, expected)
    assert result.population_path == planted
    assert result.guarantees_population_path


def test_covariance_radius_certificate_marks_invalid_spectral_regime():
    candidates, _, local, transport = _separated_factor_problem()
    result = covariance_radius_path_recovery_bound(
        local,
        transport,
        candidates,
        node_count=4,
        subset_size=2,
        covariance_spectral_errors=np.ones((3, 2)),
        minimum_block_eigenvalues=np.ones((3, 2)),
        maximum_block_eigenvalues=np.full((3, 2), 2.0),
        transport_weight=0.1,
        continuity_weight=0.0,
    )

    assert not result.all_blocks_valid
    assert not result.guarantees_population_path
