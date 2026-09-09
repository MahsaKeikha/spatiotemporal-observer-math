"""Relative covariance uncertainty propagated to observer world-tube recovery.

Proposition 58 closes the deterministic bridge from a simultaneous relative
covariance certificate to the original moving-boundary observer objective. It
maps candidate-local covariance radii through integration, independence,
persistence, local observer scores, transport scores, and finally the complete
world-tube action.
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
class RelativeCovarianceWorldTubeRecoveryBound:
    """Deterministic path certificate on simultaneous relative covariance events."""

    covariance_relative_errors: np.ndarray
    local_factor_errors: np.ndarray
    transport_factor_errors: np.ndarray
    local_score_errors: np.ndarray
    transport_score_errors: np.ndarray
    structural_integration_null_mask: np.ndarray
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


def _relative_factor_errors(
    covariance_relative_errors: np.ndarray,
    node_count: int,
    subset_size: int,
    *,
    transport: bool,
) -> tuple[np.ndarray, np.ndarray]:
    """Map candidate-local relative covariance radii to factor radii."""
    valid = covariance_relative_errors < 1.0
    factor_count = 2 if transport else 3
    errors = np.ones((*covariance_relative_errors.shape, factor_count), dtype=float)
    for index in np.ndindex(covariance_relative_errors.shape):
        if not valid[index]:
            continue
        delta = float(covariance_relative_errors[index])
        log_factor = -np.log1p(-delta)
        offset = 0
        if not transport:
            errors[index][0] = min(1.0, 4.0 * log_factor)
            offset = 1
        errors[index][offset] = min(
            1.0,
            (node_count + 2.0 * subset_size) / subset_size * log_factor,
        )
        errors[index][offset + 1] = (
            canonical_persistence_relative_covariance_error_bound(
                covariance_relative_error=delta
            )
        )
    return errors, valid


def relative_covariance_worldtube_recovery_bound(
    local_factors: ArrayLike,
    transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    node_count: int,
    subset_size: int,
    *,
    covariance_relative_errors: ArrayLike,
    structural_integration_null_mask: ArrayLike | None = None,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> RelativeCovarianceWorldTubeRecoveryBound:
    """Certify a population world-tube from candidate-local relative radii.

    For candidate ``j`` at time ``t``, the supplied radius certifies the joint
    covariance block containing all present coordinates and the candidate's
    future coordinates. The same block supports the local observer factors and
    every incoming transport edge to that future candidate.

    No probability is spent by this function. If the simultaneous covariance
    event holds with probability at least ``1-alpha``, then a positive returned
    recovery slack certifies the population world-tube with at least the same
    probability.
    """
    local, transport = _validated_factors(local_factors, transport_factors)
    time_count, candidate_count, _ = local.shape
    candidate_tuple = _validated_candidates(
        candidates,
        candidate_count,
        node_count,
        subset_size,
    )
    relative = np.asarray(covariance_relative_errors, dtype=float)
    expected = (time_count, candidate_count)
    if relative.shape != expected:
        raise ValueError(f"covariance_relative_errors must have shape {expected}")
    if np.any(~np.isfinite(relative)) or np.any(relative < 0.0):
        raise ValueError("covariance_relative_errors must be finite and nonnegative")
    if not np.isfinite(transport_weight):
        raise ValueError("transport_weight must be finite")
    if not np.isfinite(continuity_weight) or continuity_weight < 0.0:
        raise ValueError("continuity_weight must be finite and nonnegative")

    if structural_integration_null_mask is None:
        null_mask = np.zeros(expected, dtype=bool)
    else:
        null_mask = np.asarray(structural_integration_null_mask)
        if null_mask.shape != expected or null_mask.dtype != np.bool_:
            raise ValueError(
                "structural_integration_null_mask must be a Boolean state array"
            )

    local_factor_errors, valid_local = _relative_factor_errors(
        relative,
        node_count,
        subset_size,
        transport=False,
    )
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    edge_relative = np.broadcast_to(relative[:-1, None, :], edge_shape)
    transport_factor_errors, valid_transport = _relative_factor_errors(
        edge_relative,
        node_count,
        subset_size,
        transport=True,
    )

    local_scores = np.prod(local, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport, axis=3))
    local_errors = np.empty(expected, dtype=float)
    for index in np.ndindex(expected):
        local_errors[index] = product_root_error_bound(
            local[index],
            local_factor_errors[index],
        )
        if null_mask[index] and relative[index] < 1.0:
            null_integration_error = (
                gaussian_relative_null_integration_factor_error_bound(
                    subset_size,
                    covariance_relative_error=float(relative[index]),
                )
            )
            null_score_error = float(null_integration_error ** (1.0 / 3.0))
            local_errors[index] = min(local_errors[index], null_score_error)

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
    all_valid = bool(np.all(valid_local) and np.all(valid_transport))
    return RelativeCovarianceWorldTubeRecoveryBound(
        covariance_relative_errors=relative.copy(),
        local_factor_errors=local_factor_errors,
        transport_factor_errors=transport_factor_errors,
        local_score_errors=local_errors,
        transport_score_errors=transport_errors,
        structural_integration_null_mask=null_mask.copy(),
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
