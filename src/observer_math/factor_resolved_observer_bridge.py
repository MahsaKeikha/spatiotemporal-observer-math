"""Factor-resolved covariance localization for observer world-tube recovery.

Proposition 59 refines Proposition 58 by preserving the covariance geometry
actually required by each observer factor. Directed integration and local
persistence use a present/future candidate block of dimension 2s. Environmental
independence uses the full present state plus the future target, of dimension
n+s. Transport persistence uses a source/future-target block of dimension 2s.

The theorem is deterministic: it assumes valid simultaneous relative covariance
radii have already been supplied for the declared block families and propagates
those heterogeneous radii to the complete world-tube objective without spending
another probability budget.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike

from .recovery import (
    NearCompetitorScreen,
    canonical_persistence_relative_covariance_error_bound,
    gaussian_relative_null_integration_factor_error_bound,
    product_root_error_bound,
    screen_near_competitors,
)
from .worldtube import certify_worldtube


@dataclass(frozen=True)
class FactorResolvedWorldTubeRecoveryBound:
    """Deterministic world-tube certificate using factor-specific covariance radii."""

    local_candidate_relative_errors: np.ndarray
    target_full_relative_errors: np.ndarray
    transport_pair_relative_errors: np.ndarray
    local_factor_errors: np.ndarray
    transport_factor_errors: np.ndarray
    local_score_errors: np.ndarray
    transport_score_errors: np.ndarray
    structural_integration_null_mask: np.ndarray
    local_candidate_block_dimension: int
    target_full_block_dimension: int
    transport_pair_block_dimension: int
    local_candidate_block_count: int
    target_full_block_count: int
    transport_pair_block_count: int
    population_path: tuple[int, ...]
    adversarial_competitor: tuple[int, ...] | None
    population_action_margin: float
    planted_lower_action: float
    competitor_upper_action: float
    recovery_slack: float
    near_competitor_screen: NearCompetitorScreen
    all_blocks_valid: bool
    guarantees_population_path: bool


def _validated_factors(
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
) -> tuple[np.ndarray, np.ndarray]:
    local = np.asarray(local_factors, dtype=float)
    transport = np.asarray(transport_factors, dtype=float)
    if local.ndim != 3 or local.shape[2] != 3:
        raise ValueError("local_factors must have shape (time, candidates, 3)")
    time_count, candidate_count, _ = local.shape
    expected_transport = (
        max(0, time_count - 1),
        candidate_count,
        candidate_count,
        2,
    )
    if transport.shape != expected_transport:
        raise ValueError(f"transport_factors must have shape {expected_transport}")
    if (
        np.any(~np.isfinite(local))
        or np.any(~np.isfinite(transport))
        or np.any((local < 0.0) | (local > 1.0))
        or np.any((transport < 0.0) | (transport > 1.0))
    ):
        raise ValueError("factor arrays must be finite and lie in [0, 1]")
    return local, transport


def _validated_candidates(
    candidates: Sequence[Sequence[int]],
    candidate_count: int,
    node_count: int,
    subset_size: int,
) -> tuple[tuple[int, ...], ...]:
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if len(candidate_tuple) != candidate_count:
        raise ValueError("candidates and factor arrays have incompatible sizes")
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
    return candidate_tuple


def _validated_radius_array(
    values: ArrayLike,
    shape: tuple[int, ...],
    name: str,
) -> np.ndarray:
    array = np.asarray(values, dtype=float)
    if array.shape != shape:
        raise ValueError(f"{name} must have shape {shape}")
    if np.any(~np.isfinite(array)) or np.any(array < 0.0):
        raise ValueError(f"{name} must be finite and nonnegative")
    return array


def _integration_error(delta: float) -> float:
    if delta >= 1.0:
        return 1.0
    return float(min(1.0, 4.0 * (-np.log1p(-delta))))


def _independence_error(delta: float, node_count: int, subset_size: int) -> float:
    if delta >= 1.0:
        return 1.0
    coefficient = (node_count + 2.0 * subset_size) / subset_size
    return float(min(1.0, coefficient * (-np.log1p(-delta))))


def _persistence_error(delta: float) -> float:
    if delta >= 1.0:
        return 1.0
    return float(
        canonical_persistence_relative_covariance_error_bound(
            covariance_relative_error=delta
        )
    )


def factor_resolved_covariance_worldtube_recovery_bound(
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    node_count: int,
    subset_size: int,
    *,
    local_candidate_relative_errors: ArrayLike,
    target_full_relative_errors: ArrayLike,
    transport_pair_relative_errors: ArrayLike,
    structural_integration_null_mask: ArrayLike | None = None,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> FactorResolvedWorldTubeRecoveryBound:
    """Certify a world-tube while preserving factor-specific covariance geometry.

    ``local_candidate_relative_errors[t, j]`` certifies the 2s-dimensional block
    containing present candidate ``j`` and its future copy. It controls directed
    integration and local persistence.

    ``target_full_relative_errors[t, j]`` certifies the (n+s)-dimensional block
    containing all present coordinates and future candidate ``j``. It controls
    local environmental independence and every incoming transport-independence
    factor to that future target.

    ``transport_pair_relative_errors[t, u, v]`` certifies the 2s-dimensional
    block containing present source candidate ``u`` and future target candidate
    ``v``. It controls transport persistence.

    No probability is spent by this function. Any probability statement is
    inherited from the simultaneous covariance events that supplied these radii.
    """
    local, transport = _validated_factors(local_factors, transport_factors)
    time_count, candidate_count, _ = local.shape
    candidate_tuple = _validated_candidates(
        candidates,
        candidate_count,
        node_count,
        subset_size,
    )

    state_shape = (time_count, candidate_count)
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    local_relative = _validated_radius_array(
        local_candidate_relative_errors,
        state_shape,
        "local_candidate_relative_errors",
    )
    full_relative = _validated_radius_array(
        target_full_relative_errors,
        state_shape,
        "target_full_relative_errors",
    )
    pair_relative = _validated_radius_array(
        transport_pair_relative_errors,
        edge_shape,
        "transport_pair_relative_errors",
    )
    if not np.isfinite(transport_weight):
        raise ValueError("transport_weight must be finite")
    if not np.isfinite(continuity_weight) or continuity_weight < 0.0:
        raise ValueError("continuity_weight must be finite and nonnegative")

    if structural_integration_null_mask is None:
        null_mask = np.zeros(state_shape, dtype=bool)
    else:
        null_mask = np.asarray(structural_integration_null_mask)
        if null_mask.shape != state_shape or null_mask.dtype != np.bool_:
            raise ValueError(
                "structural_integration_null_mask must be a Boolean state array"
            )

    local_factor_errors = np.ones((*state_shape, 3), dtype=float)
    for time, candidate in np.ndindex(state_shape):
        delta_local = float(local_relative[time, candidate])
        delta_full = float(full_relative[time, candidate])
        local_factor_errors[time, candidate, 0] = _integration_error(delta_local)
        local_factor_errors[time, candidate, 1] = _independence_error(
            delta_full,
            node_count,
            subset_size,
        )
        local_factor_errors[time, candidate, 2] = _persistence_error(delta_local)

    transport_factor_errors = np.ones((*edge_shape, 2), dtype=float)
    for time, source, target in np.ndindex(edge_shape):
        delta_full = float(full_relative[time, target])
        delta_pair = float(pair_relative[time, source, target])
        transport_factor_errors[time, source, target, 0] = _independence_error(
            delta_full,
            node_count,
            subset_size,
        )
        transport_factor_errors[time, source, target, 1] = _persistence_error(
            delta_pair
        )

    local_scores = np.prod(local, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport, axis=3))
    local_errors = np.empty(state_shape, dtype=float)
    for index in np.ndindex(state_shape):
        local_errors[index] = product_root_error_bound(
            local[index],
            local_factor_errors[index],
        )
        if null_mask[index] and local_relative[index] < 1.0:
            null_integration_error = (
                gaussian_relative_null_integration_factor_error_bound(
                    subset_size,
                    covariance_relative_error=float(local_relative[index]),
                )
            )
            local_errors[index] = min(
                local_errors[index],
                float(null_integration_error ** (1.0 / 3.0)),
            )

    transport_errors = np.empty(edge_shape, dtype=float)
    for index in np.ndindex(edge_shape):
        transport_errors[index] = product_root_error_bound(
            transport[index],
            transport_factor_errors[index],
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
    planted_lower = float(population.result.total_action - planted_error)

    direction = 0.0 if transport_weight == 0.0 else float(np.sign(transport_weight))
    inflated = certify_worldtube(
        local_scores + local_errors,
        candidate_tuple,
        transport_scores=transport_scores + direction * transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    if inflated.result.candidate_indices == planted:
        competitor_upper = float(inflated.runner_up_action)
        adversarial = inflated.runner_up_indices
    else:
        competitor_upper = float(inflated.result.total_action)
        adversarial = inflated.result.candidate_indices

    near_competitors = screen_near_competitors(
        local_scores,
        transport_scores,
        candidate_tuple,
        local_errors,
        transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    slack = float(planted_lower - competitor_upper)
    all_valid = bool(
        np.all(local_relative < 1.0)
        and np.all(full_relative < 1.0)
        and np.all(pair_relative < 1.0)
    )
    return FactorResolvedWorldTubeRecoveryBound(
        local_candidate_relative_errors=local_relative.copy(),
        target_full_relative_errors=full_relative.copy(),
        transport_pair_relative_errors=pair_relative.copy(),
        local_factor_errors=local_factor_errors,
        transport_factor_errors=transport_factor_errors,
        local_score_errors=local_errors,
        transport_score_errors=transport_errors,
        structural_integration_null_mask=null_mask.copy(),
        local_candidate_block_dimension=2 * subset_size,
        target_full_block_dimension=node_count + subset_size,
        transport_pair_block_dimension=2 * subset_size,
        local_candidate_block_count=time_count * candidate_count,
        target_full_block_count=time_count * candidate_count,
        transport_pair_block_count=max(0, time_count - 1) * candidate_count**2,
        population_path=planted,
        adversarial_competitor=adversarial,
        population_action_margin=float(population.action_margin),
        planted_lower_action=planted_lower,
        competitor_upper_action=competitor_upper,
        recovery_slack=slack,
        near_competitor_screen=near_competitors,
        all_blocks_valid=all_valid,
        guarantees_population_path=bool(all_valid and slack > 0.0),
    )
