from itertools import combinations

import numpy as np

from observer_math import (
    canonical_path_orbit,
    certify_worldtube,
    observer_metrics_from_covariances,
    paths_equivalent_under_permutations,
    transport_metrics,
    two_point_identifiability_bound,
)
from observer_math.gaussian import stationary_covariance, two_time_covariance


def test_path_equivalence_is_computed_over_permutation_orbits():
    permutation_group = ((0, 1, 2), (2, 1, 0))
    left = ((0, 1), (1, 2))
    relabeled = ((1, 2), (0, 1))
    different = ((0, 1), (0, 1))

    assert canonical_path_orbit(left, permutation_group) == ((0, 1), (1, 2))
    assert paths_equivalent_under_permutations(left, relabeled, permutation_group)
    assert not paths_equivalent_under_permutations(left, different, permutation_group)


def test_identical_observation_laws_limit_two_point_recovery_to_one_half():
    identical = two_point_identifiability_bound(0.0)
    separated = two_point_identifiability_bound(0.4)

    assert identical.maximin_success_probability == 0.5
    assert separated.maximin_success_probability == 0.7


def test_exchangeable_dynamics_do_not_select_a_unique_boundary():
    node_count = 4
    transition = np.eye(node_count) * 0.5
    noise = np.eye(node_count) * 0.2
    present = stationary_covariance(transition, noise)
    joint = two_time_covariance(transition, noise)
    candidates = tuple(combinations(range(node_count), 2))
    local = np.array(
        [
            [
                observer_metrics_from_covariances(present, joint, candidate).observer_score
                for candidate in candidates
            ]
            for _ in range(2)
        ]
    )
    transport = np.empty((1, len(candidates), len(candidates)))
    for previous, source in enumerate(candidates):
        for current, target in enumerate(candidates):
            transport[0, previous, current] = transport_metrics(
                present, transition, noise, source, target
            ).transport_score

    certificate = certify_worldtube(
        local,
        candidates,
        transport_scores=transport,
        transport_weight=0.0,
        continuity_weight=0.0,
    )

    assert certificate.action_margin == 0.0
