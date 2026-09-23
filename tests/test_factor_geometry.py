"""Claim-level tests for Proposition 59 factor-specific covariance geometry."""

import pytest

from observer_math.factor_geometry import observer_factor_block_geometry


def test_moving_module_factor_dimensions() -> None:
    geometry = observer_factor_block_geometry(7, 3)
    assert geometry.integration_dimension == 6
    assert geometry.local_persistence_dimension == 6
    assert geometry.transport_persistence_dimension == 6
    assert geometry.local_independence_dimension == 10
    assert geometry.transport_independence_dimension == 10
    assert geometry.maximum_dimension == 10


def test_geometry_changes_with_candidate_size() -> None:
    geometry = observer_factor_block_geometry(12, 2)
    assert geometry.integration_dimension == 4
    assert geometry.local_independence_dimension == 14
    assert geometry.maximum_dimension == 14


@pytest.mark.parametrize("node_count, subset_size", [(1, 1), (4, 0), (4, 4), (4, 5)])
def test_invalid_geometry_is_rejected(node_count: int, subset_size: int) -> None:
    with pytest.raises(ValueError):
        observer_factor_block_geometry(node_count, subset_size)
