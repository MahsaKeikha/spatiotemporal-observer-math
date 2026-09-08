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
    transport_metrics_from_covariances,
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


@dataclass(frozen=True)
class GaussianSafeNearCompetitorScreen:
    """Near-competitor screen derived from first-split Gaussian concentration."""

    screen: NearCompetitorScreen
    screening_sample_count: int
    screening_confidence: float
    covariance_spectral_errors: np.ndarray
    maximum_covariance_spectral_error: float
    screening_local_factor_errors: np.ndarray
    screening_transport_factor_errors: np.ndarray
    screening_local_score_errors: np.ndarray
    screening_transport_score_errors: np.ndarray
    total_local_score_errors: np.ndarray
    total_transport_score_errors: np.ndarray
    positive_local_factor_floor_mask: np.ndarray
    positive_transport_factor_floor_mask: np.ndarray
    structural_integration_null_mask: np.ndarray
    null_local_score_errors: np.ndarray
    all_blocks_valid: bool
    guarantees_safe_screen: bool


@dataclass(frozen=True)
class GaussianRelativeNearCompetitorScreen:
    """Gaussian screen certified by population-whitened covariance errors."""

    screen: NearCompetitorScreen
    screening_sample_count: int
    screening_confidence: float
    covariance_relative_errors: np.ndarray
    maximum_covariance_relative_error: float
    screening_local_factor_errors: np.ndarray
    screening_transport_factor_errors: np.ndarray
    screening_local_score_errors: np.ndarray
    screening_transport_score_errors: np.ndarray
    total_local_score_errors: np.ndarray
    total_transport_score_errors: np.ndarray
    positive_local_factor_floor_mask: np.ndarray
    positive_transport_factor_floor_mask: np.ndarray
    structural_integration_null_mask: np.ndarray
    null_local_score_errors: np.ndarray
    all_blocks_valid: bool
    guarantees_safe_screen: bool


@dataclass(frozen=True)
class GaussianTemporalCorrelationEnvelope:
    """Norm and effective-sample bounds for Gaussian temporal correlation."""

    sample_count: int
    autocorrelation: float
    frobenius_norm_bound: float
    spectral_norm_bound: float
    variance_effective_sample_size: float
    operator_effective_sample_size: float


@dataclass(frozen=True)
class GaussianCenteredTemporalCorrelationEnvelope:
    """Centering normalization and norm bounds for temporal correlation."""

    sample_count: int
    autocorrelation: float
    centering_degrees_of_freedom: float
    projected_frobenius_norm_bound: float
    projected_spectral_norm_bound: float
    variance_effective_sample_size: float
    operator_effective_sample_size: float


@dataclass(frozen=True)
class GaussianAR1AutocorrelationInterval:
    """Finite-sample interval from standardized Gaussian increment energy."""

    sample_count: int
    channel_count: int
    confidence: float
    declared_upper_bound: float
    estimate: float
    error_radius: float
    lower_bound: float
    upper_bound: float
    interval_intersects_declared_model: bool


@dataclass(frozen=True)
class GaussianEstimatedAR1CenteredCovarianceBound:
    """Centered covariance bound after estimating a common AR(1) coefficient."""

    autocorrelation_interval: GaussianAR1AutocorrelationInterval
    covariance_confidence: float
    combined_confidence: float
    covariance_sample_count: int
    centering_degrees_of_freedom_lower_bound: float
    centering_degrees_of_freedom_upper_bound: float
    reference_centering_degrees_of_freedom: float
    temporal_frobenius_norm_bound: float
    temporal_spectral_norm_bound: float
    oracle_normalized_covariance_error: float
    normalization_error: float
    covariance_relative_error: float
    variance_effective_sample_size_lower_bound: float
    operator_effective_sample_size_lower_bound: float


@dataclass(frozen=True)
class GaussianDependentRelativeNearCompetitorScreen:
    """Relative screen for separably correlated Gaussian observations."""

    screen: NearCompetitorScreen
    sample_count: int
    confidence: float
    temporal_correlation_frobenius_norm: float
    temporal_correlation_spectral_norm: float
    variance_effective_sample_size: float
    operator_effective_sample_size: float
    covariance_relative_errors: np.ndarray
    maximum_covariance_relative_error: float
    screening_local_factor_errors: np.ndarray
    screening_transport_factor_errors: np.ndarray
    screening_local_score_errors: np.ndarray
    screening_transport_score_errors: np.ndarray
    total_local_score_errors: np.ndarray
    total_transport_score_errors: np.ndarray
    positive_local_factor_floor_mask: np.ndarray
    positive_transport_factor_floor_mask: np.ndarray
    structural_integration_null_mask: np.ndarray
    null_local_score_errors: np.ndarray
    all_blocks_valid: bool
    guarantees_safe_screen: bool


@dataclass(frozen=True)
class GaussianCenteredDependentRelativeNearCompetitorScreen:
    """Relative screen for mean-centered separably correlated Gaussians."""

    screen: NearCompetitorScreen
    sample_count: int
    confidence: float
    centering_degrees_of_freedom: float
    projected_temporal_frobenius_norm: float
    projected_temporal_spectral_norm: float
    variance_effective_sample_size: float
    operator_effective_sample_size: float
    covariance_relative_errors: np.ndarray
    maximum_covariance_relative_error: float
    screening_local_factor_errors: np.ndarray
    screening_transport_factor_errors: np.ndarray
    screening_local_score_errors: np.ndarray
    screening_transport_score_errors: np.ndarray
    total_local_score_errors: np.ndarray
    total_transport_score_errors: np.ndarray
    positive_local_factor_floor_mask: np.ndarray
    positive_transport_factor_floor_mask: np.ndarray
    structural_integration_null_mask: np.ndarray
    null_local_score_errors: np.ndarray
    all_blocks_valid: bool
    guarantees_safe_screen: bool


@dataclass(frozen=True)
class GaussianEstimatedAR1CenteredRelativeNearCompetitorScreen:
    """Complete screen using an estimated nonnegative AR(1) envelope."""

    screen: NearCompetitorScreen
    covariance_bound: GaussianEstimatedAR1CenteredCovarianceBound
    covariance_relative_errors: np.ndarray
    screening_local_factor_errors: np.ndarray
    screening_transport_factor_errors: np.ndarray
    screening_local_score_errors: np.ndarray
    screening_transport_score_errors: np.ndarray
    total_local_score_errors: np.ndarray
    total_transport_score_errors: np.ndarray
    positive_local_factor_floor_mask: np.ndarray
    positive_transport_factor_floor_mask: np.ndarray
    structural_integration_null_mask: np.ndarray
    null_local_score_errors: np.ndarray
    all_blocks_valid: bool
    guarantees_safe_screen: bool


@dataclass(frozen=True)
class GaussianCrossFittedRelativeNearCompetitorScreen:
    """Observable relative screen using a Gaussian pilot covariance."""

    screen: NearCompetitorScreen
    pilot_sample_count: int
    pilot_confidence: float
    pilot_covariance_relative_error: float
    observed_pilot_relative_errors: np.ndarray
    covariance_relative_errors: np.ndarray
    maximum_covariance_relative_error: float
    screening_local_factor_errors: np.ndarray
    screening_transport_factor_errors: np.ndarray
    screening_local_score_errors: np.ndarray
    screening_transport_score_errors: np.ndarray
    total_local_score_errors: np.ndarray
    total_transport_score_errors: np.ndarray
    positive_local_factor_floor_mask: np.ndarray
    positive_transport_factor_floor_mask: np.ndarray
    structural_integration_null_mask: np.ndarray
    null_local_score_errors: np.ndarray
    all_pilot_blocks_positive_definite: bool
    all_blocks_valid: bool
    guarantees_safe_screen: bool


@dataclass(frozen=True)
class GaussianDriftRobustRelativeNearCompetitorScreen:
    """Pilot-normalized screen with a declared population-drift envelope."""

    screen: NearCompetitorScreen
    pilot_sample_count: int
    pilot_confidence: float
    pilot_covariance_relative_error: float
    observed_pilot_relative_errors: np.ndarray
    same_population_relative_errors: np.ndarray
    population_drift_relative_errors: np.ndarray
    covariance_relative_errors: np.ndarray
    maximum_population_drift_relative_error: float
    maximum_covariance_relative_error: float
    screening_local_factor_errors: np.ndarray
    screening_transport_factor_errors: np.ndarray
    screening_local_score_errors: np.ndarray
    screening_transport_score_errors: np.ndarray
    total_local_score_errors: np.ndarray
    total_transport_score_errors: np.ndarray
    positive_local_factor_floor_mask: np.ndarray
    positive_transport_factor_floor_mask: np.ndarray
    structural_integration_null_mask: np.ndarray
    null_local_score_errors: np.ndarray
    all_pilot_blocks_positive_definite: bool
    all_drift_envelopes_valid: bool
    all_blocks_valid: bool
    guarantees_safe_screen: bool


@dataclass(frozen=True)
class GaussianCalibratedPopulationDrift:
    """Finite-sample candidate-block population-drift envelope."""

    reference_sample_count: int
    current_sample_count: int
    reference_confidence: float
    current_confidence: float
    overall_confidence_lower_bound: float
    reference_covariance_relative_error: float
    current_covariance_relative_error: float
    observed_reference_relative_errors: np.ndarray
    population_drift_relative_errors: np.ndarray
    maximum_population_drift_relative_error: float
    all_reference_blocks_positive_definite: bool
    all_bounds_valid: bool


@dataclass(frozen=True)
class GaussianCalibratedDriftRelativeNearCompetitorScreen:
    """End-to-end screen with a statistically calibrated drift envelope."""

    drift_calibration: GaussianCalibratedPopulationDrift
    screening: GaussianDriftRobustRelativeNearCompetitorScreen
    requested_confidence: float
    component_confidence: float
    overall_confidence_lower_bound: float
    guarantees_safe_screen: bool


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


