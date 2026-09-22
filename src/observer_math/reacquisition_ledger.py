"""Closed-loop reacquisition ledger for finite-sample certification.

The ledger separates certification samples from predictive evidence. Targeted
repairs explicitly reset only records whose validity is lost, then new
measurements rebuild the corresponding quantities.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from .assumption_audit import AssumptionAudit
from .repair_semantics import RepairAction, apply_repair
from .finite_sample_observer import finite_sample_observer_step
from .data_split import DataSplitLedger, certification_sample_count

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
        structural_stale=effect.reset_structural,
        evidence_stale=effect.reset_evidence)

def acquire_certification_samples(ledger:MeasurementLedger,count:int)->MeasurementLedger:
    if count<=0: raise ValueError("count must be positive")
    return replace(ledger,certification_samples=ledger.certification_samples+count,
                   structural_stale=False)

def acquire_predictive_evidence(ledger:MeasurementLedger,log_likelihood_increment:float
                               )->MeasurementLedger:
    if log_likelihood_increment<0:
        raise ValueError("this ledger accepts nonnegative evidence increments")
    return replace(ledger,log_evidence=ledger.log_evidence+log_likelihood_increment,
                   evidence_stale=False)

def evaluate_ledger(ledger:MeasurementLedger,*,evidence_threshold:float,
                    available_kl,certificate_kwargs):
    """Fail closed while a repair-invalidated record remains stale."""
    valid=ledger.audit.certificate_valid and not ledger.structural_stale and not ledger.evidence_stale
    return finite_sample_observer_step(
        sample_count=ledger.certification_samples,log_evidence=ledger.log_evidence,
        evidence_threshold=evidence_threshold,available_kl=available_kl,
        assumptions_valid=valid,certificate_kwargs=certificate_kwargs)


def evaluate_independent_split(ledger:MeasurementLedger,split:DataSplitLedger,*,
                               evidence_threshold:float,available_kl,certificate_kwargs):
    """Evaluate only with an auditable independent certification stream."""
    n=certification_sample_count(split)
    if ledger.structural_stale or ledger.evidence_stale:
        valid=False
    else:
        valid=ledger.audit.certificate_valid
    return finite_sample_observer_step(
        sample_count=n,log_evidence=ledger.log_evidence,
        evidence_threshold=evidence_threshold,available_kl=available_kl,
        assumptions_valid=valid,certificate_kwargs=certificate_kwargs)
