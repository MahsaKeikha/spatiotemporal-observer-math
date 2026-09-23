import numpy as np

from observer_math.action_intervals import path_action_interval


def test_p64_action_interval_propagates_local_and_transport_uncertainty():
    local = np.array([[1.0, 0.2], [0.9, 0.3], [0.8, 0.4]])
    local_err = np.full_like(local, 0.05)
    transport = np.zeros((2, 2, 2))
    transport[:, 0, 0] = 0.6
    transport_err = np.full_like(transport, 0.02)
    continuity = np.zeros((2, 2))
    out = path_action_interval((0, 0, 0), local, local_err, transport, transport_err, continuity, transport_weight=0.25, continuity_weight=0.1)
    assert np.isclose(out.nominal_action, 3.0)
    assert np.isclose(out.uncertainty_radius, 0.16)
    assert np.isclose(out.interval.lower, 2.84)
    assert np.isclose(out.interval.upper, 3.16)


def test_p64_transport_sign_uses_absolute_weight_for_radius():
    local = np.ones((2, 1))
    local_err = np.zeros_like(local)
    transport = np.ones((1, 1, 1))
    transport_err = np.full_like(transport, 0.2)
    continuity = np.zeros((1, 1))
    out = path_action_interval((0, 0), local, local_err, transport, transport_err, continuity, transport_weight=-0.5, continuity_weight=0.0)
    assert np.isclose(out.uncertainty_radius, 0.1)
