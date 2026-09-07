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


@dataclass(frozen=True)
class GaussianPathRecoveryBound:
    """End-to-end Gaussian path-recovery guarantee at a fixed sample size."""

    sample_count: int
    confidence: float
    covariance_spectral_error: float
    canonical_persistence_error: float
    local_score_error: float
    transport_score_error: float
    maximum_action_gap_error: float
    valid_perturbation_regime: bool
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


def canonical_persistence_covariance_error_bound(
    *,
    minimum_eigenvalue: float,
    maximum_eigenvalue: float,
    covariance_spectral_error: float,
) -> float:
    """Bound mean-squared canonical-correlation error from covariance error."""
    if minimum_eigenvalue <= 0 or maximum_eigenvalue < minimum_eigenvalue:
        raise ValueError("require 0 < minimum_eigenvalue <= maximum_eigenvalue")
    if not 0 <= covariance_spectral_error < minimum_eigenvalue:
        raise ValueError("covariance_spectral_error must lie in [0, minimum_eigenvalue)")
    eta = covariance_spectral_error
    m = minimum_eigenvalue
    upper = maximum_eigenvalue
    perturbed_minimum = m - eta
    inverse_sqrt_error = eta / (
        np.sqrt(m)
        * np.sqrt(perturbed_minimum)
        * (np.sqrt(m) + np.sqrt(perturbed_minimum))
    )
    whitened_error = (
        inverse_sqrt_error * (upper + eta) / np.sqrt(perturbed_minimum)
        + eta / np.sqrt(m * perturbed_minimum)
        + upper * inverse_sqrt_error / np.sqrt(m)
    )
    return float(min(1.0, 2.0 * whitened_error))


def gaussian_path_recovery_bound(
    population_action_margin: float,
    node_count: int,
    subset_size: int,
    time_count: int,
    sample_count: int,
    *,
    minimum_joint_eigenvalue: float,
    maximum_joint_eigenvalue: float,
    confidence: float = 0.95,
    transport_weight: float = 0.35,
) -> GaussianPathRecoveryBound:
    """Give a sufficient Gaussian ensemble size for exact population-path recovery.

    The estimator is the unbiased centered sample covariance from independent
    trajectories. A Wishart singular-value bound is union-bounded over the
    ``time_count`` adjacent covariance matrices.
    """
    if population_action_margin < 0:
        raise ValueError("population_action_margin must be nonnegative")
    if node_count < 2 or not 1 <= subset_size < node_count:
        raise ValueError("require 1 <= subset_size < node_count")
    if time_count < 1 or sample_count < 2:
        raise ValueError("time_count must be positive and sample_count at least two")
    if minimum_joint_eigenvalue <= 0 or maximum_joint_eigenvalue < minimum_joint_eigenvalue:
        raise ValueError("require valid positive joint-covariance eigenvalue bounds")
    if not 0 < confidence < 1:
        raise ValueError("confidence must lie strictly between zero and one")

    joint_dimension = 2 * node_count
    degrees_of_freedom = sample_count - 1
    failure_probability = 1.0 - confidence
    deviation = (
        np.sqrt(joint_dimension)
        + np.sqrt(2.0 * np.log(2.0 * time_count / failure_probability))
    ) / np.sqrt(degrees_of_freedom)
    covariance_error = maximum_joint_eigenvalue * (2.0 * deviation + deviation**2)
    valid = bool(covariance_error < minimum_joint_eigenvalue)

    if valid:
        persistence_error = canonical_persistence_covariance_error_bound(
            minimum_eigenvalue=minimum_joint_eigenvalue,
            maximum_eigenvalue=maximum_joint_eigenvalue,
            covariance_spectral_error=covariance_error,
        )
        integration_error = (
            4.0
            * (-np.log1p(-covariance_error / minimum_joint_eigenvalue))
            / np.log(2.0)
        )
        leakage_error = gaussian_cmi_covariance_error_bound(
            subset_size,
            node_count - subset_size,
            subset_size,
            minimum_eigenvalue=minimum_joint_eigenvalue,
            covariance_spectral_error=covariance_error,
        ) / subset_size
        integration_factor_error = min(1.0, np.log(2.0) * integration_error)
        independence_error = min(1.0, np.log(2.0) * leakage_error)
        local_error = min(
            1.0,
            (integration_factor_error + independence_error + persistence_error)
            ** (1.0 / 3.0),
        )
        transport_error = min(
            1.0, np.sqrt(independence_error + persistence_error)
        )
    else:
        persistence_error = 1.0
        local_error = 1.0
        transport_error = 1.0

    action_bound = finite_sample_recovery_bound(
        population_action_margin,
        time_count,
        local_score_error=local_error,
        transport_score_error=transport_error,
        transport_weight=transport_weight,
    )
    return GaussianPathRecoveryBound(
        sample_count=sample_count,
        confidence=confidence,
        covariance_spectral_error=float(covariance_error),
        canonical_persistence_error=float(persistence_error),
        local_score_error=float(local_error),
        transport_score_error=float(transport_error),
        maximum_action_gap_error=action_bound.maximum_action_gap_error,
        valid_perturbation_regime=valid,
        guarantees_population_path=valid and action_bound.guarantees_population_path,
    )


def minimum_gaussian_sample_size(
    population_action_margin: float,
    node_count: int,
    subset_size: int,
    time_count: int,
    *,
    minimum_joint_eigenvalue: float,
    maximum_joint_eigenvalue: float,
    confidence: float = 0.95,
    transport_weight: float = 0.35,
    maximum_sample_count: int = 10**15,
) -> int | None:
    """Find the smallest integer sample count certified by the Gaussian bound."""
    if maximum_sample_count < 2:
        raise ValueError("maximum_sample_count must be at least two")
    lower = 2
    upper = 2

    def certified(sample_count: int) -> bool:
        return gaussian_path_recovery_bound(
            population_action_margin,
            node_count,
            subset_size,
            time_count,
            sample_count,
            minimum_joint_eigenvalue=minimum_joint_eigenvalue,
            maximum_joint_eigenvalue=maximum_joint_eigenvalue,
            confidence=confidence,
            transport_weight=transport_weight,
        ).guarantees_population_path

    while upper <= maximum_sample_count and not certified(upper):
        lower = upper + 1
        upper *= 2
    if upper > maximum_sample_count:
        if not certified(maximum_sample_count):
            return None
        upper = maximum_sample_count

    while lower < upper:
        middle = (lower + upper) // 2
        if certified(middle):
            upper = middle
        else:
            lower = middle + 1
    return lower
