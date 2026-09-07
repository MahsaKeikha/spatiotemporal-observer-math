"""Deterministic conditions used in planted-path recovery arguments."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .worldtube import jaccard_distance


@dataclass(frozen=True)
class ComponentwiseRecoveryBound:
    """Sufficient population separation for a specified path."""

    planted_indices: tuple[int, ...]
    initial_margin: float
    edge_margins: tuple[float, ...]
    minimum_margin: float
    guarantees_unique_recovery: bool


@dataclass(frozen=True)
class FiniteSampleRecoveryBound:
    """Path-level recovery condition under uniform score errors."""

    population_action_margin: float
    maximum_action_gap_error: float
    recovery_slack: float
    guarantees_population_path: bool


def componentwise_recovery_bound(
    local_scores: ArrayLike,
    candidates: Sequence[Sequence[int]],
    planted_indices: Sequence[int],
    *,
    transport_scores: ArrayLike | None = None,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> ComponentwiseRecoveryBound:
    """Check a strong sufficient condition for unique planted-path recovery.

    The planted initial score must dominate every other initial state. At each
    later time, its complete local-plus-transition edge must dominate every
    other candidate edge. The condition is deliberately stronger than global
    optimality, but its margins are transparent and additive.
    """
    local = np.asarray(local_scores, dtype=float)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    path = tuple(int(index) for index in planted_indices)
    if local.ndim != 2:
        raise ValueError("local_scores must have shape (time, candidates)")
    time_count, candidate_count = local.shape
    if time_count != len(path) or candidate_count != len(candidate_tuple):
        raise ValueError("planted path, local scores, and candidates are incompatible")
    if not path or min(path) < 0 or max(path) >= candidate_count:
        raise ValueError("planted_indices must contain one valid index per time")

    if transport_scores is None:
        transport = np.zeros((max(0, time_count - 1), candidate_count, candidate_count))
    else:
        transport = np.asarray(transport_scores, dtype=float)
        expected = (time_count - 1, candidate_count, candidate_count)
        if transport.shape != expected:
            raise ValueError(f"transport_scores must have shape {expected}")

    initial_competitors = np.delete(local[0], path[0])
    initial_margin = (
        np.inf
        if initial_competitors.size == 0
        else float(local[0, path[0]] - np.max(initial_competitors))
    )

    edge_margins: list[float] = []
    for time in range(1, time_count):
        edge_values = np.empty((candidate_count, candidate_count), dtype=float)
        for previous in range(candidate_count):
            for current in range(candidate_count):
                edge_values[previous, current] = (
                    local[time, current]
                    + transport_weight * transport[time - 1, previous, current]
                    - continuity_weight
                    * jaccard_distance(candidate_tuple[previous], candidate_tuple[current])
                )
        planted_edge = (path[time - 1], path[time])
        planted_value = edge_values[planted_edge]
        edge_values[planted_edge] = -np.inf
        edge_margins.append(float(planted_value - np.max(edge_values)))

    all_margins = (initial_margin, *edge_margins)
    minimum = float(min(all_margins))
    return ComponentwiseRecoveryBound(
        planted_indices=path,
        initial_margin=initial_margin,
        edge_margins=tuple(edge_margins),
        minimum_margin=minimum,
        guarantees_unique_recovery=minimum > 0.0,
    )


def finite_sample_recovery_bound(
    population_action_margin: float,
    time_count: int,
    *,
    local_score_error: float,
    transport_score_error: float,
    transport_weight: float,
) -> FiniteSampleRecoveryBound:
    """Evaluate the uniform-error condition for recovering a population path.

    If the supplied error bounds hold jointly with probability at least
    ``1 - alpha``, a positive recovery slack implies path recovery with at least
    the same probability. This function evaluates the deterministic implication;
    it does not estimate ``alpha``.
    """
    if population_action_margin < 0:
        raise ValueError("population_action_margin must be nonnegative")
    if time_count < 1:
        raise ValueError("time_count must be positive")
    if local_score_error < 0 or transport_score_error < 0:
        raise ValueError("score error bounds must be nonnegative")
    maximum_gap_error = 2.0 * (
        time_count * local_score_error
        + abs(transport_weight) * max(0, time_count - 1) * transport_score_error
    )
    slack = float(population_action_margin - maximum_gap_error)
    return FiniteSampleRecoveryBound(
        population_action_margin=float(population_action_margin),
        maximum_action_gap_error=float(maximum_gap_error),
        recovery_slack=slack,
        guarantees_population_path=slack > 0.0,
    )


def gaussian_cmi_covariance_error_bound(
    x_dimension: int,
    y_dimension: int,
    given_dimension: int,
    *,
    minimum_eigenvalue: float,
    covariance_spectral_error: float,
) -> float:
    """Bound Gaussian CMI error caused by a covariance perturbation.

    Both population and estimated covariance blocks are assumed to be principal
    blocks of one covariance whose minimum eigenvalue is at least the supplied
    value. The spectral error must be strictly smaller than that eigenvalue.
    The result is in bits.
    """
    dimensions = (x_dimension, y_dimension, given_dimension)
    if x_dimension < 1 or y_dimension < 1 or given_dimension < 0:
        raise ValueError("require positive x/y dimensions and nonnegative given dimension")
    if minimum_eigenvalue <= 0:
        raise ValueError("minimum_eigenvalue must be positive")
    if not 0 <= covariance_spectral_error < minimum_eigenvalue:
        raise ValueError("covariance_spectral_error must lie in [0, minimum_eigenvalue)")
    if any(int(value) != value for value in dimensions):
        raise ValueError("dimensions must be integers")
    relative_error = covariance_spectral_error / minimum_eigenvalue
    logdet_factor = -np.log1p(-relative_error) / np.log(2.0)
    return float((x_dimension + y_dimension + 2 * given_dimension) * logdet_factor)
