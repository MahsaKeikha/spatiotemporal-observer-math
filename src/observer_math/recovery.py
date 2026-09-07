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
class ClassCompressedPathRecoveryBound:
    """Robust path certificate evaluated on candidate equivalence classes."""

    time_count: int
    class_count: int
    represented_state_count: int
    implicit_path_count: int
    planted_class_path: tuple[int, ...]
    adversarial_class_path: tuple[int, ...] | None
    population_planted_action: float
    planted_action_lower: float
    competitor_action_upper: float
    recovery_slack: float
    local_score_errors: np.ndarray
    transport_score_errors: np.ndarray
    all_blocks_valid: bool
    guarantees_population_path: bool


@dataclass(frozen=True)
class IntervalClassPathRecoveryBound:
    """Class-compressed certificate with heterogeneous factor intervals."""

    time_count: int
    class_count: int
    represented_state_count: int
    implicit_path_count: int
    planted_class_path: tuple[int, ...]
    adversarial_class_path: tuple[int, ...] | None
    planted_action_lower: float
    competitor_action_upper: float
    recovery_slack: float
    local_factor_error_bounds: np.ndarray
    transport_factor_error_bounds: np.ndarray
    local_score_lower_bounds: np.ndarray
    local_score_upper_bounds: np.ndarray
    transport_score_lower_bounds: np.ndarray
    transport_score_upper_bounds: np.ndarray
    all_blocks_valid: bool
    guarantees_population_path: bool


@dataclass(frozen=True)
class ResidualClassPathRecoveryBound:
    """Interval certificate derived from representative class residuals."""

    recovery: IntervalClassPathRecoveryBound
    local_factor_lower_bounds: np.ndarray
    local_factor_upper_bounds: np.ndarray
    transport_factor_lower_bounds: np.ndarray
    transport_factor_upper_bounds: np.ndarray
    local_heterogeneity_factor_errors: np.ndarray
    transport_heterogeneity_factor_errors: np.ndarray
    minimum_member_block_eigenvalues: np.ndarray
    maximum_member_block_eigenvalues: np.ndarray
    minimum_member_transport_eigenvalues: np.ndarray
    maximum_member_transport_eigenvalues: np.ndarray


@dataclass(frozen=True)
class StructuredResidualClassPathRecoveryBound:
    """Class recovery with residual radii derived from a block envelope."""

    recovery: ResidualClassPathRecoveryBound
    local_covariance_residual_bounds: np.ndarray
    transport_covariance_residual_bounds: np.ndarray


@dataclass(frozen=True)
class ScreenedStructuralClassPathRecoveryBound:
    """Population certificate using screened present environments."""

    recovery: IntervalClassPathRecoveryBound
    local_covariance_residual_bounds: np.ndarray
    transport_covariance_residual_bounds: np.ndarray
    local_factor_lower_bounds: np.ndarray
    local_factor_upper_bounds: np.ndarray
    transport_factor_lower_bounds: np.ndarray
    transport_factor_upper_bounds: np.ndarray
    local_heterogeneity_factor_errors: np.ndarray
    transport_heterogeneity_factor_errors: np.ndarray


@dataclass(frozen=True)
class SampleSplitScreenedRecoveryBound:
    """Confidence accounting for independent screening and certification."""

    screening_sample_count: int
    certification_sample_count: int
    screening_confidence: float
    certification_confidence: float
    overall_confidence: float
    retained_block_count: int
    block_dimension: int
    covariance_spectral_error: float
    maximum_admissible_covariance_error: float
    independent_splits: bool
    certification_radius_valid: bool
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


def _maximum_mismatched_class_path(
    local_upper: np.ndarray,
    edge_upper: np.ndarray,
    multiplicities: np.ndarray,
    planted: tuple[int, ...],
    feasible: np.ndarray,
) -> tuple[float, tuple[int, ...] | None]:
    """Maximize an upper action over class paths differing from planted."""
    time_count, class_count = local_upper.shape
    values = np.full((class_count, 2), -np.inf)
    paths: list[list[tuple[int, ...] | None]] = [
        [None, None] for _ in range(class_count)
    ]
    for current in range(class_count):
        if multiplicities[0, current] == 0:
            continue
        mismatch = int(current != planted[0])
        values[current, mismatch] = local_upper[0, current]
        paths[current][mismatch] = (current,)
    for time in range(1, time_count):
        next_values = np.full((class_count, 2), -np.inf)
        next_paths: list[list[tuple[int, ...] | None]] = [
            [None, None] for _ in range(class_count)
        ]
        for previous in range(class_count):
            for was_mismatch in range(2):
                if not np.isfinite(values[previous, was_mismatch]):
                    continue
                for current in range(class_count):
                    if multiplicities[time, current] == 0 or not feasible[
                        time - 1, previous, current
                    ]:
                        continue
                    mismatch = int(was_mismatch or current != planted[time])
                    candidate_value = (
                        values[previous, was_mismatch]
                        + edge_upper[time - 1, previous, current]
                        + local_upper[time, current]
                    )
                    if candidate_value > next_values[current, mismatch]:
                        next_values[current, mismatch] = candidate_value
                        previous_path = paths[previous][was_mismatch]
                        if previous_path is None:
                            raise RuntimeError("class dynamic program lost its prefix")
                        next_paths[current][mismatch] = (*previous_path, current)
        values = next_values
        paths = next_paths

    competitor_class = int(np.argmax(values[:, 1]))
    competitor_upper = float(values[competitor_class, 1])
    adversarial = paths[competitor_class][1] if np.isfinite(competitor_upper) else None
    return competitor_upper, adversarial


