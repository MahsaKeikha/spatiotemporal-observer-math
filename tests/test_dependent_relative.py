import numpy as np

from examples.gaussian_screen_calibration import empirical_factors, population_problem
from observer_math import (
    gaussian_ar1_temporal_correlation_envelope,
    gaussian_dependent_relative_covariance_error_bound,
    gaussian_dependent_relative_structural_null_near_competitor_screen,
    gaussian_wishart_relative_covariance_error_bound,
)


def _ar1_covariance(population, sample_count, autocorrelation, rng):
    dimension = population.shape[0]
    standardized = np.empty((sample_count, dimension))
    standardized[0] = rng.normal(size=dimension)
    innovation_scale = np.sqrt(1.0 - autocorrelation**2)
    innovations = rng.normal(size=(sample_count - 1, dimension))
    for index in range(1, sample_count):
        standardized[index] = (
            autocorrelation * standardized[index - 1]
            + innovation_scale * innovations[index - 1]
        )
    root = np.linalg.cholesky(population)
    observations = standardized @ root.T
    return observations.T @ observations / sample_count


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def test_ar1_temporal_norm_envelope_matches_explicit_matrix():
    sample_count = 50
    autocorrelation = -0.72
    envelope = gaussian_ar1_temporal_correlation_envelope(
        sample_count, autocorrelation
    )
    indices = np.arange(sample_count)
    correlation = autocorrelation ** np.abs(indices[:, None] - indices[None, :])

    assert np.isclose(envelope.frobenius_norm_bound, np.linalg.norm(correlation))
    assert envelope.spectral_norm_bound >= np.linalg.norm(correlation, ord=2)
    assert np.isclose(
        envelope.variance_effective_sample_size,
        sample_count**2 / np.linalg.norm(correlation) ** 2,
    )


def test_dependent_relative_radius_covers_seeded_ar1_covariance():
    sample_count = 5_000
    dimension = 4
    autocorrelation = 0.8
    envelope = gaussian_ar1_temporal_correlation_envelope(
        sample_count, autocorrelation
    )
    estimate = _ar1_covariance(
        np.eye(dimension),
        sample_count,
        autocorrelation,
        np.random.default_rng(20260925),
    )
    radius = gaussian_dependent_relative_covariance_error_bound(
        dimension,
        1,
        sample_count,
        temporal_correlation_frobenius_norm=envelope.frobenius_norm_bound,
        temporal_correlation_spectral_norm=envelope.spectral_norm_bound,
        confidence=0.975,
    )

    assert np.linalg.norm(estimate - np.eye(dimension), ord=2) <= radius


def test_dependent_screen_covers_scores_and_retains_population_path():
    problem = population_problem()
    sample_count = 200_000
    autocorrelation = 0.4
    rng = np.random.default_rng(20260926)
    empirical_joints = tuple(
        _ar1_covariance(joint, sample_count, autocorrelation, rng)
        for joint in problem["joints"]
    )
    local_factors, transport_factors = empirical_factors(empirical_joints, problem)
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    envelope = gaussian_ar1_temporal_correlation_envelope(
        sample_count, autocorrelation
    )
    result = gaussian_dependent_relative_structural_null_near_competitor_screen(
        local_factors,
        transport_factors,
        problem["candidates"],
        sample_count,
        problem["node_count"],
        3,
        temporal_correlation_frobenius_norm=envelope.frobenius_norm_bound,
        temporal_correlation_spectral_norm=envelope.spectral_norm_bound,
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
    empirical_local = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    population_local = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    empirical_transport = np.sqrt(np.prod(transport_factors, axis=3))
    population_transport = np.sqrt(np.prod(problem["transport_factors"], axis=3))

    assert result.all_blocks_valid
    assert np.all(actual <= result.covariance_relative_errors)
    assert np.all(
        np.abs(empirical_local - population_local)
        <= result.screening_local_score_errors
    )
    assert np.all(
        np.abs(empirical_transport - population_transport)
        <= result.screening_transport_score_errors
    )
    assert all(
        problem["population_path"][time] in result.screen.viable_states[time]
        for time in range(time_count)
    )


def test_temporal_dependence_reduces_effective_sample_size_and_inflates_radius():
    sample_count = 20_000
    independent = gaussian_ar1_temporal_correlation_envelope(sample_count, 0.0)
    dependent = gaussian_ar1_temporal_correlation_envelope(sample_count, 0.85)
    dependent_radius = gaussian_dependent_relative_covariance_error_bound(
        5,
        2,
        sample_count,
        temporal_correlation_frobenius_norm=dependent.frobenius_norm_bound,
        temporal_correlation_spectral_norm=dependent.spectral_norm_bound,
    )
    iid_radius = gaussian_wishart_relative_covariance_error_bound(
        5, 2, sample_count
    )

    assert dependent.variance_effective_sample_size < sample_count
    assert dependent.operator_effective_sample_size < sample_count
    assert dependent_radius > iid_radius
    assert independent.variance_effective_sample_size == sample_count
