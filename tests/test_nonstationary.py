import numpy as np

from observer_math import observer_metrics, observer_metrics_from_covariances
from observer_math.gaussian import canonical_correlations, stationary_covariance
from observer_math.nonstationary import (
    adjacent_joint_covariance,
    propagate_covariances,
    transport_metrics,
)


def test_covariance_propagation_matches_recursion():
    initial = np.array([[1.0, 0.2], [0.2, 0.7]])
    transition = np.array([[0.5, 0.1], [0.0, 0.4]])
    noise = np.diag([0.2, 0.3])
    expected = transition @ initial @ transition.T + noise

    path = propagate_covariances([transition], [noise], initial)
    joint = adjacent_joint_covariance(initial, transition, noise)

    assert len(path) == 2
    assert np.allclose(path[1], expected)
    assert np.allclose(joint[:2, 2:], initial @ transition.T)
    assert np.allclose(joint[2:, 2:], expected)


def test_canonical_correlations_are_block_coordinate_invariant():
    source = np.array([[1.3, 0.2], [0.2, 0.9]])
    target = np.array([[1.1, -0.1], [-0.1, 1.4]])
    cross = np.array([[0.45, 0.08], [-0.03, 0.31]])
    source_map = np.array([[2.0, 0.4], [-0.2, 0.7]])
    target_map = np.array([[0.8, -0.3], [0.5, 1.6]])

    baseline = canonical_correlations(source, target, cross)
    transformed = canonical_correlations(
        source_map @ source @ source_map.T,
        target_map @ target @ target_map.T,
        source_map @ cross @ target_map.T,
    )
    assert np.allclose(baseline, transformed, atol=1e-10)


def test_environmental_drive_reduces_transport_independence():
    current = np.eye(3)
    noise = np.eye(3) * 0.1
    insulated = np.diag([0.7, 0.6, 0.4])
    driven = insulated.copy()
    driven[1, 2] = 0.9

    low_leakage = transport_metrics(current, insulated, noise, (0, 1), (0, 1))
    high_leakage = transport_metrics(current, driven, noise, (0, 1), (0, 1))

    assert 0.0 <= low_leakage.transport_score <= 1.0
    assert 0.0 <= high_leakage.transport_score <= 1.0
    assert low_leakage.environmental_leakage_bits_per_node < 1e-10
    assert high_leakage.environmental_leakage_bits_per_node > 0.1
    assert high_leakage.independence < low_leakage.independence


def test_covariance_api_matches_stationary_api():
    transition = np.array([[0.55, 0.18], [0.12, 0.5]])
    noise = np.eye(2) * 0.2
    present = stationary_covariance(transition, noise)
    joint = adjacent_joint_covariance(present, transition, noise)

    stationary = observer_metrics(transition, noise, (0, 1))
    supplied = observer_metrics_from_covariances(present, joint, (0, 1))
    assert np.isclose(stationary.observer_score, supplied.observer_score)
    assert np.isclose(
        stationary.directed_integration_bits_per_node,
        supplied.directed_integration_bits_per_node,
    )
