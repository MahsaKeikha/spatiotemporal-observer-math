import numpy as np
from scipy.stats import wishart

from examples.gaussian_screen_calibration import population_problem
from observer_math import (
    compose_pilot_screening_drift_relative_error,
    gaussian_drift_robust_relative_near_competitor_screen,
)


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def test_three_sandwich_composition_covers_drifted_screening_covariance():
    pilot_population = np.array([[1.4, 0.2], [0.2, 0.9]])
    screening_population = np.array([[1.46, 0.21], [0.21, 0.87]])
    pilot = np.array([[1.43, 0.19], [0.19, 0.88]])
    screening = np.array([[1.44, 0.225], [0.225, 0.89]])
    epsilon = _relative_error(pilot_population, pilot)
    observed = _relative_error(pilot, screening)
    drift = _relative_error(pilot_population, screening_population)
    combined = compose_pilot_screening_drift_relative_error(
        observed, epsilon, drift
    )

    assert _relative_error(screening_population, screening) <= combined

    epsilon = 0.02
    observed = 0.03
    drift = 0.04
    same_population = observed + epsilon + observed * epsilon
    sharp = compose_pilot_screening_drift_relative_error(
        observed, epsilon, drift
    )
    pilot_population = 1.0
    screening_population = 1.0 - drift
    pilot = (1.0 + epsilon) * pilot_population
    screening = (1.0 + observed) * pilot
    assert np.isclose(
        screening / screening_population - 1.0,
        sharp,
    )
    assert sharp > same_population + drift


def test_drift_robust_screen_covers_scores_and_retains_population_path():
    problem = population_problem()
    sample_count = 80_000_000_000
    scale = 1.00008
    drift = scale**2 - 1.0
    screening_populations = tuple(scale**2 * joint for joint in problem["joints"])
    pilot_rng = np.random.default_rng(20260916)
    screening_rng = np.random.default_rng(20260917)
    pilot = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=pilot_rng,
        )
        for joint in problem["joints"]
    )
    screening = tuple(
        wishart.rvs(
            df=sample_count - 1,
            scale=joint / (sample_count - 1),
            random_state=screening_rng,
        )
        for joint in screening_populations
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    result = gaussian_drift_robust_relative_near_competitor_screen(
        pilot,
        screening,
        problem["candidates"],
        sample_count,
        problem["node_count"],
        3,
        population_drift_relative_errors=np.full(
            (time_count, candidate_count), drift
        ),
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
        zip(screening_populations, screening, strict=True)
    ):
        for current, candidate in enumerate(problem["candidates"]):
            indices = tuple(range(problem["node_count"])) + tuple(
                problem["node_count"] + node for node in candidate
            )
            actual[time, current] = _relative_error(
                population[np.ix_(indices, indices)],
                estimate[np.ix_(indices, indices)],
            )

    assert result.all_drift_envelopes_valid
    assert result.all_blocks_valid
    assert np.all(actual <= result.covariance_relative_errors)
    assert all(
        problem["population_path"][time] in result.screen.viable_states[time]
        for time in range(time_count)
    )


def test_drift_robust_screen_rejects_invalid_drift_envelope():
    joint = np.eye(4)
    common = {
        "structural_integration_null_mask": np.zeros((1, 1), dtype=bool),
        "certification_local_score_errors": np.zeros((1, 1)),
        "certification_transport_score_errors": np.zeros((0, 1, 1)),
    }
    try:
        gaussian_drift_robust_relative_near_competitor_screen(
            (joint,),
            (joint,),
            ((0,),),
            1_000,
            2,
            1,
            population_drift_relative_errors=np.ones((1, 1)),
            **common,
        )
    except ValueError as error:
        assert "below one" in str(error)
    else:
        raise AssertionError("a unit drift radius must be rejected")