def gaussian_relative_cmi_covariance_error_bound(
    x_dimension: int,
    y_dimension: int,
    given_dimension: int,
    *,
    covariance_relative_error: float,
) -> float:
    """Bound Gaussian CMI error on a relative covariance event.

    The event is ``||Sigma^(-1/2) (Sigma_hat-Sigma) Sigma^(-1/2)||_2 <= delta``.
    Unlike the absolute-error bound, this statement has no population condition
    number. The result is in bits.
    """
    dimensions = (x_dimension, y_dimension, given_dimension)
    if x_dimension < 1 or y_dimension < 1 or given_dimension < 0:
        raise ValueError("require positive x/y dimensions and nonnegative given dimension")
    if any(int(value) != value for value in dimensions):
        raise ValueError("dimensions must be integers")
    if not np.isfinite(covariance_relative_error) or not (
        0.0 <= covariance_relative_error < 1.0
    ):
        raise ValueError("covariance_relative_error must lie in [0, 1)")
    logdet_factor = -np.log1p(-covariance_relative_error) / np.log(2.0)
    return float((x_dimension + y_dimension + 2 * given_dimension) * logdet_factor)


def gaussian_null_cmi_covariance_error_bound(
    canonical_rank: int,
    *,
    minimum_eigenvalue: float,
    maximum_eigenvalue: float,
    covariance_spectral_error: float,
) -> float:
    """Bound empirical Gaussian CMI when population conditional CMI is zero.

    The population conditional cross-covariance is assumed to vanish. The
    result controls the perturbed CMI in bits and is quadratic in the covariance
    radius near zero. ``np.inf`` is returned when the derived conditional
    canonical-correlation radius reaches one.
    """
    if isinstance(canonical_rank, bool) or not isinstance(
        canonical_rank, (int, np.integer)
    ):
        raise TypeError("canonical_rank must be an integer")
    if canonical_rank < 1:
        raise ValueError("canonical_rank must be positive")
    if not (
        np.isfinite(minimum_eigenvalue)
        and np.isfinite(maximum_eigenvalue)
        and 0.0 < minimum_eigenvalue <= maximum_eigenvalue
    ):
        raise ValueError("require finite 0 < minimum_eigenvalue <= maximum_eigenvalue")
    if not (
        np.isfinite(covariance_spectral_error)
        and 0.0 <= covariance_spectral_error < minimum_eigenvalue
    ):
        raise ValueError("covariance_spectral_error must lie in [0, minimum_eigenvalue)")
    eta = float(covariance_spectral_error)
    if eta == 0.0:
        return 0.0
    lower = float(minimum_eigenvalue)
    upper = float(maximum_eigenvalue)
    perturbed_lower = lower - eta
    conditional_cross_error = eta * (
        1.0
        + (upper + eta) / perturbed_lower
        + upper * (upper + eta) / (lower * perturbed_lower)
        + upper / lower
    )
    canonical_radius = conditional_cross_error / perturbed_lower
    if canonical_radius >= 1.0:
        return float(np.inf)
    return float(
        -canonical_rank
        * np.log1p(-(canonical_radius**2))
        / (2.0 * np.log(2.0))
    )


def gaussian_null_integration_factor_error_bound(
    subset_size: int,
    *,
    minimum_eigenvalue: float,
    maximum_eigenvalue: float,
    covariance_spectral_error: float,
) -> float:
    """Bound an empirical integration factor at an exact population null."""
    if isinstance(subset_size, bool) or not isinstance(subset_size, (int, np.integer)):
        raise TypeError("subset_size must be an integer")
    if subset_size < 2:
        raise ValueError("subset_size must be at least two")
    rank = subset_size // 2
    one_direction = gaussian_null_cmi_covariance_error_bound(
        rank,
        minimum_eigenvalue=minimum_eigenvalue,
        maximum_eigenvalue=maximum_eigenvalue,
        covariance_spectral_error=covariance_spectral_error,
    )
    if not np.isfinite(one_direction):
        return 1.0
    directed_bits_per_node = 2.0 * one_direction / subset_size
    return float(min(1.0, 1.0 - 2.0 ** (-directed_bits_per_node)))


def gaussian_relative_null_cmi_covariance_error_bound(
    canonical_rank: int,
    *,
    covariance_relative_error: float,
) -> float:
    """Bound empirical Gaussian CMI at a population conditional null.

    Schur-complement monotonicity transfers the relative event to the
    conditional covariance. The resulting conditional canonical correlations
    are at most ``delta / (1-delta)``. The bound is in bits.
    """
    if isinstance(canonical_rank, bool) or not isinstance(
        canonical_rank, (int, np.integer)
    ):
        raise TypeError("canonical_rank must be an integer")
    if canonical_rank < 1:
        raise ValueError("canonical_rank must be positive")
    if not np.isfinite(covariance_relative_error) or not (
        0.0 <= covariance_relative_error < 1.0
    ):
        raise ValueError("covariance_relative_error must lie in [0, 1)")
    delta = float(covariance_relative_error)
    canonical_radius = delta / (1.0 - delta)
    if canonical_radius >= 1.0:
        return float(np.inf)
    return float(
        -canonical_rank
        * np.log1p(-(canonical_radius**2))
        / (2.0 * np.log(2.0))
    )


def gaussian_relative_null_integration_factor_error_bound(
    subset_size: int,
    *,
    covariance_relative_error: float,
) -> float:
    """Bound an empirical integration factor at a relative-event null."""
    if isinstance(subset_size, bool) or not isinstance(subset_size, (int, np.integer)):
        raise TypeError("subset_size must be an integer")
    if subset_size < 2:
        raise ValueError("subset_size must be at least two")
    one_direction = gaussian_relative_null_cmi_covariance_error_bound(
        subset_size // 2,
        covariance_relative_error=covariance_relative_error,
    )
    if not np.isfinite(one_direction):
        return 1.0
    directed_bits_per_node = 2.0 * one_direction / subset_size
    return float(min(1.0, 1.0 - 2.0 ** (-directed_bits_per_node)))


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


def canonical_persistence_relative_covariance_error_bound(
    *, covariance_relative_error: float
) -> float:
    """Bound canonical-persistence error on a relative covariance event.

    Separate population whitening makes both marginal covariances identities.
    The relative joint event bounds each marginal perturbation by ``delta`` and
    the normalized cross perturbation by ``2 delta``. This bound is therefore
    independent of the covariance condition number.
    """
    if not np.isfinite(covariance_relative_error) or not (
        0.0 <= covariance_relative_error < 1.0
    ):
        raise ValueError("covariance_relative_error must lie in [0, 1)")
    delta = float(covariance_relative_error)
    inverse_sqrt_norm = 1.0 / np.sqrt(1.0 - delta)
    inverse_sqrt_error = inverse_sqrt_norm - 1.0
    whitened_error = (
        inverse_sqrt_error * (1.0 + 2.0 * delta) * inverse_sqrt_norm
        + 2.0 * delta * inverse_sqrt_norm
        + inverse_sqrt_error
    )
    return float(min(1.0, 2.0 * whitened_error))


def gaussian_wishart_relative_covariance_error_bound(
    block_dimension: int,
    block_count: int,
    sample_count: int,
    *,
    confidence: float = 0.975,
) -> float:
    """Return a simultaneous population-whitened Wishart covariance radius."""
    integer_values = (block_dimension, block_count, sample_count)
    if any(
        isinstance(value, bool) or not isinstance(value, (int, np.integer))
        for value in integer_values
    ):
        raise TypeError("dimensions, block count, and sample count must be integers")
    if block_dimension < 1 or block_count < 1 or sample_count < 2:
        raise ValueError("require positive dimensions/counts and sample_count >= 2")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    deviation = (
        np.sqrt(block_dimension)
        + np.sqrt(2.0 * np.log(2.0 * block_count / (1.0 - confidence)))
    ) / np.sqrt(sample_count - 1)
    return float(2.0 * deviation + deviation**2)


def gaussian_ar1_temporal_correlation_envelope(
    sample_count: int,
    autocorrelation: float,
) -> GaussianTemporalCorrelationEnvelope:
    """Return exact Frobenius and safe spectral bounds for AR(1) correlation."""
    if isinstance(sample_count, bool) or not isinstance(
        sample_count, (int, np.integer)
    ):
        raise TypeError("sample_count must be an integer")
    if sample_count < 1:
        raise ValueError("sample_count must be positive")
    if not np.isfinite(autocorrelation) or not -1.0 < autocorrelation < 1.0:
        raise ValueError("autocorrelation must lie in (-1, 1)")
    magnitude = abs(float(autocorrelation))
    squared = magnitude**2
    if squared == 0.0 or sample_count == 1:
        frobenius_squared = float(sample_count)
    else:
        power = squared ** (sample_count - 1)
        geometric = squared * (1.0 - power) / (1.0 - squared)
        weighted = squared * (
            1.0
            - sample_count * power
            + (sample_count - 1) * power * squared
        ) / (1.0 - squared) ** 2
        frobenius_squared = float(
            sample_count + 2.0 * (sample_count * geometric - weighted)
        )
    frobenius = float(np.sqrt(frobenius_squared))
    spectral = float(
        min(sample_count, (1.0 + magnitude) / (1.0 - magnitude))
    )
    return GaussianTemporalCorrelationEnvelope(
        sample_count=int(sample_count),
        autocorrelation=float(autocorrelation),
        frobenius_norm_bound=frobenius,
        spectral_norm_bound=spectral,
        variance_effective_sample_size=float(sample_count**2 / frobenius_squared),
        operator_effective_sample_size=float(sample_count / spectral),
    )


def gaussian_ar1_centered_temporal_correlation_envelope(
    sample_count: int,
    autocorrelation: float,
) -> GaussianCenteredTemporalCorrelationEnvelope:
    """Return a safe AR(1) envelope after empirical mean removal.

    The exact projected matrix is ``P @ R @ P``. Its norms are bounded here by
    the corresponding norms of ``R``; the centering normalization
    ``trace(P @ R)`` is evaluated exactly.
    """
    temporal = gaussian_ar1_temporal_correlation_envelope(
        sample_count, autocorrelation
    )
    if sample_count < 2:
        raise ValueError("mean-centered covariance requires sample_count >= 2")
    phi = float(autocorrelation)
    if phi == 0.0:
        off_diagonal_sum = 0.0
    else:
        power = phi ** (sample_count - 1)
        geometric = phi * (1.0 - power) / (1.0 - phi)
        weighted = phi * (
            1.0
            - sample_count * power
            + (sample_count - 1) * power * phi
        ) / (1.0 - phi) ** 2
        off_diagonal_sum = sample_count * geometric - weighted
    all_entries_sum = sample_count + 2.0 * off_diagonal_sum
    degrees = float(sample_count - all_entries_sum / sample_count)
    if not degrees > 0.0:
        raise ValueError("temporal correlation leaves no centered degrees of freedom")
    frobenius = temporal.frobenius_norm_bound
    spectral = temporal.spectral_norm_bound
    return GaussianCenteredTemporalCorrelationEnvelope(
        sample_count=int(sample_count),
        autocorrelation=phi,
        centering_degrees_of_freedom=degrees,
        projected_frobenius_norm_bound=frobenius,
        projected_spectral_norm_bound=spectral,
        variance_effective_sample_size=float(degrees**2 / frobenius**2),
        operator_effective_sample_size=float(degrees / spectral),
    )


