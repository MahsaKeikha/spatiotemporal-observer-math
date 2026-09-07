import numpy as np

from observer_math import (
    adjacent_sample_covariances,
    simulate_gaussian_ensemble,
    transport_metrics,
    transport_metrics_from_covariances,
)
from observer_math.nonstationary import adjacent_joint_covariance


def test_empirical_transport_entry_point_matches_analytical_joint():
    current = np.array([[1.0, 0.2], [0.2, 0.8]])
    transition = np.array([[0.6, 0.1], [0.2, 0.5]])
    noise = np.eye(2) * 0.2
    joint = adjacent_joint_covariance(current, transition, noise)

    analytical = transport_metrics(current, transition, noise, (0,), (1,))
    supplied = transport_metrics_from_covariances(current, joint, (0,), (1,))

    assert np.isclose(analytical.persistence, supplied.persistence)
    assert np.isclose(analytical.transport_score, supplied.transport_score)


def test_simulated_covariance_converges_to_population_covariance():
    initial = np.array([[1.0, 0.25], [0.25, 0.7]])
    transition = np.array([[0.5, 0.1], [0.0, 0.6]])
    noise = np.diag([0.2, 0.15])
    rng = np.random.default_rng(12)
    states = simulate_gaussian_ensemble(
        [transition], [noise], initial, 80_000, rng=rng
    )
    present, joint = adjacent_sample_covariances(states[0], states[1], ridge=0.0)
    expected_joint = adjacent_joint_covariance(initial, transition, noise)

    assert np.allclose(present, initial, atol=0.015)
    assert np.allclose(joint, expected_joint, atol=0.015)
