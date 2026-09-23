import numpy as np

from examples.p58_p64_p63_composition_audit import controlled_factors
from observer_math.observer_bridge import relative_covariance_worldtube_recovery_bound


def test_ay_p58_score_radii_contract_with_covariance_radius():
    local, transport, candidates = controlled_factors()
    coarse = relative_covariance_worldtube_recovery_bound(
        local, transport, candidates, node_count=3, subset_size=2,
        covariance_relative_errors=np.full((3, 2), 0.04),
        transport_weight=0.25, continuity_weight=0.0,
    )
    fine = relative_covariance_worldtube_recovery_bound(
        local, transport, candidates, node_count=3, subset_size=2,
        covariance_relative_errors=np.full((3, 2), 0.01),
        transport_weight=0.25, continuity_weight=0.0,
    )
    assert np.max(fine.local_score_errors) <= np.max(coarse.local_score_errors)
    assert np.max(fine.transport_score_errors) <= np.max(coarse.transport_score_errors)
