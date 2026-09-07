import numpy as np

from observer_math import (
    moving_block_covariance_error_envelope,
    moving_block_joint_covariance_error_bound,
    screened_structural_class_path_recovery_bound,
)


def _problem(tail=0.01):
    time_count = 3
    class_count = 2
    transitions = tuple(
        np.array(
            [
                [0.20, 0.01, 0.00],
                [0.01, 0.20, 0.00],
                [0.00, 0.00, 0.20],
            ]
        )
        for _ in range(time_count)
    )
    forcings = tuple(
        np.diag([1e-8, 2e-8, 5e-5]) for _ in range(time_count)
    )
    perturbations = tuple(np.zeros((3, 3)) for _ in range(time_count))
    envelope = moving_block_covariance_error_envelope(
        transitions,
        forcings,
        perturbations,
    )
    local = np.full((time_count, class_count, 3), 0.1)
    local[:, 1] = 0.9
    transport = np.full((time_count - 1, class_count, class_count, 2), 0.1)
    transport[:, 1, 1] = 0.85
    local_present = (((0,), (1,)),) * time_count
    local_future = (((0,), (1,)),) * time_count
    edge_present_layer = (
        ((0,), (0,)),
        ((1,), (1,)),
    )
    edge_future_layer = (
        ((0,), (1,)),
        ((0,), (1,)),
    )
    edge_shape = (time_count - 1, class_count, class_count)
    return {
        "envelope": envelope,
        "local": local,
        "transport": transport,
        "local_present": local_present,
        "local_future": local_future,
        "edge_present": (edge_present_layer,) * (time_count - 1),
        "edge_future": (edge_future_layer,) * (time_count - 1),
        "local_tail": np.full((time_count, class_count), tail),
        "edge_tail": np.full(edge_shape, tail),
        "multiplicities": np.tile(np.array([5, 1]), (time_count, 1)),
        "planted": (1, 1, 1),
        "feasible": np.ones(edge_shape, dtype=bool),
        "continuity": np.zeros(edge_shape),
        "planted_distances": np.full(time_count - 1, 0.2),
        "local_minimum": np.ones((time_count, class_count)),
        "local_maximum": np.full((time_count, class_count), 2.0),
        "edge_minimum": np.ones(edge_shape),
        "edge_maximum": np.full(edge_shape, 2.0),
    }


def _certificate(problem):
    return screened_structural_class_path_recovery_bound(
        problem["envelope"],
        problem["local_present"],
        problem["local_future"],
        problem["edge_present"],
        problem["edge_future"],
        problem["local"],
        problem["transport"],
        problem["local_tail"],
        problem["edge_tail"],
        problem["multiplicities"],
        problem["planted"],
        problem["feasible"],
        problem["continuity"],
        problem["planted_distances"],
        node_count=8,
        subset_size=2,
        representative_minimum_block_eigenvalues=problem["local_minimum"],
        representative_maximum_block_eigenvalues=problem["local_maximum"],
        representative_minimum_transport_eigenvalues=problem["edge_minimum"],
        representative_maximum_transport_eigenvalues=problem["edge_maximum"],
        transport_weight=0.1,
        continuity_weight=0.02,
    )


def test_screened_residuals_equal_source_specific_joint_compressions():
    problem = _problem()
    result = _certificate(problem)

    for time in range(3):
        for current in range(2):
            expected = moving_block_joint_covariance_error_bound(
                problem["envelope"],
                time,
                problem["local_present"][time][current],
                problem["local_future"][time][current],
            )
            assert np.isclose(
                result.local_covariance_residual_bounds[time, current],
                expected,
            )
    for time in range(2):
        for previous in range(2):
            for current in range(2):
                expected = moving_block_joint_covariance_error_bound(
                    problem["envelope"],
                    time,
                    problem["edge_present"][time][previous][current],
                    problem["edge_future"][time][previous][current],
                )
                assert np.isclose(
                    result.transport_covariance_residual_bounds[
                        time, previous, current
                    ],
                    expected,
                )

    full_radius = moving_block_joint_covariance_error_bound(
        problem["envelope"],
        2,
        (0, 1, 2),
        (0, 1, 2),
    )
    assert np.max(result.local_covariance_residual_bounds) < full_radius
    assert result.recovery.guarantees_population_path


def test_omitted_leakage_tail_has_exact_insulation_multiplier():
    zero = _certificate(_problem(tail=0.0))
    positive = _certificate(_problem(tail=0.03))

    assert np.allclose(
        positive.local_factor_lower_bounds[:, :, 1],
        zero.local_factor_lower_bounds[:, :, 1] * np.exp2(-0.03),
    )
    assert np.allclose(
        positive.transport_factor_lower_bounds[:, :, :, 0],
        zero.transport_factor_lower_bounds[:, :, :, 0] * np.exp2(-0.03),
    )
    assert positive.recovery.recovery_slack <= zero.recovery.recovery_slack


def test_screened_certificate_rejects_negative_omitted_leakage():
    problem = _problem()
    problem["local_tail"][0, 0] = -0.1

    with np.testing.assert_raises_regex(ValueError, "nonnegative"):
        _certificate(problem)
