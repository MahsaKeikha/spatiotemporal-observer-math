"""Finite-sample structural certificate coupled to observer decisions.

This module makes sample count, rather than a hand-entered separation, drive
the structural side of the self-certifying state machine.
"""
from __future__ import annotations
from dataclasses import dataclass
from .finite_sample_certificate import finite_sample_pair_certificate
from .decision_diagnostics import DecisionDiagnostics, diagnose_certificate_state

@dataclass(frozen=True)
class FiniteSampleObserverStep:
    sample_count: int
    covariance_radius: float
    robust_separation: float
    certified_structurally: bool
    decision: str
    structural_deficit: float
    evidence_deficit: float

def finite_sample_observer_step(*,sample_count:int,log_evidence:float,
                                evidence_threshold:float,available_kl,
                                assumptions_valid:bool,certificate_kwargs
                                ) -> FiniteSampleObserverStep:
    cert=finite_sample_pair_certificate(sample_count=sample_count,**certificate_kwargs)
    diag=diagnose_certificate_state(
        robust_separation=cert.robust_separation,log_evidence=log_evidence,
        evidence_threshold=evidence_threshold,available_kl=available_kl,
        assumptions_valid=assumptions_valid)
    return FiniteSampleObserverStep(
        sample_count=sample_count,covariance_radius=cert.covariance_radius,
        robust_separation=cert.robust_separation,
        certified_structurally=cert.certified,decision=diag.decision,
        structural_deficit=diag.structural_deficit,
        evidence_deficit=diag.evidence_deficit)

def sample_count_trajectory(sample_counts,*,log_evidence:float,evidence_threshold:float,
                            available_kl,assumptions_valid:bool,certificate_kwargs):
    counts=tuple(int(n) for n in sample_counts)
    if not counts or any(n<2 for n in counts) or any(b<=a for a,b in zip(counts,counts[1:])):
        raise ValueError("sample_counts must be strictly increasing integers >= 2")
    return tuple(finite_sample_observer_step(
        sample_count=n,log_evidence=log_evidence,evidence_threshold=evidence_threshold,
        available_kl=available_kl,assumptions_valid=assumptions_valid,
        certificate_kwargs=certificate_kwargs) for n in counts)

def first_joint_certificate(sample_counts,**kwargs):
    """Return first supplied sample count yielding the complete decision CERTIFY."""
    for step in sample_count_trajectory(sample_counts,**kwargs):
        if step.decision=="CERTIFY":
            return step
    return None
