from itertools import product
from math import comb

import numpy as np

from observer_math import class_compressed_covariance_path_recovery_bound


def _class_problem(time_count=3, class_count=3):
    local = np.full((time_count, class_count, 3), 0.05)
    local[:, -1] = 0.9
    transport = np.full(
        (time_count - 1, class_count, class_count, 2),
        0.05,
    )
    transport[:, -1, -1] = 0.9
    multiplicities = np.tile(np.arange(1, class_count + 1), (time_count, 1))
    multiplicities[:, -1] = 1
    planted = (class_count - 1,) * time_count
    feasible = np.ones((time_count - 1, class_count, class_count), dtype=bool)
    continuity_lower = np.zeros_like(feasible, dtype=float)
    planted_distances = np.full(time_count - 1, 0.2)
    covariance_errors = np.full((time_count, class_count), 1e-10)
    minimum = np.ones_like(covariance_errors)
    maximum = np.full_like(covariance_errors, 2.0)
    return (
        local,
        transport,
        multiplicities,
        planted,
        feasible,
        continuity_lower,
        planted_distances,
        covariance_errors,
        minimum,
        maximum,
    )


def test_class_dynamic_program_matches_exhaustive_class_paths():
    problem = _class_problem()
    (
        local,
        transport,
        multiplicities,
        planted,
        feasible,
        continuity_lower,
        planted_distances,
        covariance_errors,
        minimum,
        maximum,
    ) = problem
    result = class_compressed_covariance_path_recovery_bound(
        local,
        transport,
        multiplicities,
        planted,
        feasible,
        continuity_lower,
        planted_distances,
        node_count=8,
        subset_size=2,
        covariance_spectral_errors=covariance_errors,
        minimum_block_eigenvalues=minimum,
        maximum_block_eigenvalues=maximum,
        transport_covariance_spectral_errors=np.full(feasible.shape, 1e-10),
        minimum_transport_block_eigenvalues=np.ones(feasible.shape),
        maximum_transport_block_eigenvalues=np.full(feasible.shape, 2.0),
        transport_weight=0.1,
        continuity_weight=0.02,
    )

    local_upper = np.prod(local, axis=2) ** (1.0 / 3.0) + result.local_score_errors
    transport_scores = np.sqrt(np.prod(transport, axis=3))
    edge_upper = (
        0.1 * transport_scores
        + 0.1 * result.transport_score_errors
        - 0.02 * continuity_lower
    )
    exhaustive = []
    for path in product(range(local.shape[1]), repeat=local.shape[0]):
        if path == planted:
            continue
        value = sum(local_upper[time, current] for time, current in enumerate(path))
        value += sum(
            edge_upper[time, path[time], path[time + 1]]
            for time in range(local.shape[0] - 1)
        )
        exhaustive.append((float(value), path))
    exhaustive_value, _ = max(exhaustive)

    np.testing.assert_allclose(result.competitor_action_upper, exhaustive_value)
    adversarial = result.adversarial_class_path
    assert adversarial is not None
    adversarial_value = sum(
        local_upper[time, current] for time, current in enumerate(adversarial)
    ) + sum(
        edge_upper[time, adversarial[time], adversarial[time + 1]]
        for time in range(local.shape[0] - 1)
    )
    np.testing.assert_allclose(adversarial_value, exhaustive_value)
    assert result.guarantees_population_path


def test_overlap_multiplicities_scale_without_candidate_construction():
    node_count = 1_000
    subset_size = 5
    time_count = 5
    class_count = subset_size + 1
    problem = list(_class_problem(time_count, class_count))
    overlap_multiplicities = np.array(
        [
            comb(subset_size, overlap)
            * comb(node_count - subset_size, subset_size - overlap)
            for overlap in range(class_count)
        ],
        dtype=object,
    )
    problem[2] = np.tile(overlap_multiplicities, (time_count, 1))
    problem[2] = problem[2].astype(object)
    candidate_count = comb(node_count, subset_size)

    result = class_compressed_covariance_path_recovery_bound(
        problem[0],
        problem[1],
        problem[2],
        problem[3],
        problem[4],
        problem[5],
        problem[6],
        node_count=node_count,
        subset_size=subset_size,
        covariance_spectral_errors=problem[7],
        minimum_block_eigenvalues=problem[8],
        maximum_block_eigenvalues=problem[9],
        transport_covariance_spectral_errors=np.full(problem[4].shape, 1e-10),
        minimum_transport_block_eigenvalues=np.ones(problem[4].shape),
        maximum_transport_block_eigenvalues=np.full(problem[4].shape, 2.0),
        transport_weight=0.02,
        continuity_weight=0.0,
    )

    assert sum(overlap_multiplicities) == candidate_count
    assert result.class_count == 6
    assert result.implicit_path_count == candidate_count**time_count
    assert result.guarantees_population_path


def test_class_certificate_requires_singleton_planted_classes():
    problem = list(_class_problem())
    problem[2][0, -1] = 2

    with np.testing.assert_raises_regex(ValueError, "multiplicity one"):
        class_compressed_covariance_path_recovery_bound(
            problem[0],
            problem[1],
            problem[2],
            problem[3],
            problem[4],
            problem[5],
            problem[6],
            node_count=8,
            subset_size=2,
            covariance_spectral_errors=problem[7],
            minimum_block_eigenvalues=problem[8],
            maximum_block_eigenvalues=problem[9],
            transport_covariance_spectral_errors=np.full(problem[4].shape, 1e-10),
            minimum_transport_block_eigenvalues=np.ones(problem[4].shape),
            maximum_transport_block_eigenvalues=np.full(problem[4].shape, 2.0),
        )


def test_class_certificate_checks_transport_spectral_regime_separately():
    problem = _class_problem()
    result = class_compressed_covariance_path_recovery_bound(
        problem[0],
        problem[1],
        problem[2],
        problem[3],
        problem[4],
        problem[5],
        problem[6],
        node_count=8,
        subset_size=2,
        covariance_spectral_errors=problem[7],
        minimum_block_eigenvalues=problem[8],
        maximum_block_eigenvalues=problem[9],
        transport_covariance_spectral_errors=np.ones(problem[4].shape),
        minimum_transport_block_eigenvalues=np.ones(problem[4].shape),
        maximum_transport_block_eigenvalues=np.full(problem[4].shape, 2.0),
    )

    assert not result.all_blocks_valid
    assert not result.guarantees_population_path
