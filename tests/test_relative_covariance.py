import numpy as np

from observer_math import (
    canonical_persistence_relative_covariance_error_bound,
    gaussian_relative_cmi_covariance_error_bound,
    gaussian_relative_null_cmi_covariance_error_bound,
    gaussian_relative_structural_null_near_competitor_screen,
    gaussian_wishart_relative_covariance_error_bound,
)
from observer_math.gaussian import (
    canonical_persistence,
    gaussian_conditional_mutual_information,
)


def relative_error(covariance, estimated):
    values, vectors = np.linalg.eigh(covariance)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(np.linalg.norm(inverse_sqrt @ (estimated - covariance) @ inverse_sqrt, 2))


def test_relative_information_and_persistence_bounds_cover_direct_perturbation():
    covariance = np.array(
        [
            [1.4, 0.1, 0.35, 0.05],
            [0.1, 1.1, -0.02, 0.28],
            [0.35, -0.02, 1.3, 0.08],
            [0.05, 0.28, 0.08, 1.2],
        ]
    )
    perturbation = np.array(
        [
            [0.008, 0.001, -0.003, 0.002],
            [0.001, -0.006, 0.002, -0.001],
            [-0.003, 0.002, 0.007, 0.001],
            [0.002, -0.001, 0.001, -0.005],
        ]
    )
    estimated = covariance + perturbation
    delta = relative_error(covariance, estimated)
    cmi_error = abs(
        gaussian_conditional_mutual_information(estimated, (0,), (2,), (1, 3))
        - gaussian_conditional_mutual_information(covariance, (0,), (2,), (1, 3))
    )
    persistence_error = abs(
        canonical_persistence(estimated[:2, :2], estimated[2:, 2:], estimated[:2, 2:])
        - canonical_persistence(
            covariance[:2, :2], covariance[2:, 2:], covariance[:2, 2:]
        )
    )

    assert cmi_error <= gaussian_relative_cmi_covariance_error_bound(
        1, 1, 2, covariance_relative_error=delta
    )
    assert persistence_error <= canonical_persistence_relative_covariance_error_bound(
        covariance_relative_error=delta
    )


def test_relative_null_bound_covers_conditional_independence_perturbation():
    # X and Y are conditionally independent given Z because C_XY=C_XZ C_ZZ^-1 C_ZY.
    covariance = np.array(
        [
            [1.04, 0.03, 0.2],
            [0.03, 1.0225, 0.15],
            [0.2, 0.15, 1.0],
        ]
    )
    perturbation = np.array(
        [[0.004, 0.002, -0.001], [0.002, -0.003, 0.001], [-0.001, 0.001, 0.002]]
    )
    estimated = covariance + perturbation
    delta = relative_error(covariance, estimated)
    empirical_cmi = gaussian_conditional_mutual_information(
        estimated, (0,), (1,), (2,)
    )

    assert np.isclose(
        gaussian_conditional_mutual_information(covariance, (0,), (1,), (2,)), 0.0
    )
    assert empirical_cmi <= gaussian_relative_null_cmi_covariance_error_bound(
        1, covariance_relative_error=delta
    )


def test_relative_wishart_radius_and_screen_are_condition_number_free():
    small = gaussian_wishart_relative_covariance_error_bound(10, 20, 10**6)
    large = gaussian_wishart_relative_covariance_error_bound(10, 20, 10**8)
    assert large < small

    local_factors = np.full((2, 2, 3), 0.7)
    local_factors[:, 1, 0] = 0.0
    transport_factors = np.full((1, 2, 2, 2), 0.65)
    zeros = np.zeros((2, 2))
    edge_zeros = np.zeros((1, 2, 2))
    screen = gaussian_relative_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        ((0, 1), (1, 2)),
        10**9,
        3,
        2,
        structural_integration_null_mask=np.array([[False, True], [False, True]]),
        certification_local_score_errors=zeros,
        certification_transport_score_errors=edge_zeros,
    )

    assert screen.all_blocks_valid
    assert screen.maximum_covariance_relative_error < 1.0
    assert np.all(screen.null_local_score_errors[:, 1] == 0.0)

    invalid = gaussian_relative_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        ((0, 1), (1, 2)),
        3,
        3,
        2,
        structural_integration_null_mask=np.array([[False, True], [False, True]]),
        certification_local_score_errors=zeros,
        certification_transport_score_errors=edge_zeros,
    )
    assert not invalid.all_blocks_valid
    assert not invalid.guarantees_safe_screen