def separable_gaussian_centered_covariance(
    observations: ArrayLike,
    centering_degrees_of_freedom: float,
) -> np.ndarray:
    """Estimate spatial covariance after mean removal under known separability."""
    values = np.asarray(observations, dtype=float)
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 1:
        raise ValueError("observations must have shape (sample_count, dimension)")
    if not np.all(np.isfinite(values)):
        raise ValueError("observations must be finite")
    degrees = float(centering_degrees_of_freedom)
    if not np.isfinite(degrees) or not degrees > 0.0:
        raise ValueError("centering_degrees_of_freedom must be positive and finite")
    centered = values - np.mean(values, axis=0, keepdims=True)
    return centered.T @ centered / degrees


def gaussian_dependent_centered_relative_covariance_error_bound(
    block_dimension: int,
    block_count: int,
    *,
    centering_degrees_of_freedom: float,
    projected_temporal_frobenius_norm: float,
    projected_temporal_spectral_norm: float,
    confidence: float = 0.975,
) -> float:
    """Bound relative error for a mean-centered separable Gaussian covariance."""
    integer_values = (block_dimension, block_count)
    if any(
        isinstance(value, bool) or not isinstance(value, (int, np.integer))
        for value in integer_values
    ):
        raise TypeError("block dimension and block count must be integers")
    if block_dimension < 1 or block_count < 1:
        raise ValueError("block dimension and block count must be positive")
    degrees = float(centering_degrees_of_freedom)
    frobenius = float(projected_temporal_frobenius_norm)
    spectral = float(projected_temporal_spectral_norm)
    if not all(np.isfinite(value) and value > 0.0 for value in (degrees, frobenius, spectral)):
        raise ValueError("centering normalization and projected norms must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    tail = np.log(2.0 * block_count * 9.0**block_dimension / (1.0 - confidence))
    return float(4.0 * (frobenius * np.sqrt(tail) + spectral * tail) / degrees)


def gaussian_ar1_increment_autocorrelation_interval(
    standardized_observations: ArrayLike,
    *,
    declared_upper_bound: float,
    confidence: float = 0.9875,
) -> GaussianAR1AutocorrelationInterval:
    """Estimate a shared nonnegative AR(1) coefficient from increments.

    Columns must be independent, unit-variance Gaussian calibration channels
    sharing one AR(1) coefficient. Constant channel means are unrestricted.
    """
    values = np.asarray(standardized_observations, dtype=float)
    if values.ndim == 1:
        values = values[:, None]
    if values.ndim != 2 or values.shape[0] < 2 or values.shape[1] < 1:
        raise ValueError("standardized_observations must have shape (N, K), N >= 2")
    if not np.all(np.isfinite(values)):
        raise ValueError("standardized_observations must be finite")
    upper_prior = float(declared_upper_bound)
    if not np.isfinite(upper_prior) or not 0.0 < upper_prior < 1.0:
        raise ValueError("declared_upper_bound must lie in (0, 1)")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    sample_count, channel_count = values.shape
    increments = np.diff(values, axis=0)
    increment_energy = float(np.sum(increments**2))
    pair_count = (sample_count - 1) * channel_count
    estimate = float(1.0 - increment_energy / (2.0 * pair_count))
    tail = float(np.log(2.0 / (1.0 - confidence)))
    error = float(np.sqrt(6.0 * tail / pair_count) + 4.0 * tail / pair_count)
    raw_lower = estimate - error
    raw_upper = estimate + error
    intersects = bool(raw_upper >= 0.0 and raw_lower <= upper_prior)
    if intersects:
        lower = max(0.0, raw_lower)
        upper = min(upper_prior, raw_upper)
    else:
        lower = 0.0
        upper = upper_prior
    return GaussianAR1AutocorrelationInterval(
        sample_count=int(sample_count),
        channel_count=int(channel_count),
        confidence=float(confidence),
        declared_upper_bound=upper_prior,
        estimate=estimate,
        error_radius=error,
        lower_bound=float(lower),
        upper_bound=float(upper),
        interval_intersects_declared_model=intersects,
    )


def gaussian_estimated_ar1_centered_covariance_bound(
    block_dimension: int,
    block_count: int,
    covariance_sample_count: int,
    autocorrelation_interval: GaussianAR1AutocorrelationInterval,
    *,
    covariance_confidence: float = 0.9875,
) -> GaussianEstimatedAR1CenteredCovarianceBound:
    """Compose AR(1) estimation with a centered covariance guarantee."""
    integer_values = (block_dimension, block_count, covariance_sample_count)
    if any(
        isinstance(value, bool) or not isinstance(value, (int, np.integer))
        for value in integer_values
    ):
        raise TypeError("dimensions, counts, and sample size must be integers")
    if block_dimension < 1 or block_count < 1 or covariance_sample_count < 2:
        raise ValueError("require positive dimensions/counts and at least two samples")
    if not isinstance(
        autocorrelation_interval, GaussianAR1AutocorrelationInterval
    ):
        raise TypeError("autocorrelation_interval has the wrong type")
    interval_values = (
        autocorrelation_interval.confidence,
        autocorrelation_interval.declared_upper_bound,
        autocorrelation_interval.estimate,
        autocorrelation_interval.error_radius,
        autocorrelation_interval.lower_bound,
        autocorrelation_interval.upper_bound,
    )
    if not all(np.isfinite(value) for value in interval_values):
        raise ValueError("autocorrelation_interval must contain finite values")
    if (
        autocorrelation_interval.sample_count < 2
        or autocorrelation_interval.channel_count < 1
        or not 0.0 < autocorrelation_interval.confidence < 1.0
        or not 0.0 < autocorrelation_interval.declared_upper_bound < 1.0
        or autocorrelation_interval.error_radius < 0.0
        or not 0.0
        <= autocorrelation_interval.lower_bound
        <= autocorrelation_interval.upper_bound
        <= autocorrelation_interval.declared_upper_bound
    ):
        raise ValueError("autocorrelation_interval is internally inconsistent")
    if not 0.0 < covariance_confidence < 1.0:
        raise ValueError("covariance_confidence must lie in (0, 1)")
    combined_confidence = (
        autocorrelation_interval.confidence + covariance_confidence - 1.0
    )
    if not combined_confidence > 0.0:
        raise ValueError("the union-bound combined confidence must be positive")
    temporal = gaussian_ar1_temporal_correlation_envelope(
        covariance_sample_count, autocorrelation_interval.upper_bound
    )
    degrees_lower = float(
        covariance_sample_count - temporal.spectral_norm_bound
    )
    degrees_upper = float(covariance_sample_count)
    if not degrees_lower > 0.0:
        raise ValueError("the estimated temporal envelope leaves no centered degrees")
    reference_degrees = 0.5 * (degrees_lower + degrees_upper)
    oracle_error = gaussian_dependent_centered_relative_covariance_error_bound(
        block_dimension,
        block_count,
        centering_degrees_of_freedom=degrees_lower,
        projected_temporal_frobenius_norm=temporal.frobenius_norm_bound,
        projected_temporal_spectral_norm=temporal.spectral_norm_bound,
        confidence=covariance_confidence,
    )
    quotient_lower = degrees_lower / reference_degrees
    quotient_upper = degrees_upper / reference_degrees
    normalization_error = max(
        abs(quotient_lower - 1.0), abs(quotient_upper - 1.0)
    )
    covariance_error = max(
        abs(quotient_lower - 1.0) + quotient_lower * oracle_error,
        abs(quotient_upper - 1.0) + quotient_upper * oracle_error,
    )
    return GaussianEstimatedAR1CenteredCovarianceBound(
        autocorrelation_interval=autocorrelation_interval,
        covariance_confidence=float(covariance_confidence),
        combined_confidence=float(combined_confidence),
        covariance_sample_count=int(covariance_sample_count),
        centering_degrees_of_freedom_lower_bound=degrees_lower,
        centering_degrees_of_freedom_upper_bound=degrees_upper,
        reference_centering_degrees_of_freedom=float(reference_degrees),
        temporal_frobenius_norm_bound=temporal.frobenius_norm_bound,
        temporal_spectral_norm_bound=temporal.spectral_norm_bound,
        oracle_normalized_covariance_error=float(oracle_error),
        normalization_error=float(normalization_error),
        covariance_relative_error=float(covariance_error),
        variance_effective_sample_size_lower_bound=float(
            degrees_lower**2 / temporal.frobenius_norm_bound**2
        ),
        operator_effective_sample_size_lower_bound=float(
            degrees_lower / temporal.spectral_norm_bound
        ),
    )


def gaussian_dependent_relative_covariance_error_bound(
    block_dimension: int,
    block_count: int,
    sample_count: int,
    *,
    temporal_correlation_frobenius_norm: float,
    temporal_correlation_spectral_norm: float,
    confidence: float = 0.975,
) -> float:
    """Bound relative covariance error for separably correlated Gaussians.

    Observations must be centered with known population mean and have joint
    covariance ``R tensor Gamma``. The two supplied norms must upper-bound the
    Frobenius and spectral norms of the temporal correlation matrix ``R``.
    """
    integer_values = (block_dimension, block_count, sample_count)
    if any(
        isinstance(value, bool) or not isinstance(value, (int, np.integer))
        for value in integer_values
    ):
        raise TypeError("dimensions, block count, and sample count must be integers")
    if block_dimension < 1 or block_count < 1 or sample_count < 1:
        raise ValueError("dimensions, block count, and sample count must be positive")
    frobenius = float(temporal_correlation_frobenius_norm)
    spectral = float(temporal_correlation_spectral_norm)
    if (
        not np.isfinite(frobenius)
        or not np.isfinite(spectral)
        or frobenius < np.sqrt(sample_count)
        or frobenius > sample_count
        or spectral < 1.0
        or spectral > sample_count
    ):
        raise ValueError("temporal correlation norms are outside valid bounds")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    tail = np.log(
        2.0
        * block_count
        * 9.0**block_dimension
        / (1.0 - float(confidence))
    )
    return float(
        4.0
        * (
            frobenius * np.sqrt(tail) / sample_count
            + spectral * tail / sample_count
        )
    )


def product_root_error_bound(
    population_factors: ArrayLike,
    factor_error_bounds: ArrayLike,
) -> float:
    """Bound a geometric-mean error, using positive factor floors when possible.

    The zero-safe Hölder bound is always valid. If every population factor is
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


def gaussian_safe_near_competitor_screen(
    empirical_local_scores: ArrayLike,
    empirical_transport_scores: ArrayLike,
    candidates: Sequence[Sequence[int]],
    screening_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianSafeNearCompetitorScreen:
    """Construct a high-probability screen from an independent first split.

    The empirical scores must be computed from the covariance estimates on the
    screening split. The spectral arrays are deterministic population
    envelopes for the corresponding present-plus-candidate covariance blocks.
    The certification error arrays describe the allowed score displacement on
    a later, independent split. On the simultaneous screening concentration
    event, every winner permitted by those later errors is retained.

    Edge errors follow the convention used by the localized recovery bound:
    an edge at time ``t`` entering candidate ``j`` uses the spectral envelope
    of block ``(t, j)``. This deliberately ignores the source candidate, so the
    resulting radius is uniform over every incoming edge.
    """
    local = np.asarray(empirical_local_scores, dtype=float)
    transport = np.asarray(empirical_transport_scores, dtype=float)
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    minimum = np.asarray(minimum_block_eigenvalues, dtype=float)
    maximum = np.asarray(maximum_block_eigenvalues, dtype=float)
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)

    if local.ndim != 2:
        raise ValueError("empirical_local_scores must have shape (time, candidates)")
    time_count, candidate_count = local.shape
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    if transport.shape != edge_shape:
        raise ValueError(f"empirical_transport_scores must have shape {edge_shape}")
    if certification_local.shape != local.shape:
        raise ValueError("certification local errors must match the local scores")
    if certification_transport.shape != edge_shape:
        raise ValueError("certification transport errors must match the transport scores")
    if time_count < 1 or candidate_count < 1 or len(candidate_tuple) != candidate_count:
        raise ValueError("scores and candidates have incompatible shapes")
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
    if minimum.shape != spectral_shape or maximum.shape != spectral_shape:
        raise ValueError("spectral envelopes must have shape (time, candidates)")
    arrays = (
        local,
        transport,
        certification_local,
        certification_transport,
        minimum,
        maximum,
    )
    if any(np.any(~np.isfinite(array)) for array in arrays):
        raise ValueError("scores, errors, and spectral envelopes must be finite")
    if np.any((local < 0.0) | (local > 1.0)) or np.any(
        (transport < 0.0) | (transport > 1.0)
    ):
        raise ValueError("empirical scores must lie in [0, 1]")
    if np.any(certification_local < 0.0) or np.any(certification_transport < 0.0):
        raise ValueError("certification error bounds must be nonnegative")
    if np.any(minimum <= 0.0) or np.any(maximum < minimum):
        raise ValueError("require valid positive block-covariance eigenvalue bounds")
    if (
        isinstance(screening_sample_count, bool)
        or not isinstance(screening_sample_count, (int, np.integer))
    ):
        raise TypeError("screening_sample_count must be an integer")
    if screening_sample_count < 2 or not 0.0 < confidence < 1.0:
        raise ValueError("require screening_sample_count >= 2 and confidence in (0, 1)")
    if not np.isfinite(transport_weight) or not (
        np.isfinite(continuity_weight) and continuity_weight >= 0.0
    ):
        raise ValueError("weights must be finite and continuity_weight nonnegative")

    block_count = time_count * candidate_count
    block_dimension = node_count + subset_size
    deviation = (
        np.sqrt(block_dimension)
        + np.sqrt(2.0 * np.log(2.0 * block_count / (1.0 - confidence)))
    ) / np.sqrt(screening_sample_count - 1)
    covariance_errors = maximum * (2.0 * deviation + deviation**2)
    local_factor_errors, valid_local = _local_factor_errors_from_covariance(
        covariance_errors,
        minimum,
        maximum,
        node_count,
        subset_size,
    )
    screening_local_errors = np.minimum(
        1.0, np.sum(local_factor_errors, axis=2) ** (1.0 / 3.0)
    )

    edge_covariance_errors = np.broadcast_to(
        covariance_errors[:-1, None, :], edge_shape
    )
    edge_minimum = np.broadcast_to(minimum[:-1, None, :], edge_shape)
    edge_maximum = np.broadcast_to(maximum[:-1, None, :], edge_shape)
    transport_factor_errors, valid_transport = (
        _transport_factor_errors_from_covariance(
            edge_covariance_errors,
            edge_minimum,
            edge_maximum,
            node_count,
            subset_size,
        )
    )
    screening_transport_errors = np.minimum(
        1.0, np.sum(transport_factor_errors, axis=3) ** 0.5
    )
    total_local_errors = screening_local_errors + certification_local
    total_transport_errors = screening_transport_errors + certification_transport
    screen = screen_near_competitors(
        local,
        transport,
        candidate_tuple,
        total_local_errors,
        total_transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    all_valid = bool(np.all(valid_local) and np.all(valid_transport))
    return GaussianSafeNearCompetitorScreen(
        screen=screen,
        screening_sample_count=int(screening_sample_count),
        screening_confidence=float(confidence),
        covariance_spectral_errors=covariance_errors,
        maximum_covariance_spectral_error=float(np.max(covariance_errors)),
        screening_local_factor_errors=local_factor_errors,
        screening_transport_factor_errors=transport_factor_errors,
        screening_local_score_errors=screening_local_errors,
        screening_transport_score_errors=screening_transport_errors,
        total_local_score_errors=total_local_errors,
        total_transport_score_errors=total_transport_errors,
        positive_local_factor_floor_mask=np.zeros(local.shape, dtype=bool),
        positive_transport_factor_floor_mask=np.zeros(edge_shape, dtype=bool),
        structural_integration_null_mask=np.zeros(local.shape, dtype=bool),
        null_local_score_errors=np.ones(local.shape, dtype=float),
        all_blocks_valid=all_valid,
        guarantees_safe_screen=all_valid,
    )


def gaussian_factor_aware_near_competitor_screen(
    empirical_local_factors: ArrayLike,
    empirical_transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    screening_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianSafeNearCompetitorScreen:
    """Construct a Gaussian-safe screen with positive-factor refinement.

    The factor arrays contain the three empirical local factors and two
    empirical transport factors used by the geometric observer scores. Where
    every factor remains positive after subtracting its perturbation radius,
    the local Lipschitz part of Proposition 10 can improve the zero-safe
    Hölder radius. At all other entries the calculation automatically falls
    back to the zero-safe bound.
    """
    local_factors = np.asarray(empirical_local_factors, dtype=float)
    transport_factors = np.asarray(empirical_transport_factors, dtype=float)
    if local_factors.ndim != 3 or local_factors.shape[2] != 3:
        raise ValueError("empirical_local_factors must have shape (time, candidates, 3)")
    time_count, candidate_count, _ = local_factors.shape
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    if transport_factors.shape != (*edge_shape, 2):
        raise ValueError(
            "empirical_transport_factors must have shape "
            "(time - 1, candidates, candidates, 2)"
        )
    if (
        np.any(~np.isfinite(local_factors))
        or np.any(~np.isfinite(transport_factors))
        or np.any((local_factors < 0.0) | (local_factors > 1.0))
        or np.any((transport_factors < 0.0) | (transport_factors > 1.0))
    ):
        raise ValueError("empirical factors must be finite and lie in [0, 1]")

    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    baseline = gaussian_safe_near_competitor_screen(
        local_scores,
        transport_scores,
        candidates,
        screening_sample_count,
        node_count,
        subset_size,
        minimum_block_eigenvalues=minimum_block_eigenvalues,
        maximum_block_eigenvalues=maximum_block_eigenvalues,
        certification_local_score_errors=certification_local_score_errors,
        certification_transport_score_errors=certification_transport_score_errors,
        confidence=confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )

    local_errors = np.empty((time_count, candidate_count), dtype=float)
    for index in np.ndindex(local_errors.shape):
        local_errors[index] = product_root_error_bound(
            local_factors[index], baseline.screening_local_factor_errors[index]
        )
    transport_errors = np.empty(edge_shape, dtype=float)
    for index in np.ndindex(edge_shape):
        transport_errors[index] = product_root_error_bound(
            transport_factors[index],
            baseline.screening_transport_factor_errors[index],
        )
    local_floor_mask = np.all(
        local_factors - baseline.screening_local_factor_errors > 0.0, axis=2
    )
    transport_floor_mask = np.all(
        transport_factors - baseline.screening_transport_factor_errors > 0.0,
        axis=3,
    )
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    total_local_errors = local_errors + certification_local
    total_transport_errors = transport_errors + certification_transport
    screen = screen_near_competitors(
        local_scores,
        transport_scores,
        candidates,
        total_local_errors,
        total_transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return GaussianSafeNearCompetitorScreen(
        screen=screen,
        screening_sample_count=baseline.screening_sample_count,
        screening_confidence=baseline.screening_confidence,
        covariance_spectral_errors=baseline.covariance_spectral_errors,
        maximum_covariance_spectral_error=(
            baseline.maximum_covariance_spectral_error
        ),
        screening_local_factor_errors=baseline.screening_local_factor_errors,
        screening_transport_factor_errors=(
            baseline.screening_transport_factor_errors
        ),
        screening_local_score_errors=local_errors,
        screening_transport_score_errors=transport_errors,
        total_local_score_errors=total_local_errors,
        total_transport_score_errors=total_transport_errors,
        positive_local_factor_floor_mask=local_floor_mask,
        positive_transport_factor_floor_mask=transport_floor_mask,
        structural_integration_null_mask=np.zeros(
            (time_count, candidate_count), dtype=bool
        ),
        null_local_score_errors=np.ones(
            (time_count, candidate_count), dtype=float
        ),
        all_blocks_valid=baseline.all_blocks_valid,
        guarantees_safe_screen=baseline.guarantees_safe_screen,
    )


def gaussian_structural_null_near_competitor_screen(
    empirical_local_factors: ArrayLike,
    empirical_transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    screening_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    structural_integration_null_mask: ArrayLike,
    minimum_block_eigenvalues: ArrayLike,
    maximum_block_eigenvalues: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianSafeNearCompetitorScreen:
    """Refine screening at predeclared exact integration nulls.

    A true mask entry asserts, independently of the screening observations,
    that the population integration factor is exactly zero. The corresponding
    population local score is therefore zero. The empirical score itself is an
    exact error radius, while the null-CMI perturbation theorem supplies an
    a-priori quadratic alternative on the Gaussian covariance event. Unmasked
    entries retain the positive-factor or zero-safe calculation.
    """
    local_factors = np.asarray(empirical_local_factors, dtype=float)
    transport_factors = np.asarray(empirical_transport_factors, dtype=float)
    null_mask = np.asarray(structural_integration_null_mask)
    if local_factors.ndim != 3 or local_factors.shape[2] != 3:
        raise ValueError("empirical_local_factors must have shape (time, candidates, 3)")
    time_count, candidate_count, _ = local_factors.shape
    if null_mask.shape != (time_count, candidate_count) or null_mask.dtype != np.bool_:
        raise ValueError("structural_integration_null_mask must be a Boolean state array")
    baseline = gaussian_factor_aware_near_competitor_screen(
        local_factors,
        transport_factors,
        candidates,
        screening_sample_count,
        node_count,
        subset_size,
        minimum_block_eigenvalues=minimum_block_eigenvalues,
        maximum_block_eigenvalues=maximum_block_eigenvalues,
        certification_local_score_errors=certification_local_score_errors,
        certification_transport_score_errors=certification_transport_score_errors,
        confidence=confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    minimum = np.asarray(minimum_block_eigenvalues, dtype=float)
    maximum = np.asarray(maximum_block_eigenvalues, dtype=float)
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    local_errors = baseline.screening_local_score_errors.copy()
    null_errors = np.ones((time_count, candidate_count), dtype=float)
    for index in zip(*np.nonzero(null_mask), strict=True):
        eta = float(baseline.covariance_spectral_errors[index])
        if eta < minimum[index]:
            integration_error = gaussian_null_integration_factor_error_bound(
                subset_size,
                minimum_eigenvalue=float(minimum[index]),
                maximum_eigenvalue=float(maximum[index]),
                covariance_spectral_error=eta,
            )
            quadratic_score_error = integration_error ** (1.0 / 3.0)
        else:
            quadratic_score_error = 1.0
        null_errors[index] = min(local_scores[index], quadratic_score_error)
        local_errors[index] = min(local_errors[index], null_errors[index])

    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    total_local_errors = local_errors + certification_local
    total_transport_errors = (
        baseline.screening_transport_score_errors + certification_transport
    )
    screen = screen_near_competitors(
        local_scores,
        np.sqrt(np.prod(transport_factors, axis=3)),
        candidates,
        total_local_errors,
        total_transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return GaussianSafeNearCompetitorScreen(
        screen=screen,
        screening_sample_count=baseline.screening_sample_count,
        screening_confidence=baseline.screening_confidence,
        covariance_spectral_errors=baseline.covariance_spectral_errors,
        maximum_covariance_spectral_error=(
            baseline.maximum_covariance_spectral_error
        ),
        screening_local_factor_errors=baseline.screening_local_factor_errors,
        screening_transport_factor_errors=(
            baseline.screening_transport_factor_errors
        ),
        screening_local_score_errors=local_errors,
        screening_transport_score_errors=(
            baseline.screening_transport_score_errors
        ),
        total_local_score_errors=total_local_errors,
        total_transport_score_errors=total_transport_errors,
        positive_local_factor_floor_mask=(
            baseline.positive_local_factor_floor_mask
        ),
        positive_transport_factor_floor_mask=(
            baseline.positive_transport_factor_floor_mask
        ),
        structural_integration_null_mask=null_mask.copy(),
        null_local_score_errors=null_errors,
        all_blocks_valid=baseline.all_blocks_valid,
        guarantees_safe_screen=baseline.guarantees_safe_screen,
    )


def _factor_errors_from_relative_covariance(
    relative_errors: np.ndarray,
    node_count: int,
    subset_size: int,
    *,
    transport: bool,
) -> tuple[np.ndarray, np.ndarray]:
    """Map relative covariance radii to local or transport factor radii."""
    valid = relative_errors < 1.0
    factor_count = 2 if transport else 3
    errors = np.ones((*relative_errors.shape, factor_count), dtype=float)
    for index in np.ndindex(relative_errors.shape):
        if not valid[index]:
            continue
        delta = float(relative_errors[index])
        logdet_factor = -np.log1p(-delta) / np.log(2.0)
        offset = 0
        if not transport:
            errors[index][0] = min(1.0, 4.0 * np.log(2.0) * logdet_factor)
            offset = 1
        errors[index][offset] = min(
            1.0,
            np.log(2.0)
            * (node_count + 2 * subset_size)
            / subset_size
            * logdet_factor,
        )
        errors[index][offset + 1] = (
            canonical_persistence_relative_covariance_error_bound(
                covariance_relative_error=delta
            )
        )
    return errors, valid


def _relative_structural_null_screen_from_radii(
    local_factors: np.ndarray,
    transport_factors: np.ndarray,
    candidates: tuple[tuple[int, ...], ...],
    relative_errors: np.ndarray,
    node_count: int,
    subset_size: int,
    null_mask: np.ndarray,
    certification_local: np.ndarray,
    certification_transport: np.ndarray,
    transport_weight: float,
    continuity_weight: float,
) -> dict[str, object]:
    """Propagate candidate-local relative radii through the complete screen."""
    time_count, candidate_count, _ = local_factors.shape
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    local_factor_errors, valid_local = _factor_errors_from_relative_covariance(
        relative_errors, node_count, subset_size, transport=False
    )
    edge_relative_errors = np.broadcast_to(relative_errors[:-1, None, :], edge_shape)
    transport_factor_errors, valid_transport = _factor_errors_from_relative_covariance(
        edge_relative_errors, node_count, subset_size, transport=True
    )
    local_scores = np.prod(local_factors, axis=2) ** (1.0 / 3.0)
    transport_scores = np.sqrt(np.prod(transport_factors, axis=3))
    local_errors = np.empty((time_count, candidate_count), dtype=float)
    for index in np.ndindex(local_errors.shape):
        local_errors[index] = product_root_error_bound(
            local_factors[index], local_factor_errors[index]
        )
    transport_errors = np.empty(edge_shape, dtype=float)
    for index in np.ndindex(edge_shape):
        transport_errors[index] = product_root_error_bound(
            transport_factors[index], transport_factor_errors[index]
        )
    local_floor_mask = np.all(local_factors - local_factor_errors > 0.0, axis=2)
    transport_floor_mask = np.all(
        transport_factors - transport_factor_errors > 0.0, axis=3
    )
    null_errors = np.ones((time_count, candidate_count), dtype=float)
    for index in zip(*np.nonzero(null_mask), strict=True):
        delta = float(relative_errors[index])
        if delta < 1.0:
            integration_error = gaussian_relative_null_integration_factor_error_bound(
                subset_size, covariance_relative_error=delta
            )
            quadratic_score_error = integration_error ** (1.0 / 3.0)
        else:
            quadratic_score_error = 1.0
        null_errors[index] = min(local_scores[index], quadratic_score_error)
        local_errors[index] = min(local_errors[index], null_errors[index])
    total_local_errors = local_errors + certification_local
    total_transport_errors = transport_errors + certification_transport
    screen = screen_near_competitors(
        local_scores,
        transport_scores,
        candidates,
        total_local_errors,
        total_transport_errors,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    return {
        "screen": screen,
        "screening_local_factor_errors": local_factor_errors,
        "screening_transport_factor_errors": transport_factor_errors,
        "screening_local_score_errors": local_errors,
        "screening_transport_score_errors": transport_errors,
        "total_local_score_errors": total_local_errors,
        "total_transport_score_errors": total_transport_errors,
        "positive_local_factor_floor_mask": local_floor_mask,
        "positive_transport_factor_floor_mask": transport_floor_mask,
        "null_local_score_errors": null_errors,
        "all_blocks_valid": bool(np.all(valid_local) and np.all(valid_transport)),
    }


def gaussian_relative_structural_null_near_competitor_screen(
    empirical_local_factors: ArrayLike,
    empirical_transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    screening_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    structural_integration_null_mask: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianRelativeNearCompetitorScreen:
    """Screen near competitors using a condition-number-free Wishart event.

    Every candidate block has dimension ``node_count + subset_size``. A union
    bound supplies one relative covariance radius for all such blocks. Factor
    errors use relative log-determinant and canonical-correlation perturbation
    bounds; predeclared integration nulls receive the Schur-complement bound.
    """
    local_factors = np.asarray(empirical_local_factors, dtype=float)
    transport_factors = np.asarray(empirical_transport_factors, dtype=float)
    null_mask = np.asarray(structural_integration_null_mask)
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if local_factors.ndim != 3 or local_factors.shape[2] != 3:
        raise ValueError("empirical_local_factors must have shape (time, candidates, 3)")
    time_count, candidate_count, _ = local_factors.shape
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    if transport_factors.shape != (*edge_shape, 2):
        raise ValueError(
            "empirical_transport_factors must have shape "
            "(time - 1, candidates, candidates, 2)"
        )
    if null_mask.shape != (time_count, candidate_count) or null_mask.dtype != np.bool_:
        raise ValueError("structural_integration_null_mask must be a Boolean state array")
    if certification_local.shape != (time_count, candidate_count):
        raise ValueError("certification local errors must match the local scores")
    if certification_transport.shape != edge_shape:
        raise ValueError("certification transport errors must match the transport scores")
    if len(candidate_tuple) != candidate_count or candidate_count < 1 or time_count < 1:
        raise ValueError("factors and candidates have incompatible shapes")
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
    arrays = (
        local_factors,
        transport_factors,
        certification_local,
        certification_transport,
    )
    if any(np.any(~np.isfinite(array)) for array in arrays):
        raise ValueError("factors and certification errors must be finite")
    if (
        np.any((local_factors < 0.0) | (local_factors > 1.0))
        or np.any((transport_factors < 0.0) | (transport_factors > 1.0))
        or np.any(certification_local < 0.0)
        or np.any(certification_transport < 0.0)
    ):
        raise ValueError("factors must lie in [0, 1] and errors must be nonnegative")

    block_count = time_count * candidate_count
    delta = gaussian_wishart_relative_covariance_error_bound(
        node_count + subset_size,
        block_count,
        screening_sample_count,
        confidence=confidence,
    )
    relative_errors = np.full((time_count, candidate_count), delta)
    propagated = _relative_structural_null_screen_from_radii(
        local_factors,
        transport_factors,
        candidate_tuple,
        relative_errors,
        node_count,
        subset_size,
        null_mask,
        certification_local,
        certification_transport,
        transport_weight,
        continuity_weight,
    )
    all_valid = bool(propagated["all_blocks_valid"])
    return GaussianRelativeNearCompetitorScreen(
        screen=propagated["screen"],
        screening_sample_count=int(screening_sample_count),
        screening_confidence=float(confidence),
        covariance_relative_errors=relative_errors,
        maximum_covariance_relative_error=delta,
        screening_local_factor_errors=propagated["screening_local_factor_errors"],
        screening_transport_factor_errors=propagated[
            "screening_transport_factor_errors"
        ],
        screening_local_score_errors=propagated["screening_local_score_errors"],
        screening_transport_score_errors=propagated[
            "screening_transport_score_errors"
        ],
        total_local_score_errors=propagated["total_local_score_errors"],
        total_transport_score_errors=propagated["total_transport_score_errors"],
        positive_local_factor_floor_mask=propagated[
            "positive_local_factor_floor_mask"
        ],
        positive_transport_factor_floor_mask=propagated[
            "positive_transport_factor_floor_mask"
        ],
        structural_integration_null_mask=null_mask.copy(),
        null_local_score_errors=propagated["null_local_score_errors"],
        all_blocks_valid=all_valid,
        guarantees_safe_screen=all_valid,
    )


def gaussian_dependent_relative_structural_null_near_competitor_screen(
    empirical_local_factors: ArrayLike,
    empirical_transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    temporal_correlation_frobenius_norm: float,
    temporal_correlation_spectral_norm: float,
    structural_integration_null_mask: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianDependentRelativeNearCompetitorScreen:
    """Screen under a separable Gaussian temporal-correlation envelope."""
    gaussian_relative_structural_null_near_competitor_screen(
        empirical_local_factors,
        empirical_transport_factors,
        candidates,
        sample_count,
        node_count,
        subset_size,
        structural_integration_null_mask=structural_integration_null_mask,
        certification_local_score_errors=certification_local_score_errors,
        certification_transport_score_errors=certification_transport_score_errors,
        confidence=confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    local_factors = np.asarray(empirical_local_factors, dtype=float)
    transport_factors = np.asarray(empirical_transport_factors, dtype=float)
    null_mask = np.asarray(structural_integration_null_mask)
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    time_count, candidate_count, _ = local_factors.shape
    block_count = time_count * candidate_count
    delta = gaussian_dependent_relative_covariance_error_bound(
        node_count + subset_size,
        block_count,
        sample_count,
        temporal_correlation_frobenius_norm=(
            temporal_correlation_frobenius_norm
        ),
        temporal_correlation_spectral_norm=temporal_correlation_spectral_norm,
        confidence=confidence,
    )
    relative_errors = np.full((time_count, candidate_count), delta)
    propagated = _relative_structural_null_screen_from_radii(
        local_factors,
        transport_factors,
        candidate_tuple,
        relative_errors,
        node_count,
        subset_size,
        null_mask,
        certification_local,
        certification_transport,
        transport_weight,
        continuity_weight,
    )
    frobenius = float(temporal_correlation_frobenius_norm)
    spectral = float(temporal_correlation_spectral_norm)
    all_valid = bool(propagated["all_blocks_valid"])
    return GaussianDependentRelativeNearCompetitorScreen(
        screen=propagated["screen"],
        sample_count=int(sample_count),
        confidence=float(confidence),
        temporal_correlation_frobenius_norm=frobenius,
        temporal_correlation_spectral_norm=spectral,
        variance_effective_sample_size=float(sample_count**2 / frobenius**2),
        operator_effective_sample_size=float(sample_count / spectral),
        covariance_relative_errors=relative_errors,
        maximum_covariance_relative_error=delta,
        screening_local_factor_errors=propagated["screening_local_factor_errors"],
        screening_transport_factor_errors=propagated[
            "screening_transport_factor_errors"
        ],
        screening_local_score_errors=propagated["screening_local_score_errors"],
        screening_transport_score_errors=propagated[
            "screening_transport_score_errors"
        ],
        total_local_score_errors=propagated["total_local_score_errors"],
        total_transport_score_errors=propagated["total_transport_score_errors"],
        positive_local_factor_floor_mask=propagated[
            "positive_local_factor_floor_mask"
        ],
        positive_transport_factor_floor_mask=propagated[
            "positive_transport_factor_floor_mask"
        ],
        structural_integration_null_mask=null_mask.copy(),
        null_local_score_errors=propagated["null_local_score_errors"],
        all_blocks_valid=all_valid,
        guarantees_safe_screen=all_valid,
    )


def gaussian_dependent_centered_relative_structural_null_near_competitor_screen(
    empirical_local_factors: ArrayLike,
    empirical_transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    centering_degrees_of_freedom: float,
    projected_temporal_frobenius_norm: float,
    projected_temporal_spectral_norm: float,
    structural_integration_null_mask: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianCenteredDependentRelativeNearCompetitorScreen:
    """Screen after empirical mean removal under separable Gaussian dependence."""
    gaussian_relative_structural_null_near_competitor_screen(
        empirical_local_factors,
        empirical_transport_factors,
        candidates,
        sample_count,
        node_count,
        subset_size,
        structural_integration_null_mask=structural_integration_null_mask,
        certification_local_score_errors=certification_local_score_errors,
        certification_transport_score_errors=certification_transport_score_errors,
        confidence=confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    local_factors = np.asarray(empirical_local_factors, dtype=float)
    transport_factors = np.asarray(empirical_transport_factors, dtype=float)
    null_mask = np.asarray(structural_integration_null_mask)
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    time_count, candidate_count, _ = local_factors.shape
    delta = gaussian_dependent_centered_relative_covariance_error_bound(
        node_count + subset_size,
        time_count * candidate_count,
        centering_degrees_of_freedom=centering_degrees_of_freedom,
        projected_temporal_frobenius_norm=projected_temporal_frobenius_norm,
        projected_temporal_spectral_norm=projected_temporal_spectral_norm,
        confidence=confidence,
    )
    relative_errors = np.full((time_count, candidate_count), delta)
    propagated = _relative_structural_null_screen_from_radii(
        local_factors,
        transport_factors,
        candidate_tuple,
        relative_errors,
        node_count,
        subset_size,
        null_mask,
        certification_local,
        certification_transport,
        transport_weight,
        continuity_weight,
    )
    degrees = float(centering_degrees_of_freedom)
    frobenius = float(projected_temporal_frobenius_norm)
    spectral = float(projected_temporal_spectral_norm)
    all_valid = bool(propagated["all_blocks_valid"])
    return GaussianCenteredDependentRelativeNearCompetitorScreen(
        screen=propagated["screen"],
        sample_count=int(sample_count),
        confidence=float(confidence),
        centering_degrees_of_freedom=degrees,
        projected_temporal_frobenius_norm=frobenius,
        projected_temporal_spectral_norm=spectral,
        variance_effective_sample_size=float(degrees**2 / frobenius**2),
        operator_effective_sample_size=float(degrees / spectral),
        covariance_relative_errors=relative_errors,
        maximum_covariance_relative_error=delta,
        screening_local_factor_errors=propagated["screening_local_factor_errors"],
        screening_transport_factor_errors=propagated[
            "screening_transport_factor_errors"
        ],
        screening_local_score_errors=propagated["screening_local_score_errors"],
        screening_transport_score_errors=propagated[
            "screening_transport_score_errors"
        ],
        total_local_score_errors=propagated["total_local_score_errors"],
        total_transport_score_errors=propagated["total_transport_score_errors"],
        positive_local_factor_floor_mask=propagated[
            "positive_local_factor_floor_mask"
        ],
        positive_transport_factor_floor_mask=propagated[
            "positive_transport_factor_floor_mask"
        ],
        structural_integration_null_mask=null_mask.copy(),
        null_local_score_errors=propagated["null_local_score_errors"],
        all_blocks_valid=all_valid,
        guarantees_safe_screen=all_valid,
    )


def gaussian_estimated_ar1_centered_relative_structural_null_near_competitor_screen(
    empirical_local_factors: ArrayLike,
    empirical_transport_factors: ArrayLike,
    candidates: Sequence[Sequence[int]],
    sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    covariance_bound: GaussianEstimatedAR1CenteredCovarianceBound,
    structural_integration_null_mask: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianEstimatedAR1CenteredRelativeNearCompetitorScreen:
    """Propagate an estimated AR(1) envelope through the complete screen.

    The autocorrelation interval and covariance event may use the same record:
    their stated combined confidence follows from a union bound and therefore
    does not require independence between the two events.
    """
    if not isinstance(
        covariance_bound, GaussianEstimatedAR1CenteredCovarianceBound
    ):
        raise TypeError("covariance_bound has the wrong type")
    if covariance_bound.covariance_sample_count != sample_count:
        raise ValueError("sample_count must match covariance_bound")
    gaussian_relative_structural_null_near_competitor_screen(
        empirical_local_factors,
        empirical_transport_factors,
        candidates,
        sample_count,
        node_count,
        subset_size,
        structural_integration_null_mask=structural_integration_null_mask,
        certification_local_score_errors=certification_local_score_errors,
        certification_transport_score_errors=certification_transport_score_errors,
        confidence=covariance_bound.combined_confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    local_factors = np.asarray(empirical_local_factors, dtype=float)
    transport_factors = np.asarray(empirical_transport_factors, dtype=float)
    null_mask = np.asarray(structural_integration_null_mask)
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    time_count, candidate_count, _ = local_factors.shape
    relative_errors = np.full(
        (time_count, candidate_count), covariance_bound.covariance_relative_error
    )
    propagated = _relative_structural_null_screen_from_radii(
        local_factors,
        transport_factors,
        candidate_tuple,
        relative_errors,
        node_count,
        subset_size,
        null_mask,
        certification_local,
        certification_transport,
        transport_weight,
        continuity_weight,
    )
    all_valid = bool(propagated["all_blocks_valid"])
    return GaussianEstimatedAR1CenteredRelativeNearCompetitorScreen(
        screen=propagated["screen"],
        covariance_bound=covariance_bound,
        covariance_relative_errors=relative_errors,
        screening_local_factor_errors=propagated[
            "screening_local_factor_errors"
        ],
        screening_transport_factor_errors=propagated[
            "screening_transport_factor_errors"
        ],
        screening_local_score_errors=propagated["screening_local_score_errors"],
        screening_transport_score_errors=propagated[
            "screening_transport_score_errors"
        ],
        total_local_score_errors=propagated["total_local_score_errors"],
        total_transport_score_errors=propagated["total_transport_score_errors"],
        positive_local_factor_floor_mask=propagated[
            "positive_local_factor_floor_mask"
        ],
        positive_transport_factor_floor_mask=propagated[
            "positive_transport_factor_floor_mask"
        ],
        structural_integration_null_mask=null_mask.copy(),
        null_local_score_errors=propagated["null_local_score_errors"],
        all_blocks_valid=all_valid,
        guarantees_safe_screen=all_valid,
    )


def gaussian_cross_fitted_relative_near_competitor_screen(
    pilot_joint_covariances: Sequence[ArrayLike],
    screening_joint_covariances: Sequence[ArrayLike],
    candidates: Sequence[Sequence[int]],
    pilot_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    structural_integration_null_mask: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianCrossFittedRelativeNearCompetitorScreen:
    """Build an observable relative screen from pilot and screening covariances.

    The pilot covariance defines the whitening metric. If its population-relative
    error is at most ``epsilon`` and the observed pilot-normalized discrepancy of
    the screening covariance is ``r``, then the screening population-relative
    error is at most ``r + epsilon + r * epsilon``. Candidate factors are
    computed internally from the screening covariances.
    """
    pilots = tuple(np.asarray(value, dtype=float) for value in pilot_joint_covariances)
    screenings = tuple(
        np.asarray(value, dtype=float) for value in screening_joint_covariances
    )
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if not pilots or len(pilots) != len(screenings):
        raise ValueError("pilot and screening covariance sequences must have equal positive length")
    time_count = len(pilots)
    candidate_count = len(candidate_tuple)
    if candidate_count < 1 or node_count < 2 or not 1 <= subset_size < node_count:
        raise ValueError("require candidates and 1 <= subset_size < node_count")
    if any(
        len(candidate) != subset_size
        or len(set(candidate)) != subset_size
        or any(
            isinstance(node, bool) or not isinstance(node, (int, np.integer))
            for node in candidate
        )
        or min(candidate) < 0
        or max(candidate) >= node_count
        for candidate in candidate_tuple
    ):
        raise ValueError("candidates must contain distinct valid nodes of subset_size")
    expected_joint_shape = (2 * node_count, 2 * node_count)
    for name, sequence in (("pilot", pilots), ("screening", screenings)):
        if any(matrix.shape != expected_joint_shape for matrix in sequence):
            raise ValueError(f"{name} joint covariances must have shape {expected_joint_shape}")
        if any(np.any(~np.isfinite(matrix)) for matrix in sequence):
            raise ValueError(f"{name} joint covariances must be finite")
        if any(not np.allclose(matrix, matrix.T, rtol=1e-10, atol=1e-12) for matrix in sequence):
            raise ValueError(f"{name} joint covariances must be symmetric")
    if any(np.linalg.eigvalsh(matrix)[0] <= 0.0 for matrix in screenings):
        raise ValueError("screening joint covariances must be positive definite")

    null_mask = np.asarray(structural_integration_null_mask)
    local_shape = (time_count, candidate_count)
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    if null_mask.shape != local_shape or null_mask.dtype != np.bool_:
        raise ValueError("structural_integration_null_mask must be a Boolean state array")
    if certification_local.shape != local_shape or certification_transport.shape != edge_shape:
        raise ValueError("certification error arrays have incompatible shapes")
    if (
        np.any(~np.isfinite(certification_local))
        or np.any(~np.isfinite(certification_transport))
        or np.any(certification_local < 0.0)
        or np.any(certification_transport < 0.0)
    ):
        raise ValueError("certification error bounds must be finite and nonnegative")

    block_count = time_count * candidate_count
    epsilon = gaussian_wishart_relative_covariance_error_bound(
        node_count + subset_size,
        block_count,
        pilot_sample_count,
        confidence=confidence,
    )
    observed = np.full(local_shape, np.inf)
    all_pilot_positive = True
    for time, (pilot, screening) in enumerate(zip(pilots, screenings, strict=True)):
        for current, candidate in enumerate(candidate_tuple):
            indices = tuple(range(node_count)) + tuple(
                node_count + node for node in candidate
            )
            pilot_block = pilot[np.ix_(indices, indices)]
            screening_block = screening[np.ix_(indices, indices)]
            values, vectors = np.linalg.eigh(pilot_block)
            if values[0] <= 0.0:
                all_pilot_positive = False
                continue
            inverse_sqrt = (vectors / np.sqrt(values)) @ vectors.T
            observed[time, current] = np.linalg.norm(
                inverse_sqrt @ (screening_block - pilot_block) @ inverse_sqrt,
                ord=2,
            )
    relative_errors = observed + epsilon + observed * epsilon

    local_factors = np.empty((*local_shape, 3), dtype=float)
    transport_factors = np.empty((*edge_shape, 2), dtype=float)
    for time, joint in enumerate(screenings):
        present = joint[:node_count, :node_count]
        for current, candidate in enumerate(candidate_tuple):
            metrics = observer_metrics_from_covariances(present, joint, candidate)
            local_factors[time, current] = (
                metrics.integration_strength,
                metrics.independence,
                metrics.persistence,
            )
        if time < time_count - 1:
            for previous, source in enumerate(candidate_tuple):
                for current, target in enumerate(candidate_tuple):
                    metrics = transport_metrics_from_covariances(
                        present, joint, source, target
                    )
                    transport_factors[time, previous, current] = (
                        metrics.independence,
                        metrics.persistence,
                    )
    propagated = _relative_structural_null_screen_from_radii(
        local_factors,
        transport_factors,
        candidate_tuple,
        relative_errors,
        node_count,
        subset_size,
        null_mask,
        certification_local,
        certification_transport,
        transport_weight,
        continuity_weight,
    )
    all_valid = bool(all_pilot_positive and propagated["all_blocks_valid"])
    return GaussianCrossFittedRelativeNearCompetitorScreen(
        screen=propagated["screen"],
        pilot_sample_count=int(pilot_sample_count),
        pilot_confidence=float(confidence),
        pilot_covariance_relative_error=epsilon,
        observed_pilot_relative_errors=observed,
        covariance_relative_errors=relative_errors,
        maximum_covariance_relative_error=float(np.max(relative_errors)),
        screening_local_factor_errors=propagated["screening_local_factor_errors"],
        screening_transport_factor_errors=propagated[
            "screening_transport_factor_errors"
        ],
        screening_local_score_errors=propagated["screening_local_score_errors"],
        screening_transport_score_errors=propagated[
            "screening_transport_score_errors"
        ],
        total_local_score_errors=propagated["total_local_score_errors"],
        total_transport_score_errors=propagated["total_transport_score_errors"],
        positive_local_factor_floor_mask=propagated[
            "positive_local_factor_floor_mask"
        ],
        positive_transport_factor_floor_mask=propagated[
            "positive_transport_factor_floor_mask"
        ],
        structural_integration_null_mask=null_mask.copy(),
        null_local_score_errors=propagated["null_local_score_errors"],
        all_pilot_blocks_positive_definite=all_pilot_positive,
        all_blocks_valid=all_valid,
        guarantees_safe_screen=all_valid,
    )


def compose_pilot_screening_drift_relative_error(
    observed_pilot_relative_error: ArrayLike,
    pilot_relative_error: float,
    population_drift_relative_error: ArrayLike,
) -> np.ndarray:
    """Compose pilot error, observed discrepancy, and population drift.

    The returned radius is relative to the screening population. Inputs may be
    scalars or broadcast-compatible arrays. A drift radius must be strictly
    below one so that the pilot population has a positive lower bound in the
    screening-population metric.
    """
    observed = np.asarray(observed_pilot_relative_error, dtype=float)
    drift = np.asarray(population_drift_relative_error, dtype=float)
    epsilon = float(pilot_relative_error)
    if (
        np.any(~np.isfinite(observed))
        or np.any(~np.isfinite(drift))
        or not np.isfinite(epsilon)
        or np.any(observed < 0.0)
        or np.any(drift < 0.0)
        or epsilon < 0.0
    ):
        raise ValueError("relative errors must be finite and nonnegative")
    if epsilon >= 1.0:
        raise ValueError("pilot_relative_error must be below one")
    if np.any(drift >= 1.0):
        raise ValueError("population drift relative errors must be below one")
    same_population = observed + epsilon + observed * epsilon
    return (same_population + drift) / (1.0 - drift)


def compose_calibrated_population_drift_relative_error(
    observed_reference_relative_error: ArrayLike,
    reference_relative_error: float,
    current_relative_error: float,
) -> np.ndarray:
    """Convert two covariance-estimation events into a drift envelope."""
    observed = np.asarray(observed_reference_relative_error, dtype=float)
    reference_error = float(reference_relative_error)
    current_error = float(current_relative_error)
    if (
        np.any(~np.isfinite(observed))
        or not np.isfinite(reference_error)
        or not np.isfinite(current_error)
        or np.any(observed < 0.0)
        or reference_error < 0.0
        or current_error < 0.0
    ):
        raise ValueError("relative errors must be finite and nonnegative")
    if reference_error >= 1.0 or current_error >= 1.0:
        raise ValueError("calibration relative errors must be below one")
    return (
        (1.0 + observed) * (1.0 + reference_error) / (1.0 - current_error)
        - 1.0
    )


def gaussian_calibrated_population_drift_bound(
    reference_joint_covariances: Sequence[ArrayLike],
    current_joint_covariances: Sequence[ArrayLike],
    candidates: Sequence[Sequence[int]],
    reference_sample_count: int,
    current_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    reference_confidence: float = 0.9875,
    current_confidence: float = 0.9875,
) -> GaussianCalibratedPopulationDrift:
    """Estimate a simultaneous population-drift envelope from two cohorts.

    The two supplied covariance sequences are empirical estimates of the old
    and current populations. The returned confidence is the union-bound lower
    bound and therefore does not require independence between the cohorts.
    """
    references = tuple(
        np.asarray(value, dtype=float) for value in reference_joint_covariances
    )
    currents = tuple(
        np.asarray(value, dtype=float) for value in current_joint_covariances
    )
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    if not references or len(references) != len(currents):
        raise ValueError(
            "reference and current covariance sequences must have equal positive length"
        )
    time_count = len(references)
    candidate_count = len(candidate_tuple)
    local_zeros = np.zeros((time_count, candidate_count))
    edge_zeros = np.zeros(
        (max(0, time_count - 1), candidate_count, candidate_count)
    )
    diagnostic = gaussian_cross_fitted_relative_near_competitor_screen(
        references,
        currents,
        candidate_tuple,
        reference_sample_count,
        node_count,
        subset_size,
        structural_integration_null_mask=np.zeros(
            (time_count, candidate_count), dtype=bool
        ),
        certification_local_score_errors=local_zeros,
        certification_transport_score_errors=edge_zeros,
        confidence=reference_confidence,
    )
    block_count = time_count * candidate_count
    current_error = gaussian_wishart_relative_covariance_error_bound(
        node_count + subset_size,
        block_count,
        current_sample_count,
        confidence=current_confidence,
    )
    if current_error >= 1.0:
        raise ValueError("current calibration relative error must be below one")
    observed = diagnostic.observed_pilot_relative_errors
    reference_error = diagnostic.pilot_covariance_relative_error
    drift_errors = compose_calibrated_population_drift_relative_error(
        observed,
        reference_error,
        current_error,
    )
    overall_confidence = max(
        0.0, float(reference_confidence) + float(current_confidence) - 1.0
    )
    all_valid = bool(
        diagnostic.all_pilot_blocks_positive_definite
        and np.all(drift_errors < 1.0)
    )
    return GaussianCalibratedPopulationDrift(
        reference_sample_count=int(reference_sample_count),
        current_sample_count=int(current_sample_count),
        reference_confidence=float(reference_confidence),
        current_confidence=float(current_confidence),
        overall_confidence_lower_bound=overall_confidence,
        reference_covariance_relative_error=reference_error,
        current_covariance_relative_error=current_error,
        observed_reference_relative_errors=observed.copy(),
        population_drift_relative_errors=drift_errors,
        maximum_population_drift_relative_error=float(np.max(drift_errors)),
        all_reference_blocks_positive_definite=(
            diagnostic.all_pilot_blocks_positive_definite
        ),
        all_bounds_valid=all_valid,
    )


def gaussian_drift_robust_relative_near_competitor_screen(
    pilot_joint_covariances: Sequence[ArrayLike],
    screening_joint_covariances: Sequence[ArrayLike],
    candidates: Sequence[Sequence[int]],
    pilot_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    population_drift_relative_errors: ArrayLike,
    structural_integration_null_mask: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianDriftRobustRelativeNearCompetitorScreen:
    """Extend pilot-normalized screening to a declared covariance drift.

    ``population_drift_relative_errors[t, c]`` must bound the candidate block
    change from the pilot population covariance to the screening population
    covariance, normalized by the pilot population. The drift envelope is an
    assumption supplied independently of the screening draw; it is not inferred
    by this function.
    """
    baseline = gaussian_cross_fitted_relative_near_competitor_screen(
        pilot_joint_covariances,
        screening_joint_covariances,
        candidates,
        pilot_sample_count,
        node_count,
        subset_size,
        structural_integration_null_mask=structural_integration_null_mask,
        certification_local_score_errors=certification_local_score_errors,
        certification_transport_score_errors=certification_transport_score_errors,
        confidence=confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    drift = np.asarray(population_drift_relative_errors, dtype=float)
    expected_shape = baseline.observed_pilot_relative_errors.shape
    if drift.shape != expected_shape:
        raise ValueError(
            "population_drift_relative_errors must match the candidate state array"
        )
    relative_errors = compose_pilot_screening_drift_relative_error(
        baseline.observed_pilot_relative_errors,
        baseline.pilot_covariance_relative_error,
        drift,
    )

    screenings = tuple(
        np.asarray(value, dtype=float) for value in screening_joint_covariances
    )
    candidate_tuple = tuple(tuple(candidate) for candidate in candidates)
    time_count, candidate_count = expected_shape
    edge_shape = (max(0, time_count - 1), candidate_count, candidate_count)
    local_factors = np.empty((*expected_shape, 3), dtype=float)
    transport_factors = np.empty((*edge_shape, 2), dtype=float)
    for time, joint in enumerate(screenings):
        present = joint[:node_count, :node_count]
        for current, candidate in enumerate(candidate_tuple):
            metrics = observer_metrics_from_covariances(present, joint, candidate)
            local_factors[time, current] = (
                metrics.integration_strength,
                metrics.independence,
                metrics.persistence,
            )
        if time < time_count - 1:
            for previous, source in enumerate(candidate_tuple):
                for current, target in enumerate(candidate_tuple):
                    metrics = transport_metrics_from_covariances(
                        present, joint, source, target
                    )
                    transport_factors[time, previous, current] = (
                        metrics.independence,
                        metrics.persistence,
                    )

    null_mask = np.asarray(structural_integration_null_mask)
    certification_local = np.asarray(certification_local_score_errors, dtype=float)
    certification_transport = np.asarray(
        certification_transport_score_errors, dtype=float
    )
    propagated = _relative_structural_null_screen_from_radii(
        local_factors,
        transport_factors,
        candidate_tuple,
        relative_errors,
        node_count,
        subset_size,
        null_mask,
        certification_local,
        certification_transport,
        transport_weight,
        continuity_weight,
    )
    all_drift_valid = bool(np.all(drift < 1.0))
    all_valid = bool(
        baseline.all_pilot_blocks_positive_definite
        and all_drift_valid
        and propagated["all_blocks_valid"]
    )
    same_population = baseline.covariance_relative_errors.copy()
    return GaussianDriftRobustRelativeNearCompetitorScreen(
        screen=propagated["screen"],
        pilot_sample_count=baseline.pilot_sample_count,
        pilot_confidence=baseline.pilot_confidence,
        pilot_covariance_relative_error=baseline.pilot_covariance_relative_error,
        observed_pilot_relative_errors=baseline.observed_pilot_relative_errors.copy(),
        same_population_relative_errors=same_population,
        population_drift_relative_errors=drift.copy(),
        covariance_relative_errors=relative_errors,
        maximum_population_drift_relative_error=float(np.max(drift)),
        maximum_covariance_relative_error=float(np.max(relative_errors)),
        screening_local_factor_errors=propagated["screening_local_factor_errors"],
        screening_transport_factor_errors=propagated[
            "screening_transport_factor_errors"
        ],
        screening_local_score_errors=propagated["screening_local_score_errors"],
        screening_transport_score_errors=propagated[
            "screening_transport_score_errors"
        ],
        total_local_score_errors=propagated["total_local_score_errors"],
        total_transport_score_errors=propagated["total_transport_score_errors"],
        positive_local_factor_floor_mask=propagated[
            "positive_local_factor_floor_mask"
        ],
        positive_transport_factor_floor_mask=propagated[
            "positive_transport_factor_floor_mask"
        ],
        structural_integration_null_mask=null_mask.copy(),
        null_local_score_errors=propagated["null_local_score_errors"],
        all_pilot_blocks_positive_definite=(
            baseline.all_pilot_blocks_positive_definite
        ),
        all_drift_envelopes_valid=all_drift_valid,
        all_blocks_valid=all_valid,
        guarantees_safe_screen=all_valid,
    )


def gaussian_calibrated_drift_relative_near_competitor_screen(
    reference_joint_covariances: Sequence[ArrayLike],
    current_calibration_joint_covariances: Sequence[ArrayLike],
    screening_joint_covariances: Sequence[ArrayLike],
    candidates: Sequence[Sequence[int]],
    reference_sample_count: int,
    current_calibration_sample_count: int,
    node_count: int,
    subset_size: int,
    *,
    structural_integration_null_mask: ArrayLike,
    certification_local_score_errors: ArrayLike,
    certification_transport_score_errors: ArrayLike,
    confidence: float = 0.975,
    transport_weight: float = 0.35,
    continuity_weight: float = 0.15,
) -> GaussianCalibratedDriftRelativeNearCompetitorScreen:
    """Calibrate drift and propagate it through the complete safe screen.

    The total failure budget is split equally between the old-population
    reference event and the current-population calibration event. The screening
    covariance may be arbitrary once those two simultaneous events hold.
    """
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must lie in (0, 1)")
    component_confidence = 0.5 * (1.0 + float(confidence))
    drift = gaussian_calibrated_population_drift_bound(
        reference_joint_covariances,
        current_calibration_joint_covariances,
        candidates,
        reference_sample_count,
        current_calibration_sample_count,
        node_count,
        subset_size,
        reference_confidence=component_confidence,
        current_confidence=component_confidence,
    )
    if not drift.all_bounds_valid:
        raise ValueError(
            "calibrated population drift must remain below one for screening"
        )
    screening = gaussian_drift_robust_relative_near_competitor_screen(
        reference_joint_covariances,
        screening_joint_covariances,
        candidates,
        reference_sample_count,
        node_count,
        subset_size,
        population_drift_relative_errors=drift.population_drift_relative_errors,
        structural_integration_null_mask=structural_integration_null_mask,
        certification_local_score_errors=certification_local_score_errors,
        certification_transport_score_errors=certification_transport_score_errors,
        confidence=component_confidence,
        transport_weight=transport_weight,
        continuity_weight=continuity_weight,
    )
    guarantees = bool(drift.all_bounds_valid and screening.guarantees_safe_screen)
    return GaussianCalibratedDriftRelativeNearCompetitorScreen(
        drift_calibration=drift,
        screening=screening,
        requested_confidence=float(confidence),
        component_confidence=component_confidence,
        overall_confidence_lower_bound=drift.overall_confidence_lower_bound,
        guarantees_safe_screen=guarantees,
    )


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
