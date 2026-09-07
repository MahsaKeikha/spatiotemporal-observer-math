from itertools import combinations

import numpy as np

from observer_math import (
    adjacent_joint_covariance,
    certify_worldtube,
    covariance_preserving_moving_clique_bound,
    covariance_preserving_moving_cliques,
    observer_metrics,
    observer_metrics_from_covariances,
    perturbed_covariance_preserving_moving_cliques,
    perturbed_moving_clique_recovery_bound,
    propagate_covariances,
    screen_near_competitors,
    support_resolved_moving_clique_recovery_bound,
    transport_metrics,
    transport_metrics_from_covariances,
)


def test_closed_form_moving_clique_score_matches_covariance_calculation():
    planted, systems = covariance_preserving_moving_cliques(
        node_count=5,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    symbolic = covariance_preserving_moving_clique_bound(
        0.2,
        0.3,
        2,
        minimum_consecutive_overlap=1,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    numerical = observer_metrics(*systems[0], planted[0])

    assert np.isclose(
        symbolic.directed_integration_bits_per_node,
        numerical.directed_integration_bits_per_node,
    )
    assert np.isclose(symbolic.persistence, numerical.persistence)
    assert np.isclose(symbolic.planted_local_score, numerical.observer_score)


def test_symbolic_margin_guarantees_moving_clique_path():
    planted, systems = covariance_preserving_moving_cliques(
        node_count=5,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    candidates = tuple(combinations(range(5), 2))
    local = np.array(
        [
            [observer_metrics(*system, candidate).observer_score for candidate in candidates]
            for system in systems
        ]
    )
    transport = np.empty((2, len(candidates), len(candidates)))
    for time, (transition, noise) in enumerate(systems[:-1]):
        for previous, source in enumerate(candidates):
            for current, target in enumerate(candidates):
                transport[time, previous, current] = transport_metrics(
                    np.eye(5), transition, noise, source, target
                ).transport_score
    symbolic = covariance_preserving_moving_clique_bound(
        0.2,
        0.3,
        2,
        minimum_consecutive_overlap=1,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    certificate = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    assert symbolic.guarantees_unique_planted_path
    assert certificate.result.path == planted
    assert certificate.action_margin >= symbolic.per_mismatch_action_margin


def test_near_competitor_screen_removes_paths_below_robust_lower_action():
    local = np.array([[1.0, 0.1, 0.1], [1.0, 0.1, 0.1]])
    transport = np.zeros((1, 3, 3))
    local_errors = np.full_like(local, 0.01)
    transport_errors = np.full_like(transport, 0.01)
    screen = screen_near_competitors(
        local,
        transport,
        ((0,), (1,), (2,)),
        local_errors,
        transport_errors,
        transport_weight=0.2,
        continuity_weight=0.0,
    )

    assert screen.population_path == (0, 0)
    assert screen.viable_states == ((0,), (0,))
    assert screen.viable_edges == (((0, 0),),)


def test_perturbed_generator_has_requested_norms_and_nonzero_external_entries():
    planted, base = covariance_preserving_moving_cliques(
        node_count=5,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    _, perturbed = perturbed_covariance_preserving_moving_cliques(
        node_count=5,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
        external_coupling_norm=1e-5,
        noise_perturbation_norm=1e-6,
    )

    for active, (base_transition, base_noise), (transition, noise) in zip(
        planted, base, perturbed, strict=True
    ):
        outside = tuple(node for node in range(5) if node not in active)
        assert np.isclose(np.linalg.norm(transition - base_transition, ord=2), 1e-5)
        assert np.isclose(np.linalg.norm(noise - base_noise, ord=2), 1e-6)
        assert np.linalg.norm(transition[np.ix_(active, outside)], ord=2) > 0.0
        assert np.linalg.eigvalsh(noise)[0] > 0.0


def test_perturbed_symbolic_margin_guarantees_numerical_path():
    node_count = 5
    module_size = 2
    time_count = 3
    planted, systems = perturbed_covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=time_count,
        self_memory=0.2,
        internal_coupling=0.3,
        external_coupling_norm=1e-5,
        noise_perturbation_norm=1e-6,
    )
    _, base_systems = covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=time_count,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    transitions = tuple(system[0] for system in systems)
    noises = tuple(system[1] for system in systems)
    covariances = propagate_covariances(transitions, noises, np.eye(node_count))
    joints = tuple(
        adjacent_joint_covariance(covariances[time], *systems[time])
        for time in range(time_count)
    )
    candidates = tuple(combinations(range(node_count), module_size))
    metrics = tuple(
        tuple(
            observer_metrics_from_covariances(covariances[time], joints[time], candidate)
            for candidate in candidates
        )
        for time in range(time_count)
    )
    local = np.array([[entry.observer_score for entry in row] for row in metrics])
    transport = np.array(
        [
            [
                [
                    transport_metrics_from_covariances(
                        covariances[time], joints[time], source, target
                    ).transport_score
                    for target in candidates
                ]
                for source in candidates
            ]
            for time in range(time_count - 1)
        ]
    )
    symbolic = perturbed_moving_clique_recovery_bound(
        0.2,
        0.3,
        module_size,
        node_count,
        time_count,
        transition_perturbation=1e-5,
        noise_perturbation=1e-6,
        minimum_consecutive_overlap=1,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    certificate = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    wrong_integration = [
        entry.integration_strength
        for time, row in enumerate(metrics)
        for entry in row
        if entry.subset != planted[time]
    ]

    assert symbolic.guarantees_unique_planted_path
    assert certificate.result.path == planted
    assert certificate.action_margin >= symbolic.per_mismatch_action_margin
    assert max(
        np.linalg.norm(covariance - np.eye(node_count), ord=2)
        for covariance in covariances
    ) <= symbolic.maximum_state_covariance_error
    assert max(
        np.linalg.norm(
            joints[time]
            - adjacent_joint_covariance(np.eye(node_count), *base_systems[time]),
            ord=2,
        )
        for time in range(time_count)
    ) <= symbolic.maximum_joint_covariance_error
    assert max(
        abs(
            metrics[time][candidates.index(planted[time])].observer_score
            - symbolic.base.planted_local_score
        )
        for time in range(time_count)
    ) <= symbolic.planted_score_error
    assert max(wrong_integration) > 0.0
    assert max(wrong_integration) <= symbolic.incorrect_integration_factor_upper_bound
    assert symbolic.incorrect_score_upper_bound < symbolic.integration_factor_error ** (1 / 3)
    assert max(
        local[time, candidate]
        for time in range(time_count)
        for candidate in range(len(candidates))
        if candidates[candidate] != planted[time]
    ) <= symbolic.incorrect_score_upper_bound


def test_perturbed_bound_rejects_nonfinite_radius_and_extends_certified_radius():
    with np.testing.assert_raises(ValueError):
        perturbed_moving_clique_recovery_bound(
            0.2,
            0.3,
            2,
            5,
            3,
            transition_perturbation=np.nan,
            noise_perturbation=0.0,
        )

    improved = perturbed_moving_clique_recovery_bound(
        0.2,
        0.3,
        2,
        5,
        3,
        transition_perturbation=1e-4,
        noise_perturbation=1e-6,
        minimum_consecutive_overlap=1,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    unresolved = perturbed_moving_clique_recovery_bound(
        0.2,
        0.3,
        2,
        5,
        3,
        transition_perturbation=5e-4,
        noise_perturbation=1e-6,
        minimum_consecutive_overlap=1,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    assert improved.guarantees_unique_planted_path
    assert not unresolved.guarantees_unique_planted_path


def test_perturbed_factor_bounds_cover_random_dense_directions():
    rng = np.random.default_rng(8128)
    node_count = 5
    planted, base_systems = covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    candidates = tuple(combinations(range(node_count), 2))
    symbolic = perturbed_moving_clique_recovery_bound(
        0.2,
        0.3,
        2,
        node_count,
        3,
        transition_perturbation=1e-5,
        noise_perturbation=1e-6,
        minimum_consecutive_overlap=1,
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    for _ in range(12):
        systems = []
        for base_transition, base_noise in base_systems:
            transition_direction = rng.normal(size=(node_count, node_count))
            transition_direction /= np.linalg.norm(transition_direction, ord=2)
            noise_direction = rng.normal(size=(node_count, node_count))
            noise_direction = (noise_direction + noise_direction.T) / 2.0
            noise_direction /= np.linalg.norm(noise_direction, ord=2)
            systems.append(
                (
                    base_transition + 1e-5 * transition_direction,
                    base_noise + 1e-6 * noise_direction,
                )
            )
        covariances = propagate_covariances(
            tuple(system[0] for system in systems),
            tuple(system[1] for system in systems),
            np.eye(node_count),
        )
        for time, system in enumerate(systems):
            joint = adjacent_joint_covariance(covariances[time], *system)
            base_joint = adjacent_joint_covariance(
                np.eye(node_count), *base_systems[time]
            )
            assert (
                np.linalg.norm(joint - base_joint, ord=2)
                <= symbolic.maximum_joint_covariance_error
            )
            for candidate in candidates:
                score = observer_metrics_from_covariances(
                    covariances[time], joint, candidate
                ).observer_score
                if candidate == planted[time]:
                    assert (
                        abs(score - symbolic.base.planted_local_score)
                        <= symbolic.planted_score_error
                    )
                else:
                    assert score <= symbolic.incorrect_score_upper_bound


def test_support_resolved_bound_covers_scores_and_improves_global_margin():
    node_count = 5
    module_size = 2
    planted, systems = perturbed_covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
        external_coupling_norm=1e-5,
        noise_perturbation_norm=1e-6,
    )
    transitions = tuple(system[0] for system in systems)
    noises = tuple(system[1] for system in systems)
    covariances = propagate_covariances(transitions, noises, np.eye(node_count))
    joints = tuple(
        adjacent_joint_covariance(covariances[time], *systems[time])
        for time in range(len(systems))
    )
    support = support_resolved_moving_clique_recovery_bound(
        transitions,
        noises,
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    local = np.array(
        [
            [
                observer_metrics_from_covariances(
                    covariances[time], joints[time], candidate
                ).observer_score
                for candidate in support.candidates
            ]
            for time in range(len(systems))
        ]
    )
    transport = np.array(
        [
            [
                [
                    transport_metrics_from_covariances(
                        covariances[time], joints[time], source, target
                    ).transport_score
                    for target in support.candidates
                ]
                for source in support.candidates
            ]
            for time in range(len(systems) - 1)
        ]
    )
    certificate = certify_worldtube(
        local,
        support.candidates,
        transport_scores=transport,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    global_bound = perturbed_moving_clique_recovery_bound(
        0.2,
        0.3,
        module_size,
        node_count,
        len(systems),
        transition_perturbation=1e-5,
        noise_perturbation=1e-6,
        minimum_consecutive_overlap=1,
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    for time, candidate_bounds in enumerate(support.incorrect_score_upper_bounds):
        for candidate_index, candidate in enumerate(support.candidates):
            score = observer_metrics_from_covariances(
                covariances[time], joints[time], candidate
            ).observer_score
            if candidate == planted[time]:
                assert score >= support.planted_score_lower_bounds[time]
            else:
                assert score <= candidate_bounds[candidate_index]

    assert support.all_local_covariance_bounds_valid
    assert support.guarantees_unique_planted_path
    assert certificate.result.path == planted
    assert certificate.action_margin >= support.per_mismatch_action_margin
    assert support.per_mismatch_action_margin > global_bound.per_mismatch_action_margin
    assert np.allclose(
        support.incident_edge_penalties,
        (0.02 + 0.02 / 3.0, 2.0 * (0.02 + 0.02 / 3.0), 0.02 + 0.02 / 3.0),
    )


def test_support_resolved_bound_rejects_indefinite_noise():
    planted, systems = covariance_preserving_moving_cliques(
        node_count=5,
        module_size=2,
        step_count=2,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    transitions = tuple(system[0] for system in systems)
    noises = [system[1].copy() for system in systems]
    noises[0][0, 0] = -1.0

    with np.testing.assert_raises_regex(ValueError, "positive definite"):
        support_resolved_moving_clique_recovery_bound(
            transitions,
            noises,
            planted,
            self_memory=0.2,
            internal_coupling=0.3,
        )
