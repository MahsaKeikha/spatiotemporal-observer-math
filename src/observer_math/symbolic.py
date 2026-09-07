"""Closed-form recovery conditions for structured Gaussian dynamics."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import combinations
from math import comb

import numpy as np
from numpy.typing import ArrayLike

from .nonstationary import adjacent_joint_covariance, propagate_covariances
from .recovery import (
    canonical_persistence_covariance_error_bound,
    product_root_error_bound,
)


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


@dataclass(frozen=True)
class PerturbedMovingCliqueRecoveryBound:
    """Recovery margin under transition and anisotropic-noise perturbations."""

    base: MovingCliqueRecoveryBound
    node_count: int
    time_count: int
    transition_perturbation: float
    noise_perturbation: float
    base_transition_norm: float
    perturbed_transition_norm_bound: float
    one_step_covariance_forcing: float
    minimum_base_joint_eigenvalue: float
    maximum_state_covariance_error: float
    maximum_joint_covariance_error: float
    integration_factor_error: float
    independence_factor_error: float
    persistence_factor_error: float
    planted_score_error: float
    conditional_cross_covariance_error: float
    conditional_canonical_correlation_bound: float
    incorrect_integration_factor_upper_bound: float
    incorrect_score_upper_bound: float
    perturbed_local_separation: float
    per_mismatch_action_margin: float
    valid_noise_covariance: bool
    valid_covariance_perturbation: bool
    valid_zero_cut_perturbation: bool
    guarantees_unique_planted_path: bool


@dataclass(frozen=True)
class SupportResolvedMovingCliqueRecoveryBound:
    """Candidate-local recovery bound for a specified perturbed system.

    This exact small-family certificate enumerates all fixed-size candidates;
    its candidate-level arrays can therefore grow combinatorially.
    """

    base: MovingCliqueRecoveryBound
    node_count: int
    time_count: int
    candidate_count: int
    candidates: tuple[tuple[int, ...], ...]
    candidate_overlaps: tuple[tuple[int, ...], ...]
    candidate_covariance_errors: tuple[tuple[float, ...], ...]
    candidate_base_eigenvalue_bounds: tuple[
        tuple[tuple[float, float], ...], ...
    ]
    incorrect_score_upper_bounds: tuple[tuple[float, ...], ...]
    planted_local_covariance_errors: tuple[float, ...]
    planted_leakage_covariance_errors: tuple[float, ...]
    planted_score_lower_bounds: tuple[float, ...]
    maximum_incorrect_score_upper_bounds: tuple[float, ...]
    local_separations: tuple[float, ...]
    incident_edge_penalties: tuple[float, ...]
    per_time_mismatch_margins: tuple[float, ...]
    maximum_planted_score_error: float
    maximum_incorrect_score_upper_bound: float
    minimum_local_separation: float
    per_mismatch_action_margin: float
    all_local_covariance_bounds_valid: bool
    guarantees_unique_planted_path: bool


@dataclass(frozen=True)
class APrioriSupportMovingCliqueRecoveryBound:
    """Support-aware recovery bound obtained without covariance propagation."""

    base: MovingCliqueRecoveryBound
    node_count: int
    time_count: int
    candidate_count: int
    candidates: tuple[tuple[int, ...], ...]
    candidate_overlaps: tuple[tuple[int, ...], ...]
    global_state_covariance_error_bounds: tuple[float, ...]
    planted_local_joint_error_bounds: tuple[float, ...]
    planted_leakage_joint_error_bounds: tuple[float, ...]
    candidate_joint_error_bounds: tuple[tuple[float, ...], ...]
    planted_score_lower_bounds: tuple[float, ...]
    incorrect_score_upper_bounds: tuple[tuple[float, ...], ...]
    maximum_incorrect_score_upper_bounds: tuple[float, ...]
    local_separations: tuple[float, ...]
    incident_edge_penalties: tuple[float, ...]
    per_time_mismatch_margins: tuple[float, ...]
    per_mismatch_action_margin: float
    candidate_family_is_complete: bool
    all_noise_covariances_positive_definite: bool
    all_local_covariance_bounds_valid: bool
    guarantees_unique_planted_path_in_candidate_family: bool


@dataclass(frozen=True)
class OverlapClassMovingCliqueRecoveryBound:
    """Matrix-free recovery bound indexed by planted-candidate overlap."""

    base: MovingCliqueRecoveryBound
    node_count: int
    time_count: int
    module_size: int
    candidate_count: int
    overlap_class_count: int
    overlap_values: tuple[int, ...]
    overlap_class_multiplicities: tuple[int, ...]
    feasible_consecutive_overlap_pairs: tuple[tuple[tuple[int, int], ...], ...]
    global_state_covariance_error_bounds: tuple[float, ...]
    local_next_state_error_bounds: tuple[tuple[float, ...], ...]
    planted_local_joint_error_bounds: tuple[float, ...]
    planted_leakage_joint_error_bounds: tuple[float, ...]
    overlap_class_joint_error_bounds: tuple[tuple[float, ...], ...]
    planted_score_lower_bounds: tuple[float, ...]
    incorrect_score_upper_bounds: tuple[tuple[float, ...], ...]
    maximum_incorrect_score_upper_bounds: tuple[float, ...]
    local_separations: tuple[float, ...]
    incident_edge_penalties: tuple[float, ...]
    per_time_mismatch_margins: tuple[float, ...]
    per_mismatch_action_margin: float
    all_noise_covariance_classes_valid: bool
    all_local_covariance_bounds_valid: bool
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
    if isinstance(module_size, bool) or not isinstance(module_size, (int, np.integer)):
        raise TypeError("module_size must be an integer")
    if isinstance(minimum_consecutive_overlap, bool) or not isinstance(
        minimum_consecutive_overlap, (int, np.integer)
    ):
        raise TypeError("minimum_consecutive_overlap must be an integer")
    if module_size < 2:
        raise ValueError("module_size must be at least two")
    if not 0 <= minimum_consecutive_overlap <= module_size:
        raise ValueError("minimum_consecutive_overlap must lie in [0, module_size]")
    if not np.isfinite(transport_weight) or not np.isfinite(continuity_weight):
        raise ValueError("action weights must be finite")
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


def perturbed_moving_clique_recovery_bound(
    self_memory: float,
    internal_coupling: float,
    module_size: int,
    node_count: int,
    time_count: int,
    *,
    transition_perturbation: float,
    noise_perturbation: float,
    minimum_consecutive_overlap: int = 0,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> PerturbedMovingCliqueRecoveryBound:
    """Certify recovery near the covariance-preserving moving-clique family.

    The transition perturbation is an operator-norm bound on ``A_t - A_t^0``;
    it may contain nonzero external coupling. The noise perturbation bounds
    ``Q_t - (I - A_t^0 A_t^0.T)`` and therefore permits anisotropic noise.
    The initial covariance is the identity.
    """
    if isinstance(node_count, bool) or not isinstance(node_count, (int, np.integer)):
        raise TypeError("node_count must be an integer")
    if isinstance(time_count, bool) or not isinstance(time_count, (int, np.integer)):
        raise TypeError("time_count must be an integer")
    if node_count < module_size:
        raise ValueError("node_count must be at least module_size")
    if time_count < 1:
        raise ValueError("time_count must be positive")
    if not np.isfinite(transition_perturbation) or not np.isfinite(noise_perturbation):
        raise ValueError("perturbation radii must be finite")
    if transition_perturbation < 0.0 or noise_perturbation < 0.0:
        raise ValueError("perturbation radii must be nonnegative")
    base = covariance_preserving_moving_clique_bound(
        self_memory,
        internal_coupling,
        module_size,
        minimum_consecutive_overlap=minimum_consecutive_overlap,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    alpha = float(self_memory)
    beta = float(internal_coupling)
    rho = max(
        abs(alpha),
        abs(alpha - beta),
        abs(alpha + (module_size - 1) * beta),
    )
    gamma = float(transition_perturbation)
    nu = float(noise_perturbation)
    perturbed_transition_norm = rho + gamma
    if perturbed_transition_norm >= 1.0:
        raise ValueError("base transition norm plus perturbation must be below one")

    valid_noise = nu < 1.0 - rho**2
    one_step_forcing = 2.0 * rho * gamma + gamma**2 + nu
    covariance_errors = [0.0]
    joint_errors = []
    for _ in range(time_count):
        current_error = covariance_errors[-1]
        next_error = (
            perturbed_transition_norm**2 * current_error + one_step_forcing
        )
        cross_error = perturbed_transition_norm * current_error + gamma
        joint_error = 0.5 * (
            current_error
            + next_error
            + np.sqrt((current_error - next_error) ** 2 + 4.0 * cross_error**2)
        )
        covariance_errors.append(float(next_error))
        joint_errors.append(float(joint_error))

    maximum_covariance_error = max(covariance_errors)
    maximum_joint_error = max(joint_errors)
    joint_minimum = 1.0 - rho
    joint_maximum = 1.0 + rho
    valid_perturbation = maximum_joint_error < joint_minimum

    if valid_perturbation:
        logdet_factor = (
            -np.log1p(-maximum_joint_error / joint_minimum) / np.log(2.0)
        )
        integration_error = min(1.0, np.log(2.0) * 4.0 * logdet_factor)
        leakage_error = (
            (node_count + 2 * module_size) / module_size * logdet_factor
        )
        independence_error = min(1.0, np.log(2.0) * leakage_error)
        persistence_error = canonical_persistence_covariance_error_bound(
            minimum_eigenvalue=joint_minimum,
            maximum_eigenvalue=joint_maximum,
            covariance_spectral_error=maximum_joint_error,
        )
        planted_error = product_root_error_bound(
            (
                base.integration_strength,
                1.0,
                base.persistence,
            ),
            (integration_error, independence_error, persistence_error),
        )
        perturbed_minimum = joint_minimum - maximum_joint_error
        conditional_cross_error = maximum_joint_error * (
            1.0
            + (joint_maximum + maximum_joint_error) / perturbed_minimum
            + joint_maximum
            * (joint_maximum + maximum_joint_error)
            / (joint_minimum * perturbed_minimum)
            + joint_maximum / joint_minimum
        )
        conditional_correlation = conditional_cross_error / perturbed_minimum
        valid_zero_cut = conditional_correlation < 1.0
        if valid_zero_cut:
            incorrect_integration = 1.0 - (
                1.0 - conditional_correlation**2
            ) ** (1.0 / module_size)
            incorrect_upper = incorrect_integration ** (1.0 / 3.0)
        else:
            incorrect_integration = 1.0
            incorrect_upper = 1.0
    else:
        integration_error = 1.0
        independence_error = 1.0
        persistence_error = 1.0
        planted_error = 1.0
        conditional_cross_error = np.inf
        conditional_correlation = 1.0
        incorrect_integration = 1.0
        incorrect_upper = 1.0
        valid_zero_cut = False

    local_separation = base.planted_local_score - planted_error - incorrect_upper
    action_margin = local_separation - 2.0 * base.edge_uncertainty_per_incident_edge
    guarantee = bool(
        valid_noise
        and valid_perturbation
        and valid_zero_cut
        and action_margin > 0.0
    )
    return PerturbedMovingCliqueRecoveryBound(
        base=base,
        node_count=node_count,
        time_count=time_count,
        transition_perturbation=gamma,
        noise_perturbation=nu,
        base_transition_norm=float(rho),
        perturbed_transition_norm_bound=float(perturbed_transition_norm),
        one_step_covariance_forcing=float(one_step_forcing),
        minimum_base_joint_eigenvalue=float(joint_minimum),
        maximum_state_covariance_error=float(maximum_covariance_error),
        maximum_joint_covariance_error=float(maximum_joint_error),
        integration_factor_error=float(integration_error),
        independence_factor_error=float(independence_error),
        persistence_factor_error=float(persistence_error),
        planted_score_error=float(planted_error),
        conditional_cross_covariance_error=float(conditional_cross_error),
        conditional_canonical_correlation_bound=float(conditional_correlation),
        incorrect_integration_factor_upper_bound=float(incorrect_integration),
        incorrect_score_upper_bound=float(incorrect_upper),
        perturbed_local_separation=float(local_separation),
        per_mismatch_action_margin=float(action_margin),
        valid_noise_covariance=valid_noise,
        valid_covariance_perturbation=valid_perturbation,
        valid_zero_cut_perturbation=valid_zero_cut,
        guarantees_unique_planted_path=guarantee,
    )


def _covariance_block_error(
    base_joint: np.ndarray,
    actual_joint: np.ndarray,
    indices: tuple[int, ...],
) -> tuple[float, float, float]:
    base_block = base_joint[np.ix_(indices, indices)]
    actual_block = actual_joint[np.ix_(indices, indices)]
    eigenvalues = np.linalg.eigvalsh(base_block)
    minimum = float(eigenvalues[0])
    maximum = float(eigenvalues[-1])
    error = float(np.linalg.norm(actual_block - base_block, ord=2))
    return minimum, maximum, error


def _zero_cut_integration_bound(
    minimum: float,
    maximum: float,
    error: float,
    module_size: int,
) -> tuple[float, bool]:
    if error >= minimum:
        return 1.0, False
    perturbed_minimum = minimum - error
    conditional_cross_error = error * (
        1.0
        + (maximum + error) / perturbed_minimum
        + maximum * (maximum + error) / (minimum * perturbed_minimum)
        + maximum / minimum
    )
    partial_correlation = conditional_cross_error / perturbed_minimum
    if partial_correlation >= 1.0:
        return 1.0, False
    integration = 1.0 - (1.0 - partial_correlation**2) ** (1.0 / module_size)
    return float(integration), True


def _symmetric_block_norm_bound(
    first_diagonal: float,
    second_diagonal: float,
    off_diagonal: float,
) -> float:
    """Bound a symmetric two-by-two operator block from its block norms."""
    return float(
        0.5
        * (
            first_diagonal
            + second_diagonal
            + np.sqrt(
                (first_diagonal - second_diagonal) ** 2
                + 4.0 * off_diagonal**2
            )
        )
    )


def _moving_clique_transition(
    node_count: int,
    planted: tuple[int, ...],
    self_memory: float,
    internal_coupling: float,
) -> np.ndarray:
    transition = np.eye(node_count) * float(self_memory)
    for target in planted:
        for source in planted:
            if source != target:
                transition[target, source] = float(internal_coupling)
    return transition


def support_resolved_moving_clique_recovery_bound(
    transitions: Sequence[ArrayLike],
    noise_covariances: Sequence[ArrayLike],
    planted_path: Sequence[Sequence[int]],
    *,
    self_memory: float,
    internal_coupling: float,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> SupportResolvedMovingCliqueRecoveryBound:
    """Certify a specified perturbation using candidate-local covariance blocks.

    The reference family is the covariance-preserving moving clique on the
    supplied planted path. Actual covariances are propagated from the identity.
    Unlike :func:`perturbed_moving_clique_recovery_bound`, this function uses
    the realized support of the perturbations rather than global norm radii.
    It enumerates all size-matched candidates and is intended for small exact
    studies rather than unrestricted population-scale searches.
    """
    if len(transitions) != len(noise_covariances) or len(transitions) != len(
        planted_path
    ):
        raise ValueError("dynamics and planted_path must have equal lengths")
    if not transitions:
        raise ValueError("at least one transition is required")
    transition_arrays = tuple(np.asarray(matrix, dtype=float) for matrix in transitions)
    noise_arrays = tuple(np.asarray(matrix, dtype=float) for matrix in noise_covariances)
    if any(
        matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]
        for matrix in transition_arrays
    ):
        raise ValueError("transitions must be square matrices")
    node_count = transition_arrays[0].shape[0]
    if any(
        matrix.shape != (node_count, node_count)
        for matrix in transition_arrays + noise_arrays
    ):
        raise ValueError("all transition and noise matrices must have equal dimensions")
    if any(np.any(~np.isfinite(matrix)) for matrix in transition_arrays + noise_arrays):
        raise ValueError("dynamical matrices must be finite")
    if any(
        not np.allclose(matrix, matrix.T)
        or np.linalg.eigvalsh(matrix)[0] <= 0.0
        for matrix in noise_arrays
    ):
        raise ValueError("noise covariances must be symmetric positive definite")

    path = tuple(tuple(sorted({int(node) for node in subset})) for subset in planted_path)
    module_size = len(path[0])
    if module_size < 2 or node_count <= module_size:
        raise ValueError("require 2 <= module_size < node_count")
    if any(
        len(subset) != module_size
        or subset[0] < 0
        or subset[-1] >= node_count
        for subset in path
    ):
        raise ValueError("planted boundaries must be valid and equal in size")
    if continuity_weight < 0.0 or not np.isfinite(
        [transport_weight, continuity_weight]
    ).all():
        raise ValueError("action weights must be finite and continuity nonnegative")

    overlaps = [
        len(set(path[time]) & set(path[time + 1]))
        for time in range(len(path) - 1)
    ]
    minimum_overlap = min(overlaps, default=module_size)
    base = covariance_preserving_moving_clique_bound(
        self_memory,
        internal_coupling,
        module_size,
        minimum_consecutive_overlap=minimum_overlap,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    covariances = propagate_covariances(
        transition_arrays, noise_arrays, np.eye(node_count)
    )
    actual_joints = tuple(
        adjacent_joint_covariance(
            covariances[time], transition_arrays[time], noise_arrays[time]
        )
        for time in range(len(path))
    )
    if any(np.linalg.eigvalsh(joint)[0] <= 0.0 for joint in actual_joints):
        raise ValueError("actual adjacent covariances must be positive definite")

    candidates = tuple(combinations(range(node_count), module_size))
    planted_lowers = []
    wrong_maxima = []
    local_separations = []
    overlap_rows = []
    wrong_bound_rows = []
    candidate_error_rows = []
    candidate_spectrum_rows = []
    planted_errors = []
    planted_local_errors = []
    planted_leakage_errors = []
    all_valid = True
    for time, planted in enumerate(path):
        base_transition = _moving_clique_transition(
            node_count, planted, self_memory, internal_coupling
        )
        base_joint = np.block(
            [
                [np.eye(node_count), base_transition.T],
                [base_transition, np.eye(node_count)],
            ]
        )
        actual_joint = actual_joints[time]

        planted_indices = planted + tuple(node_count + node for node in planted)
        local_minimum, local_maximum, local_error = _covariance_block_error(
            base_joint, actual_joint, planted_indices
        )
        local_valid = local_error < local_minimum
        leakage_indices = tuple(range(node_count)) + tuple(
            node_count + node for node in planted
        )
        leakage_minimum, _, leakage_error = _covariance_block_error(
            base_joint, actual_joint, leakage_indices
        )
        leakage_valid = leakage_error < leakage_minimum
        planted_local_errors.append(float(local_error))
        planted_leakage_errors.append(float(leakage_error))
        if local_valid and leakage_valid:
            local_logdet = -np.log1p(-local_error / local_minimum) / np.log(2.0)
            leakage_logdet = (
                -np.log1p(-leakage_error / leakage_minimum) / np.log(2.0)
            )
            integration_error = min(1.0, 4.0 * np.log(2.0) * local_logdet)
            independence_error = min(
                1.0,
                np.log(2.0)
                * (node_count + 2 * module_size)
                / module_size
                * leakage_logdet,
            )
            persistence_error = canonical_persistence_covariance_error_bound(
                minimum_eigenvalue=local_minimum,
                maximum_eigenvalue=local_maximum,
                covariance_spectral_error=local_error,
            )
            planted_error = product_root_error_bound(
                (base.integration_strength, 1.0, base.persistence),
                (integration_error, independence_error, persistence_error),
            )
        else:
            planted_error = 1.0
        planted_lower = max(0.0, base.planted_local_score - planted_error)
        planted_errors.append(float(planted_error))
        planted_lowers.append(float(planted_lower))

        overlap_row = []
        wrong_row = []
        candidate_error_row = []
        candidate_spectrum_row = []
        valid_row = local_valid and leakage_valid
        for candidate in candidates:
            overlap_row.append(len(set(candidate) & set(planted)))
            indices = candidate + tuple(node_count + node for node in candidate)
            minimum, maximum, error = _covariance_block_error(
                base_joint, actual_joint, indices
            )
            candidate_error_row.append(float(error))
            candidate_spectrum_row.append((float(minimum), float(maximum)))
            if candidate == planted:
                wrong_row.append(0.0)
                continue
            integration_upper, valid = _zero_cut_integration_bound(
                minimum, maximum, error, module_size
            )
            wrong_row.append(float(integration_upper ** (1.0 / 3.0)))
            valid_row = valid_row and valid
        maximum_wrong = max(wrong_row)
        overlap_rows.append(tuple(overlap_row))
        candidate_error_rows.append(tuple(candidate_error_row))
        candidate_spectrum_rows.append(tuple(candidate_spectrum_row))
        wrong_bound_rows.append(tuple(wrong_row))
        wrong_maxima.append(float(maximum_wrong))
        local_separations.append(float(planted_lower - maximum_wrong))
        all_valid = all_valid and valid_row

    planted_edge_penalties = [
        abs(transport_weight)
        + continuity_weight
        * (
            1.0
            - len(set(path[time]) & set(path[time + 1]))
            / len(set(path[time]) | set(path[time + 1]))
        )
        for time in range(len(path) - 1)
    ]
    incident_penalties = []
    for time in range(len(path)):
        penalty = 0.0
        if time > 0:
            penalty += planted_edge_penalties[time - 1]
        if time + 1 < len(path):
            penalty += planted_edge_penalties[time]
        incident_penalties.append(float(penalty))
    mismatch_margins = tuple(
        float(separation - penalty)
        for separation, penalty in zip(
            local_separations, incident_penalties, strict=True
        )
    )
    action_margin = min(mismatch_margins)
    return SupportResolvedMovingCliqueRecoveryBound(
        base=base,
        node_count=node_count,
        time_count=len(path),
        candidate_count=len(candidates),
        candidates=candidates,
        candidate_overlaps=tuple(overlap_rows),
        candidate_covariance_errors=tuple(candidate_error_rows),
        candidate_base_eigenvalue_bounds=tuple(candidate_spectrum_rows),
        incorrect_score_upper_bounds=tuple(wrong_bound_rows),
        planted_local_covariance_errors=tuple(planted_local_errors),
        planted_leakage_covariance_errors=tuple(planted_leakage_errors),
        planted_score_lower_bounds=tuple(planted_lowers),
        maximum_incorrect_score_upper_bounds=tuple(wrong_maxima),
        local_separations=tuple(local_separations),
        incident_edge_penalties=tuple(incident_penalties),
        per_time_mismatch_margins=mismatch_margins,
        maximum_planted_score_error=max(planted_errors),
        maximum_incorrect_score_upper_bound=max(wrong_maxima),
        minimum_local_separation=min(local_separations),
        per_mismatch_action_margin=float(action_margin),
        all_local_covariance_bounds_valid=all_valid,
        guarantees_unique_planted_path=bool(all_valid and action_margin > 0.0),
    )


def a_priori_support_moving_clique_recovery_bound(
    transition_perturbations: Sequence[ArrayLike],
    noise_perturbations: Sequence[ArrayLike],
    planted_path: Sequence[Sequence[int]],
    *,
    self_memory: float,
    internal_coupling: float,
    candidate_family: Sequence[Sequence[int]] | None = None,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> APrioriSupportMovingCliqueRecoveryBound:
    """Certify structured perturbations without propagating actual covariances.

    The inputs are the additive matrices ``E_t=A_t-A_t^0`` and
    ``F_t=Q_t-Q_t^0`` around the covariance-preserving moving-clique family.
    Candidate-local state and joint-covariance errors are bounded from row
    restrictions of ``A_t`` and compressions of the covariance forcing. If a
    candidate family is supplied, uniqueness is certified only within it.
    """
    time_count = len(planted_path)
    if (
        len(transition_perturbations) != time_count
        or len(noise_perturbations) != time_count
        or time_count < 1
    ):
        raise ValueError("perturbations and planted_path must have equal positive lengths")
    transition_errors = tuple(
        np.asarray(matrix, dtype=float) for matrix in transition_perturbations
    )
    noise_errors = tuple(
        np.asarray(matrix, dtype=float) for matrix in noise_perturbations
    )
    if transition_errors[0].ndim != 2 or transition_errors[0].shape[0] != transition_errors[0].shape[1]:
        raise ValueError("transition perturbations must be square matrices")
    node_count = transition_errors[0].shape[0]
    if any(
        matrix.shape != (node_count, node_count)
        for matrix in transition_errors + noise_errors
    ):
        raise ValueError("all perturbations must have equal square dimensions")
    if any(np.any(~np.isfinite(matrix)) for matrix in transition_errors + noise_errors):
        raise ValueError("perturbation matrices must be finite")
    if any(not np.allclose(matrix, matrix.T) for matrix in noise_errors):
        raise ValueError("noise perturbations must be symmetric")

    path = tuple(tuple(sorted({int(node) for node in subset})) for subset in planted_path)
    module_size = len(path[0])
    if module_size < 2 or node_count <= module_size:
        raise ValueError("require 2 <= module_size < node_count")
    if any(
        len(subset) != module_size
        or subset[0] < 0
        or subset[-1] >= node_count
        for subset in path
    ):
        raise ValueError("planted boundaries must be valid and equal in size")
    if continuity_weight < 0.0 or not np.isfinite(
        [transport_weight, continuity_weight]
    ).all():
        raise ValueError("action weights must be finite and continuity nonnegative")

    complete_candidates = tuple(combinations(range(node_count), module_size))
    if candidate_family is None:
        candidates = complete_candidates
    else:
        candidates = tuple(
            tuple(sorted({int(node) for node in candidate}))
            for candidate in candidate_family
        )
        if not candidates or len(set(candidates)) != len(candidates):
            raise ValueError("candidate_family must contain distinct candidates")
        if any(
            len(candidate) != module_size
            or candidate[0] < 0
            or candidate[-1] >= node_count
            for candidate in candidates
        ):
            raise ValueError("candidate boundaries must be valid and size matched")
        if any(planted not in candidates for planted in path):
            raise ValueError("candidate_family must contain every planted boundary")
    family_complete = set(candidates) == set(complete_candidates)

    overlaps = [
        len(set(path[time]) & set(path[time + 1]))
        for time in range(time_count - 1)
    ]
    base = covariance_preserving_moving_clique_bound(
        self_memory,
        internal_coupling,
        module_size,
        minimum_consecutive_overlap=min(overlaps, default=module_size),
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    base_transitions = tuple(
        _moving_clique_transition(
            node_count, planted, self_memory, internal_coupling
        )
        for planted in path
    )
    transitions = tuple(
        base_transition + error
        for base_transition, error in zip(
            base_transitions, transition_errors, strict=True
        )
    )
    base_noises = tuple(
        np.eye(node_count) - transition @ transition.T
        for transition in base_transitions
    )
    noises = tuple(
        base_noise + error
        for base_noise, error in zip(base_noises, noise_errors, strict=True)
    )
    valid_noises = all(np.linalg.eigvalsh(noise)[0] > 0.0 for noise in noises)
    if not valid_noises:
        raise ValueError("perturbed noise covariances must be positive definite")

    forcings = tuple(
        base_transition @ transition_error.T
        + transition_error @ base_transition.T
        + transition_error @ transition_error.T
        + noise_error
        for base_transition, transition_error, noise_error in zip(
            base_transitions, transition_errors, noise_errors, strict=True
        )
    )
    global_errors = [0.0]
    for transition, forcing in zip(transitions, forcings, strict=True):
        global_errors.append(
            float(
                np.linalg.norm(transition, ord=2) ** 2 * global_errors[-1]
                + np.linalg.norm(forcing, ord=2)
            )
        )

    def state_error_bound(time: int, subset: tuple[int, ...]) -> float:
        if time == 0:
            return 0.0
        previous_transition = transitions[time - 1]
        previous_forcing = forcings[time - 1]
        row_norm = np.linalg.norm(previous_transition[np.ix_(subset, range(node_count))], ord=2)
        forcing_norm = np.linalg.norm(previous_forcing[np.ix_(subset, subset)], ord=2)
        return float(row_norm**2 * global_errors[time - 1] + forcing_norm)

    planted_local_radii = []
    planted_leakage_radii = []
    candidate_radius_rows = []
    planted_lowers = []
    wrong_rows = []
    wrong_maxima = []
    local_separations = []
    overlap_rows = []
    all_valid = True
    all_nodes = tuple(range(node_count))
    for time, planted in enumerate(path):
        base_transition = base_transitions[time]
        transition = transitions[time]
        transition_error = transition_errors[time]
        base_joint = np.block(
            [
                [np.eye(node_count), base_transition.T],
                [base_transition, np.eye(node_count)],
            ]
        )

        current_local = state_error_bound(time, planted)
        next_local = state_error_bound(time + 1, planted)
        local_cross = float(
            np.linalg.norm(transition[np.ix_(planted, all_nodes)], ord=2)
            * global_errors[time]
            + np.linalg.norm(transition_error[np.ix_(planted, planted)], ord=2)
        )
        local_radius = _symmetric_block_norm_bound(
            current_local, next_local, local_cross
        )
        planted_local_radii.append(local_radius)

        leakage_cross = float(
            np.linalg.norm(transition[np.ix_(planted, all_nodes)], ord=2)
            * global_errors[time]
            + np.linalg.norm(transition_error[np.ix_(planted, all_nodes)], ord=2)
        )
        leakage_radius = _symmetric_block_norm_bound(
            global_errors[time], next_local, leakage_cross
        )
        planted_leakage_radii.append(leakage_radius)

        planted_indices = planted + tuple(node_count + node for node in planted)
        planted_block = base_joint[np.ix_(planted_indices, planted_indices)]
        planted_eigenvalues = np.linalg.eigvalsh(planted_block)
        local_minimum = float(planted_eigenvalues[0])
        local_maximum = float(planted_eigenvalues[-1])
        leakage_indices = all_nodes + tuple(node_count + node for node in planted)
        leakage_minimum = float(
            np.linalg.eigvalsh(base_joint[np.ix_(leakage_indices, leakage_indices)])[0]
        )
        planted_valid = local_radius < local_minimum and leakage_radius < leakage_minimum
        if planted_valid:
            local_logdet = -np.log1p(-local_radius / local_minimum) / np.log(2.0)
            leakage_logdet = (
                -np.log1p(-leakage_radius / leakage_minimum) / np.log(2.0)
            )
            integration_error = min(1.0, 4.0 * np.log(2.0) * local_logdet)
            independence_error = min(
                1.0,
                np.log(2.0)
                * (node_count + 2 * module_size)
                / module_size
                * leakage_logdet,
            )
            persistence_error = canonical_persistence_covariance_error_bound(
                minimum_eigenvalue=local_minimum,
                maximum_eigenvalue=local_maximum,
                covariance_spectral_error=local_radius,
            )
            planted_error = product_root_error_bound(
                (base.integration_strength, 1.0, base.persistence),
                (integration_error, independence_error, persistence_error),
            )
        else:
            planted_error = 1.0
        planted_lower = max(0.0, base.planted_local_score - planted_error)
        planted_lowers.append(float(planted_lower))

        radius_row = []
        wrong_row = []
        overlap_row = []
        valid_row = planted_valid
        for candidate in candidates:
            overlap_row.append(len(set(candidate) & set(planted)))
            current_candidate = state_error_bound(time, candidate)
            next_candidate = state_error_bound(time + 1, candidate)
            candidate_cross = float(
                np.linalg.norm(transition[np.ix_(candidate, all_nodes)], ord=2)
                * global_errors[time]
                + np.linalg.norm(
                    transition_error[np.ix_(candidate, candidate)], ord=2
                )
            )
            candidate_radius = _symmetric_block_norm_bound(
                current_candidate, next_candidate, candidate_cross
            )
            radius_row.append(candidate_radius)
            if candidate == planted:
                wrong_row.append(0.0)
                continue
            indices = candidate + tuple(node_count + node for node in candidate)
            eigenvalues = np.linalg.eigvalsh(base_joint[np.ix_(indices, indices)])
            integration_upper, valid = _zero_cut_integration_bound(
                float(eigenvalues[0]),
                float(eigenvalues[-1]),
                candidate_radius,
                module_size,
            )
            wrong_row.append(float(integration_upper ** (1.0 / 3.0)))
            valid_row = valid_row and valid
        maximum_wrong = max(wrong_row)
        candidate_radius_rows.append(tuple(radius_row))
        wrong_rows.append(tuple(wrong_row))
        overlap_rows.append(tuple(overlap_row))
        wrong_maxima.append(float(maximum_wrong))
        local_separations.append(float(planted_lower - maximum_wrong))
        all_valid = all_valid and valid_row

    edge_penalties = [
        abs(transport_weight)
        + continuity_weight
        * (
            1.0
            - len(set(path[time]) & set(path[time + 1]))
            / len(set(path[time]) | set(path[time + 1]))
        )
        for time in range(time_count - 1)
    ]
    incident_penalties = tuple(
        float(
            (edge_penalties[time - 1] if time > 0 else 0.0)
            + (edge_penalties[time] if time + 1 < time_count else 0.0)
        )
        for time in range(time_count)
    )
    mismatch_margins = tuple(
        float(separation - penalty)
        for separation, penalty in zip(
            local_separations, incident_penalties, strict=True
        )
    )
    action_margin = min(mismatch_margins)
    return APrioriSupportMovingCliqueRecoveryBound(
        base=base,
        node_count=node_count,
        time_count=time_count,
        candidate_count=len(candidates),
        candidates=candidates,
        candidate_overlaps=tuple(overlap_rows),
        global_state_covariance_error_bounds=tuple(global_errors),
        planted_local_joint_error_bounds=tuple(planted_local_radii),
        planted_leakage_joint_error_bounds=tuple(planted_leakage_radii),
        candidate_joint_error_bounds=tuple(candidate_radius_rows),
        planted_score_lower_bounds=tuple(planted_lowers),
        incorrect_score_upper_bounds=tuple(wrong_rows),
        maximum_incorrect_score_upper_bounds=tuple(wrong_maxima),
        local_separations=tuple(local_separations),
        incident_edge_penalties=incident_penalties,
        per_time_mismatch_margins=mismatch_margins,
        per_mismatch_action_margin=float(action_margin),
        candidate_family_is_complete=family_complete,
        all_noise_covariances_positive_definite=valid_noises,
        all_local_covariance_bounds_valid=all_valid,
        guarantees_unique_planted_path_in_candidate_family=bool(
            all_valid and action_margin > 0.0
        ),
    )


def _feasible_overlap_pairs(
    node_count: int,
    module_size: int,
    planted_overlap: int,
) -> tuple[tuple[int, int], ...]:
    """Feasible overlaps of one candidate with two planted boundaries."""
    pairs = []
    for previous_overlap in range(module_size + 1):
        for current_overlap in range(module_size + 1):
            shared_lower = max(
                0,
                previous_overlap - (module_size - planted_overlap),
                current_overlap - (module_size - planted_overlap),
                previous_overlap + current_overlap - module_size,
            )
            shared_upper = min(
                planted_overlap,
                previous_overlap,
                current_overlap,
                node_count
                - 3 * module_size
                + planted_overlap
                + previous_overlap
                + current_overlap,
            )
            if shared_lower <= shared_upper:
                pairs.append((previous_overlap, current_overlap))
    return tuple(pairs)


def _moving_clique_row_norm(
    self_memory: float,
    internal_coupling: float,
    module_size: int,
    planted_overlap: int,
) -> float:
    """Norm of base-transition rows selected by an overlap class."""
    alpha = float(self_memory)
    beta = float(internal_coupling)
    if planted_overlap == 0:
        return abs(alpha)
    diagonal = alpha**2 + (module_size - 1) * beta**2
    off_diagonal = 2.0 * alpha * beta + (module_size - 2) * beta**2
    eigenvalues = [diagonal + (planted_overlap - 1) * off_diagonal]
    if planted_overlap > 1:
        eigenvalues.append(diagonal - off_diagonal)
    if planted_overlap < module_size:
        eigenvalues.append(alpha**2)
    return float(np.sqrt(max(0.0, *eigenvalues)))


def _moving_clique_within_norm(
    self_memory: float,
    internal_coupling: float,
    module_size: int,
    planted_overlap: int,
) -> float:
    """Norm of the base transition compressed to an overlap class."""
    alpha = float(self_memory)
    beta = float(internal_coupling)
    values = [abs(alpha)]
    if planted_overlap > 1:
        values.extend(
            [
                abs(alpha - beta),
                abs(alpha + (planted_overlap - 1) * beta),
            ]
        )
    return float(max(values))


def overlap_class_moving_clique_recovery_bound(
    node_count: int,
    planted_path: Sequence[Sequence[int]],
    *,
    self_memory: float,
    internal_coupling: float,
    transition_perturbation_bounds: ArrayLike,
    noise_perturbation_bounds: ArrayLike,
    row_transition_perturbation_bounds: ArrayLike,
    within_transition_perturbation_bounds: ArrayLike,
    local_noise_perturbation_bounds: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> OverlapClassMovingCliqueRecoveryBound:
    """Certify all fixed-size candidates from overlap-indexed norm budgets.

    Local radius tables have shape ``(time_count, module_size + 1)``. Entry
    ``[t, q]`` must bound every size-matched candidate whose overlap with the
    planted boundary at time ``t`` is ``q``. The function evaluates overlap
    classes and never constructs the individual candidates.
    """
    if isinstance(node_count, bool) or not isinstance(node_count, (int, np.integer)):
        raise TypeError("node_count must be an integer")
    time_count = len(planted_path)
    if time_count < 1:
        raise ValueError("planted_path must be nonempty")
    path = tuple(tuple(sorted({int(node) for node in subset})) for subset in planted_path)
    module_size = len(path[0])
    if module_size < 2 or node_count <= module_size:
        raise ValueError("require 2 <= module_size < node_count")
    if any(
        len(subset) != module_size
        or subset[0] < 0
        or subset[-1] >= node_count
        for subset in path
    ):
        raise ValueError("planted boundaries must be valid and equal in size")
    if continuity_weight < 0.0 or not np.isfinite(
        [transport_weight, continuity_weight]
    ).all():
        raise ValueError("action weights must be finite and continuity nonnegative")

    global_transition = np.asarray(transition_perturbation_bounds, dtype=float)
    global_noise = np.asarray(noise_perturbation_bounds, dtype=float)
    row_transition = np.asarray(row_transition_perturbation_bounds, dtype=float)
    within_transition = np.asarray(
        within_transition_perturbation_bounds, dtype=float
    )
    local_noise = np.asarray(local_noise_perturbation_bounds, dtype=float)
    if global_transition.shape != (time_count,) or global_noise.shape != (time_count,):
        raise ValueError("global perturbation bounds must have shape (time_count,)")
    local_shape = (time_count, module_size + 1)
    if any(
        table.shape != local_shape
        for table in (row_transition, within_transition, local_noise)
    ):
        raise ValueError(
            "local perturbation tables must have shape "
            "(time_count, module_size + 1)"
        )
    radius_arrays = (
        global_transition,
        global_noise,
        row_transition,
        within_transition,
        local_noise,
    )
    if any(np.any(~np.isfinite(array)) or np.any(array < 0.0) for array in radius_arrays):
        raise ValueError("perturbation bounds must be finite and nonnegative")
    if np.any(row_transition > global_transition[:, None] + 1e-15):
        raise ValueError("row transition bounds cannot exceed global bounds")
    if np.any(within_transition > row_transition + 1e-15):
        raise ValueError("within transition bounds cannot exceed row bounds")
    if np.any(local_noise > global_noise[:, None] + 1e-15):
        raise ValueError("local noise bounds cannot exceed global bounds")

    consecutive_overlaps = [
        len(set(path[time]) & set(path[time + 1]))
        for time in range(time_count - 1)
    ]
    base = covariance_preserving_moving_clique_bound(
        self_memory,
        internal_coupling,
        module_size,
        minimum_consecutive_overlap=min(consecutive_overlaps, default=module_size),
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    alpha = float(self_memory)
    beta = float(internal_coupling)
    base_norm = max(
        abs(alpha),
        abs(alpha - beta),
        abs(alpha + (module_size - 1) * beta),
    )
    base_noise_minimum = 1.0 - base_norm**2
    valid_noise_classes = bool(np.all(global_noise < base_noise_minimum))

    overlap_minimum = max(0, 2 * module_size - node_count)
    overlap_values = tuple(range(overlap_minimum, module_size + 1))
    multiplicities = tuple(
        comb(module_size, overlap)
        * comb(node_count - module_size, module_size - overlap)
        for overlap in overlap_values
    )
    feasible_pairs = tuple(
        _feasible_overlap_pairs(node_count, module_size, overlap)
        for overlap in consecutive_overlaps
    )
    base_row_norms = tuple(
        _moving_clique_row_norm(alpha, beta, module_size, overlap)
        for overlap in range(module_size + 1)
    )
    base_within_norms = tuple(
        _moving_clique_within_norm(alpha, beta, module_size, overlap)
        for overlap in range(module_size + 1)
    )

    global_errors = [0.0]
    local_next_errors = []
    for time in range(time_count):
        gamma = float(global_transition[time])
        nu = float(global_noise[time])
        global_forcing = 2.0 * base_norm * gamma + gamma**2 + nu
        global_errors.append(
            float((base_norm + gamma) ** 2 * global_errors[-1] + global_forcing)
        )
        local_row = []
        for overlap in range(module_size + 1):
            row_error = float(row_transition[time, overlap])
            local_forcing = (
                2.0 * base_row_norms[overlap] * row_error
                + row_error**2
                + float(local_noise[time, overlap])
            )
            local_row.append(
                float(
                    (base_row_norms[overlap] + row_error) ** 2
                    * global_errors[time]
                    + local_forcing
                )
            )
        local_next_errors.append(tuple(local_row))

    def current_class_error(time: int, overlap: int) -> float:
        if time == 0:
            return 0.0
        previous_values = [
            local_next_errors[time - 1][previous_overlap]
            for previous_overlap, current_overlap in feasible_pairs[time - 1]
            if current_overlap == overlap
        ]
        if not previous_values:
            raise RuntimeError("overlap occupancy calculation produced an empty class")
        return float(max(previous_values))

    planted_local_radii = []
    planted_leakage_radii = []
    class_radius_rows = []
    planted_lowers = []
    wrong_rows = []
    wrong_maxima = []
    local_separations = []
    all_valid = valid_noise_classes
    for time in range(time_count):
        if time == 0:
            planted_current = 0.0
        else:
            planted_current = local_next_errors[time - 1][
                consecutive_overlaps[time - 1]
            ]
        planted_next = local_next_errors[time][module_size]
        planted_cross = (
            (base_row_norms[module_size] + row_transition[time, module_size])
            * global_errors[time]
            + within_transition[time, module_size]
        )
        planted_radius = _symmetric_block_norm_bound(
            planted_current, planted_next, float(planted_cross)
        )
        planted_local_radii.append(planted_radius)
        leakage_cross = (
            (base_row_norms[module_size] + row_transition[time, module_size])
            * global_errors[time]
            + row_transition[time, module_size]
        )
        leakage_radius = _symmetric_block_norm_bound(
            global_errors[time], planted_next, float(leakage_cross)
        )
        planted_leakage_radii.append(leakage_radius)

        planted_minimum = 1.0 - base_within_norms[module_size]
        planted_maximum = 1.0 + base_within_norms[module_size]
        planted_valid = (
            planted_radius < planted_minimum
            and leakage_radius < 1.0 - base_norm
        )
        if planted_valid:
            local_logdet = -np.log1p(-planted_radius / planted_minimum) / np.log(2.0)
            leakage_logdet = (
                -np.log1p(-leakage_radius / (1.0 - base_norm)) / np.log(2.0)
            )
            integration_error = min(1.0, 4.0 * np.log(2.0) * local_logdet)
            independence_error = min(
                1.0,
                np.log(2.0)
                * (node_count + 2 * module_size)
                / module_size
                * leakage_logdet,
            )
            persistence_error = canonical_persistence_covariance_error_bound(
                minimum_eigenvalue=planted_minimum,
                maximum_eigenvalue=planted_maximum,
                covariance_spectral_error=planted_radius,
            )
            planted_error = product_root_error_bound(
                (base.integration_strength, 1.0, base.persistence),
                (integration_error, independence_error, persistence_error),
            )
        else:
            planted_error = 1.0
        planted_lower = max(0.0, base.planted_local_score - planted_error)
        planted_lowers.append(float(planted_lower))

        class_radii = []
        class_scores = []
        valid_row = planted_valid
        for overlap in overlap_values:
            current_error = current_class_error(time, overlap)
            next_error = local_next_errors[time][overlap]
            cross_error = (
                (base_row_norms[overlap] + row_transition[time, overlap])
                * global_errors[time]
                + within_transition[time, overlap]
            )
            class_radius = _symmetric_block_norm_bound(
                current_error, next_error, float(cross_error)
            )
            class_radii.append(class_radius)
            if overlap == module_size:
                class_scores.append(0.0)
                continue
            class_minimum = 1.0 - base_within_norms[overlap]
            class_maximum = 1.0 + base_within_norms[overlap]
            integration_upper, valid = _zero_cut_integration_bound(
                class_minimum, class_maximum, class_radius, module_size
            )
            class_scores.append(float(integration_upper ** (1.0 / 3.0)))
            valid_row = valid_row and valid
        maximum_wrong = max(
            score
            for overlap, score in zip(overlap_values, class_scores, strict=True)
            if overlap < module_size
        )
        class_radius_rows.append(tuple(class_radii))
        wrong_rows.append(tuple(class_scores))
        wrong_maxima.append(float(maximum_wrong))
        local_separations.append(float(planted_lower - maximum_wrong))
        all_valid = all_valid and valid_row

    edge_penalties = [
        abs(transport_weight)
        + continuity_weight
        * (
            1.0
            - overlap / (2 * module_size - overlap)
        )
        for overlap in consecutive_overlaps
    ]
    incident_penalties = tuple(
        float(
            (edge_penalties[time - 1] if time > 0 else 0.0)
            + (edge_penalties[time] if time + 1 < time_count else 0.0)
        )
        for time in range(time_count)
    )
    mismatch_margins = tuple(
        float(separation - penalty)
        for separation, penalty in zip(
            local_separations, incident_penalties, strict=True
        )
    )
    action_margin = min(mismatch_margins)
    return OverlapClassMovingCliqueRecoveryBound(
        base=base,
        node_count=node_count,
        time_count=time_count,
        module_size=module_size,
        candidate_count=comb(node_count, module_size),
        overlap_class_count=len(overlap_values),
        overlap_values=overlap_values,
        overlap_class_multiplicities=multiplicities,
        feasible_consecutive_overlap_pairs=feasible_pairs,
        global_state_covariance_error_bounds=tuple(global_errors),
        local_next_state_error_bounds=tuple(local_next_errors),
        planted_local_joint_error_bounds=tuple(planted_local_radii),
        planted_leakage_joint_error_bounds=tuple(planted_leakage_radii),
        overlap_class_joint_error_bounds=tuple(class_radius_rows),
        planted_score_lower_bounds=tuple(planted_lowers),
        incorrect_score_upper_bounds=tuple(wrong_rows),
        maximum_incorrect_score_upper_bounds=tuple(wrong_maxima),
        local_separations=tuple(local_separations),
        incident_edge_penalties=incident_penalties,
        per_time_mismatch_margins=mismatch_margins,
        per_mismatch_action_margin=float(action_margin),
        all_noise_covariance_classes_valid=valid_noise_classes,
        all_local_covariance_bounds_valid=all_valid,
        guarantees_unique_planted_path=bool(all_valid and action_margin > 0.0),
    )
