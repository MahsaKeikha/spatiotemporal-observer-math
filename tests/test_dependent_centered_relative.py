import numpy as np

from examples.gaussian_screen_calibration import empirical_factors, population_problem
from observer_math import (
    gaussian_ar1_centered_temporal_correlation_envelope,
    gaussian_dependent_centered_relative_covariance_error_bound,
    gaussian_dependent_centered_relative_structural_null_near_competitor_screen,
    separable_gaussian_centered_covariance,
)


def _ar1_observations(population, mean, sample_count, autocorrelation, rng):
    dimension = population.shape[0]
    standardized = np.empty((sample_count, dimension))
    standardized[0] = rng.normal(size=dimension)
    innovations = rng.normal(size=(sample_count - 1, dimension))
    scale = np.sqrt(1.0 - autocorrelation**2)
    for index in range(1, sample_count):
        standardized[index] = (
            autocorrelation * standardized[index - 1]
            + scale * innovations[index - 1]
        )
    return standardized @ np.linalg.cholesky(population).T + mean


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def test_centered_ar1_envelope_matches_projection_trace_and_bounds_norms():
    sample_count = 40
    autocorrelation = -0.65
    envelope = gaussian_ar1_centered_temporal_correlation_envelope(
        sample_count, autocorrelation
    )
    indices = np.arange(sample_count)
    correlation = autocorrelation ** np.abs(indices[:, None] - indices[None, :])
    projection = np.eye(sample_count) - np.ones((sample_count, sample_count)) / sample_count
    projected = projection @ correlation @ projection

    assert np.isclose(
        envelope.centering_degrees_of_freedom, np.trace(projected)
    )
    assert envelope.projected_frobenius_norm_bound >= np.linalg.norm(projected)
    assert envelope.projected_spectral_norm_bound >= np.linalg.norm(projected, ord=2)


def test_centered_covariance_is_translation_invariant_and_uses_declared_normalizer():
    observations = np.arange(30.0).reshape(10, 3)
    degrees = 7.25
    shift = np.array([100.0, -30.0, 8.0])
    estimate = separable_gaussian_centered_covariance(observations, degrees)
    shifted = separable_gaussian_centered_covariance(observations + shift, degrees)
    centered = observations - np.mean(observations, axis=0, keepdims=True)

    assert np.allclose(estimate, centered.T @ centered / degrees)
    assert np.allclose(shifted, estimate)


def test_centered_dependent_radius_covers_unknown_mean_ar1_covariance():
    sample_count = 5_000
    dimension = 4
    autocorrelation = 0.8
    envelope = gaussian_ar1_centered_temporal_correlation_envelope(
        sample_count, autocorrelation
    )
    observations = _ar1_observations(
        np.eye(dimension),
        np.array([2.0, -1.5, 0.5, 4.0]),
        sample_count,
        autocorrelation,
        np.random.default_rng(20260928),
    )
    estimate = separable_gaussian_centered_covariance(
        observations, envelope.centering_degrees_of_freedom
    )
    radius = gaussian_dependent_centered_relative_covariance_error_bound(
        dimension,
        1,
        centering_degrees_of_freedom=envelope.centering_degrees_of_freedom,
        projected_temporal_frobenius_norm=envelope.projected_frobenius_norm_bound,
        projected_temporal_spectral_norm=envelope.projected_spectral_norm_bound,
    )

    assert np.linalg.norm(estimate - np.eye(dimension), ord=2) <= radius


def test_centered_dependent_screen_covers_scores_and_retains_population_path():
    problem = population_problem()
    sample_count = 150_000
    autocorrelation = 0.4
    envelope = gaussian_ar1_centered_temporal_correlation_envelope(
        sample_count, autocorrelation
    )
    rng = np.random.default_rng(20260929)
    empirical_joints = []
    for time, joint in enumerate(problem["joints"]):
        mean = np.linspace(-2.0, 2.0, joint.shape[0]) + time
        observations = _ar1_observations(
            joint, mean, sample_count, autocorrelation, rng
        )
        empirical_joints.append(
            separable_gaussian_centered_covariance(
                observations, envelope.centering_degrees_of_freedom
            )
        )
    empirical_joints = tuple(empirical_joints)
    local_factors, transport_factors = empirical_factors(empirical_joints, problem)
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    result = gaussian_dependent_centered_relative_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        problem["candidates"],
        sample_count,
        problem["node_count"],
        3,
        centering_degrees_of_freedom=envelope.centering_degrees_of_freedom,
        projected_temporal_frobenius_norm=envelope.projected_frobenius_norm_bound,
        projected_temporal_spectral_norm=envelope.projected_spectral_norm_bound,
        structural_integration_null_mask=np.zeros(
            (time_count, candidate_count), dtype=bool
        ),
        certification_local_score_errors=np.zeros((time_count, candidate_count)),
        certification_transport_score_errors=np.zeros(
            (time_count - 1, candidate_count, candidate_count)
        ),
        transport_weight=0.25,
        continuity_weight=0.08,
    )
    actual = np.empty((time_count, candidate_count))
    for time, (population, estimate) in enumerate(
        zip(problem["joints"], empirical_joints, strict=True)
    ):
        for current, candidate in enumerate(problem["candidates"]):
            indices = tuple(range(problem["node_count"])) + tuple(
                problem["node_count"] + node for node in candidate
            )
            actual[time, current] = _relative_error(
                population[np.ix_(indices, indices)],
                estimate[np.ix_(indices, indices)],
            )

    assert result.all_blocks_valid
    assert np.all(actual <= result.covariance_relative_errors)
    assert all(
        problem["population_path"][time] in result.screen.viable_states[time]
        for time in range(time_count)
    )


def test_centered_iid_envelope_recovers_n_minus_one_normalization():
    envelope = gaussian_ar1_centered_temporal_correlation_envelope(100, 0.0)

    assert envelope.centering_degrees_of_freedom == 99.0
    assert envelope.projected_frobenius_norm_bound == 10.0
    assert envelope.projected_spectral_norm_bound == 1.0
