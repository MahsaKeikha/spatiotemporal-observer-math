import numpy as np
from scipy.stats import wishart

from examples.gaussian_screen_calibration import population_problem
from observer_math import gaussian_cross_fitted_relative_near_competitor_screen


def _relative_error(population, estimated):
    values, vectors = np.linalg.eigh(population)
    inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
    return float(
        np.linalg.norm(inverse_sqrt @ (estimated - population) @ inverse_sqrt, ord=2)
    )


def test_pilot_sandwich_composition_covers_screening_covariance():
    population = np.array([[1.4, 0.2], [0.2, 0.9]])
    pilot = np.array([[1.43, 0.19], [0.19, 0.88]])
    screening = np.array([[1.38, 0.215], [0.215, 0.92]])
    epsilon = _relative_error(population, pilot)
    observed = _relative_error(pilot, screening)
    combined = observed + epsilon + observed * epsilon

    assert _relative_error(population, screening) <= combined


def test_cross_fitted_screen_covers_scores_and_retains_population_path():
    problem = population_problem()
    sample_count = 80_000_000_000
    pilot_rng = np.random.default_rng(20260913)
    screening_rng = np.random.default_rng(20260914)
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
        for joint in problem["joints"]
    )
    time_count = len(problem["joints"])
    candidate_count = len(problem["candidates"])
    null_mask = np.zeros((time_count, candidate_count), dtype=bool)
    result = gaussian_cross_fitted_relative_near_competitor_screen(
        pilot,
        screening,
        problem["candidates"],
        sample_count,
        problem["node_count"],
        3,
        structural_integration_null_mask=null_mask,
        certification_local_score_errors=np.zeros((time_count, candidate_count)),
        certification_transport_score_errors=np.zeros(
            (time_count - 1, candidate_count, candidate_count)
        ),
        transport_weight=0.25,
        continuity_weight=0.08,
    )

    actual = np.empty((time_count, candidate_count))
    for time, (population, estimate) in enumerate(
        zip(problem["joints"], screening, strict=True)
    ):
        for current, candidate in enumerate(problem["candidates"]):
            indices = tuple(range(problem["node_count"])) + tuple(
                problem["node_count"] + node for node in candidate
            )
            actual[time, current] = _relative_error(
                population[np.ix_(indices, indices)], estimate[np.ix_(indices, indices)]
            )

    assert result.all_pilot_blocks_positive_definite
    assert result.all_blocks_valid
    assert np.all(actual <= result.covariance_relative_errors)
    assert all(
        problem["population_path"][time] in result.screen.viable_states[time]
        for time in range(time_count)
    )


def test_cross_fitted_screen_rejects_mismatched_covariance_sequences():
    joint = np.eye(4)
    try:
        gaussian_cross_fitted_relative_near_competitor_screen(
            (joint,),
            (joint, joint),
            ((0,),),
            100,
            2,
            1,
            structural_integration_null_mask=np.zeros((1, 1), dtype=bool),
            certification_local_score_errors=np.zeros((1, 1)),
            certification_transport_score_errors=np.zeros((0, 1, 1)),
        )
    except ValueError as error:
        assert "equal positive length" in str(error)
    else:
        raise AssertionError("mismatched covariance sequences must be rejected")
