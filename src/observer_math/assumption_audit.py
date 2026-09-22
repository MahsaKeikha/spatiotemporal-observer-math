"""Assumption-audit controls for self-certifying moving-boundary inference.

The audit distinguishes ordinary ambiguity from certificate invalidity.
A certificate can be emitted only when its coverage and calibration assumptions
are explicitly marked valid. This module intentionally injects violations to
test fail-closed behavior.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class AssumptionAudit:
    coverage_valid: bool
    covariance_calibration_valid: bool
    temporal_model_valid: bool
    predictive_model_valid: bool

    @property
    def certificate_valid(self) -> bool:
        return (
            self.coverage_valid
            and self.covariance_calibration_valid
            and self.temporal_model_valid
            and self.predictive_model_valid
        )

def audited_certificate(
    *,
    robust_separation: float,
    log_evidence: float,
    evidence_threshold: float,
    audit: AssumptionAudit,
) -> str:
    """Return CERTIFY, MEASURE_MORE, or ABSTAIN_INVALID_ASSUMPTIONS."""
    if not audit.certificate_valid:
        return "ABSTAIN_INVALID_ASSUMPTIONS"
    if robust_separation > 0.0 and log_evidence >= evidence_threshold:
        return "CERTIFY"
    return "MEASURE_MORE"

def calibration_stress(true_radius: float, declared_radius: float) -> bool:
    """Whether the declared uncertainty radius covers the injected truth."""
    if true_radius < 0 or declared_radius < 0:
        raise ValueError("radii must be nonnegative")
    return declared_radius >= true_radius

def motion_regime_valid(observed_jump: float, allowed_jump: float) -> bool:
    """Check a declared temporal regularity envelope."""
    if observed_jump < 0 or allowed_jump < 0:
        raise ValueError("jump magnitudes must be nonnegative")
    return observed_jump <= allowed_jump
