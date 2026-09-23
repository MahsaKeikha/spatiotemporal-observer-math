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
    """Propagate the canonical Research I relative radius to Omega uncertainty."""
    from .recovery import product_root_error_bound, relative_covariance_factor_error_bounds
    errors, valid = relative_covariance_factor_error_bounds(
        covariance_relative_error, ambient_size, subset_size, transport=False
    )
    if not valid:
        return {"integration":1.0,"insulation":1.0,"persistence":1.0,"observer_score":1.0}
    omega=product_root_error_bound(
        [integration_factor,insulation_factor,persistence_factor], errors
    )
    return {"integration":float(errors[0]),"insulation":float(errors[1]),
            "persistence":float(errors[2]),"observer_score":float(omega)}


def transport_score_radius_from_relative_covariance(
    *,
    subset_size: int,
    ambient_size: int,
    covariance_relative_error: float,
    insulation_factor: float,
    persistence_factor: float,
) -> dict[str, float]:
    """Propagate the canonical Research I relative radius to Theta uncertainty."""
    from .recovery import product_root_error_bound, relative_covariance_factor_error_bounds
    errors, valid = relative_covariance_factor_error_bounds(
        covariance_relative_error, ambient_size, subset_size, transport=True
    )
    if not valid:
        return {"insulation":1.0,"persistence":1.0,"transport_score":1.0}
    theta=product_root_error_bound([insulation_factor,persistence_factor],errors)
    return {"insulation":float(errors[0]),"persistence":float(errors[1]),
            "transport_score":float(theta)}


def complete_path_radius_from_relative_covariance(
    local_relative_errors,
    transport_relative_errors,
    local_factors,
    transport_factors,
    *,
    subset_size: int,
    ambient_size: int,
    transport_weight: float,
) -> float:
    """Compose relative covariance radii into the AM18 complete path radius.

    local_factors has shape (T, 3): integration, insulation, persistence.
    transport_factors has shape (T-1, 2): insulation, persistence.
    """
    local_relative_errors = np.asarray(local_relative_errors, dtype=float)
    transport_relative_errors = np.asarray(transport_relative_errors, dtype=float)
    local_factors = np.asarray(local_factors, dtype=float)
    transport_factors = np.asarray(transport_factors, dtype=float)
    if local_factors.shape != (local_relative_errors.size, 3):
        raise ValueError("local_factors must have shape (T, 3)")
    if transport_factors.shape != (transport_relative_errors.size, 2):
        raise ValueError("transport_factors must have shape (T-1, 2)")
    local_radii = [
        observer_factor_radii_from_relative_covariance(
            subset_size=subset_size,
            ambient_size=ambient_size,
            covariance_relative_error=float(delta),
            integration_factor=float(factors[0]),
            insulation_factor=float(factors[1]),
            persistence_factor=float(factors[2]),
        )["observer_score"]
        for delta, factors in zip(local_relative_errors, local_factors)
    ]
    transport_radii = [
        transport_score_radius_from_relative_covariance(
            subset_size=subset_size,
            ambient_size=ambient_size,
            covariance_relative_error=float(delta),
            insulation_factor=float(factors[0]),
            persistence_factor=float(factors[1]),
        )["transport_score"]
        for delta, factors in zip(transport_relative_errors, transport_factors)
    ]
    return path_action_radius(
        local_radii, transport_radii, transport_weight=transport_weight
    )