def _local_factor_errors_from_covariance(
    covariance_errors: np.ndarray,
    minimum: np.ndarray,
    maximum: np.ndarray,
    node_count: int,
    subset_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return integration, insulation, and persistence error arrays."""
    valid = covariance_errors < minimum
    errors = np.ones((*covariance_errors.shape, 3), dtype=float)
    for index in np.ndindex(covariance_errors.shape):
        if not valid[index]:
            continue
        eta = float(covariance_errors[index])
        lower = float(minimum[index])
        upper = float(maximum[index])
        logdet_factor = -np.log1p(-eta / lower) / np.log(2.0)
        errors[index][0] = min(1.0, 4.0 * np.log(2.0) * logdet_factor)
        errors[index][1] = min(
            1.0,
            np.log(2.0)
            * (node_count + 2 * subset_size)
            / subset_size
            * logdet_factor,
        )
        errors[index][2] = canonical_persistence_covariance_error_bound(
            minimum_eigenvalue=lower,
            maximum_eigenvalue=upper,
            covariance_spectral_error=eta,
        )
    return errors, valid


def _transport_factor_errors_from_covariance(
    covariance_errors: np.ndarray,
    minimum: np.ndarray,
    maximum: np.ndarray,
    node_count: int,
    subset_size: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return insulation and persistence error arrays for class edges."""
    valid = covariance_errors < minimum
    errors = np.ones((*covariance_errors.shape, 2), dtype=float)
    for index in np.ndindex(covariance_errors.shape):
        if not valid[index]:
            continue
        eta = float(covariance_errors[index])
        lower = float(minimum[index])
        upper = float(maximum[index])
        logdet_factor = -np.log1p(-eta / lower) / np.log(2.0)
        errors[index][0] = min(
            1.0,
            np.log(2.0)
            * (node_count + 2 * subset_size)
            / subset_size
            * logdet_factor,
        )
        errors[index][1] = canonical_persistence_covariance_error_bound(
            minimum_eigenvalue=lower,
            maximum_eigenvalue=upper,
            covariance_spectral_error=eta,
        )
    return errors, valid


def class_compressed_covariance_path_recovery_bound(
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
    class_multiplicities: ArrayLike,
    planted_class_indices: Sequence[int],
    feasible_class_edges: ArrayLike,
    continuity_distance_lower_bounds: ArrayLike,
    planted_continuity_distances: ArrayLike,
    node_count: int,
    subset_size: int,
    *,
    covariance_spectral_errors: ArrayLike,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    transport_covariance_spectral_errors: ArrayLike,
    minimum_transport_block_eigenvalues: ArrayLike,
    maximum_transport_block_eigenvalues: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> ClassCompressedPathRecoveryBound:
    """Certify an implicit candidate family through exact symmetry classes.

    Factor values must be constant within each declared class or class pair.
    State and edge covariance arrays must separately bound every represented
    member. Each planted class must contain exactly one candidate, which makes
    the all-planted class path unique.
    """
    local = np.asarray(local_factors, dtype=float)
    transport = np.asarray(transport_factors, dtype=float)
    raw_multiplicities = np.asarray(class_multiplicities)
    feasible = np.asarray(feasible_class_edges)
    continuity_lower = np.asarray(continuity_distance_lower_bounds, dtype=float)
    planted_distances = np.asarray(planted_continuity_distances, dtype=float)
    covariance_errors = np.asarray(covariance_spectral_errors, dtype=float)
    minimum = np.asarray(minimum_block_eigenvalues, dtype=float)
    maximum = np.asarray(maximum_block_eigenvalues, dtype=float)
    transport_covariance_errors = np.asarray(
        transport_covariance_spectral_errors, dtype=float
    )
    transport_minimum = np.asarray(minimum_transport_block_eigenvalues, dtype=float)
    transport_maximum = np.asarray(maximum_transport_block_eigenvalues, dtype=float)
    planted = tuple(int(index) for index in planted_class_indices)

    if local.ndim != 3 or local.shape[2] != 3:
        raise ValueError("local_factors must have shape (time, classes, 3)")
    time_count, class_count, _ = local.shape
    edge_shape = (max(0, time_count - 1), class_count, class_count)
    if transport.shape != (*edge_shape, 2):
        raise ValueError(f"transport_factors must have shape {(*edge_shape, 2)}")
    if time_count < 1 or class_count < 1 or len(planted) != time_count:
        raise ValueError("require one planted class for every nonempty time layer")
    if node_count < 2 or not 1 <= subset_size < node_count:
        raise ValueError("require 1 <= subset_size < node_count")
    if not np.isfinite([transport_weight, continuity_weight]).all() or (
        continuity_weight < 0.0
    ):
        raise ValueError("weights must be finite and continuity nonnegative")

    state_shape = (time_count, class_count)
    if raw_multiplicities.shape != state_shape or any(
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        for value in raw_multiplicities.flat
    ):
        raise TypeError("class_multiplicities must be an integer (time, classes) array")
    multiplicities = raw_multiplicities.astype(object)
    if np.any(multiplicities < 0) or np.any(np.sum(multiplicities, axis=1) == 0):
        raise ValueError("each layer must contain nonnegative, nonempty classes")
    if any(not 0 <= index < class_count for index in planted):
        raise ValueError("planted class indices lie outside the class arrays")
    if any(multiplicities[time, index] != 1 for time, index in enumerate(planted)):
        raise ValueError("each planted class must have multiplicity one")
    if feasible.shape != edge_shape or feasible.dtype != np.bool_:
        raise TypeError("feasible_class_edges must be a boolean edge array")
    if continuity_lower.shape != edge_shape or planted_distances.shape != (
        max(0, time_count - 1),
    ):
        raise ValueError("continuity arrays have incompatible shapes")
    if (
        np.any(~np.isfinite(continuity_lower))
        or np.any((continuity_lower < 0.0) | (continuity_lower > 1.0))
        or np.any(~np.isfinite(planted_distances))
        or np.any((planted_distances < 0.0) | (planted_distances > 1.0))
    ):
        raise ValueError("continuity distances must be finite and lie in [0, 1]")
    if any(
        not feasible[time, planted[time], planted[time + 1]]
        for time in range(time_count - 1)
    ):
        raise ValueError("every planted class edge must be feasible")
    if not (
        covariance_errors.shape == minimum.shape == maximum.shape == state_shape
    ):
        raise ValueError("spectral arrays must have shape (time, classes)")
    if not (
        transport_covariance_errors.shape
        == transport_minimum.shape
        == transport_maximum.shape
        == edge_shape
    ):
        raise ValueError(
            "transport spectral arrays must have shape (time - 1, classes, classes)"
        )
    if (
        np.any(~np.isfinite(local))
        or np.any(~np.isfinite(transport))
        or np.any((local < 0.0) | (local > 1.0))
        or np.any((transport < 0.0) | (transport > 1.0))
    ):
        raise ValueError("class factors must be finite and lie in [0, 1]")
    if (
        np.any(~np.isfinite(covariance_errors))
        or np.any(~np.isfinite(minimum))
        or np.any(~np.isfinite(maximum))
        or np.any(covariance_errors < 0.0)
        or np.any(minimum <= 0.0)
        or np.any(maximum < minimum)
        or np.any(~np.isfinite(transport_covariance_errors))
        or np.any(~np.isfinite(transport_minimum))
        or np.any(~np.isfinite(transport_maximum))
        or np.any(transport_covariance_errors < 0.0)
        or np.any(transport_minimum <= 0.0)
        or np.any(transport_maximum < transport_minimum)
    ):
        raise ValueError("require valid covariance errors and spectral envelopes")

    local_factor_errors, valid_blocks = _local_factor_errors_from_covariance(
        covariance_errors,
        minimum,
        maximum,
        node_count,
        subset_size,
    )
    local_errors = np.ones(state_shape, dtype=float)
    for time in range(time_count):
        for current in range(class_count):
            local_errors[time, current] = product_root_error_bound(
                local[time, current],
                local_factor_errors[time, current],
            )

    transport_factor_errors, valid_transport_blocks = (
        _transport_factor_errors_from_covariance(
            transport_covariance_errors,
            transport_minimum,
            transport_maximum,
            node_count,
            subset_size,
        )
    )
    transport_errors = np.ones(edge_shape, dtype=float)
    for time in range(time_count - 1):
        for previous in range(class_count):
            for current in range(class_count):
                transport_errors[time, previous, current] = product_root_error_bound(
                    transport[time, previous, current],
                    transport_factor_errors[time, previous, current],
                )

    local_scores = np.prod(local, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport, axis=3))
    planted_nominal = float(
        sum(local_scores[time, current] for time, current in enumerate(planted))
        + sum(
            transport_weight
            * transport_scores[time, planted[time], planted[time + 1]]
            - continuity_weight * planted_distances[time]
            for time in range(time_count - 1)
        )
    )
    planted_error = float(
        sum(local_errors[time, current] for time, current in enumerate(planted))
        + abs(transport_weight)
        * sum(
            transport_errors[time, planted[time], planted[time + 1]]
            for time in range(time_count - 1)
        )
    )
    planted_lower = planted_nominal - planted_error
    local_upper = local_scores + local_errors
    edge_upper = (
        transport_weight * transport_scores
        + abs(transport_weight) * transport_errors
        - continuity_weight * continuity_lower
    )
    competitor_upper, adversarial = _maximum_mismatched_class_path(
        local_upper,
        edge_upper,
        multiplicities,
        planted,
        feasible,
    )
    slack = float(planted_lower - competitor_upper)
    active = multiplicities > 0
    active_edges = (
        feasible
        & (multiplicities[:-1, :, None] > 0)
        & (multiplicities[1:, None, :] > 0)
    )
    all_valid = bool(
        np.all(valid_blocks[active])
        and np.all(valid_transport_blocks[active_edges])
    )
    implicit_path_count = 1
    for layer_count in np.sum(multiplicities, axis=1):
        implicit_path_count *= int(layer_count)
    return ClassCompressedPathRecoveryBound(
        time_count=time_count,
        class_count=class_count,
        represented_state_count=int(np.sum(multiplicities)),
        implicit_path_count=implicit_path_count,
        planted_class_path=planted,
        adversarial_class_path=adversarial,
        population_planted_action=planted_nominal,
        planted_action_lower=float(planted_lower),
        competitor_action_upper=competitor_upper,
        recovery_slack=slack,
        local_score_errors=local_errors,
        transport_score_errors=transport_errors,
        all_blocks_valid=all_valid,
        guarantees_population_path=all_valid and slack > 0.0,
    )


def interval_class_covariance_path_recovery_bound(
    local_factor_lower_bounds: ArrayLike,
    local_factor_upper_bounds: ArrayLike,
    transport_factor_lower_bounds: ArrayLike,
    transport_factor_upper_bounds: ArrayLike,
    class_multiplicities: ArrayLike,
    planted_class_indices: Sequence[int],
    feasible_class_edges: ArrayLike,
    continuity_distance_lower_bounds: ArrayLike,
    planted_continuity_distances: ArrayLike,
    node_count: int,
    subset_size: int,
    *,
    covariance_spectral_errors: ArrayLike,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    transport_covariance_spectral_errors: ArrayLike,
    minimum_transport_block_eigenvalues: ArrayLike,
    maximum_transport_block_eigenvalues: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> IntervalClassPathRecoveryBound:
    """Certify heterogeneous classes using componentwise factor intervals."""
    local_lower = np.asarray(local_factor_lower_bounds, dtype=float)
    local_upper = np.asarray(local_factor_upper_bounds, dtype=float)
    transport_lower = np.asarray(transport_factor_lower_bounds, dtype=float)
    transport_upper = np.asarray(transport_factor_upper_bounds, dtype=float)
    raw_multiplicities = np.asarray(class_multiplicities)
    feasible = np.asarray(feasible_class_edges)
    continuity_lower = np.asarray(continuity_distance_lower_bounds, dtype=float)
    planted_distances = np.asarray(planted_continuity_distances, dtype=float)
    covariance_errors = np.asarray(covariance_spectral_errors, dtype=float)
    minimum = np.asarray(minimum_block_eigenvalues, dtype=float)
    maximum = np.asarray(maximum_block_eigenvalues, dtype=float)
    transport_covariance_errors = np.asarray(
        transport_covariance_spectral_errors, dtype=float
    )
    transport_minimum = np.asarray(minimum_transport_block_eigenvalues, dtype=float)
    transport_maximum = np.asarray(maximum_transport_block_eigenvalues, dtype=float)
    planted = tuple(int(index) for index in planted_class_indices)

    if local_lower.ndim != 3 or local_lower.shape[2] != 3:
        raise ValueError("local factor bounds must have shape (time, classes, 3)")
    if local_upper.shape != local_lower.shape:
        raise ValueError("local lower and upper factor arrays must have equal shapes")
    time_count, class_count, _ = local_lower.shape
    state_shape = (time_count, class_count)
    edge_shape = (max(0, time_count - 1), class_count, class_count)
    if transport_lower.shape != (*edge_shape, 2) or (
        transport_upper.shape != transport_lower.shape
    ):
        raise ValueError(
            "transport factor bounds must have shape (time - 1, classes, classes, 2)"
        )
    if time_count < 1 or class_count < 1 or len(planted) != time_count:
        raise ValueError("require one planted class for every nonempty time layer")
    if node_count < 2 or not 1 <= subset_size < node_count:
        raise ValueError("require 1 <= subset_size < node_count")
    if not np.isfinite([transport_weight, continuity_weight]).all() or (
        continuity_weight < 0.0
    ):
        raise ValueError("weights must be finite and continuity nonnegative")
    factor_arrays = (local_lower, local_upper, transport_lower, transport_upper)
    if any(np.any(~np.isfinite(array)) for array in factor_arrays) or any(
        np.any((array < 0.0) | (array > 1.0)) for array in factor_arrays
    ):
        raise ValueError("factor bounds must be finite and lie in [0, 1]")
    if np.any(local_lower > local_upper) or np.any(
        transport_lower > transport_upper
    ):
        raise ValueError("factor lower bounds cannot exceed upper bounds")

    if raw_multiplicities.shape != state_shape or any(
        isinstance(value, (bool, np.bool_))
        or not isinstance(value, (int, np.integer))
        for value in raw_multiplicities.flat
    ):
        raise TypeError("class_multiplicities must be an integer (time, classes) array")
    multiplicities = raw_multiplicities.astype(object)
    if np.any(multiplicities < 0) or np.any(np.sum(multiplicities, axis=1) == 0):
        raise ValueError("each layer must contain nonnegative, nonempty classes")
    if any(not 0 <= index < class_count for index in planted):
        raise ValueError("planted class indices lie outside the class arrays")
    if any(multiplicities[time, index] != 1 for time, index in enumerate(planted)):
        raise ValueError("each planted class must have multiplicity one")
    if feasible.shape != edge_shape or feasible.dtype != np.bool_:
        raise TypeError("feasible_class_edges must be a boolean edge array")
    if continuity_lower.shape != edge_shape or planted_distances.shape != (
        max(0, time_count - 1),
    ):
        raise ValueError("continuity arrays have incompatible shapes")
    if (
        np.any(~np.isfinite(continuity_lower))
        or np.any((continuity_lower < 0.0) | (continuity_lower > 1.0))
        or np.any(~np.isfinite(planted_distances))
        or np.any((planted_distances < 0.0) | (planted_distances > 1.0))
    ):
        raise ValueError("continuity distances must be finite and lie in [0, 1]")
    if any(
        not feasible[time, planted[time], planted[time + 1]]
        for time in range(time_count - 1)
    ):
        raise ValueError("every planted class edge must be feasible")

    if not (
        covariance_errors.shape == minimum.shape == maximum.shape == state_shape
    ) or not (
        transport_covariance_errors.shape
        == transport_minimum.shape
        == transport_maximum.shape
        == edge_shape
    ):
        raise ValueError("state or transport spectral arrays have incompatible shapes")
    spectral_arrays = (
        covariance_errors,
        minimum,
        maximum,
        transport_covariance_errors,
        transport_minimum,
        transport_maximum,
    )
    if any(np.any(~np.isfinite(array)) for array in spectral_arrays) or (
        np.any(covariance_errors < 0.0)
        or np.any(minimum <= 0.0)
        or np.any(maximum < minimum)
        or np.any(transport_covariance_errors < 0.0)
        or np.any(transport_minimum <= 0.0)
        or np.any(transport_maximum < transport_minimum)
    ):
        raise ValueError("require valid covariance errors and spectral envelopes")

    local_errors, valid_local = _local_factor_errors_from_covariance(
        covariance_errors,
        minimum,
        maximum,
        node_count,
        subset_size,
    )
    transport_errors, valid_transport = _transport_factor_errors_from_covariance(
        transport_covariance_errors,
        transport_minimum,
        transport_maximum,
        node_count,
        subset_size,
    )
    perturbed_local_lower = np.clip(local_lower - local_errors, 0.0, 1.0)
    perturbed_local_upper = np.clip(local_upper + local_errors, 0.0, 1.0)
    local_score_lower = np.prod(perturbed_local_lower, axis=2) ** (1.0 / 3.0)
    local_score_upper = np.prod(perturbed_local_upper, axis=2) ** (1.0 / 3.0)
    perturbed_transport_lower = np.clip(
        transport_lower - transport_errors, 0.0, 1.0
    )
    perturbed_transport_upper = np.clip(
        transport_upper + transport_errors, 0.0, 1.0
    )
    transport_score_lower = np.sqrt(np.prod(perturbed_transport_lower, axis=3))
    transport_score_upper = np.sqrt(np.prod(perturbed_transport_upper, axis=3))

    planted_transport = (
        transport_score_lower if transport_weight >= 0.0 else transport_score_upper
    )
    planted_lower = float(
        sum(
            local_score_lower[time, current]
            for time, current in enumerate(planted)
        )
        + sum(
            transport_weight
            * planted_transport[time, planted[time], planted[time + 1]]
            - continuity_weight * planted_distances[time]
            for time in range(time_count - 1)
        )
    )
    competitor_transport = (
        transport_score_upper if transport_weight >= 0.0 else transport_score_lower
    )
    edge_upper = (
        transport_weight * competitor_transport
        - continuity_weight * continuity_lower
    )
    competitor_upper, adversarial = _maximum_mismatched_class_path(
        local_score_upper,
        edge_upper,
        multiplicities,
        planted,
        feasible,
    )
    slack = float(planted_lower - competitor_upper)
    active = multiplicities > 0
    active_edges = (
        feasible
        & (multiplicities[:-1, :, None] > 0)
        & (multiplicities[1:, None, :] > 0)
    )
    all_valid = bool(
        np.all(valid_local[active]) and np.all(valid_transport[active_edges])
    )
    implicit_path_count = 1
    for layer_count in np.sum(multiplicities, axis=1):
        implicit_path_count *= int(layer_count)
    return IntervalClassPathRecoveryBound(
        time_count=time_count,
        class_count=class_count,
        represented_state_count=int(np.sum(multiplicities)),
        implicit_path_count=implicit_path_count,
        planted_class_path=planted,
        adversarial_class_path=adversarial,
        planted_action_lower=planted_lower,
        competitor_action_upper=competitor_upper,
        recovery_slack=slack,
        local_factor_error_bounds=local_errors,
        transport_factor_error_bounds=transport_errors,
        local_score_lower_bounds=local_score_lower,
        local_score_upper_bounds=local_score_upper,
        transport_score_lower_bounds=transport_score_lower,
        transport_score_upper_bounds=transport_score_upper,
        all_blocks_valid=all_valid,
        guarantees_population_path=all_valid and slack > 0.0,
    )


def residual_class_covariance_path_recovery_bound(
    representative_local_factors: ArrayLike,
    representative_transport_factors: ArrayLike,
    class_multiplicities: ArrayLike,
    planted_class_indices: Sequence[int],
    feasible_class_edges: ArrayLike,
    continuity_distance_lower_bounds: ArrayLike,
    planted_continuity_distances: ArrayLike,
    node_count: int,
    subset_size: int,
    *,
    local_covariance_residual_bounds: ArrayLike,
    representative_minimum_block_eigenvalues: ArrayLike,
    representative_maximum_block_eigenvalues: ArrayLike,
    transport_covariance_residual_bounds: ArrayLike,
    representative_minimum_transport_eigenvalues: ArrayLike,
    representative_maximum_transport_eigenvalues: ArrayLike,
    covariance_spectral_errors: ArrayLike,
    transport_covariance_spectral_errors: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> ResidualClassPathRecoveryBound:
    """Derive factor boxes from covariance residuals and certify recovery.

    Each representative covariance is the center of a classwise spectral-norm
    ball. The resulting factor errors define population factor intervals. A
    second covariance radius then controls perturbation of each class member.
    """
    local = np.asarray(representative_local_factors, dtype=float)
    transport = np.asarray(representative_transport_factors, dtype=float)
    local_residuals = np.asarray(local_covariance_residual_bounds, dtype=float)
    local_minimum = np.asarray(
        representative_minimum_block_eigenvalues, dtype=float
    )
    local_maximum = np.asarray(
        representative_maximum_block_eigenvalues, dtype=float
    )
    transport_residuals = np.asarray(
        transport_covariance_residual_bounds, dtype=float
    )
    transport_minimum = np.asarray(
        representative_minimum_transport_eigenvalues, dtype=float
    )
    transport_maximum = np.asarray(
        representative_maximum_transport_eigenvalues, dtype=float
    )

    if local.ndim != 3 or local.shape[2] != 3:
        raise ValueError("representative local factors must have shape (time, classes, 3)")
    time_count, class_count, _ = local.shape
    state_shape = (time_count, class_count)
    edge_shape = (max(0, time_count - 1), class_count, class_count)
    if transport.shape != (*edge_shape, 2):
        raise ValueError(
            "representative transport factors must have shape "
            "(time - 1, classes, classes, 2)"
        )
    if not (
        local_residuals.shape
        == local_minimum.shape
        == local_maximum.shape
        == state_shape
    ) or not (
        transport_residuals.shape
        == transport_minimum.shape
        == transport_maximum.shape
        == edge_shape
    ):
        raise ValueError("representative residual and spectral arrays have wrong shapes")
    if (
        np.any(~np.isfinite(local))
        or np.any(~np.isfinite(transport))
        or np.any((local < 0.0) | (local > 1.0))
        or np.any((transport < 0.0) | (transport > 1.0))
    ):
        raise ValueError("representative factors must be finite and lie in [0, 1]")
    spectral_arrays = (
        local_residuals,
        local_minimum,
        local_maximum,
        transport_residuals,
        transport_minimum,
        transport_maximum,
    )
    if any(np.any(~np.isfinite(array)) for array in spectral_arrays) or (
        np.any(local_residuals < 0.0)
        or np.any(local_minimum <= 0.0)
        or np.any(local_maximum < local_minimum)
        or np.any(local_residuals >= local_minimum)
        or np.any(transport_residuals < 0.0)
        or np.any(transport_minimum <= 0.0)
        or np.any(transport_maximum < transport_minimum)
        or np.any(transport_residuals >= transport_minimum)
    ):
        raise ValueError(
            "residual radii must be smaller than valid representative eigenvalue floors"
        )

    local_heterogeneity_errors, _ = _local_factor_errors_from_covariance(
        local_residuals,
        local_minimum,
        local_maximum,
        node_count,
        subset_size,
    )
    transport_heterogeneity_errors, _ = _transport_factor_errors_from_covariance(
        transport_residuals,
        transport_minimum,
        transport_maximum,
        node_count,
        subset_size,
    )
    local_lower = np.clip(local - local_heterogeneity_errors, 0.0, 1.0)
    local_upper = np.clip(local + local_heterogeneity_errors, 0.0, 1.0)
    transport_lower = np.clip(
        transport - transport_heterogeneity_errors, 0.0, 1.0
    )
    transport_upper = np.clip(
        transport + transport_heterogeneity_errors, 0.0, 1.0
    )

    member_minimum = local_minimum - local_residuals
    member_maximum = local_maximum + local_residuals
    member_transport_minimum = transport_minimum - transport_residuals
    member_transport_maximum = transport_maximum + transport_residuals
    recovery = interval_class_covariance_path_recovery_bound(
        local_lower,
        local_upper,
        transport_lower,
        transport_upper,
        class_multiplicities,
        planted_class_indices,
        feasible_class_edges,
        continuity_distance_lower_bounds,
        planted_continuity_distances,
        node_count,
        subset_size,
        covariance_spectral_errors=covariance_spectral_errors,
        minimum_block_eigenvalues=member_minimum,
        maximum_block_eigenvalues=member_maximum,
        transport_covariance_spectral_errors=transport_covariance_spectral_errors,
        minimum_transport_block_eigenvalues=member_transport_minimum,
        maximum_transport_block_eigenvalues=member_transport_maximum,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return ResidualClassPathRecoveryBound(
        recovery=recovery,
        local_factor_lower_bounds=local_lower,
        local_factor_upper_bounds=local_upper,
        transport_factor_lower_bounds=transport_lower,
        transport_factor_upper_bounds=transport_upper,
        local_heterogeneity_factor_errors=local_heterogeneity_errors,
        transport_heterogeneity_factor_errors=transport_heterogeneity_errors,
        minimum_member_block_eigenvalues=member_minimum,
        maximum_member_block_eigenvalues=member_maximum,
        minimum_member_transport_eigenvalues=member_transport_minimum,
        maximum_member_transport_eigenvalues=member_transport_maximum,
    )


def structured_residual_class_path_recovery_bound(
    envelope: MovingBlockCovarianceErrorEnvelope,
    future_class_blocks: Sequence[Sequence[Sequence[int]]],
    representative_local_factors: ArrayLike,
    representative_transport_factors: ArrayLike,
    class_multiplicities: ArrayLike,
    planted_class_indices: Sequence[int],
    feasible_class_edges: ArrayLike,
    continuity_distance_lower_bounds: ArrayLike,
    planted_continuity_distances: ArrayLike,
    node_count: int,
    subset_size: int,
    *,
    representative_minimum_block_eigenvalues: ArrayLike,
    representative_maximum_block_eigenvalues: ArrayLike,
    representative_minimum_transport_eigenvalues: ArrayLike,
    representative_maximum_transport_eigenvalues: ArrayLike,
    covariance_spectral_errors: ArrayLike,
    transport_covariance_spectral_errors: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> StructuredResidualClassPathRecoveryBound:
    """Derive class residuals from a moving block comparison envelope."""
    local = np.asarray(representative_local_factors, dtype=float)
    if local.ndim != 3 or local.shape[2] != 3:
        raise ValueError("representative local factors must have shape (time, classes, 3)")
    time_count, class_count, _ = local.shape
    if envelope.time_count != time_count:
        raise ValueError("envelope and representative factors must have equal time_count")
    selections = tuple(
        tuple(tuple(blocks) for blocks in time_selections)
        for time_selections in future_class_blocks
    )
    if len(selections) != time_count or any(
        len(time_selections) != class_count for time_selections in selections
    ):
        raise ValueError("future_class_blocks must have shape (time, classes, blocks)")

    local_residuals = np.empty((time_count, class_count), dtype=float)
    for time in range(time_count):
        present_blocks = tuple(range(envelope.block_counts[time]))
        for current in range(class_count):
            local_residuals[time, current] = (
                moving_block_joint_covariance_error_bound(
                    envelope,
                    time,
                    present_blocks,
                    selections[time][current],
                )
            )

    transport_residuals = np.empty(
        (max(0, time_count - 1), class_count, class_count),
        dtype=float,
    )
    for time in range(time_count - 1):
        present_blocks = tuple(range(envelope.block_counts[time]))
        for current in range(class_count):
            radius = moving_block_joint_covariance_error_bound(
                envelope,
                time,
                present_blocks,
                selections[time][current],
            )
            transport_residuals[time, :, current] = radius

    recovery = residual_class_covariance_path_recovery_bound(
        local,
        representative_transport_factors,
        class_multiplicities,
        planted_class_indices,
        feasible_class_edges,
        continuity_distance_lower_bounds,
        planted_continuity_distances,
        node_count,
        subset_size,
        local_covariance_residual_bounds=local_residuals,
        representative_minimum_block_eigenvalues=(
            representative_minimum_block_eigenvalues
        ),
        representative_maximum_block_eigenvalues=(
            representative_maximum_block_eigenvalues
        ),
        transport_covariance_residual_bounds=transport_residuals,
        representative_minimum_transport_eigenvalues=(
            representative_minimum_transport_eigenvalues
        ),
        representative_maximum_transport_eigenvalues=(
            representative_maximum_transport_eigenvalues
        ),
        covariance_spectral_errors=covariance_spectral_errors,
        transport_covariance_spectral_errors=transport_covariance_spectral_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return StructuredResidualClassPathRecoveryBound(
        recovery=recovery,
        local_covariance_residual_bounds=local_residuals,
        transport_covariance_residual_bounds=transport_residuals,
    )


def screened_structural_class_path_recovery_bound(
    envelope: MovingBlockCovarianceErrorEnvelope,
    local_present_class_blocks: Sequence[Sequence[Sequence[int]]],
    local_future_class_blocks: Sequence[Sequence[Sequence[int]]],
    transport_present_class_blocks: Sequence[
        Sequence[Sequence[Sequence[int]]]
    ],
    transport_future_class_blocks: Sequence[
        Sequence[Sequence[Sequence[int]]]
    ],
    screened_representative_local_factors: ArrayLike,
    screened_representative_transport_factors: ArrayLike,
    local_omitted_leakage_bits_per_node: ArrayLike,
    transport_omitted_leakage_bits_per_node: ArrayLike,
    class_multiplicities: ArrayLike,
    planted_class_indices: Sequence[int],
    feasible_class_edges: ArrayLike,
    continuity_distance_lower_bounds: ArrayLike,
    planted_continuity_distances: ArrayLike,
    node_count: int,
    subset_size: int,
    *,
    representative_minimum_block_eigenvalues: ArrayLike,
    representative_maximum_block_eigenvalues: ArrayLike,
    representative_minimum_transport_eigenvalues: ArrayLike,
    representative_maximum_transport_eigenvalues: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> ScreenedStructuralClassPathRecoveryBound:
    """Certify population recovery with bounded omitted environmental leakage."""
    local = np.asarray(screened_representative_local_factors, dtype=float)
    transport = np.asarray(screened_representative_transport_factors, dtype=float)
    if local.ndim != 3 or local.shape[2] != 3:
        raise ValueError("screened local factors must have shape (time, classes, 3)")
    time_count, class_count, _ = local.shape
    state_shape = (time_count, class_count)
    edge_shape = (max(0, time_count - 1), class_count, class_count)
    if transport.shape != (*edge_shape, 2):
        raise ValueError(
            "screened transport factors must have shape "
            "(time - 1, classes, classes, 2)"
        )
    if envelope.time_count < time_count:
        raise ValueError("envelope does not cover every factor time")

    local_present = tuple(
        tuple(tuple(blocks) for blocks in layer)
        for layer in local_present_class_blocks
    )
    local_future = tuple(
        tuple(tuple(blocks) for blocks in layer)
        for layer in local_future_class_blocks
    )
    if len(local_present) != time_count or len(local_future) != time_count or any(
        len(local_present[time]) != class_count
        or len(local_future[time]) != class_count
        for time in range(time_count)
    ):
        raise ValueError("local block selections must have shape (time, classes, blocks)")

    transport_present = tuple(
        tuple(tuple(tuple(blocks) for blocks in row) for row in layer)
        for layer in transport_present_class_blocks
    )
    transport_future = tuple(
        tuple(tuple(tuple(blocks) for blocks in row) for row in layer)
        for layer in transport_future_class_blocks
    )
    if len(transport_present) != edge_shape[0] or len(transport_future) != edge_shape[
        0
    ] or any(
        len(transport_present[time]) != class_count
        or len(transport_future[time]) != class_count
        or any(
            len(transport_present[time][previous]) != class_count
            or len(transport_future[time][previous]) != class_count
            for previous in range(class_count)
        )
        for time in range(edge_shape[0])
    ):
        raise ValueError(
            "transport block selections must have shape "
            "(time - 1, classes, classes, blocks)"
        )

    local_tail = np.asarray(local_omitted_leakage_bits_per_node, dtype=float)
    transport_tail = np.asarray(
        transport_omitted_leakage_bits_per_node, dtype=float
    )
    if local_tail.shape != state_shape or transport_tail.shape != edge_shape:
        raise ValueError("omitted leakage bounds have incompatible shapes")
    if (
        np.any(~np.isfinite(local_tail))
        or np.any(local_tail < 0.0)
        or np.any(~np.isfinite(transport_tail))
        or np.any(transport_tail < 0.0)
    ):
        raise ValueError("omitted leakage bounds must be finite and nonnegative")

    local_minimum = np.asarray(
        representative_minimum_block_eigenvalues, dtype=float
    )
    local_maximum = np.asarray(
        representative_maximum_block_eigenvalues, dtype=float
    )
    transport_minimum = np.asarray(
        representative_minimum_transport_eigenvalues, dtype=float
    )
    transport_maximum = np.asarray(
        representative_maximum_transport_eigenvalues, dtype=float
    )
    if not (
        local_minimum.shape == local_maximum.shape == state_shape
    ) or not (
        transport_minimum.shape == transport_maximum.shape == edge_shape
    ):
        raise ValueError("representative spectral arrays have incompatible shapes")

    local_residuals = np.empty(state_shape, dtype=float)
    for time in range(time_count):
        for current in range(class_count):
            local_residuals[time, current] = (
                moving_block_joint_covariance_error_bound(
                    envelope,
                    time,
                    local_present[time][current],
                    local_future[time][current],
                )
            )
    transport_residuals = np.empty(edge_shape, dtype=float)
    for time in range(edge_shape[0]):
        for previous in range(class_count):
            for current in range(class_count):
                transport_residuals[time, previous, current] = (
                    moving_block_joint_covariance_error_bound(
                        envelope,
                        time,
                        transport_present[time][previous][current],
                        transport_future[time][previous][current],
                    )
                )

    spectral_arrays = (
        local_minimum,
        local_maximum,
        transport_minimum,
        transport_maximum,
    )
    if any(np.any(~np.isfinite(array)) for array in spectral_arrays) or (
        np.any(local_minimum <= 0.0)
        or np.any(local_maximum < local_minimum)
        or np.any(local_residuals >= local_minimum)
        or np.any(transport_minimum <= 0.0)
        or np.any(transport_maximum < transport_minimum)
        or np.any(transport_residuals >= transport_minimum)
    ):
        raise ValueError("selected residuals must preserve representative eigenvalue floors")

    local_errors, _ = _local_factor_errors_from_covariance(
        local_residuals,
        local_minimum,
        local_maximum,
        node_count,
        subset_size,
    )
    transport_errors, _ = _transport_factor_errors_from_covariance(
        transport_residuals,
        transport_minimum,
        transport_maximum,
        node_count,
        subset_size,
    )
    local_lower = np.clip(local - local_errors, 0.0, 1.0)
    local_upper = np.clip(local + local_errors, 0.0, 1.0)
    transport_lower = np.clip(transport - transport_errors, 0.0, 1.0)
    transport_upper = np.clip(transport + transport_errors, 0.0, 1.0)
    local_lower[:, :, 1] *= np.exp2(-local_tail)
    transport_lower[:, :, :, 0] *= np.exp2(-transport_tail)

    recovery = interval_class_covariance_path_recovery_bound(
        local_lower,
        local_upper,
        transport_lower,
        transport_upper,
        class_multiplicities,
        planted_class_indices,
        feasible_class_edges,
        continuity_distance_lower_bounds,
        planted_continuity_distances,
        node_count,
        subset_size,
        covariance_spectral_errors=np.zeros(state_shape),
        minimum_block_eigenvalues=local_minimum - local_residuals,
        maximum_block_eigenvalues=local_maximum + local_residuals,
        transport_covariance_spectral_errors=np.zeros(edge_shape),
        minimum_transport_block_eigenvalues=(
            transport_minimum - transport_residuals
        ),
        maximum_transport_block_eigenvalues=(
            transport_maximum + transport_residuals
        ),
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return ScreenedStructuralClassPathRecoveryBound(
        recovery=recovery,
        local_covariance_residual_bounds=local_residuals,
        transport_covariance_residual_bounds=transport_residuals,
        local_factor_lower_bounds=local_lower,
        local_factor_upper_bounds=local_upper,
        transport_factor_lower_bounds=transport_lower,
        transport_factor_upper_bounds=transport_upper,
        local_heterogeneity_factor_errors=local_errors,
        transport_heterogeneity_factor_errors=transport_errors,
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


def sample_split_screened_recovery_bound(
    screening_sample_count: int,
    certification_sample_count: int,
    retained_block_count: int,
    block_dimension: int,
    maximum_block_eigenvalue: float,
    maximum_admissible_covariance_error: float,
    *,
    screening_confidence: float = 0.975,
    certification_confidence: float = 0.975,
    independent_splits: bool,
) -> SampleSplitScreenedRecoveryBound:
    """Compose a safe screening event with independent Gaussian certification.

    The screening procedure must retain every path capable of challenging the
    population winner on its advertised event. The deterministic downstream
    certificate must hold whenever every retained covariance block has error
    below ``maximum_admissible_covariance_error``.
    """
    counts = (
        screening_sample_count,
        certification_sample_count,
        retained_block_count,
        block_dimension,
    )
    if any(isinstance(value, bool) or not isinstance(value, (int, np.integer)) for value in counts):
        raise TypeError("sample, block-count, and dimension inputs must be integers")
    if screening_sample_count < 2 or certification_sample_count < 2:
        raise ValueError("both sample splits must contain at least two observations")
    if retained_block_count < 1 or block_dimension < 1:
        raise ValueError("retained_block_count and block_dimension must be positive")
    if not (
        np.isfinite(maximum_block_eigenvalue)
        and maximum_block_eigenvalue > 0.0
        and np.isfinite(maximum_admissible_covariance_error)
        and maximum_admissible_covariance_error > 0.0
    ):
        raise ValueError("eigenvalue and admissible-error bounds must be positive")
    if not 0.0 < screening_confidence < 1.0 or not (
        0.0 < certification_confidence < 1.0
    ):
        raise ValueError("stage confidence levels must lie strictly between zero and one")
    if not isinstance(independent_splits, (bool, np.bool_)):
        raise TypeError("independent_splits must be boolean")

    certification_failure = 1.0 - certification_confidence
    deviation = (
        np.sqrt(block_dimension)
        + np.sqrt(
            2.0
            * np.log(2.0 * retained_block_count / certification_failure)
        )
    ) / np.sqrt(certification_sample_count - 1)
    covariance_error = maximum_block_eigenvalue * (
        2.0 * deviation + deviation**2
    )
    radius_valid = bool(covariance_error < maximum_admissible_covariance_error)
    overall_confidence = float(screening_confidence * certification_confidence)
    return SampleSplitScreenedRecoveryBound(
        screening_sample_count=int(screening_sample_count),
        certification_sample_count=int(certification_sample_count),
        screening_confidence=float(screening_confidence),
        certification_confidence=float(certification_confidence),
        overall_confidence=overall_confidence,
        retained_block_count=int(retained_block_count),
        block_dimension=int(block_dimension),
        covariance_spectral_error=float(covariance_error),
        maximum_admissible_covariance_error=float(
            maximum_admissible_covariance_error
        ),
        independent_splits=bool(independent_splits),
        certification_radius_valid=radius_valid,
        guarantees_population_path=bool(independent_splits) and radius_valid,
    )


def minimum_sample_split_certification_size(
    screening_sample_count: int,
    retained_block_count: int,
    block_dimension: int,
    maximum_block_eigenvalue: float,
    maximum_admissible_covariance_error: float,
    *,
    screening_confidence: float = 0.975,
    certification_confidence: float = 0.975,
    maximum_sample_count: int = 10**15,
) -> int | None:
    """Find the smallest independent certification split meeting the radius."""
    if maximum_sample_count < 2:
        raise ValueError("maximum_sample_count must be at least two")

    def certified(sample_count: int) -> bool:
        return sample_split_screened_recovery_bound(
            screening_sample_count,
            sample_count,
            retained_block_count,
            block_dimension,
            maximum_block_eigenvalue,
            maximum_admissible_covariance_error,
            screening_confidence=screening_confidence,
            certification_confidence=certification_confidence,
            independent_splits=True,
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
