"""Certification-aware active measurement primitives.

These routines implement algebraic pieces of the public adaptive-measurement
extension. They do not claim an end-to-end statistical guarantee unless the
supplied factor radii or predictive models themselves satisfy their declared
assumptions.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import numpy as np


@dataclass(frozen=True)
class PathCertificate:
    leader_lower: float
    competitor_upper: float
    robust_separation: float
    certified: bool


def path_action_radius(
    local_radii: Sequence[float],
    transport_radii: Sequence[float],
    *,
    transport_weight: float,
) -> float:
    """AM18 path radius from factorwise local and transport bounds."""
    local = np.asarray(local_radii, dtype=float)
    transport = np.asarray(transport_radii, dtype=float)
    if np.any(local < 0) or np.any(transport < 0):
        raise ValueError("Uncertainty radii must be nonnegative.")
    return float(local.sum() + abs(transport_weight) * transport.sum())


def robust_pairwise_certificate(
    leader_action: float,
    competitor_action: float,
    leader_radius: float,
    competitor_radius: float,
) -> PathCertificate:
    """AM18 interval-separation certificate for a retained path pair."""
    if leader_radius < 0 or competitor_radius < 0:
        raise ValueError("Path radii must be nonnegative.")
    lower = float(leader_action - leader_radius)
    upper = float(competitor_action + competitor_radius)
    separation = lower - upper
    return PathCertificate(lower, upper, separation, separation > 0.0)


def certificate_pressure(
    leader_local_radii: Sequence[float],
    competitor_local_radii: Sequence[float],
    leader_transport_radii: Sequence[float],
    competitor_transport_radii: Sequence[float],
    *,
    transport_weight: float,
) -> dict[str, np.ndarray]:
    """Factorwise uncertainty burden for a leader/competitor pair."""
    lo = np.asarray(leader_local_radii, dtype=float)
    co = np.asarray(competitor_local_radii, dtype=float)
    lt = np.asarray(leader_transport_radii, dtype=float)
    ct = np.asarray(competitor_transport_radii, dtype=float)
    if lo.shape != co.shape or lt.shape != ct.shape:
        raise ValueError("Leader and competitor radius arrays must align.")
    if any(np.any(x < 0) for x in (lo, co, lt, ct)):
        raise ValueError("Uncertainty radii must be nonnegative.")
    return {
        "local": lo + co,
        "transport": abs(transport_weight) * (lt + ct),
    }


def gaussian_equal_variance_kl(
    mean_p: np.ndarray,
    mean_r: np.ndarray,
    variance: np.ndarray,
) -> np.ndarray:
    """Per-coordinate KL for equal-variance Gaussian predictive laws."""
    p = np.asarray(mean_p, dtype=float)
    r = np.asarray(mean_r, dtype=float)
    v = np.asarray(variance, dtype=float)
    if p.shape != r.shape or p.shape != v.shape:
        raise ValueError("Means and variances must have identical shapes.")
    if np.any(v <= 0):
        raise ValueError("Predictive variances must be positive.")
    return 0.5 * (p - r) ** 2 / v


def signed_evidence_gap(threshold: float, log_likelihood_ratio: float) -> float:
    """Remaining signed evidence debt S=h-L."""
    return float(threshold - log_likelihood_ratio)


def minimum_expected_measurements(gap: float, max_kl_per_measurement: float):
    """AM11 lower bound on measurements needed to close expected gap."""
    if gap <= 0:
        return 0
    if max_kl_per_measurement < 0:
        raise ValueError("KL bound must be nonnegative.")
    if max_kl_per_measurement == 0:
        return np.inf
    return int(np.ceil(gap / max_kl_per_measurement))


def observer_factor_radii_from_relative_covariance(
    *,
    subset_size: int,
    ambient_size: int,
    covariance_relative_error: float,
    integration_factor: float,
    insulation_factor: float,
    persistence_factor: float,
) -> dict[str, float]:
    """Propagate a Research I relative covariance radius to Omega uncertainty.

    This composes the existing relative Gaussian-CMI and canonical-persistence
    perturbation bounds with the repository's zero-safe product-root bound.
    The supplied factors are population/reference values in [0, 1].
    """
    from .recovery import (
        canonical_persistence_relative_covariance_error_bound,
        gaussian_relative_cmi_covariance_error_bound,
        product_root_error_bound,
    )

    if subset_size < 2 or ambient_size <= subset_size:
        raise ValueError("require 2 <= subset_size < ambient_size")
    delta = float(covariance_relative_error)
    # Internal integration uses the worst bipartition. A conservative
    # factorwise bound uses the largest CMI dimensional coefficient among
    # admissible nonempty bipartitions, attained at 1 versus s-1.
    cmi_integration = gaussian_relative_cmi_covariance_error_bound(
        1, subset_size - 1, subset_size, covariance_relative_error=delta
    )
    # J is bidirectional and normalized by subset size.
    integration_bits = 2.0 * cmi_integration / subset_size
    integration_radius = min(1.0, np.log(2.0) * integration_bits)

    cmi_insulation = gaussian_relative_cmi_covariance_error_bound(
        subset_size,
        ambient_size - subset_size,
        subset_size,
        covariance_relative_error=delta,
    )
    insulation_bits = cmi_insulation / subset_size
    insulation_radius = min(1.0, np.log(2.0) * insulation_bits)

    persistence_radius = canonical_persistence_relative_covariance_error_bound(
        covariance_relative_error=delta
    )
    omega_radius = product_root_error_bound(
        [integration_factor, insulation_factor, persistence_factor],
        [integration_radius, insulation_radius, persistence_radius],
    )
    return {
        "integration": float(integration_radius),
        "insulation": float(insulation_radius),
        "persistence": float(persistence_radius),
        "observer_score": float(omega_radius),
    }
