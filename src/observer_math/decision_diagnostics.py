"""Decision semantics for uncertainty versus model invalidity.

The observer separates three epistemic states:
1. reducible uncertainty: the model is valid but current certificate/evidence is insufficient;
2. observational non-identifiability: valid model, but available actions cannot distinguish competitors;
3. model invalidity: assumptions required by the certificate have failed.

Only the first state is assigned MEASURE_MORE.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class DecisionDiagnostics:
    decision: str
    structural_deficit: float
    evidence_deficit: float
    best_available_kl: float
    assumptions_valid: bool
    observationally_identifiable: bool

def diagnose_certificate_state(
    *,
    robust_separation: float,
    log_evidence: float,
    evidence_threshold: float,
    available_kl,
    assumptions_valid: bool,
    kl_tolerance: float = 1e-12,
) -> DecisionDiagnostics:
    """Classify why a singleton certificate is or is not currently possible."""
    kl=np.asarray(available_kl,dtype=float)
    if kl.ndim != 1 or kl.size == 0 or np.any(~np.isfinite(kl)) or np.any(kl < 0):
        raise ValueError("available_kl must be a nonempty finite nonnegative vector")
    if evidence_threshold <= 0 or kl_tolerance < 0:
        raise ValueError("require positive evidence_threshold and nonnegative kl_tolerance")
    separation=float(robust_separation)
    structural_deficit=max(0.0,-separation)
    evidence_deficit=max(0.0,float(evidence_threshold)-float(log_evidence))
    best=float(np.max(kl))
    identifiable=best > kl_tolerance
    if not assumptions_valid:
        decision="ABSTAIN_INVALID_ASSUMPTIONS"
    elif not identifiable and evidence_deficit > 0:
        decision="ABSTAIN_UNIDENTIFIABLE"
    elif separation > 0.0 and evidence_deficit == 0.0:
        decision="CERTIFY"
    else:
        decision="MEASURE_MORE"
    return DecisionDiagnostics(
        decision,structural_deficit,evidence_deficit,best,bool(assumptions_valid),identifiable
    )

def evidence_measurement_lower_bound(evidence_deficit: float, best_available_kl: float):
    """Expected-gap measurement lower bound; infinity marks non-identifiability."""
    if evidence_deficit < 0 or best_available_kl < 0:
        raise ValueError("arguments must be nonnegative")
    if evidence_deficit == 0:
        return 0
    if best_available_kl == 0:
        return float("inf")
    return int(np.ceil(evidence_deficit/best_available_kl))
