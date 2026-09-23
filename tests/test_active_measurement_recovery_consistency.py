import numpy as np
from observer_math.active_measurement import (
    observer_factor_radii_from_relative_covariance,
    transport_score_radius_from_relative_covariance,
)
from observer_math.recovery import relative_covariance_factor_error_bounds

def test_local_adaptive_bridge_uses_canonical_recovery_factor_bounds():
    delta=.2
    expected,valid=relative_covariance_factor_error_bounds(delta,7,3,transport=False)
    assert valid
    got=observer_factor_radii_from_relative_covariance(
        subset_size=3,ambient_size=7,covariance_relative_error=delta,
        integration_factor=.6,insulation_factor=.7,persistence_factor=.8)
    np.testing.assert_allclose(
        [got["integration"],got["insulation"],got["persistence"]],expected)

def test_transport_adaptive_bridge_uses_canonical_recovery_factor_bounds():
    delta=.2
    expected,valid=relative_covariance_factor_error_bounds(delta,7,3,transport=True)
    assert valid
    got=transport_score_radius_from_relative_covariance(
        subset_size=3,ambient_size=7,covariance_relative_error=delta,
        insulation_factor=.7,persistence_factor=.8)
    np.testing.assert_allclose([got["insulation"],got["persistence"]],expected)

def test_invalid_relative_radius_fails_conservatively():
    got=observer_factor_radii_from_relative_covariance(
        subset_size=3,ambient_size=7,covariance_relative_error=1.0,
        integration_factor=.6,insulation_factor=.7,persistence_factor=.8)
    assert got["observer_score"]==1.0
