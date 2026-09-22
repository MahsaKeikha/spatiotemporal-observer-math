"""Closed-loop reacquisition ledger for finite-sample certification.

Repairs accumulate stale-state flags. A stale structural record is cleared only
by an explicit rebuild, never by merely appending samples. Predictive
log-likelihood increments are signed random quantities and may be negative.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
import math
from .assumption_audit import AssumptionAudit
from .repair_semantics import RepairAction, apply_repair
from .finite_sample_observer import finite_sample_observer_step
from .data_split import DataSplitLedger, certification_effective_dof

@dataclass(frozen=True)
class MeasurementLedger:
    certification_samples: int
    log_evidence: float
    audit: AssumptionAudit
    structural_stale: bool=False
    evidence_stale: bool=False

def apply_targeted_repair(ledger:MeasurementLedger, action:RepairAction)->MeasurementLedger:
    effect=apply_repair(ledger.audit,action)
    return MeasurementLedger(
        certification_samples=ledger.certification_samples,
        log_evidence=0.0 if effect.reset_evidence else ledger.log_evidence,
        audit=effect.audit,
        structural_stale=ledger.structural_stale or effect.reset_structural,
        evidence_stale=ledger.evidence_stale or effect.reset_evidence)

def acquire_certification_samples(ledger:MeasurementLedger,count:int)->MeasurementLedger:
    """Append raw observations without claiming a stale certificate was rebuilt."""
    if count<=0: raise ValueError("count must be positive")
    return replace(ledger,certification_samples=ledger.certification_samples+count)

def mark_structural_rebuilt(ledger:MeasurementLedger)->MeasurementLedger:
    """Declare completion of the structural estimator/certificate rebuild."""
    if not ledger.audit.certificate_valid:
        raise ValueError("cannot rebuild while certificate assumptions are invalid")
    return replace(ledger,structural_stale=False)

def acquire_predictive_evidence(ledger:MeasurementLedger,log_likelihood_increment:float
                               )->MeasurementLedger:
    """Accumulate a finite signed log-likelihood-ratio increment."""
    if not math.isfinite(log_likelihood_increment):
        raise ValueError("log-likelihood increment must be finite")
    return replace(ledger,log_evidence=ledger.log_evidence+log_likelihood_increment,
                   evidence_stale=False)

def _evaluate(ledger, sample_count, *, evidence_threshold, available_kl, certificate_kwargs):
    """Separate recoverable stale records from genuinely invalid assumptions."""
    if not ledger.audit.certificate_valid:
        return finite_sample_observer_step(
            sample_count=sample_count,log_evidence=ledger.log_evidence,
            evidence_threshold=evidence_threshold,available_kl=available_kl,
            assumptions_valid=False,certificate_kwargs=certificate_kwargs)
    # Staleness means reacquisition is incomplete, not that the model is invalid.
    if ledger.structural_stale or ledger.evidence_stale:
        step=finite_sample_observer_step(
            sample_count=sample_count,log_evidence=ledger.log_evidence,
            evidence_threshold=evidence_threshold,available_kl=available_kl,
            assumptions_valid=True,certificate_kwargs=certificate_kwargs)
        return replace(step,decision="MEASURE_MORE",certified_structurally=(
            step.certified_structurally and not ledger.structural_stale))
    return finite_sample_observer_step(
        sample_count=sample_count,log_evidence=ledger.log_evidence,
        evidence_threshold=evidence_threshold,available_kl=available_kl,
        assumptions_valid=True,certificate_kwargs=certificate_kwargs)

def evaluate_ledger(ledger:MeasurementLedger,*,evidence_threshold:float,
                    available_kl,certificate_kwargs):
    return _evaluate(ledger,ledger.certification_samples,evidence_threshold=evidence_threshold,
                     available_kl=available_kl,certificate_kwargs=certificate_kwargs)

def evaluate_independent_split(ledger:MeasurementLedger,split:DataSplitLedger,*,
                               evidence_threshold:float,available_kl,certificate_kwargs):
    """Evaluate with the effective innovation degrees of freedom of the held-out stream."""
    r=certification_effective_dof(split)
    return _evaluate(ledger,r,evidence_threshold=evidence_threshold,
                     available_kl=available_kl,certificate_kwargs=certificate_kwargs)
