import numpy as np

from examples.gaussian_screen_calibration import empirical_factors, population_problem
from observer_math import (
    gaussian_ar1_increment_autocorrelation_interval,
    gaussian_estimated_ar1_centered_covariance_bound,
    gaussian_estimated_ar1_centered_relative_structural_null_near_competitor_screen,
    separable_gaussian_centered_covariance,
)


def _ar1_standardized(sample_count, channel_count, autocorrelation, rng):
    values = np.empty((sample_count, channel_count))
    values[0] = rng.normal(size=channel_count)
    innovations = rng.normal(size=(sample_count - 1, channel_count))
    scale = np.sqrt(1.0 - autocorrelation**2)
    for index in range(1, sample_count):
        values[index] = (
            autocorrelation * values[index - 1] + scale * innovations[index - 1]
        )
    return values


def test_increment_interval_contains_phi_and_is_translation_invariant():
    observations = _ar1_standardized(
        40_000, 8, 0.72, np.random.default_rng(20261001)
    )
    shifted = observations + np.linspace(-10.0, 15.0, observations.shape[1])
    interval = gaussian_ar1_increment_autocorrelation_interval(
        observations, declared_upper_bound=0.98
    )
    shifted_interval = gaussian_ar1_increment_autocorrelation_interval(
        shifted, declared_upper_bound=0.98
    )

    assert interval.lower_bound <= 0.72 <= interval.upper_bound
    assert interval.interval_intersects_declared_model
    assert np.isclose(interval.estimate, shifted_interval.estimate)
    assert interval.lower_bound == shifted_interval.lower_bound
    assert interval.upper_bound == shifted_interval.upper_bound


def test_increment_covariance_obeys_uniform_norm_bounds():
    length = 31
    for autocorrelation in (0.0, 0.35, 0.8, 0.97):
        indices = np.arange(length)
        covariance = np.empty((length, length))
        separation = np.abs(indices[:, None] - indices[None, :])
        covariance[separation == 0] = 1.0 - autocorrelation
        nonzero = separation > 0
        covariance[nonzero] = (
            -0.5
            * (1.0 - autocorrelation) ** 2
            * autocorrelation ** (separation[nonzero] - 1)
        )

        assert np.linalg.norm(covariance, ord=2) <= 2.0 + 1e-12
        assert np.linalg.norm(covariance, ord="fro") ** 2 <= 1.5 * length


def test_estimated_ar1_bound_covers_same_record_centered_covariance():
    sample_count = 50_000
    dimension = 6
    autocorrelation = 0.78
    standardized = _ar1_standardized(
        sample_count, dimension, autocorrelation, np.random.default_rng(20261002)
    )
    observations = standardized + np.linspace(-4.0, 3.0, dimension)
    interval = gaussian_ar1_increment_autocorrelation_interval(
        standardized, declared_upper_bound=0.98
    )
    bound = gaussian_estimated_ar1_centered_covariance_bound(
        dimension, 1, sample_count, interval
    )
    estimate = separable_gaussian_centered_covariance(
        observations, bound.reference_centering_degrees_of_freedom
    )
    actual_error = np.linalg.norm(estimate - np.eye(dimension), ord=2)

    assert bound.combined_confidence == 0.9750000000000001
    assert bound.normalization_error > 0.0
    assert actual_error <= bound.covariance_relative_error


def test_estimated_ar1_bound_propagates_through_complete_screen():
    problem = population_problem()
    sample_count = 400_000
    standardized = _ar1_standardized(
        sample_count, 8, 0.35, np.random.default_rng(20261003)
    )
    interval = gaussian_ar1_increment_autocorrelation_interval(
        standardized, declared_upper_bound=0.98
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    bound = gaussian_estimated_ar1_centered_covariance_bound(
        problem["node_count"] + 3,
        time_count * candidate_count,
        sample_count,
        interval,
    )
    local_factors, transport_factors = empirical_factors(
        problem["joints"], problem
    )
    result = (
        gaussian_estimated_ar1_centered_relative_structural_null_near_competitor_screen(
            local_factors,
            transport_factors,
            problem["candidates"],
            sample_count,
            problem["node_count"],
            3,
            covariance_bound=bound,
            structural_integration_null_mask=np.zeros(
                (time_count, candidate_count), dtype=bool
            ),
            certification_local_score_errors=np.zeros(
                (time_count, candidate_count)
            ),
            certification_transport_score_errors=np.zeros(
                (time_count - 1, candidate_count, candidate_count)
            ),
            transport_weight=0.25,
            continuity_weight=0.08,
        )
    )

    assert result.all_blocks_valid
    assert np.all(
        result.covariance_relative_errors == bound.covariance_relative_error
    )
    assert all(
        problem["population_path"][time] in result.screen.viable_states[time]
        for time in range(time_count)
    )


def test_more_calibration_channels_tighten_the_interval():
    observations = np.zeros((2_000, 12))
    narrow = gaussian_ar1_increment_autocorrelation_interval(
        observations, declared_upper_bound=0.98
    )
    wide = gaussian_ar1_increment_autocorrelation_interval(
        observations[:, :1], declared_upper_bound=0.98
    )

    assert narrow.error_radius < wide.error_radius
    assert narrow.channel_count == 12
    assert wide.channel_count == 1
