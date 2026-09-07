from itertools import combinations

import numpy as np

from observer_math import (
    certify_worldtube,
    covariance_preserving_moving_clique_bound,
    covariance_preserving_moving_cliques,
    observer_metrics,
    screen_near_competitors,
    transport_metrics,
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
