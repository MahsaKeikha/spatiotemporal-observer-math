"""Claim-level tests for Proposition 58 observer-certification bridge."""

from __future__ import annotations

import numpy as np

from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound


def _controlled_factors() -> tuple[np.ndarray, np.ndarray, tuple[tuple[int, ...], ...]]:
    candidates = ((0, 1), (1, 2))
    local = np.array(
        [
            [[0.72, 0.94, 0.82], [0.18, 0.88, 0.45]],
            [[0.70, 0.93, 0.80], [0.16, 0.86, 0.42]],
            [[0.68, 0.92, 0.78], [0.15, 0.85, 0.40]],
        ],
        dtype=float,
    )
    transport = np.full((2, 2, 2, 2), 0.20, dtype=float)
    transport[:, 0, 0] = (0.94, 0.86)
    transport[:, 1, 1] = (0.75, 0.52)
    transport[:, 0, 1] = (0.50, 0.35)
    transport[:, 1, 0] = (0.48, 0.32)
    return local, transport, candidates


def test_zero_covariance_error_recovers_population_worldtube() -> None:
    local, transport, candidates = _controlled_factors()
    bound = relative_covariance_worldtube_recovery_bound(
        local,
        transport,
        candidates,
        node_count=3,
        subset_size=2,
        covariance_relative_errors=np.zeros((3, 2)),
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    assert bound.all_blocks_valid
    assert bound.guarantees_population_path
    assert bound.population_path == (0, 0, 0)
    assert np.max(bound.local_factor_errors) == 0.0
    assert np.max(bound.transport_factor_errors) == 0.0
    assert np.max(bound.local_score_errors) == 0.0
    assert np.max(bound.transport_score_errors) == 0.0
    assert np.isclose(bound.recovery_slack, bound.population_action_margin)


def test_relative_radius_one_is_reported_as_outside_perturbative_regime() -> None:
    local, transport, candidates = _controlled_factors()
    radii = np.full((3, 2), 0.02)
    radii[1, 1] = 1.0
    bound = relative_covariance_worldtube_recovery_bound(
        local,
        transport,
        candidates,
        node_count=3,
        subset_size=2,
        covariance_relative_errors=radii,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    assert not bound.all_blocks_valid
    assert not bound.guarantees_population_path
    assert bound.local_factor_errors[1, 1, 0] == 1.0


def test_declared_structural_null_tightens_zero_integration_state() -> None:
    local, transport, candidates = _controlled_factors()
    local = local.copy()
    local[0, 1, 0] = 0.0
    radii = np.full((3, 2), 0.10)
    baseline = relative_covariance_worldtube_recovery_bound(
        local,
        transport,
        candidates,
        node_count=3,
        subset_size=2,
        covariance_relative_errors=radii,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    null_mask = np.zeros((3, 2), dtype=bool)
    null_mask[0, 1] = True
    refined = relative_covariance_worldtube_recovery_bound(
        local,
        transport,
        candidates,
        node_count=3,
        subset_size=2,
        covariance_relative_errors=radii,
        structural_integration_null_mask=null_mask,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    assert refined.local_score_errors[0, 1] <= baseline.local_score_errors[0, 1]
    assert refined.structural_integration_null_mask[0, 1]


def test_candidate_local_radius_controls_every_incoming_edge_to_that_candidate() -> None:
    local, transport, candidates = _controlled_factors()
    radii = np.full((3, 2), 0.01)
    radii[0, 1] = 0.04
    bound = relative_covariance_worldtube_recovery_bound(
        local,
        transport,
        candidates,
        node_count=3,
        subset_size=2,
        covariance_relative_errors=radii,
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    entering_candidate_one = bound.transport_factor_errors[0, :, 1]
    entering_candidate_zero = bound.transport_factor_errors[0, :, 0]
    assert np.allclose(entering_candidate_one[0], entering_candidate_one[1])
    assert np.allclose(entering_candidate_zero[0], entering_candidate_zero[1])
    assert np.all(entering_candidate_one > entering_candidate_zero)
