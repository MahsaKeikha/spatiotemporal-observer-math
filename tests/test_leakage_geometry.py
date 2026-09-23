"""Tests for Proposition 60 leakage measurement architecture."""

import pytest

from observer_math.leakage_geometry import leakage_measurement_geometry


def test_exact_leakage_geometry_matches_worldtube_benchmark() -> None:
    g = leakage_measurement_geometry(7, 3)
    assert g.environment_size == 4
    assert g.exact_block_dimension == 10
    assert g.screened_block_dimension is None
    assert not g.exact_reduction_justified


def test_screened_geometry_is_not_declared_exact_without_certificate() -> None:
    g = leakage_measurement_geometry(7, 3, screened_environment_size=2)
    assert g.screened_block_dimension == 8
    assert not g.exact_reduction_justified


def test_external_conditional_certificate_can_mark_reduction_exact() -> None:
    g = leakage_measurement_geometry(
        7, 3, screened_environment_size=2, conditional_screening_certified=True
    )
    assert g.screened_block_dimension == 8
    assert g.exact_reduction_justified


@pytest.mark.parametrize("m", [-1, 5])
def test_invalid_screened_environment_size_is_rejected(m: int) -> None:
    with pytest.raises(ValueError):
        leakage_measurement_geometry(7, 3, screened_environment_size=m)
