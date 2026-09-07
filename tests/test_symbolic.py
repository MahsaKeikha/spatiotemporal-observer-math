from itertools import combinations

import numpy as np

from observer_math import (
    a_priori_support_moving_clique_recovery_bound,
    adjacent_joint_covariance,
    certify_worldtube,
    covariance_preserving_moving_clique_bound,
    covariance_preserving_moving_cliques,
    observer_metrics,
    observer_metrics_from_covariances,
    overlap_class_moving_clique_recovery_bound,
    perturbed_covariance_preserving_moving_cliques,
    perturbed_moving_clique_recovery_bound,
    propagate_covariances,
    screen_near_competitors,
    support_resolved_moving_clique_recovery_bound,
    transport_metrics,
    transport_metrics_from_covariances,
)
from observer_math.symbolic import (
    _feasible_overlap_pairs,
    _moving_clique_row_norm,
    _moving_clique_transition,
    _moving_clique_within_norm,
)


def _overlap_class_profile(transition_errors, noise_errors, planted):
    """Aggregate exact matrix norms into overlap-indexed audit budgets."""
    node_count = transition_errors[0].shape[0]
    module_size = len(planted[0])
    candidates = tuple(combinations(range(node_count), module_size))
    global_transition = np.array(
        [np.linalg.norm(error, ord=2) for error in transition_errors]
    )
    global_noise = np.array(
        [np.linalg.norm(error, ord=2) for error in noise_errors]
    )
    row_transition = np.zeros((len(planted), module_size + 1))
    within_transition = np.zeros_like(row_transition)
    local_noise = np.zeros_like(row_transition)
    all_nodes = tuple(range(node_count))
    for time, active in enumerate(planted):
        for candidate in candidates:
            overlap = len(set(candidate) & set(active))
            row_transition[time, overlap] = max(
                row_transition[time, overlap],
                np.linalg.norm(
                    transition_errors[time][np.ix_(candidate, all_nodes)],
                    ord=2,
                ),
            )
            within_transition[time, overlap] = max(
                within_transition[time, overlap],
                np.linalg.norm(
                    transition_errors[time][np.ix_(candidate, candidate)],
                    ord=2,
                ),
            )
            local_noise[time, overlap] = max(
                local_noise[time, overlap],
                np.linalg.norm(
                    noise_errors[time][np.ix_(candidate, candidate)],
                    ord=2,
                ),
            )
    return (
        global_transition,
        global_noise,
        row_transition,
        within_transition,
        local_noise,
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


def test_a_priori_support_bound_is_nested_and_nonvacuous():
    node_count = 5
    planted, base_systems = covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    _, systems = perturbed_covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
        external_coupling_norm=1e-5,
        noise_perturbation_norm=1e-6,
    )
    transition_errors = tuple(
        system[0] - base[0]
        for system, base in zip(systems, base_systems, strict=True)
    )
    noise_errors = tuple(
        system[1] - base[1]
        for system, base in zip(systems, base_systems, strict=True)
    )
    a_priori = a_priori_support_moving_clique_recovery_bound(
        transition_errors,
        noise_errors,
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    realized = support_resolved_moving_clique_recovery_bound(
        tuple(system[0] for system in systems),
        tuple(system[1] for system in systems),
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    assert a_priori.candidate_family_is_complete
    assert a_priori.all_local_covariance_bounds_valid
    assert a_priori.guarantees_unique_planted_path_in_candidate_family
    assert 0.0 < a_priori.per_mismatch_action_margin <= realized.per_mismatch_action_margin
    assert np.all(
        np.asarray(realized.planted_local_covariance_errors)
        <= np.asarray(a_priori.planted_local_joint_error_bounds)
    )
    assert np.all(
        np.asarray(realized.planted_leakage_covariance_errors)
        <= np.asarray(a_priori.planted_leakage_joint_error_bounds)
    )
    assert np.all(
        np.asarray(realized.candidate_covariance_errors)
        <= np.asarray(a_priori.candidate_joint_error_bounds) + 1e-14
    )
    assert np.all(
        np.asarray(a_priori.planted_score_lower_bounds)
        <= np.asarray(realized.planted_score_lower_bounds)
    )
    assert np.all(
        np.asarray(a_priori.incorrect_score_upper_bounds)
        >= np.asarray(realized.incorrect_score_upper_bounds)
    )

    reduced = a_priori_support_moving_clique_recovery_bound(
        transition_errors,
        noise_errors,
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        candidate_family=planted,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    assert not reduced.candidate_family_is_complete
    assert reduced.candidate_count == len(set(planted))
    assert reduced.guarantees_unique_planted_path_in_candidate_family


def test_a_priori_support_bounds_cover_random_dense_perturbations():
    rng = np.random.default_rng(271828)
    node_count = 5
    planted, base_systems = covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=2,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )

    for _ in range(8):
        transition_errors = []
        noise_errors = []
        systems = []
        for base_transition, base_noise in base_systems:
            transition_direction = rng.normal(size=(node_count, node_count))
            transition_direction /= np.linalg.norm(transition_direction, ord=2)
            noise_direction = rng.normal(size=(node_count, node_count))
            noise_direction = (noise_direction + noise_direction.T) / 2.0
            noise_direction /= np.linalg.norm(noise_direction, ord=2)
            transition_error = 1e-5 * transition_direction
            noise_error = 1e-6 * noise_direction
            transition_errors.append(transition_error)
            noise_errors.append(noise_error)
            systems.append(
                (base_transition + transition_error, base_noise + noise_error)
            )
        bound = a_priori_support_moving_clique_recovery_bound(
            transition_errors,
            noise_errors,
            planted,
            self_memory=0.2,
            internal_coupling=0.3,
            transport_weight=0.02,
            continuity_weight=0.01,
        )
        profile = _overlap_class_profile(
            transition_errors, noise_errors, planted
        )
        class_bound = overlap_class_moving_clique_recovery_bound(
            node_count,
            planted,
            self_memory=0.2,
            internal_coupling=0.3,
            transition_perturbation_bounds=profile[0],
            noise_perturbation_bounds=profile[1],
            row_transition_perturbation_bounds=profile[2],
            within_transition_perturbation_bounds=profile[3],
            local_noise_perturbation_bounds=profile[4],
            transport_weight=0.02,
            continuity_weight=0.01,
        )
        overlap_indices = {
            overlap: index
            for index, overlap in enumerate(class_bound.overlap_values)
        }
        covariances = propagate_covariances(
            tuple(system[0] for system in systems),
            tuple(system[1] for system in systems),
            np.eye(node_count),
        )
        for time, (system, base_system) in enumerate(
            zip(systems, base_systems, strict=True)
        ):
            joint = adjacent_joint_covariance(covariances[time], *system)
            base_joint = adjacent_joint_covariance(
                np.eye(node_count), *base_system
            )
            assert (
                np.linalg.norm(covariances[time] - np.eye(node_count), ord=2)
                <= bound.global_state_covariance_error_bounds[time] + 1e-14
            )
            for candidate_index, candidate in enumerate(bound.candidates):
                indices = candidate + tuple(node_count + node for node in candidate)
                actual_error = np.linalg.norm(
                    (joint - base_joint)[np.ix_(indices, indices)], ord=2
                )
                assert actual_error <= (
                    bound.candidate_joint_error_bounds[time][candidate_index]
                    + 1e-14
                )
                overlap = bound.candidate_overlaps[time][candidate_index]
                assert bound.candidate_joint_error_bounds[time][
                    candidate_index
                ] <= (
                    class_bound.overlap_class_joint_error_bounds[time][
                        overlap_indices[overlap]
                    ]
                    + 1e-14
                )
                score = observer_metrics_from_covariances(
                    covariances[time], joint, candidate
                ).observer_score
                if candidate == planted[time]:
                    assert score >= bound.planted_score_lower_bounds[time]
                else:
                    assert score <= bound.incorrect_score_upper_bounds[time][
                        candidate_index
                    ]


def test_a_priori_support_bound_rejects_invalid_model_or_family():
    planted, base_systems = covariance_preserving_moving_cliques(
        node_count=5,
        module_size=2,
        step_count=2,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    zero_errors = tuple(np.zeros((5, 5)) for _ in base_systems)

    with np.testing.assert_raises_regex(ValueError, "every planted boundary"):
        a_priori_support_moving_clique_recovery_bound(
            zero_errors,
            zero_errors,
            planted,
            self_memory=0.2,
            internal_coupling=0.3,
            candidate_family=((0, 1),),
        )

    invalid_noise_errors = list(zero_errors)
    invalid_noise_errors[0] = -2.0 * np.eye(5)
    with np.testing.assert_raises_regex(ValueError, "positive definite"):
        a_priori_support_moving_clique_recovery_bound(
            zero_errors,
            invalid_noise_errors,
            planted,
            self_memory=0.2,
            internal_coupling=0.3,
        )


def test_overlap_class_occupancy_matches_exhaustive_candidates():
    for node_count in range(3, 11):
        for module_size in range(2, min(5, node_count - 1) + 1):
            minimum_overlap = max(0, 2 * module_size - node_count)
            previous = tuple(range(module_size))
            for planted_overlap in range(minimum_overlap, module_size + 1):
                current = tuple(range(planted_overlap)) + tuple(
                    range(module_size, 2 * module_size - planted_overlap)
                )
                exhaustive_pairs = {
                    (
                        len(set(candidate) & set(previous)),
                        len(set(candidate) & set(current)),
                    )
                    for candidate in combinations(range(node_count), module_size)
                }
                assert set(
                    _feasible_overlap_pairs(
                        node_count, module_size, planted_overlap
                    )
                ) == exhaustive_pairs

    path = ((0, 1, 2), (1, 2, 3))
    zeros = np.zeros((2, 4))
    bound = overlap_class_moving_clique_recovery_bound(
        7,
        path,
        self_memory=0.2,
        internal_coupling=0.15,
        transition_perturbation_bounds=np.zeros(2),
        noise_perturbation_bounds=np.zeros(2),
        row_transition_perturbation_bounds=zeros,
        within_transition_perturbation_bounds=zeros,
        local_noise_perturbation_bounds=zeros,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    assert sum(bound.overlap_class_multiplicities) == bound.candidate_count
    assert bound.candidate_count == 35
    assert bound.overlap_class_count == 4


def test_overlap_class_base_norm_formulas_match_direct_matrices():
    node_count = 8
    module_size = 4
    planted = tuple(range(module_size))
    for self_memory, internal_coupling in ((0.2, 0.1), (-0.1, 0.12), (0.3, -0.08)):
        transition = _moving_clique_transition(
            node_count,
            planted,
            self_memory,
            internal_coupling,
        )
        for overlap in range(module_size + 1):
            candidate = tuple(range(overlap)) + tuple(
                range(module_size, 2 * module_size - overlap)
            )
            assert np.isclose(
                _moving_clique_row_norm(
                    self_memory, internal_coupling, module_size, overlap
                ),
                np.linalg.norm(transition[candidate, :], ord=2),
            )
            assert np.isclose(
                _moving_clique_within_norm(
                    self_memory, internal_coupling, module_size, overlap
                ),
                np.linalg.norm(transition[np.ix_(candidate, candidate)], ord=2),
            )


def test_overlap_class_bound_dominates_every_candidate_certificate():
    node_count = 5
    module_size = 2
    planted, base_systems = covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
    )
    _, systems = perturbed_covariance_preserving_moving_cliques(
        node_count=node_count,
        module_size=module_size,
        step_count=3,
        self_memory=0.2,
        internal_coupling=0.3,
        external_coupling_norm=1e-5,
        noise_perturbation_norm=1e-6,
    )
    transition_errors = tuple(
        system[0] - base[0]
        for system, base in zip(systems, base_systems, strict=True)
    )
    noise_errors = tuple(
        system[1] - base[1]
        for system, base in zip(systems, base_systems, strict=True)
    )
    profile = _overlap_class_profile(transition_errors, noise_errors, planted)
    class_bound = overlap_class_moving_clique_recovery_bound(
        node_count,
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        transition_perturbation_bounds=profile[0],
        noise_perturbation_bounds=profile[1],
        row_transition_perturbation_bounds=profile[2],
        within_transition_perturbation_bounds=profile[3],
        local_noise_perturbation_bounds=profile[4],
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    candidate_bound = a_priori_support_moving_clique_recovery_bound(
        transition_errors,
        noise_errors,
        planted,
        self_memory=0.2,
        internal_coupling=0.3,
        transport_weight=0.02,
        continuity_weight=0.01,
    )
    overlap_indices = {
        overlap: index for index, overlap in enumerate(class_bound.overlap_values)
    }

    assert class_bound.candidate_count == candidate_bound.candidate_count
    assert class_bound.overlap_class_count == 3
    assert class_bound.all_local_covariance_bounds_valid
    assert class_bound.guarantees_unique_planted_path
    assert 0.0 < class_bound.per_mismatch_action_margin
    assert (
        class_bound.per_mismatch_action_margin
        <= candidate_bound.per_mismatch_action_margin
    )
    assert np.all(
        np.asarray(class_bound.global_state_covariance_error_bounds)
        >= np.asarray(candidate_bound.global_state_covariance_error_bounds) - 1e-14
    )
    assert np.all(
        np.asarray(class_bound.planted_local_joint_error_bounds)
        >= np.asarray(candidate_bound.planted_local_joint_error_bounds) - 1e-14
    )
    assert np.all(
        np.asarray(class_bound.planted_leakage_joint_error_bounds)
        >= np.asarray(candidate_bound.planted_leakage_joint_error_bounds) - 1e-14
    )
    for time, candidates in enumerate(candidate_bound.candidate_joint_error_bounds):
        for candidate_index, candidate_radius in enumerate(candidates):
            overlap = candidate_bound.candidate_overlaps[time][candidate_index]
            class_index = overlap_indices[overlap]
            assert candidate_radius <= (
                class_bound.overlap_class_joint_error_bounds[time][class_index]
                + 1e-14
            )
            assert candidate_bound.incorrect_score_upper_bounds[time][
                candidate_index
            ] <= (
                class_bound.incorrect_score_upper_bounds[time][class_index]
                + 1e-14
            )


def test_overlap_class_bound_rejects_inconsistent_local_budgets():
    planted = ((0, 1), (1, 2))
    zeros = np.zeros((2, 3))
    invalid_rows = zeros.copy()
    invalid_rows[0, 1] = 0.2

    with np.testing.assert_raises_regex(ValueError, "cannot exceed global"):
        overlap_class_moving_clique_recovery_bound(
            5,
            planted,
            self_memory=0.2,
            internal_coupling=0.3,
            transition_perturbation_bounds=np.array([0.1, 0.1]),
            noise_perturbation_bounds=np.zeros(2),
            row_transition_perturbation_bounds=invalid_rows,
            within_transition_perturbation_bounds=zeros,
            local_noise_perturbation_bounds=zeros,
        )


def test_overlap_class_bound_scales_without_candidate_construction():
    module_size = 5
    path = (
        (0, 1, 2, 3, 4),
        (1, 2, 3, 4, 5),
        (2, 3, 4, 5, 6),
    )
    zeros = np.zeros((len(path), module_size + 1))
    bound = overlap_class_moving_clique_recovery_bound(
        100,
        path,
        self_memory=0.2,
        internal_coupling=0.1,
        transition_perturbation_bounds=np.zeros(len(path)),
        noise_perturbation_bounds=np.zeros(len(path)),
        row_transition_perturbation_bounds=zeros,
        within_transition_perturbation_bounds=zeros,
        local_noise_perturbation_bounds=zeros,
        transport_weight=0.02,
        continuity_weight=0.01,
    )

    assert bound.candidate_count == 75_287_520
    assert bound.overlap_class_count == module_size + 1
    assert bound.guarantees_unique_planted_path
