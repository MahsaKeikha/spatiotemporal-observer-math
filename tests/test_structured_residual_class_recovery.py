import numpy as np

from observer_math import (
    moving_block_covariance_error_envelope,
    moving_block_joint_covariance_error_bound,
    residual_class_covariance_path_recovery_bound,
    structured_residual_class_path_recovery_bound,
)


def _problem(forcing_scale=1e-7):
    time_count = 3
    class_count = 2
    transitions = tuple(np.eye(2) * 0.2 for _ in range(time_count))
    forcings = tuple(np.eye(2) * forcing_scale for _ in range(time_count))
    perturbations = tuple(np.zeros((2, 2)) for _ in range(time_count))
    envelope = moving_block_covariance_error_envelope(
        transitions,
        forcings,
        perturbations,
    )
    local = np.full((time_count, class_count, 3), 0.1)
    local[:, 1] = 0.9
    transport = np.full((time_count - 1, class_count, class_count, 2), 0.1)
    transport[:, 1, 1] = 0.85
    return {
        "envelope": envelope,
        "selections": (((0,), (1,)),) * time_count,
        "local": local,
        "transport": transport,
        "multiplicities": np.tile(np.array([4, 1]), (time_count, 1)),
        "planted": (1, 1, 1),
        "feasible": np.ones((time_count - 1, class_count, class_count), dtype=bool),
        "continuity_lower": np.zeros(
            (time_count - 1, class_count, class_count)
        ),
        "planted_distances": np.full(time_count - 1, 0.2),
        "local_minimum": np.ones((time_count, class_count)),
        "local_maximum": np.full((time_count, class_count), 2.0),
        "edge_minimum": np.ones(
            (time_count - 1, class_count, class_count)
        ),
        "edge_maximum": np.full(
            (time_count - 1, class_count, class_count), 2.0
        ),
        "local_sampling": np.full((time_count, class_count), 1e-9),
        "edge_sampling": np.full(
            (time_count - 1, class_count, class_count), 1e-9
        ),
    }


def _certificate(problem):
    return structured_residual_class_path_recovery_bound(
        problem["envelope"],
        problem["selections"],
        problem["local"],
        problem["transport"],
        problem["multiplicities"],
        problem["planted"],
        problem["feasible"],
        problem["continuity_lower"],
        problem["planted_distances"],
        node_count=8,
        subset_size=2,
        representative_minimum_block_eigenvalues=problem["local_minimum"],
        representative_maximum_block_eigenvalues=problem["local_maximum"],
        representative_minimum_transport_eigenvalues=problem["edge_minimum"],
        representative_maximum_transport_eigenvalues=problem["edge_maximum"],
        covariance_spectral_errors=problem["local_sampling"],
        transport_covariance_spectral_errors=problem["edge_sampling"],
        transport_weight=0.1,
        continuity_weight=0.02,
    )


def test_structured_residuals_equal_direct_block_compressions():
    problem = _problem()
    result = _certificate(problem)
    expected_local = np.empty((3, 2))
    for time in range(3):
        for current in range(2):
            expected_local[time, current] = moving_block_joint_covariance_error_bound(
                problem["envelope"],
                time,
                (0, 1),
                problem["selections"][time][current],
            )
    expected_transport = np.repeat(
        expected_local[:-1, None, :],
        2,
        axis=1,
    )

    assert np.allclose(result.local_covariance_residual_bounds, expected_local)
    assert np.allclose(
        result.transport_covariance_residual_bounds,
        expected_transport,
    )
    assert result.recovery.recovery.guarantees_population_path


def test_structured_wrapper_matches_explicit_residual_composition():
    problem = _problem()
    result = _certificate(problem)
    direct = residual_class_covariance_path_recovery_bound(
        problem["local"],
        problem["transport"],
        problem["multiplicities"],
        problem["planted"],
        problem["feasible"],
        problem["continuity_lower"],
        problem["planted_distances"],
        node_count=8,
        subset_size=2,
        local_covariance_residual_bounds=result.local_covariance_residual_bounds,
        representative_minimum_block_eigenvalues=problem["local_minimum"],
        representative_maximum_block_eigenvalues=problem["local_maximum"],
        transport_covariance_residual_bounds=(
            result.transport_covariance_residual_bounds
        ),
        representative_minimum_transport_eigenvalues=problem["edge_minimum"],
        representative_maximum_transport_eigenvalues=problem["edge_maximum"],
        covariance_spectral_errors=problem["local_sampling"],
        transport_covariance_spectral_errors=problem["edge_sampling"],
        transport_weight=0.1,
        continuity_weight=0.02,
    )

    assert np.isclose(
        result.recovery.recovery.recovery_slack,
        direct.recovery.recovery_slack,
    )


def test_structured_wrapper_rejects_invalid_class_block_selection():
    problem = _problem()
    selections = list(problem["selections"])
    selections[1] = ((0,), (2,))
    problem["selections"] = selections

    with np.testing.assert_raises_regex(ValueError, "outside"):
        _certificate(problem)
