"""Equivalence classes and impossibility bounds for observer paths."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class TwoPointIdentifiabilityBound:
    """Maximin recovery ceiling for two incompatible data-generating models."""

    total_variation_distance: float
    maximin_success_probability: float


def canonical_path_orbit(
    path: Sequence[Sequence[int]],
    permutations: Sequence[Sequence[int]],
) -> tuple[tuple[int, ...], ...]:
    """Return a canonical representative under admissible node permutations."""
    path_tuple = tuple(tuple(int(node) for node in subset) for subset in path)
    permutation_tuple = tuple(tuple(int(node) for node in item) for item in permutations)
    if not permutation_tuple:
        raise ValueError("at least one permutation is required")
    node_count = len(permutation_tuple[0])
    expected = set(range(node_count))
    if any(len(item) != node_count or set(item) != expected for item in permutation_tuple):
        raise ValueError("each permutation must be a bijection of the same node set")
    if any(node < 0 or node >= node_count for subset in path_tuple for node in subset):
        raise ValueError("path contains a node outside the permutation domain")

    orbit = []
    for permutation in permutation_tuple:
        orbit.append(
            tuple(tuple(sorted(permutation[node] for node in subset)) for subset in path_tuple)
        )
    return min(orbit)


def paths_equivalent_under_permutations(
    left: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
    permutations: Sequence[Sequence[int]],
) -> bool:
    """Test whether two paths belong to the same admissible relabeling orbit."""
    return canonical_path_orbit(left, permutations) == canonical_path_orbit(
        right, permutations
    )


def two_point_identifiability_bound(
    total_variation_distance: float,
) -> TwoPointIdentifiabilityBound:
    """Bound recovery when two models assign different correct path orbits.

    If the observation laws have total-variation distance ``tau`` and their
    correct path orbits are disjoint, every data-only estimator has success
    probability at most ``(1 + tau) / 2`` on at least one model.
    """
    if not 0.0 <= total_variation_distance <= 1.0:
        raise ValueError("total_variation_distance must lie in [0, 1]")
    return TwoPointIdentifiabilityBound(
        total_variation_distance=float(total_variation_distance),
        maximin_success_probability=(1.0 + float(total_variation_distance)) / 2.0,
    )
