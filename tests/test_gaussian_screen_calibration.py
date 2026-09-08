import numpy as np

from examples.gaussian_screen_calibration import (
    aggregate,
    population_problem,
    run_trial,
    wilson_interval,
)


def test_calibration_problem_has_declared_population_path():
    problem = population_problem()

    assert problem["node_count"] == 7
    assert len(problem["candidates"]) == 8
    assert len(problem["joints"]) == 5
    assert problem["population_path"] == (0, 1, 2, 3, 4)
    assert np.all(problem["minimum"] > 0.0)
    assert np.all(problem["maximum"] >= problem["minimum"])


def test_calibration_trial_is_reproducible_and_in_range():
    first = run_trial((80_000, 4123))
    second = run_trial((80_000, 4123))

    assert first == second
    assert first["covariance_covered"]
    assert first["factor_covered"]
    assert first["score_covered"]
    assert first["population_path_retained"]
    for name, value in first.items():
        if name.endswith("_fraction"):
            assert 0.0 <= value <= 1.0


def test_calibration_aggregation_preserves_events_and_means():
    result = {
        "covariance_covered": True,
        "factor_covered": True,
        "score_covered": True,
        "population_path_retained": True,
        "valid_perturbation_regime": True,
        "maximum_covariance_radius_ratio": 0.25,
        "retained_state_fraction": 0.5,
        "retained_edge_fraction": 0.25,
        "positive_local_floor_fraction": 0.75,
        "positive_transport_floor_fraction": 1.0,
    }
    records = aggregate([100], 2, [result, result])

    assert len(records) == 1
    assert records[0]["covariance_covered_rate"] == 1.0
    assert records[0]["mean_retained_state_fraction"] == 0.5
    assert records[0]["standard_error_retained_state_fraction"] == 0.0
    assert records[0]["covariance_covered_wilson_95"] == wilson_interval(2, 2)
