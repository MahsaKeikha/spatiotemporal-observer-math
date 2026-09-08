import numpy as np
from scipy.stats import wishart

from examples.gaussian_screen_calibration import empirical_factors, population_problem
from observer_math import (
    compose_calibrated_population_drift_relative_error,
    gaussian_calibrated_drift_relative_near_competitor_screen,
    gaussian_calibrated_population_drift_bound,
)


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def test_calibrated_drift_composition_is_sharp_in_one_dimension():
    observed = 0.03
    reference_error = 0.02
    current_error = 0.04
    bound = compose_calibrated_population_drift_relative_error(
        observed, reference_error, current_error
    )
    reference_population = 1.0
    reference_estimate = (1.0 + reference_error) * reference_population
    current_estimate = (1.0 + observed) * reference_estimate
    current_population = current_estimate / (1.0 - current_error)

    assert np.isclose(current_population / reference_population - 1.0, bound)


def test_calibrated_population_drift_bound_covers_known_change():
    problem = population_problem()
    sample_count = 80_000_000_000
    scale = 1.00008
    current_populations = tuple(scale**2 * joint for joint in problem["joints"])
    reference_rng = np.random.default_rng(20260919)
    current_rng = np.random.default_rng(20260920)
    reference = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=reference_rng,
        )
        for joint in problem["joints"]
    )
    current = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=current_rng,
        )
        for joint in current_populations
    )
    result = gaussian_calibrated_population_drift_bound(
        reference,
        current,
        problem["candidates"],
        sample_count,
        sample_count,
        problem["node_count"],
        3,
    )

    assert np.isclose(result.overall_confidence_lower_bound, 0.975)
    assert result.all_bounds_valid
    assert np.all(scale**2 - 1.0 <= result.population_drift_relative_errors)


def test_calibrated_drift_screen_covers_scores_and_retains_path():
    problem = population_problem()
    sample_count = 80_000_000_000
    scale = 1.00008
    current_populations = tuple(scale**2 * joint for joint in problem["joints"])
    reference_rng = np.random.default_rng(20260921)
    calibration_rng = np.random.default_rng(20260922)
    screening_rng = np.random.default_rng(20260923)
    reference = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=reference_rng,
        )
        for joint in problem["joints"]
    )
    calibration = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=calibration_rng,
        )
        for joint in current_populations
    )
    screening = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=screening_rng,
        )
        for joint in current_populations
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    result = gaussian_calibrated_drift_relative_near_competitor_screen(
        reference,
        calibration,
        screening,
        problem["candidates"],
        sample_count,
        sample_count,
        problem["node_count"],
        3,
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
        zip(current_populations, screening, strict=True)
    ):
        for current, candidate in enumerate(problem["candidates"]):
            indices = tuple(range(problem["node_count"])) + tuple(
                problem["node_count"] + node for node in candidate
            )
            actual[time, current] = _relative_error(
                population[np.ix_(indices, indices)],
                estimate[np.ix_(indices, indices)],
            )

    assert result.guarantees_safe_screen
    assert np.all(actual <= result.screening.covariance_relative_errors)
    local_factors, transport_factors = empirical_factors(screening, problem)
    empirical_local = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    population_local = np.prod(problem["local_factors"], axis=2) ** (1.0 / 3.0)
    empirical_transport = np.sqrt(np.prod(transport_factors, axis=3))
    population_transport = np.sqrt(np.prod(problem["transport_factors"], axis=3))
    assert np.all(
        np.abs(empirical_local - population_local)
        <= result.screening.screening_local_score_errors
    )
    assert np.all(
        np.abs(empirical_transport - population_transport)
        <= result.screening.screening_transport_score_errors
    )
    assert all(
        problem["population_path"][time]
        in result.screening.screen.viable_states[time]
        for time in range(time_count)
    )


def test_calibrated_drift_rejects_invalid_confidence():
    joint = np.eye(4)
    try:
        gaussian_calibrated_drift_relative_near_competitor_screen(
            (joint,),
            (joint,),
            (joint,),
            ((0,),),
            1_000,
            1_000,
            2,
            1,
            structural_integration_null_mask=np.zeros((1, 1), dtype=bool),
            certification_local_score_errors=np.zeros((1, 1)),
            certification_transport_score_errors=np.zeros((0, 1, 1)),
            confidence=1.0,
        )
    except ValueError as error:
        assert "confidence" in str(error)
    else:
        raise AssertionError("unit confidence must be rejected")
