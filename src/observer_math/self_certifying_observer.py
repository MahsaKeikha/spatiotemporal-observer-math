"""Unified state machine for self-certifying moving-boundary observation.

This composes decision diagnostics and bounded reacquisition without weakening
either gate. It is deliberately policy-light: scientific models supply the
diagnostics and recovery actions; the machine only enforces safe transitions.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from .decision_diagnostics import diagnose_certificate_state
from .reacquisition import (
    ReacquisitionAction, bounded_reacquisition_status, select_reacquisition_action,
)

class ObserverState(str,Enum):
    INFER="INFER"
    MEASURE_MORE="MEASURE_MORE"
    REACQUIRE="REACQUIRE"
    CERTIFY="CERTIFY"
    ABSTAIN_UNIDENTIFIABLE="ABSTAIN_UNIDENTIFIABLE"
    ABSTAIN_INVALID_ASSUMPTIONS="ABSTAIN_INVALID_ASSUMPTIONS"
    ABSTAIN_UNRECOVERABLE="ABSTAIN_UNRECOVERABLE"

@dataclass(frozen=True)
class ObserverStep:
    state: ObserverState
    action: str|None
    reason: str

def transition(*,robust_separation:float,log_evidence:float,evidence_threshold:float,
               available_kl,assumptions_valid:bool,recovery_actions=(),
               reacquisition_steps:int=0,reacquisition_budget:int=3) -> ObserverStep:
    d=diagnose_certificate_state(
        robust_separation=robust_separation,log_evidence=log_evidence,
        evidence_threshold=evidence_threshold,available_kl=available_kl,
        assumptions_valid=assumptions_valid,
    )
    if d.decision=="CERTIFY":
        return ObserverStep(ObserverState.CERTIFY,None,"structural and evidence gates satisfied")
    if d.decision=="MEASURE_MORE":
        return ObserverStep(ObserverState.MEASURE_MORE,None,"valid model with reducible deficit")
    if d.decision=="ABSTAIN_UNIDENTIFIABLE":
        return ObserverStep(ObserverState.ABSTAIN_UNIDENTIFIABLE,None,
                            "no available action has positive predictive discrimination")

    # Invalid assumptions: recovery is allowed only through a validity-restoring action.
    if reacquisition_steps >= reacquisition_budget:
        return ObserverStep(ObserverState.ABSTAIN_UNRECOVERABLE,None,
                            "reacquisition budget exhausted")
    plan=select_reacquisition_action(
        recovery_actions,evidence_deficit=d.evidence_deficit,
        structural_deficit=d.structural_deficit,
    )
    if plan.decision=="REACQUIRE":
        return ObserverStep(ObserverState.REACQUIRE,plan.action,plan.reason)
    return ObserverStep(ObserverState.ABSTAIN_UNRECOVERABLE,None,plan.reason)

def recovery_transition(*,steps_used:int,step_budget:int,
                        assumptions_restored:bool,certificate_restored:bool) -> ObserverState:
    status=bounded_reacquisition_status(
        steps_used=steps_used,step_budget=step_budget,
        assumptions_restored=assumptions_restored,certificate_restored=certificate_restored,
    )
    if status=="CERTIFY":
        return ObserverState.CERTIFY
    if status=="REACQUIRE":
        return ObserverState.REACQUIRE
    return ObserverState.ABSTAIN_UNRECOVERABLE
