import numpy as np

from observer_math.gaussian import (
    gaussian_conditional_mutual_information,
    gaussian_mutual_information,
    stationary_covariance,
    two_time_covariance,
)


def test_stationary_covariance_satisfies_lyapunov_equation():
    transition = np.array([[0.6, 0.1], [0.0, 0.5]])
    noise = np.eye(2) * 0.2
    covariance = stationary_covariance(transition, noise)
    assert np.allclose(covariance, transition @ covariance @ transition.T + noise)


def test_independent_variables_have_zero_mutual_information():
    covariance = np.eye(3)
    assert gaussian_mutual_information(covariance, (0,), (1, 2)) == 0.0
    assert gaussian_conditional_mutual_information(covariance, (0,), (1,), (2,)) == 0.0


def test_two_time_covariance_has_expected_shape_and_symmetry():
    transition = np.eye(3) * 0.5
    joint = two_time_covariance(transition, np.eye(3), lag=2)
    assert joint.shape == (6, 6)
    assert np.allclose(joint, joint.T)
