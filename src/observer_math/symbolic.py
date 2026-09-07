"""Closed-form recovery conditions for structured Gaussian dynamics."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MovingCliqueRecoveryBound:
    """Symbolic planted-path margin for a covariance-preserving moving clique."""

    self_memory: float
    internal_coupling: float
    module_size: int
    minimum_consecutive_overlap: int
    maximum_planted_jaccard_distance: float
    directed_integration_bits_per_node: float
    integration_strength: float
    persistence: float
    planted_local_score: float
    edge_uncertainty_per_incident_edge: float
    per_mismatch_action_margin: float
    stable_covariance_preserving_dynamics: bool
    guarantees_unique_planted_path: bool


def _residual_logdet(
    row_count: int,
    column_count: int,
    self_memory: float,
    internal_coupling: float,
) -> float:
    """Log determinant of I - A_RC A_RC.T for an equicoupled block."""
    alpha = self_memory
    beta = internal_coupling
    diagonal = alpha**2 + (column_count - 1) * beta**2
    off_diagonal = 2.0 * alpha * beta + (column_count - 2) * beta**2
    transverse = 1.0 - diagonal + off_diagonal
    longitudinal = 1.0 - diagonal - (row_count - 1) * off_diagonal
    if transverse <= 0.0 or longitudinal <= 0.0:
        raise ValueError("parameters do not produce positive conditional covariance")
    return float((row_count - 1) * np.log(transverse) + np.log(longitudinal))


def covariance_preserving_moving_clique_bound(
    self_memory: float,
    internal_coupling: float,
    module_size: int,
    *,
    minimum_consecutive_overlap: int = 0,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> MovingCliqueRecoveryBound:
    """Evaluate a closed-form sufficient condition for a moving clique path.

    The model has unit population covariance, transition coefficient
    ``self_memory`` on every diagonal, and ``internal_coupling`` between every
    ordered pair inside the active module. Process noise is ``I - A A.T``.
    Candidate boundaries all have size ``module_size``.
    """
    if module_size < 2:
        raise ValueError("module_size must be at least two")
    if not 0 <= minimum_consecutive_overlap <= module_size:
        raise ValueError("minimum_consecutive_overlap must lie in [0, module_size]")
    if continuity_weight < 0.0:
        raise ValueError("continuity_weight must be nonnegative")
    if not np.isfinite(self_memory) or not np.isfinite(internal_coupling):
        raise ValueError("dynamical parameters must be finite")
    alpha = float(self_memory)
    beta = float(internal_coupling)
    active_longitudinal = alpha + (module_size - 1) * beta
    active_transverse = alpha - beta
    spectral_radius = max(abs(alpha), abs(active_longitudinal), abs(active_transverse))
    stable = spectral_radius < 1.0
    if not stable:
        raise ValueError("require spectral norm below one so I - A A.T is positive")

    split_values = []
    for left_size in range(1, module_size):
        right_size = module_size - left_size
        left_information = 0.5 / np.log(2.0) * (
            _residual_logdet(left_size, left_size, alpha, beta)
            - _residual_logdet(left_size, module_size, alpha, beta)
        )
        right_information = 0.5 / np.log(2.0) * (
            _residual_logdet(right_size, right_size, alpha, beta)
            - _residual_logdet(right_size, module_size, alpha, beta)
        )
        split_values.append((left_information + right_information) / module_size)

    directed_rate = float(min(split_values))
    integration_strength = float(1.0 - 2.0 ** (-directed_rate))
    persistence = float(alpha**2 + (module_size - 1) * beta**2)
    local_score = float((integration_strength * persistence) ** (1.0 / 3.0))
    maximum_jaccard = 1.0 - minimum_consecutive_overlap / (
        2 * module_size - minimum_consecutive_overlap
    )
    edge_uncertainty = abs(transport_weight) + continuity_weight * maximum_jaccard
    per_mismatch_margin = float(local_score - 2.0 * edge_uncertainty)
    return MovingCliqueRecoveryBound(
        self_memory=alpha,
        internal_coupling=beta,
        module_size=module_size,
        minimum_consecutive_overlap=minimum_consecutive_overlap,
        maximum_planted_jaccard_distance=float(maximum_jaccard),
        directed_integration_bits_per_node=directed_rate,
        integration_strength=integration_strength,
        persistence=persistence,
        planted_local_score=local_score,
        edge_uncertainty_per_incident_edge=float(edge_uncertainty),
        per_mismatch_action_margin=per_mismatch_margin,
        stable_covariance_preserving_dynamics=stable,
        guarantees_unique_planted_path=per_mismatch_margin > 0.0,
    )
