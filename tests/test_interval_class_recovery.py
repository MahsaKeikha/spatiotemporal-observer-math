from itertools import product

import numpy as np

from observer_math import interval_class_covariance_path_recovery_bound


def _interval_problem(width=0.05):
    time_count = 3
    class_count = 2
    local_center = np.full((time_count, class_count, 3), 0.1)
    local_center[:, 1] = 0.9
    local_lower = np.clip(local_center - width, 0.0, 1.0)
    local_upper = np.clip(local_center + width, 0.0, 1.0)
    transport_center = np.full((2, class_count, class_count, 2), 0.1)
    transport_center[:, 1, 1] = 0.85
    transport_lower = np.clip(transport_center - width, 0.0, 1.0)
    transport_upper = np.clip(transport_center + width, 0.0, 1.0)
    multiplicities = np.tile(np.array([3, 1]), (time_count, 1))
    planted = (1, 1, 1)
    feasible = np.ones((2, class_count, class_count), dtype=bool)
    continuity_lower = np.zeros((2, class_count, class_count))
    planted_distances = np.full(2, 0.1)
    local_covariance_errors = np.full((time_count, class_count), 1e-8)
    edge_covariance_errors = np.full((2, class_count, class_count), 1e-8)
    return (
        local_lower,
        local_upper,
        transport_lower,
        transport_upper,
        multiplicities,
        planted,
        feasible,
        continuity_lower,
        planted_distances,
        local_covariance_errors,
        edge_covariance_errors,
    )


def _certificate(problem):
    return interval_class_covariance_path_recovery_bound(
        *problem[:9],
        node_count=8,
        subset_size=2,
        covariance_spectral_errors=problem[9],
        minimum_block_eigenvalues=np.ones(problem[9].shape),
        maximum_block_eigenvalues=np.full(problem[9].shape, 2.0),
        transport_covariance_spectral_errors=problem[10],
        minimum_transport_block_eigenvalues=np.ones(problem[10].shape),
        maximum_transport_block_eigenvalues=np.full(problem[10].shape, 2.0),
        transport_weight=0.1,
        continuity_weight=0.02,
    )


def test_interval_class_certificate_contains_random_heterogeneous_members():
    problem = _interval_problem()
    result = _certificate(problem)
    rng = np.random.default_rng(223607)
    planted = problem[5]

    for _ in range(100):
        local_population = rng.uniform(problem[0], problem[1])
        transport_population = rng.uniform(problem[2], problem[3])
        local_perturbed = np.clip(
            local_population
            + rng.uniform(-1.0, 1.0, local_population.shape)
            * result.local_factor_error_bounds,
            0.0,
            1.0,
        )
        transport_perturbed = np.clip(
            transport_population
            + rng.uniform(-1.0, 1.0, transport_population.shape)
            * result.transport_factor_error_bounds,
            0.0,
            1.0,
        )
        local_scores = np.prod(local_perturbed, axis=2) ** (1.0 / 3.0)
        transport_scores = np.sqrt(np.prod(transport_perturbed, axis=3))

        actions = {}
        for path in product(range(2), repeat=3):
            action = sum(
                local_scores[time, current]
                for time, current in enumerate(path)
            )
            action += sum(
                0.1 * transport_scores[time, path[time], path[time + 1]]
                - 0.02 * (0.1 if path == planted else 0.3)
                for time in range(2)
            )
            actions[path] = float(action)
        competitor = max(value for path, value in actions.items() if path != planted)
        assert actions[planted] >= result.planted_action_lower - 1e-14
        assert competitor <= result.competitor_action_upper + 1e-14

    assert result.recovery_slack > 0.0
    assert result.guarantees_population_path


def test_wider_factor_intervals_cannot_improve_recovery_slack():
    narrow = _certificate(_interval_problem(width=0.01))
    wide = _certificate(_interval_problem(width=0.08))

    assert wide.recovery_slack <= narrow.recovery_slack


def test_negative_transport_weight_reverses_interval_endpoints():
    problem = _interval_problem(width=0.05)
    result = interval_class_covariance_path_recovery_bound(
        *problem[:9],
        node_count=8,
        subset_size=2,
        covariance_spectral_errors=problem[9],
        minimum_block_eigenvalues=np.ones(problem[9].shape),
        maximum_block_eigenvalues=np.full(problem[9].shape, 2.0),
        transport_covariance_spectral_errors=problem[10],
        minimum_transport_block_eigenvalues=np.ones(problem[10].shape),
        maximum_transport_block_eigenvalues=np.full(problem[10].shape, 2.0),
        transport_weight=-0.1,
        continuity_weight=0.02,
    )
    planted = problem[5]
    expected = sum(
        result.local_score_lower_bounds[time, current]
        for time, current in enumerate(planted)
    ) + sum(
        -0.1
        * result.transport_score_upper_bounds[time, planted[time], planted[time + 1]]
        - 0.02 * problem[8][time]
        for time in range(2)
    )
    competitor_actions = []
    for path in product(range(2), repeat=3):
        if path == planted:
            continue
        competitor_actions.append(
            sum(
                result.local_score_upper_bounds[time, current]
                for time, current in enumerate(path)
            )
            + sum(
                -0.1
                * result.transport_score_lower_bounds[
                    time, path[time], path[time + 1]
                ]
                - 0.02 * problem[7][time, path[time], path[time + 1]]
                for time in range(2)
            )
        )

    assert np.isclose(result.planted_action_lower, expected)
    assert np.isclose(result.competitor_action_upper, max(competitor_actions))


def test_interval_class_certificate_rejects_reversed_bounds():
    problem = list(_interval_problem())
    problem[0][0, 0, 0] = problem[1][0, 0, 0] + 0.1

    with np.testing.assert_raises_regex(ValueError, "cannot exceed"):
        _certificate(problem)
