import numpy as np
import pytest

from observer_math.active_measurement import (
    certificate_pressure,
    gaussian_equal_variance_kl,
    minimum_expected_measurements,
    path_action_radius,
    robust_pairwise_certificate,
    signed_evidence_gap,
)


def test_path_action_radius_matches_am18_sum():
    assert np.isclose(path_action_radius([0.1, 0.2], [0.3], transport_weight=-2.0), 0.9)


def test_robust_certificate_requires_strict_interval_separation():
    good = robust_pairwise_certificate(2.0, 1.0, 0.2, 0.3)
    assert good.certified
    assert np.isclose(good.robust_separation, 0.5)
    boundary = robust_pairwise_certificate(2.0, 1.0, 0.5, 0.5)
    assert not boundary.certified
    assert boundary.robust_separation == 0.0


def test_certificate_pressure_is_factorwise_and_weighted():
    pressure = certificate_pressure(
        [0.1, 0.2], [0.3, 0.4], [0.2], [0.1], transport_weight=-2.0
    )
    assert np.allclose(pressure["local"], [0.4, 0.6])
    assert np.allclose(pressure["transport"], [0.6])


def test_equal_variance_gaussian_kl_and_equivalence():
    kl = gaussian_equal_variance_kl(
        np.array([1.0, 0.0]), np.array([0.0, 0.0]), np.array([2.0, 1.0])
    )
    assert np.allclose(kl, [0.25, 0.0])


def test_information_debt_lower_bound_and_impossibility():
    assert signed_evidence_gap(5.0, 2.0) == 3.0
    assert minimum_expected_measurements(3.0, 0.7) == 5
    assert np.isinf(minimum_expected_measurements(3.0, 0.0))


def test_invalid_radii_and_variance_rejected():
    with pytest.raises(ValueError):
        path_action_radius([-0.1], [], transport_weight=1.0)
    with pytest.raises(ValueError):
        gaussian_equal_variance_kl(np.array([0.0]), np.array([1.0]), np.array([0.0]))
