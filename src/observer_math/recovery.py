"""Deterministic conditions used in planted-path recovery arguments."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .localization import (
    MovingBlockCovarianceErrorEnvelope,
    moving_block_joint_covariance_error_bound,
)
from .metrics import observer_metrics_from_covariances
from .nonstationary import (
    adjacent_joint_covariance,
    propagate_covariances,
    transport_metrics,
)
from .worldtube import certify_worldtube, jaccard_distance


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


@dataclass(frozen=True)
class LocalizedGaussianPathRecoveryBound:
    """Candidate-local Gaussian recovery certificate."""

    sample_count: int
    confidence: float
    population_path: tuple[int, ...]
    adversarial_competitor: tuple[int, ...] | None
    population_action_margin: float
    planted_lower_action: float
    competitor_upper_action: float
    recovery_slack: float
    maximum_covariance_spectral_error: float
    maximum_local_score_error: float
    maximum_transport_score_error: float
    viable_state_count: int
    viable_edge_count: int
    all_blocks_valid: bool
    guarantees_population_path: bool


@dataclass(frozen=True)
class CovarianceRadiusPathRecoveryBound:
    """Deterministic path certificate from candidate-local covariance radii."""

    population_path: tuple[int, ...]
    adversarial_competitor: tuple[int, ...] | None
    population_action_margin: float
    planted_lower_action: float
    competitor_upper_action: float
    recovery_slack: float
    covariance_spectral_errors: np.ndarray
    local_score_errors: np.ndarray
    transport_score_errors: np.ndarray
    viable_state_count: int
    viable_edge_count: int
    all_blocks_valid: bool
    guarantees_population_path: bool


@dataclass(frozen=True)
class NearCompetitorScreen:
    """State and edge graph that can still challenge a robust path lower bound."""

    population_path: tuple[int, ...]
    planted_lower_action: float
    viable_states: tuple[tuple[int, ...], ...]
    viable_edges: tuple[tuple[tuple[int, int], ...], ...]
    state_upper_actions: tuple[tuple[float, ...], ...]
    viable_state_count: int
    viable_edge_count: int


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


def product_root_error_bound(
    population_factors: ArrayLike,
    factor_error_bounds: ArrayLike,
) -> float:
    """Bound a geometric-mean error, using positive factor floors when possible.

    The zero-safe Holder bound is always valid. If every population factor is
    separated from zero by more than its error radius, a local Lipschitz bound
    is also evaluated and the tighter certificate is returned.
    """
    factors = np.asarray(population_factors, dtype=float)
    errors = np.asarray(factor_error_bounds, dtype=float)
    if factors.ndim != 1 or factors.size < 1 or errors.shape != factors.shape:
        raise ValueError("population_factors and factor_error_bounds must be equal vectors")
    if np.any(~np.isfinite(factors)) or np.any(~np.isfinite(errors)):
        raise ValueError("factors and error bounds must be finite")
    if np.any((factors < 0.0) | (factors > 1.0)) or np.any(errors < 0.0):
        raise ValueError("factors must lie in [0, 1] and errors must be nonnegative")

    degree = factors.size
    holder_bound = min(1.0, float(np.sum(errors)) ** (1.0 / degree))
    lower_factors = factors - errors
    if np.any(lower_factors <= 0.0):
        return holder_bound
    exponent = (degree - 1.0) / degree
    lipschitz_bound = float(
        np.sum(errors / lower_factors**exponent) / degree
    )
    return min(1.0, holder_bound, lipschitz_bound)


def screen_near_competitors(
    local_scores: ArrayLike,
    transport_scores: ArrayLike,
    candidates: Sequence[Sequence[int]],
    local_score_errors: ArrayLike,
    transport_score_errors: ArrayLike,
    *,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> NearCompetitorScreen:
    """Find the state-edge graph containing every error-plausible winner.

    A state or edge is retained when some path through it has an error-inflated
    population action at least as large as the population winner's deflated
    action. All empirical winners lie in the retained graph whenever the
    supplied score-error bounds hold.
    """
    local = np.asarray(local_scores, dtype=float)
    transport = np.asarray(transport_scores, dtype=float)
    local_errors = np.asarray(local_score_errors, dtype=float)
    transport_errors = np.asarray(transport_score_errors, dtype=float)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if local.ndim != 2 or local_errors.shape != local.shape:
        raise ValueError("local scores and errors must have equal two-dimensional shapes")
    time_count, candidate_count = local.shape
    expected = (max(0, time_count - 1), candidate_count, candidate_count)
    if transport.shape != expected or transport_errors.shape != expected:
        raise ValueError(f"transport scores and errors must have shape {expected}")
    if time_count < 1 or candidate_count != len(candidate_tuple):
        raise ValueError("scores and candidates have incompatible shapes")
    if (
        np.any(~np.isfinite(local))
        or np.any(~np.isfinite(transport))
        or np.any(~np.isfinite(local_errors))
        or np.any(~np.isfinite(transport_errors))
        or np.any(local_errors < 0.0)
        or np.any(transport_errors < 0.0)
    ):
        raise ValueError("scores must be finite and error bounds nonnegative")

    continuity = np.empty((candidate_count, candidate_count), dtype=float)
    for previous in range(candidate_count):
        for current in range(candidate_count):
            continuity[previous, current] = jaccard_distance(
                candidate_tuple[previous], candidate_tuple[current]
            )
    inflated_local = local + local_errors
    inflated_edges = (
        transport_weight * transport
        + abs(transport_weight) * transport_errors
        - continuity_weight * continuity[None, :, :]
    )
    population = certify_worldtube(
        local,
        candidate_tuple,
        transport_scores=transport,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    planted = population.result.candidate_indices
    planted_error = float(
        sum(local_errors[time, current] for time, current in enumerate(planted))
        + abs(transport_weight)
        * sum(
            transport_errors[time, planted[time], planted[time + 1]]
            for time in range(time_count - 1)
        )
    )
    planted_lower = population.result.total_action - planted_error

    forward = np.full((time_count, candidate_count), -np.inf)
    forward[0] = inflated_local[0]
    for time in range(1, time_count):
        forward[time] = inflated_local[time] + np.max(
            forward[time - 1, :, None] + inflated_edges[time - 1], axis=0
        )
    backward = np.zeros((time_count, candidate_count), dtype=float)
    for time in range(time_count - 2, -1, -1):
        backward[time] = np.max(
            inflated_edges[time]
            + inflated_local[time + 1, None, :]
            + backward[time + 1, None, :],
            axis=1,
        )
    state_upper = forward + backward
    viable_state_mask = state_upper >= planted_lower

    viable_edges: list[tuple[tuple[int, int], ...]] = []
    for time in range(time_count - 1):
        edge_upper = (
            forward[time, :, None]
            + inflated_edges[time]
            + inflated_local[time + 1, None, :]
            + backward[time + 1, None, :]
        )
        viable_edges.append(
            tuple(
                (previous, current)
                for previous in range(candidate_count)
                for current in range(candidate_count)
                if edge_upper[previous, current] >= planted_lower
            )
        )
    viable_states = tuple(
        tuple(np.flatnonzero(viable_state_mask[time]).tolist())
        for time in range(time_count)
    )
    return NearCompetitorScreen(
        population_path=planted,
        planted_lower_action=float(planted_lower),
        viable_states=viable_states,
        viable_edges=tuple(viable_edges),
        state_upper_actions=tuple(tuple(row.tolist()) for row in state_upper),
        viable_state_count=sum(len(states) for states in viable_states),
        viable_edge_count=sum(len(edges) for edges in viable_edges),
    )


def covariance_radius_path_recovery_bound(
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    node_count: int,
    subset_size: int,
    *,
    covariance_spectral_errors: ArrayLike,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> CovarianceRadiusPathRecoveryBound:
    """Certify path recovery from deterministic candidate-local radii."""
    local = np.asarray(local_factors, dtype=float)
    transport = np.asarray(transport_factors, dtype=float)
    covariance_errors = np.asarray(covariance_spectral_errors, dtype=float)
    minimum = np.asarray(minimum_block_eigenvalues, dtype=float)
    maximum = np.asarray(maximum_block_eigenvalues, dtype=float)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if local.ndim != 3 or local.shape[2] != 3:
        raise ValueError("local_factors must have shape (time, candidates, 3)")
    time_count, candidate_count, _ = local.shape
    expected_transport = (max(0, time_count - 1), candidate_count, candidate_count, 2)
    if transport.shape != expected_transport:
        raise ValueError(f"transport_factors must have shape {expected_transport}")
    if time_count < 1 or candidate_count != len(candidate_tuple):
        raise ValueError("factor arrays and candidates have incompatible shapes")
    if node_count < 2 or not 1 <= subset_size < node_count:
        raise ValueError("require 1 <= subset_size < node_count")
    if any(
        len(candidate) != subset_size
        or len(set(candidate)) != subset_size
        or min(candidate) < 0
        or max(candidate) >= node_count
        for candidate in candidate_tuple
    ):
        raise ValueError("candidates must contain distinct valid nodes of subset_size")
    spectral_shape = (time_count, candidate_count)
    if not (
        covariance_errors.shape == minimum.shape == maximum.shape == spectral_shape
    ):
        raise ValueError("spectral arrays must have shape (time, candidates)")
    if (
        np.any(~np.isfinite(local))
        or np.any(~np.isfinite(transport))
        or np.any((local < 0.0) | (local > 1.0))
        or np.any((transport < 0.0) | (transport > 1.0))
    ):
        raise ValueError("population factors must be finite and lie in [0, 1]")
    if (
        np.any(~np.isfinite(covariance_errors))
        or np.any(~np.isfinite(minimum))
        or np.any(~np.isfinite(maximum))
        or np.any(covariance_errors < 0.0)
        or np.any(minimum <= 0.0)
        or np.any(maximum < minimum)
    ):
        raise ValueError("require valid covariance errors and spectral envelopes")

    valid_blocks = covariance_errors < minimum
    local_errors = np.ones(spectral_shape, dtype=float)
    independence_errors = np.ones(spectral_shape, dtype=float)
    persistence_errors = np.ones(spectral_shape, dtype=float)
    for time in range(time_count):
        for current in range(candidate_count):
            if not valid_blocks[time, current]:
                continue
            eta = float(covariance_errors[time, current])
            lower = float(minimum[time, current])
            upper = float(maximum[time, current])
            logdet_factor = -np.log1p(-eta / lower) / np.log(2.0)
            integration_error = min(1.0, np.log(2.0) * 4.0 * logdet_factor)
            leakage_error = (node_count + 2 * subset_size) * logdet_factor / subset_size
            independence_error = min(1.0, np.log(2.0) * leakage_error)
            persistence_error = canonical_persistence_covariance_error_bound(
                minimum_eigenvalue=lower,
                maximum_eigenvalue=upper,
                covariance_spectral_error=eta,
            )
            independence_errors[time, current] = independence_error
            persistence_errors[time, current] = persistence_error
            local_errors[time, current] = product_root_error_bound(
                local[time, current],
                (integration_error, independence_error, persistence_error),
            )

    transport_errors = np.ones(expected_transport[:-1], dtype=float)
    for time in range(time_count - 1):
        for previous in range(candidate_count):
            for current in range(candidate_count):
                transport_errors[time, previous, current] = product_root_error_bound(
                    transport[time, previous, current],
                    (
                        independence_errors[time, current],
                        persistence_errors[time, current],
                    ),
                )

    local_scores = np.prod(local, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport, axis=3))
    near_competitors = screen_near_competitors(
        local_scores,
        transport_scores,
        candidate_tuple,
        local_errors,
        transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    population = certify_worldtube(
        local_scores,
        candidate_tuple,
        transport_scores=transport_scores,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    planted = population.result.candidate_indices
    planted_error = float(
        sum(local_errors[time, current] for time, current in enumerate(planted))
        + abs(transport_weight)
        * sum(
            transport_errors[time, planted[time], planted[time + 1]]
            for time in range(time_count - 1)
        )
    )
    planted_lower = population.result.total_action - planted_error
    direction = 0.0 if transport_weight == 0.0 else np.sign(transport_weight)
    upper_result = certify_worldtube(
        local_scores + local_errors,
        candidate_tuple,
        transport_scores=transport_scores + direction * transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    if upper_result.result.candidate_indices == planted:
        competitor_upper = upper_result.runner_up_action
        adversarial_competitor = upper_result.runner_up_indices
    else:
        competitor_upper = upper_result.result.total_action
        adversarial_competitor = upper_result.result.candidate_indices
    slack = float(planted_lower - competitor_upper)
    all_valid = bool(np.all(valid_blocks))
    return CovarianceRadiusPathRecoveryBound(
        population_path=planted,
        adversarial_competitor=adversarial_competitor,
        population_action_margin=population.action_margin,
        planted_lower_action=float(planted_lower),
        competitor_upper_action=float(competitor_upper),
        recovery_slack=slack,
        covariance_spectral_errors=covariance_errors.copy(),
        local_score_errors=local_errors,
        transport_score_errors=transport_errors,
        viable_state_count=near_competitors.viable_state_count,
        viable_edge_count=near_competitors.viable_edge_count,
        all_blocks_valid=all_valid,
        guarantees_population_path=all_valid and slack > 0.0,
    )


def moving_partition_localized_recovery_bound(
    envelope: MovingBlockCovarianceErrorEnvelope,
    future_candidate_blocks: Sequence[Sequence[Sequence[int]]],
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    node_count: int,
    subset_size: int,
    *,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> CovarianceRadiusPathRecoveryBound:
    """Certify path recovery using a moving block covariance envelope."""
    local = np.asarray(local_factors, dtype=float)
    if local.ndim != 3:
        raise ValueError("local_factors must have three dimensions")
    time_count, candidate_count, _ = local.shape
    selections = tuple(
        tuple(tuple(blocks) for blocks in time_selections)
        for time_selections in future_candidate_blocks
    )
    if envelope.time_count != time_count:
        raise ValueError("envelope and factor arrays must have the same time_count")
    if len(selections) != time_count or any(
        len(time_selections) != candidate_count for time_selections in selections
    ):
        raise ValueError(
            "future_candidate_blocks must have shape (time, candidates, blocks)"
        )

    covariance_errors = np.empty((time_count, candidate_count), dtype=float)
    for time in range(time_count):
        present_blocks = tuple(range(envelope.block_counts[time]))
        for current in range(candidate_count):
            covariance_errors[time, current] = (
                moving_block_joint_covariance_error_bound(
                    envelope,
                    time,
                    present_blocks,
                    selections[time][current],
                )
            )
    return covariance_radius_path_recovery_bound(
        local,
        transport_factors,
        candidates,
        node_count,
        subset_size,
        covariance_spectral_errors=covariance_errors,
        minimum_block_eigenvalues=minimum_block_eigenvalues,
        maximum_block_eigenvalues=maximum_block_eigenvalues,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )


def localized_gaussian_path_recovery_bound(
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    confidence: float = 0.95,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> LocalizedGaussianPathRecoveryBound:
    """Certify a path with candidate-local spectra and factor-aware errors.

    ``local_factors[t, j]`` contains integration strength, independence, and
    persistence. ``transport_factors[t, i, j]`` contains independence and
    persistence. Spectral envelopes correspond to the principal covariance of
    all present nodes together with the future nodes in candidate ``j``.
    """
    local = np.asarray(local_factors, dtype=float)
    transport = np.asarray(transport_factors, dtype=float)
    minimum = np.asarray(minimum_block_eigenvalues, dtype=float)
    maximum = np.asarray(maximum_block_eigenvalues, dtype=float)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if local.ndim != 3 or local.shape[2] != 3:
        raise ValueError("local_factors must have shape (time, candidates, 3)")
    time_count, candidate_count, _ = local.shape
    if time_count < 1 or candidate_count < 1:
        raise ValueError("at least one time and candidate are required")
    expected_transport = (max(0, time_count - 1), candidate_count, candidate_count, 2)
    if transport.shape != expected_transport:
        raise ValueError(f"transport_factors must have shape {expected_transport}")
    if len(candidate_tuple) != candidate_count:
        raise ValueError("candidates and factor arrays have incompatible shapes")
    if node_count < 2 or not 1 <= subset_size < node_count:
        raise ValueError("require 1 <= subset_size < node_count")
    if any(
        len(candidate) != subset_size
        or len(set(candidate)) != subset_size
        or min(candidate) < 0
        or max(candidate) >= node_count
        for candidate in candidate_tuple
    ):
        raise ValueError("candidates must contain distinct valid nodes of subset_size")
    if minimum.shape != (time_count, candidate_count) or maximum.shape != minimum.shape:
        raise ValueError("spectral envelopes must have shape (time, candidates)")
    if np.any(~np.isfinite(local)) or np.any(~np.isfinite(transport)):
        raise ValueError("all population score factors must be finite")
    if np.any((local < 0.0) | (local > 1.0)) or np.any(
        (transport < 0.0) | (transport > 1.0)
    ):
        raise ValueError("all population score factors must lie in [0, 1]")
    if sample_count < 2 or not 0.0 < confidence < 1.0:
        raise ValueError("require sample_count >= 2 and confidence in (0, 1)")
    if (
        np.any(~np.isfinite(minimum))
        or np.any(~np.isfinite(maximum))
        or np.any(minimum <= 0.0)
        or np.any(maximum < minimum)
    ):
        raise ValueError("require valid positive block-covariance eigenvalue bounds")

    block_count = time_count * candidate_count
    block_dimension = node_count + subset_size
    deviation = (
        np.sqrt(block_dimension)
        + np.sqrt(2.0 * np.log(2.0 * block_count / (1.0 - confidence)))
    ) / np.sqrt(sample_count - 1)
    covariance_errors = maximum * (2.0 * deviation + deviation**2)
    deterministic = covariance_radius_path_recovery_bound(
        local,
        transport,
        candidate_tuple,
        node_count,
        subset_size,
        covariance_spectral_errors=covariance_errors,
        minimum_block_eigenvalues=minimum,
        maximum_block_eigenvalues=maximum,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return LocalizedGaussianPathRecoveryBound(
        sample_count=sample_count,
        confidence=confidence,
        population_path=deterministic.population_path,
        adversarial_competitor=deterministic.adversarial_competitor,
        population_action_margin=deterministic.population_action_margin,
        planted_lower_action=deterministic.planted_lower_action,
        competitor_upper_action=deterministic.competitor_upper_action,
        recovery_slack=deterministic.recovery_slack,
        maximum_covariance_spectral_error=float(np.max(covariance_errors)),
        maximum_local_score_error=float(np.max(deterministic.local_score_errors)),
        maximum_transport_score_error=float(
            np.max(deterministic.transport_score_errors, initial=0.0)
        ),
        viable_state_count=deterministic.viable_state_count,
        viable_edge_count=deterministic.viable_edge_count,
        all_blocks_valid=deterministic.all_blocks_valid,
        guarantees_population_path=deterministic.guarantees_population_path,
    )


def minimum_localized_gaussian_sample_size(
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    node_count: int,
    subset_size: int,
    *,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    confidence: float = 0.95,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
    maximum_sample_count: int = 10**15,
) -> int | None:
    """Find the first sample count certified by the localized path bound."""
    if maximum_sample_count < 2:
        raise ValueError("maximum_sample_count must be at least two")

    def certified(sample_count: int) -> bool:
        return localized_gaussian_path_recovery_bound(
            local_factors,
            transport_factors,
            candidates,
            sample_count,
            node_count,
            subset_size,
            minimum_block_eigenvalues=minimum_block_eigenvalues,
            maximum_block_eigenvalues=maximum_block_eigenvalues,
            confidence=confidence,
            transport_weight=transport_weight,
            continuity_weight=continuity_weight,
        ).guarantees_population_path

    lower = 2
    upper = 2
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


def linear_gaussian_localized_recovery_bound(
    transitions: Sequence[ArrayLike],
    noise_covariances: Sequence[ArrayLike],
    initial_covariance: ArrayLike,
    candidates: Sequence[Sequence[int]],
    sample_count: int,
    *,
    confidence: float = 0.95,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> LocalizedGaussianPathRecoveryBound:
    """Construct the localized certificate directly from linear dynamics.

    There is one transition per candidate time. The final transition supplies
    the future state used by the final local score; transitions before it also
    supply transport between successive candidate times.
    """
    transition_tuple = tuple(transitions)
    noise_tuple = tuple(noise_covariances)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if not transition_tuple or len(transition_tuple) != len(noise_tuple):
        raise ValueError("require equal nonzero transition and noise sequences")
    if not candidate_tuple:
        raise ValueError("at least one candidate is required")
    subset_size = len(candidate_tuple[0])
    if subset_size < 1 or any(len(candidate) != subset_size for candidate in candidate_tuple):
        raise ValueError("all candidates must have the same nonzero size")

    time_count = len(transition_tuple)
    candidate_count = len(candidate_tuple)
    initial = np.asarray(initial_covariance, dtype=float)
    if initial.ndim != 2 or initial.shape[0] != initial.shape[1]:
        raise ValueError("initial_covariance must be square")
    node_count = initial.shape[0]
    covariances = propagate_covariances(
        transition_tuple[:-1], noise_tuple[:-1], initial
    )
    local_factors = np.empty((time_count, candidate_count, 3), dtype=float)
    transport_factors = np.empty(
        (max(0, time_count - 1), candidate_count, candidate_count, 2), dtype=float
    )
    minimum = np.empty((time_count, candidate_count), dtype=float)
    maximum = np.empty_like(minimum)

    for time, (transition, noise) in enumerate(
        zip(transition_tuple, noise_tuple, strict=True)
    ):
        joint = adjacent_joint_covariance(covariances[time], transition, noise)
        for current, candidate in enumerate(candidate_tuple):
            metrics = observer_metrics_from_covariances(
                covariances[time], joint, candidate
            )
            local_factors[time, current] = (
                metrics.integration_strength,
                metrics.independence,
                metrics.persistence,
            )
            block_indices = tuple(range(node_count)) + tuple(
                node_count + node for node in candidate
            )
            eigenvalues = np.linalg.eigvalsh(
                joint[np.ix_(block_indices, block_indices)]
            )
            minimum[time, current] = eigenvalues[0]
            maximum[time, current] = eigenvalues[-1]
        if time < time_count - 1:
            for previous, source in enumerate(candidate_tuple):
                for current, target in enumerate(candidate_tuple):
                    metrics = transport_metrics(
                        covariances[time], transition, noise, source, target
                    )
                    transport_factors[time, previous, current] = (
                        metrics.independence,
                        metrics.persistence,
                    )

    return localized_gaussian_path_recovery_bound(
        local_factors,
        transport_factors,
        candidate_tuple,
        sample_count,
        node_count,
        subset_size,
        minimum_block_eigenvalues=minimum,
        maximum_block_eigenvalues=maximum,
        confidence=confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )


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
